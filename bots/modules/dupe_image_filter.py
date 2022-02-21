from scarletio import Task, IgnoreCaseString, LOOP_TIME, sleep, CancelledError
from scarletio.web_common.headers import CONTENT_LENGTH
from hata import Embed, KOKORO, seconds_to_elapsed_time, Client, Message, DiscordException, ERROR_CODES, now_as_id, \
    seconds_to_id_difference, Guild
from hata.ext.slash import Button, abort
from bot_utils.constants import GUILD__SUPPORT

SLASH_CLIENT: Client

GUILD__KOISHI_CLAN = Guild.precreate(866746184990720020)

E_TAG = IgnoreCaseString('ETag')

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
        return f'<{self.__class__.__name__} url={self.url!r}>'


class ProcessedMessage:
    __slots__ = ('message_id', 'urls')
    
    def __init__(self, message_id, urls):
        self.message_id = message_id
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

FILTERED_CHANNEL_IDS = set()

UPDATE_INTERVAL = 5.0

CUSTOM_ID_CLOSE_MESSAGE = 'dupe_image_filter.close'

CLOSE_BUTTON = Button(
    'close',
    custom_id = CUSTOM_ID_CLOSE_MESSAGE,
)


class DupeImageFilter:
    __slots__ = (
        'after_id', 'channel_id', 'client', 'request_more', 'urls', 'message_ids_to_delete', 'total_scanned_messages',
        'total_deleted_messages', 'runner', 'message_delete_task', 'started_at', 'update_waiter',
        'all_delete_message_id'
    )
    
    def __init__(self, client, event, look_back):
        after_id = now_as_id() - seconds_to_id_difference(DAY_IN_SECONDS * look_back)
        if after_id < 0:
            after_id = 0
        
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
        
        Task(self.run(), KOKORO)
        Task(self.state_update_loop(client, event), KOKORO)
        
        FILTERED_CHANNEL_IDS.add(self.channel_id)
    
    
    async def run(self):
        try:
            await self.message_request_loop()
            await self.message_delete_loop()
        finally:
            self.update_waiter.cancel()
    
    
    async def message_request_loop(self):
        while self.request_more:
            messages = await self.client.message_get_chunk(self.channel_id, after=self.after_id)
            if len(messages) < 100:
                self.request_more = False
            else:
                self.after_id = messages[0].id
            
            for message in reversed(messages):
                await self.scan_message(message)
                self.total_scanned_messages += 1
            
            continue
    
    
    async def message_delete_loop(self):
        message_ids_to_delete = self.message_ids_to_delete
        while message_ids_to_delete:
            message_id = message_ids_to_delete.pop()
            
            try:
                await self.client.message_delete((self.channel_id, message_id))
            except DiscordException as err:
                if err.code != ERROR_CODES.unknown_message:
                    raise
            
            self.total_deleted_messages += 1
    
    
    async def get_processed_urls_of(self, message):
        urls = None
        
        embeds = message.embeds
        if (embeds is not None):
            for embed in embeds:
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
        
        attachments = message.attachments
        if (attachments is not None):
            for attachment in attachments:
                content_type = attachment.content_type
                if (content_type is None) or (content_type.startswith('image')):
                    if urls is None:
                        urls = set()
                    
                    urls.add(attachment.url)
        
        if (urls is None) or (not urls):
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
                response = await self.client.http.head(attachment_url)
                headers = response.headers
                
                identifier = headers.get(CONTENT_LENGTH), headers.get(E_TAG)
                
                processed_url = ProcessedUrl(True, attachment_url, identifier)
                processed_urls.add(processed_url)
        
        return processed_urls
    
    
    async def scan_message(self, message):
        # referenced message
        referenced_message = message.referenced_message
        if referenced_message is None:
            message_id = 0
        elif isinstance(referenced_message, Message):
            message_id = referenced_message.id
        else:
            message_id = referenced_message.message_id
        
        processed_urls = await self.get_processed_urls_of(message)
        
        urls = self.urls
        if message_id:
            self.message_ids_to_delete.discard(message_id)
            
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
                    self.message_ids_to_delete.add(message.id)
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
                f'{seconds_to_elapsed_time(LOOP_TIME()-self.started_at)}\n'
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
    
    
    async def state_update_loop(self, client, event):
        try:
            await client.interaction_response_message_create(event, embed=self.get_embed())
            
            while True:
                try:
                    await self.update_waiter
                except CancelledError:
                    break
                
                self.update_waiter = sleep(UPDATE_INTERVAL, KOKORO)
                await client.interaction_response_message_edit(event, embed=self.get_embed())
            
            await client.interaction_response_message_edit(event, embed=self.get_embed(), components=CLOSE_BUTTON)
            
            
        finally:
            FILTERED_CHANNEL_IDS.discard(self.channel_id)


@SLASH_CLIENT.interactions(guild=[GUILD__KOISHI_CLAN, GUILD__SUPPORT])
async def dupe_image_filter(
    client,
    event,
    look_back: ('int', 'For how much days it should look back for?')
):
    """Deletes duplicated images (and other files) | ou must have manage messages permission."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to do this.')
    
    if not event.user_permissions.can_manage_messages:
        abort('You must have manage messages permission to use this command.')
    
    if not guild.cached_permissions_for(client).can_manage_messages:
        abort(f'{client.name_at(guild)} must have manage messages permission to execute this command.')
    
    if event.channel_id in FILTERED_CHANNEL_IDS:
        abort('There is already one message filter running in the channel.')
    
    if look_back <= 0:
        abort('look-back cannot be non-positive')
    
    DupeImageFilter(client, event, look_back)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_CLOSE_MESSAGE)
async def close_dupe_image_filter(client, event):
    if event.user_permissions.can_manage_messages:
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)
