from scarletio import Task, WaitTillExc, LOOP_TIME, WaitTillAll, Future
from hata import Client, Guild, DiscordException, ERROR_CODES, ChannelThread, KOKORO, Emoji, format_loop_time, \
    mention_channel_by_id, TIMESTAMP_STYLES, Embed, is_id
from hata.ext.slash import abort, Button, Row, ButtonStyle, Form, TextInput

from bot_utils.constants import GUILD__SUPPORT

SLASH_CLIENT: Client

GUILD__KOISHI_CLAN = Guild.precreate(866746184990720020)

async def get_message(client, channel, message_id):
    try:
        message = await client.message_get(channel, message_id)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            abort(f'Unknown message: {message_id}')
        
        raise
    
    return message


async def get_attachment(client, attachment):
    file = await client.download_attachment(attachment)
    return attachment, file


async def get_attachments(client, attachments):
    tasks = []
    for attachment in attachments:
        tasks.append(Task(get_attachment(client, attachment), KOKORO))
    
    done, pending = await WaitTillExc(tasks, KOKORO)
    
    # We do not care about the pending ones
    for task in pending:
        task.cancel()
    
    attachment_map = {}
    for task in done:
        # This line might raise
        attachment, file = task.result()
        
        attachment_map[attachment] = file
    
    return [(attachment.name, attachment_map[attachment], attachment.description) for attachment in attachments]


async def get_message_and_files(client, channel, message_id):
    message = await get_message(client, channel, message_id)
    files = await get_files(client, message)
    
    return message, files


async def get_webhook(client, channel_id):
    executor_webhook = await client.webhook_get_own_channel(channel_id)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel_id, 'Koishi hook')
    
    return executor_webhook


async def message_delete(client, message):
    try:
        await client.message_delete(message)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            return
        
        raise
    
    except ConnectionError:
        return


async def get_files(client, message):
    attachments = message.attachments
    if (attachments is None):
        files = None
    else:
        files = await get_attachments(client, attachments)
    
    return files


def check_permissions(client, event, channel):
    user_permissions = event.user_permissions
    if (not user_permissions.can_manage_messages):
        abort('You need to have manage messages to invoke this command.')
    
    source_channel = event.channel
    if (source_channel is None) or (not source_channel.cached_permissions_for(client).can_manage_messages):
        abort('I require manage messages permission in this channel to execute the command.')
    
    if (not channel.cached_permissions_for(client).can_manage_webhooks):
        abort('I need manage webhook permission in the target channel to execute this this command.')
    

@SLASH_CLIENT.interactions(guild=[GUILD__KOISHI_CLAN, GUILD__SUPPORT])
async def move_message(
    client,
    event,
    channel: ('channel_group_messageable', 'Where to move the message.'),
    message_id: ('int', 'The message\'s identifier. The message must be from this channel.')
):
    """Moves a message | Mod only"""
    check_permissions(client, event, channel)
    
    if isinstance(channel, ChannelThread):
        channel_id = channel.parent_id
        thread_id = channel.id
    else:
        channel_id = channel.id
        thread_id = 0
    
    get_message_and_files_task = Task(get_message_and_files(client, event.channel, message_id), KOKORO)
    get_webhook_task = Task(get_webhook(client, channel_id), KOKORO)
    
    done, pending = await WaitTillExc(
        [
            get_message_and_files_task,
            get_webhook_task,
            Task(client.interaction_application_command_acknowledge(event, show_for_invoking_user_only=True), KOKORO)
        ],
        KOKORO,
    )
    
    for task in pending:
        task.cancel()
    
    for task in done:
        result = task.result()
        
        if task is get_message_and_files_task:
            message, files = result
            continue
        
        if task is get_webhook_task:
            webhook = result
            continue
    
    await client.webhook_message_create(
        webhook,
        message.content,
        embed = message.clean_embeds,
        file = files,
        allowed_mentions = None,
        name = message.author.name_at(event.guild_id),
        avatar_url = message.author.avatar_url_at(event.guild_id),
        thread = thread_id,
    )
    
    files = None
    
    Task(message_delete(client, message), KOKORO)
    
    await client.interaction_response_message_edit(event, 'Message moved successfully.')



MESSAGE_MOVER_CONTEXT_TIMEOUT = 600.0

MESSAGE_MOVER_CONTEXTS = {}

def timeout_message_mover_context(key):
    try:
        message_mover_context = MESSAGE_MOVER_CONTEXTS[key]
    except KeyError:
        pass
    else:
        message_mover_context.trigger_timeout()

