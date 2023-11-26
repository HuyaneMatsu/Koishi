__all__ = ()

from scarletio import Task, IgnoreCaseString, LOOP_TIME, sleep, CancelledError, TaskGroup
from scarletio.web_common.headers import CONTENT_LENGTH
from hata import Embed, KOKORO, seconds_to_elapsed_time, Message, DiscordException, ERROR_CODES, now_as_id, \
    seconds_to_id_difference, format_loop_time, TIMESTAMP_STYLES, Permission
from hata.ext.slash import Button, abort, ButtonStyle, Row, wait_for_component_interaction

from ..bots import FEATURE_CLIENTS, MAIN_CLIENT


HEADER_E_TAG = IgnoreCaseString('ETag')

DAY_IN_SECONDS = 60 * 60 * 24


class ProcessedUrl:
    __slots__ = ('_hash', 'is_attachment', 'url', 'identifier')
    
    def __init__(self, is_attachment, url, identifier):
        if is_attachment:
            hash_ = hash(identifier)
        else:
            hash_ = hash(url)
        
        self._hash = hash_
        self.is_attachment = is_attachment
        self.url = url
        self.identifier = identifier
    
    def __hash__(self):
        return self._hash
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._hash != other._hash:
            return False
        
        is_attachment = self.is_attachment
        if is_attachment != other.is_attachment:
            return False
        
        if is_attachment:
            if self.identifier != other.identifier:
                return False
        
        else:
            if self.url != other.url:
                return False
        
        return True
    
    def __repr__(self):
        return f'<{self.__class__.__name__} url = {self.url!r}>'


class ProcessedMessage:
    __slots__ = ('message_id', 'replied_message_id', 'urls')
    
    def __init__(self, message_id, replied_message_id, urls):
        self.message_id = message_id
        self.replied_message_id = replied_message_id
        self.urls = urls
    
    def __repr__(self):
        return f'<{self.__class__.__name__} url count: {len(self.urls)}>'
    
    def __hash__(self):
        return self.message_id
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.message_id != other.message_id:
            return False
        
        return True


def is_attachment_url(url):
    return url.startswith('https://cdn.discordapp.com/attachments')

FILTERERS = {}

UPDATE_INTERVAL = 5.0

CUSTOM_ID_APPROVE = 'dupe_image_filter.approve'
CUSTOM_ID_CANCEL = 'dupe_image_filter.cancel'
CUSTOM_ID_CLOSE = 'dupe_image_filter.close'



BUTTON_APPROVE = Button(
    'approve',
    custom_id = CUSTOM_ID_APPROVE,
    style = ButtonStyle.green,
)

BUTTON_CANCEL = Button(
    'cancel',
    custom_id = CUSTOM_ID_CANCEL,
    style = ButtonStyle.red,
)

COMPONENTS_APPROVE = Row(
    BUTTON_APPROVE,
    BUTTON_CANCEL,
)

BUTTON_CLOSE = Button(
    'close',
    custom_id = CUSTOM_ID_CLOSE,
)




