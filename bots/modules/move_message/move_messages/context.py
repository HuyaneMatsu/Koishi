__all__ = ()

from hata import Embed, KOKORO, TIMESTAMP_STYLES, format_loop_time, mention_channel_by_id
from scarletio import Future, LOOP_TIME, Task, TaskGroup

from ..helpers import get_files, get_webhook, message_delete

from .constants import (
    MESSAGE_MOVER_COMPONENTS_AFTERLIFE, MESSAGE_MOVER_COMPONENTS_ENABLED, MESSAGE_MOVER_CONTEXTS,
    MESSAGE_MOVER_CONTEXT_TIMEOUT, MESSAGE_MOVER_SUBMITTING_EMOJI
)

MESSAGE_MOVER_FINALIZATION_REASON_NONE = 0
MESSAGE_MOVER_FINALIZATION_REASON_CANCELLED = 1
MESSAGE_MOVER_FINALIZATION_REASON_TIMEOUT = 2
MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTED = 3
MESSAGE_MOVER_FINALIZATION_REASON_SUBMITTING = 4


def timeout_message_mover_context(key):
    try:
        message_mover_context = MESSAGE_MOVER_CONTEXTS[key]
    except KeyError:
        pass
    else:
        message_mover_context.trigger_timeout()


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
        await TaskGroup(KOKORO, (Task(self.move_message(message), KOKORO) for message in self.messages)).wait_all()
    
    
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