CUSTOM_ID_MESSAGE_MOVER_SUBMIT = 'message_mover.submit'
CUSTOM_ID_MESSAGE_MOVER_CANCEL = 'message_mover.cancel'
CUSTOM_ID_MESSAGE_MOVER_CLOSE = 'message_mover.close'
CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID = 'message_mover.add_by_id'

BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED = Button(
    'Submit',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_SUBMIT,
    style = ButtonStyle.green,
)

BUTTON_MESSAGE_MOVE_SUBMIT_DISABLED = BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED.copy_with(enabled=False)

BUTTON_MESSAGE_MOVE_ADD_BY_ID= Button(
    'Enter message id',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID,
    style = ButtonStyle.violet,
)

BUTTON_MESSAGE_MOVE_CANCEL = Button(
    'Cancel',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_CANCEL,
    style = ButtonStyle.red,
)

BUTTON_MESSAGE_MOVE_CLOSE = Button(
    'Close',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_CLOSE,
    style = ButtonStyle.red,
)

MESSAGE_MOVER_COMPONENTS_ENABLED = Row(
    BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED,
    BUTTON_MESSAGE_MOVE_ADD_BY_ID,
    BUTTON_MESSAGE_MOVE_CANCEL,
)

MESSAGE_MOVER_COMPONENTS_DISABLED = Row(
    BUTTON_MESSAGE_MOVE_SUBMIT_DISABLED,
    BUTTON_MESSAGE_MOVE_ADD_BY_ID,
    BUTTON_MESSAGE_MOVE_CANCEL,
)

MESSAGE_MOVER_COMPONENTS_AFTERLIFE = Row(
    BUTTON_MESSAGE_MOVE_CLOSE,
)

MESSAGE_MODER_ADD_BY_ID_FORM = Form(
    'Add message by id to move group',
    [
        TextInput(
            'message\'s id',
            min_length = 7,
            max_length = 21,
            custom_id = 'message_id',
        )
    ],
    custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID,
)

@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_MESSAGE_MOVER_SUBMIT)
async def submit_message_mover(event):
    await maybe_call_message_mover_method(event, MessageMoverContext.submit)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_MESSAGE_MOVER_CANCEL)
async def cancel_message_mover(event):
    await maybe_call_message_mover_method(event, MessageMoverContext.cancel)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_MESSAGE_MOVER_CLOSE)
async def close_message_mover(client, event):
    if event.user_permissions.can_manage_messages:
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)


async def maybe_call_message_mover_method(event, function):
    if not event.user_permissions.can_manage_messages:
        return
    
    try:
        message_mover_context = MESSAGE_MOVER_CONTEXTS[(event.user.id, event.channel_id)]
    except KeyError:
        pass
    else:
        await function(message_mover_context, event)

MESSAGE_MOVER_FINALIZATION_REASON_NONE = 0
MESSAGE_MOVER_FINALIZATION_REASON_CANCELLED = 1
MESSAGE_MOVER_FINALIZATION_REASON_TIMEOUT = 2
MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTED = 3
MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTING = 4

MESSAGE_MOVER_SUBMITTING_EMOJI = Emoji.precreate(704393708467912875)