class DupeImageFilter:
    __slots__ = (
        'after_id', 'channel_id', 'client', 'request_more', 'urls', 'message_ids_to_delete', 'total_scanned_messages',
        'total_deleted_messages', 'runner', 'message_delete_task', 'started_at', 'update_waiter', 'message',
        'all_delete_message_id', 'task',
    )
    
    def __init__(self, client, event, look_back):
        after_id = now_as_id() - seconds_to_id_difference(DAY_IN_SECONDS * look_back)
        if after_id < 0:
            after_id = 0
        
        self.task = None
        self.message = None
        self.request_more = True
        self.after_id = after_id
        self.client = client
        self.channel_id = event.channel_id
        self.urls = set()
        self.total_deleted_messages = 0
        self.message_ids_to_delete = set()
        self.started_at = LOOP_TIME()
        
        self.total_scanned_messages = 0
        
        self.update_waiter = sleep(UPDATE_INTERVAL, KOKORO)
        
        self.task = Task(KOKORO, self.state_update_loop(client, event))
        
        FILTERERS[self.channel_id] = self
    
    
    async def message_request_loop(self):
        try:
            task = None
            
            try:
                while self.request_more:
                    messages = await self.client.message_get_chunk(self.channel_id, after = self.after_id)
                    if len(messages) < 100:
                        self.request_more = False
                    else:
                        self.after_id = messages[0].id
                    
                    task = Task(KOKORO, self.scan_messages(messages, task))
                    continue
            except:
                task.cancel()
                raise
            
            finally:
                # Clear references
                task = None
                tasks = None
        
        finally:
            self.update_waiter.cancel()
        
    
    async def message_delete_loop(self):
        try:
            message_ids_to_delete = self.message_ids_to_delete
            while message_ids_to_delete:
                message_id = message_ids_to_delete.pop()
                
                try:
                    await self.client.message_delete((self.channel_id, message_id))
                except DiscordException as err:
                    if err.code != ERROR_CODES.unknown_message:
                        raise
                
                self.total_deleted_messages += 1
        finally:
            self.update_waiter.cancel()
    
    
    async def get_processed_urls_of(self, message):
        urls = None
        
        for embed in message.iter_embeds():
            if embed.type in ('image', 'video'):
                thumbnail = embed.thumbnail
                if (thumbnail is not None):
                    url = thumbnail.url
                    if (url is not None):
                        if urls is None:
                            urls = set()
                        
                        urls.add(url)
            
            else:
                image = embed.image
                if (image is not None):
                    url = image.url
                    if (url is not None):
                        if urls is None:
                            urls = set()
                        
                        urls.add(url)
        
        for attachment in message.iter_attachments():
            content_type = attachment.content_type
            if (content_type is None) or (content_type.startswith('image')):
                if urls is None:
                    urls = set()
                
                urls.add(attachment.url)
        
        if (urls is None):
            return None
        
        processed_urls = set()
        attachment_urls = None
        
        for url in urls:
            if is_attachment_url(url):
                if attachment_urls is None:
                    attachment_urls = set()
                
                attachment_urls.add(url)
            
            else:
                processed_url = ProcessedUrl(False, url, None)
                processed_urls.add(processed_url)
        
        if attachment_urls is not None:
            for attachment_url in attachment_urls:
                
                retries = 5
                while True:
                    try:
                        response = await self.client.http.head(attachment_url)
                    except ConnectionError:
                        if retries <= 0:
                            raise
                        
                        retries -= 1
                        continue
                    
                    else:
                        break
                
                if response.status != 200:
                    # Message probably deleted meanwhile or something
                    return None
                
                headers = response.headers
                
                identifier = headers.get(CONTENT_LENGTH), headers.get(HEADER_E_TAG)
                
                processed_url = ProcessedUrl(True, attachment_url, identifier)
                processed_urls.add(processed_url)
        
        return processed_urls
    
    
    async def scan_messages(self, messages, previous_task):
        try:
            processed_messages = []
            for message in reversed(messages):
                processed_message = await self.scan_message(message)
                processed_messages.append(processed_message)
                self.total_scanned_messages += 1
            
            if (previous_task is not None):
                await previous_task.wait_for_completion()
                previous_task = None
            
            for processed_message in processed_messages:
                self.decide_about_message(processed_message)
        
        except CancelledError:
            if (previous_task is not None):
                previous_task.cancel()
                previous_task = None
        
            raise
        
        except:
            if (previous_task is not None):
                previous_task = None
            
            raise
    
    async def scan_message(self, message):
        # referenced message
        referenced_message = message.referenced_message
        if referenced_message is None:
            replied_message_id = 0
        elif isinstance(referenced_message, Message):
            replied_message_id = referenced_message.id
        else:
            replied_message_id = referenced_message.message_id
        
        processed_urls = await self.get_processed_urls_of(message)
        
        return ProcessedMessage(message.id, replied_message_id, processed_urls)
    
    
    def decide_about_message(self, processed_message):
        replied_message_id = processed_message.replied_message_id
        processed_urls = processed_message.urls
        
        urls = self.urls
        if replied_message_id:
            self.message_ids_to_delete.discard(replied_message_id)
            
            if (processed_urls is not None):
                urls.update(processed_urls)
                
        else:
            if (processed_urls is not None):
                for url in processed_urls:
                    if url not in urls:
                        is_present = False
                        break
                
                else:
                    is_present = True
                
                if is_present:
                    self.message_ids_to_delete.add(processed_message.message_id)
                else:
                    urls.update(processed_urls)
    
    
    def get_embed(self):
        embed = Embed('Filtering out dupe images')
        
        embed.add_field(
            'Messages scanned',
            (
                f'```\n'
                f'{self.total_scanned_messages}\n'
                f'```'
            ),
            inline = True,
        )
        
        embed.add_field(
            'Unique images',
            (
                f'```\n'
                f'{len(self.urls)}\n'
                f'```'
            ),
            inline = True,
        )
        
        embed.add_field(
            'Elapsed time',
            (
                f'```\n'
                f'{seconds_to_elapsed_time(LOOP_TIME() - self.started_at)}\n'
                f'```'
            ),
        )
        
        embed.add_field(
            'Messages deleted',
            (
                f'```\n'
                f'{self.total_deleted_messages}\n'
                f'```'
            ),
            inline = True,
            
        )
        
        embed.add_field(
            'Messages ensured for deletion',
            (
                f'```\n'
                f'{len(self.message_ids_to_delete)}\n'
                f'```'
            ),
            inline = True,
        )
        
        
        return embed
    
    async def message_update_loop(self, client, message, footer):
        while True:
            try:
                await self.update_waiter
            except CancelledError:
                break
            
            self.update_waiter = sleep(UPDATE_INTERVAL, KOKORO)
            embed = self.get_embed()
            embed.add_footer(footer)
            await client.message_edit(message, embed = embed)
            embed = None
    
    
    async def try_message_user(self, user_id, message):
        try:
            channel = await self.client.channel_private_create(user_id)
        except ConnectionError:
            return
        
        dupe_count = len(self.message_ids_to_delete)
        if dupe_count:
            description = f'Please confirm to remove **{dupe_count}** messages with dupe images.'
        else:
            description = 'There are no dupe images in the channel.'
            
        try:
            await self.client.message_create(
                channel,
                f'Your dupe message filtering finished.\n\n{description}',
                components = Button('Go to message', url = message.url),
            )
        except ConnectionError:
            return
        
        except DiscordException as err:
            if err.code == ERROR_CODES.cannot_message_user:
                return
            
            raise
        
        return
    
    
    async def state_update_loop(self, client, event):
        try:
            Task(KOKORO, self.message_request_loop())
            
            embed = self.get_embed()
            embed.add_footer('Requesting and processing messages')
            await client.interaction_response_message_create(event, embed = embed)
            message = await client.interaction_response_message_get(event)
            self.message = message
            
            user_id = event.user.id
            event = None
            
            await self.message_update_loop(client, message, 'Requesting and processing messages')
            
            await self.try_message_user(user_id, message)
            
            if self.message_ids_to_delete:
                embed = self.get_embed()
                embed.description = (
                    f'**Please confirm the deletion**\n\n'
                    f'Expires after 15 minutes | {format_loop_time(LOOP_TIME()+900.0, TIMESTAMP_STYLES.relative_time)}'
                )
                
                await client.message_edit(message, embed = embed, components = COMPONENTS_APPROVE)
                embed = None
                
                try:
                    event = await wait_for_component_interaction(
                        message,
                        timeout = 900.0,
                        check = has_manage_messages_permission,
                    )
                except TimeoutError:
                    embed = self.get_embed()
                    embed.add_footer('Timed out')
                    await client.message_edit(message, embed = embed, components = BUTTON_CLOSE)
                    embed = None
                    return
                
                if event.interaction == BUTTON_CANCEL:
                    embed = self.get_embed()
                    embed.add_footer('Edit cancelled')
                    await client.interaction_component_message_edit(event, embed = embed, components = BUTTON_CLOSE)
                    embed = None
                    return
                
                # Reset update waiter
                self.update_waiter = sleep(UPDATE_INTERVAL, KOKORO)
                Task(KOKORO, self.message_delete_loop())
                
                embed = self.get_embed()
                embed.add_footer('Deleting dupes')
                await client.interaction_component_message_edit(event, embed = embed, components = None)
                
                await self.message_update_loop(client, message, 'Deleting dupes')
                
            await client.message_edit(message, embed = self.get_embed(), components = BUTTON_CLOSE)
        
        except:
            self.update_waiter.cancel()
            raise
        
        finally:
            if FILTERERS.get(self.channel_id, self) is self:
                del FILTERERS[self.channel_id]
            
            self.task = None
    
    
    def get_cancel_task(self):
        task = self.task
        if (task is not None):
            self.task = None
            task.cancel()
            
            message = self.message
            if (message is not None):
                embed = self.get_embed()
                embed.description = (
                    f'```\n'
                    f'!!!! {self.client.name} is shutting down, sorry for the inconvenience. '
                    f'Please try re-invoking the command later !!!!\n'
                    f'```'
                )
                
                return Task(
                    KOKORO,
                    self.client.message_edit(
                        message,
                        embed = embed,
                        components = BUTTON_CLOSE,
                    ),
                )