class MessageMoverContext:
    def __init__(self, client, event, source_channel_id, target_channel_id, target_thread_id):
        self.client = client
        self.event = event
        self.webhook_waiter = None
        self.source_channel_id = source_channel_id
        self.target_channel_id = target_channel_id
        self.target_thread_id = target_thread_id
        self.messages = set()
        self.next_update = LOOP_TIME() + MESSAGE_MOVER_CONTEXT_TIMEOUT
        self._timeout_handle = None
        key = (event.user.id, source_channel_id)
        self.key = key
        
        MESSAGE_MOVER_CONTEXTS[key] = self
    
    
    def get_embed(self, finalization_reason):
        target_thread_id = self.target_thread_id
        if target_thread_id:
            channel_id = target_thread_id
        else:
            channel_id = self.target_channel_id
        
        if finalization_reason == MESSAGE_MOVER_FINALIZATION_REASON_NONE:
            title = None
            description = (
                f'To channel: {mention_channel_by_id(channel_id)}\n\n'
                f'Expires after 10 minutes | {format_loop_time(self.next_update, TIMESTAMP_STYLES.relative_time)}'
            )
            color = None
        
        elif finalization_reason == MESSAGE_MOVER_FINALIZATION_REASON_CANCELLED:
            title = 'Cancelled'
            description = None
            color = 0xff0000
        
        elif finalization_reason == MESSAGE_MOVER_FINALIZATION_REASON_TIMEOUT:
            title = 'Timeout'
            description = None
            color = 0xff0000
        
        elif finalization_reason == MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTED:
            title = 'Messages moved'
            description = None
            color = 0x00ff00
        
        elif finalization_reason == MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTING:
            title = 'Moving right now!'
            description = None
            color = None
        
        else:
            title = None
            description = None
            color = None
        
        if description is None:
            description = f'To channel: {mention_channel_by_id(channel_id)}'
        
        if title is None:
            title = 'Moving messages'
        else:
            title = f'Moving messages | {title}'
        
        embed = Embed(
            title,
            description,
            color = color,
        )
        
        messages = self.messages
        for index, message in enumerate(sorted(messages), 1):
            embed.add_field(
                f'Message {index}',
                (
                    f'Id: {message.id}\n'
                    f'Author: {message.author.full_name}\n'
                    f'Length: {len(message)}'
                ),
                inline = True,
            )
        
        embed.add_footer('Up to 20 messages')
        
        if (
            (finalization_reason == MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTING) or
            (finalization_reason == MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTED)
        ):
            embed.add_thumbnail(MESSAGE_MOVER_SUBMITTING_EMOJI.url)
        
        return embed
    
    
    async def start(self):
        try:
            await self.client.interaction_response_message_create(
                self.event,
                embed = self.get_embed(MESSAGE_MOVER_FINALIZATION_REASON_NONE),
                components = MESSAGE_MOVER_COMPONENTS_ENABLED,
            )
        except:
            try:
                MESSAGE_MOVER_CONTEXTS[self.key]
            except KeyError:
                pass
            
            raise
        
        self._timeout_handle = KOKORO.call_at(self.next_update, timeout_message_mover_context, self.key)
    
    
    def trigger_timeout(self):
        next_update = self.next_update
        if next_update <= LOOP_TIME():
            Task(self.do_timeout(), KOKORO)
            timeout_handle = None
        else:
            timeout_handle = KOKORO.call_at(next_update, timeout_message_mover_context, self.key)
        self._timeout_handle = timeout_handle
    
    
    def _cancel(self):
        try:
            MESSAGE_MOVER_CONTEXTS[self.key]
        except KeyError:
            pass
        
        timeout_handle = self._timeout_handle
        if (timeout_handle is not None):
            self._timeout_handle = timeout_handle
            timeout_handle.cancel()
    
    
    async def do_timeout(self):
        self._cancel()
        
        await self.client.interaction_response_message_edit(
            self.event,
            embed = self.get_embed(MESSAGE_MOVER_FINALIZATION_REASON_TIMEOUT),
            components = MESSAGE_MOVER_COMPONENTS_AFTERLIFE,
        )
    
    
    async def add_message(self, event, message):
        messages = self.messages
        if len(messages) == 20:
            await self.client.interaction_response_message_create(
                event,
                '20 message limit reached',
                show_for_invoking_user_only = True,
            )
        
        else:
            messages.add(message)
            await self.client.interaction_response_message_create(
                event,
                embed = self.get_embed(MESSAGE_MOVER_FINALIZATION_REASON_NONE),
                components = MESSAGE_MOVER_COMPONENTS_ENABLED,
            )
            await self.client.interaction_response_message_delete(self.event)
            self.next_update = LOOP_TIME() + MESSAGE_MOVER_CONTEXT_TIMEOUT
            self.event = event
    
    
    async def submit(self, event):
        self._cancel()
        
        move_messages_task = Task(self.move_messages_parallelly(), KOKORO)
        try:
            await self.client.interaction_component_message_edit(
                event,
                embed = self.get_embed(MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTING),
                components = None,
            )
        except:
            move_messages_task.cancel()
            raise
        
        await self.client.interaction_response_message_edit(
            event,
            embed = self.get_embed(MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTED),
            components = MESSAGE_MOVER_COMPONENTS_AFTERLIFE,
        )
    
    
    async def cancel(self, event):
        self._cancel()
        
        await self.client.interaction_component_message_edit(
            event,
            embed = self.get_embed(MESSAGE_MOVER_FINALIZATION_REASON_CANCELLED),
            components = MESSAGE_MOVER_COMPONENTS_AFTERLIFE,
        )
    
    async def move_messages_parallelly(self):
        self.get_webhook_waiter()
        
        tasks = []
        for message in self.messages:
            task = Task(self.move_message(message), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(
            tasks,
            KOKORO,
        )
    
    def get_webhook_waiter(self):
        webhook_waiter = self.webhook_waiter
        if (webhook_waiter is None):
            webhook_waiter = Future(KOKORO)
            self.webhook_waiter = webhook_waiter
            Task(self.get_webhook_task(webhook_waiter), KOKORO)
        
        return webhook_waiter
    
    
    async def get_webhook_task(self, webhook_waiter):
        try:
            webhook = await get_webhook(self.client, self.target_channel_id)
        except GeneratorExit:
            webhook_waiter.cancel()
            raise
        except BaseException as err:
            webhook_waiter.set_exception_if_pending(err)
        else:
            webhook_waiter.set_result_if_pending(webhook)
    
    
    async def move_message(self, message):
        files = await get_files(self.client, message)
        webhook = await self.get_webhook_waiter()
        
        guild_id = self.event.guild_id
        
        await self.client.webhook_message_create(
            webhook,
            message.content,
            embed = message.clean_embeds,
            file = files,
            allowed_mentions = None,
            name = message.author.name_at(guild_id),
            avatar_url = message.author.avatar_url_at(guild_id),
            thread = self.target_thread_id,
        )
        
        files = None
        
        Task(message_delete(self.client, message), KOKORO)


@SLASH_CLIENT.interactions(guild=[GUILD__KOISHI_CLAN, GUILD__SUPPORT])
async def move_messages(
    client,
    event,
    channel: ('channel_group_messageable', 'Where to move the message.'),
):
    """Moves messages | Mod only"""
    check_permissions(client, event, channel)
    
    if isinstance(channel, ChannelThread):
        channel_id = channel.parent_id
        thread_id = channel.id
    else:
        channel_id = channel.id
        thread_id = 0
    
    context = MessageMoverContext(client, event, event.channel_id, channel_id, thread_id)
    await context.start()


@SLASH_CLIENT.interactions(guild=[GUILD__KOISHI_CLAN, GUILD__SUPPORT], target='message')
async def add_to_move_group(
    event,
    message,
):
    """Adds a message to message move context."""
    await add_message_to_move_group(event, message)



@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID)
async def add_message_by_id_button_click(event):
    if event.user_permissions.can_manage_messages:
        return MESSAGE_MODER_ADD_BY_ID_FORM


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID, target='form')
async def add_message_by_id_form_submit(client, event, *, message_id):
    if not is_id(message_id):
        abort(f'Please submit a message\'s id.')
    
    try:
        message = await client.message_get(event.channel_id, int(message_id))
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            abort('The given id refers to a non-existing message.')
        
        raise
    
    await add_message_to_move_group(event, message)
    


async def add_message_to_move_group(event, message):
    key = (event.user.id, event.channel_id)
    
    try:
        context = MESSAGE_MOVER_CONTEXTS[key]
    except KeyError:
        abort('There is no message mover context in the channel.')
    else:
        await context.add_message(event, message)


@SLASH_CLIENT.interactions(guild=[GUILD__KOISHI_CLAN, GUILD__SUPPORT], show_for_invoking_user_only=True)
async def move_channel(
    client,
    event,
    channel: ('channel_group_messageable', 'Where to move the channel\'s messages.'),
):
    """Moves channel's all messages | Mod only"""
    check_permissions(client, event, channel)
    
    yield f'Starting to move messages to {channel.name}'
    
    if isinstance(channel, ChannelThread):
        channel_id = channel.parent_id
        thread_id = channel.id
    else:
        channel_id = channel.id
        thread_id = 0
    
    source_channel_id = event.channel_id
    guild_id = event.guild_id
    
    request_more = True
    after_id = 0
    webhook = await get_webhook(client, channel_id)
    
    while request_more:
        messages = await client.message_get_chunk(source_channel_id, after=after_id)
        
        if len(messages) < 100:
            request_more = False
        else:
            after_id = messages[0].id
        
        for message in reversed(messages):
            files = await get_files(client, message)
            
            await client.webhook_message_create(
                webhook,
                message.content,
                embed = message.clean_embeds,
                file = files,
                allowed_mentions = None,
                name = message.author.name_at(guild_id),
                avatar_url = message.author.avatar_url_at(guild_id),
                thread = thread_id,
            )
            
            files = None