def has_manage_messages_permission(event):
    return bool(event.user_permissions.can_manage_messages)



@FEATURE_CLIENTS.interactions(
    is_global = True,
    required_permissions = Permission().update_by_keys(manage_messages = True),
    allow_in_dm = False,
)
async def dupe_image_filter(
    client,
    event,
    look_back: ('int', 'For how much days it should look back for?')
):
    """Deletes duplicated images (and other files) | You must have manage messages permission."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to do this.')
    
    if not event.user_permissions.can_manage_messages:
        abort('You must have manage messages permission to use this command.')
    
    if not guild.cached_permissions_for(client).can_manage_messages:
        abort(f'{client.name_at(guild)} must have manage messages permission to execute this command.')
    
    if event.channel_id in FILTERERS:
        abort('There is already one message filter running in the channel.')
    
    if look_back <= 0:
        abort('look-back cannot be non-positive')
    
    DupeImageFilter(client, event, look_back)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLOSE)
async def close_dupe_image_filter(client, event):
    if event.user_permissions.can_manage_messages:
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)


@MAIN_CLIENT.events
async def shutdown(client):
    cancel_tasks = []
    
    for filterer in FILTERERS.values():
        cancel_task = filterer.get_cancel_task()
        if (cancel_task is not None):
            cancel_tasks.append(cancel_task)
    
    cancel_task = None
    
    await TaskGroup(KOKORO, cancel_tasks).wait_all()
