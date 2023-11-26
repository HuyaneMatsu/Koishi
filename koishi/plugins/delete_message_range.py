__all__ = ()

from functools import partial as partial_func

from hata import DATETIME_FORMAT_CODE, Embed, KOKORO
from hata.ext.slash import abort
from scarletio import Task

from ..bot_utils.constants import GUILD__SUPPORT
from ..bots import FEATURE_CLIENTS


DELETE_RANGE_CONTEXTS = {}

DELETE_RANGE_TIMEOUT = 300.0

DELETE_RANGE_CONTEXT_STATE_NONE = 0
DELETE_RANGE_CONTEXT_STATE_TIMEOUT = 1
DELETE_RANGE_CONTEXT_STATE_STARTING = 2
DELETE_RANGE_CONTEXT_STATE_FINISHED = 3


class DeleteRangeContext:
    
    __slots__ = ('__weakref__', 'client', 'event', 'message_since', 'timeout_handle', 'message_till')
    
    def __init__(self, client, event, message):
        self.client = client
        self.event = event
        self.message_since = message
        self.message_till = None
        self.timeout_handle = KOKORO.call_after_weak(DELETE_RANGE_TIMEOUT, self.timeout)
        DELETE_RANGE_CONTEXTS[(event.user.id, message.channel_id)] = self
    
    def timeout(self):
        self.cancel()
        Task(KOKORO, self.notify_timeout())
    
    
    def cancel(self):
        timeout_handle = self.timeout_handle
        if (timeout_handle is not None):
            self.timeout_handle = None
            timeout_handle.cancel()
        
        try:
            del DELETE_RANGE_CONTEXTS[(self.event.user.id, self.message_since.channel_id)]
        except KeyError:
            pass
    
    
    def get_embed(self, state):
        user = self.message_since.author
        
        if state == DELETE_RANGE_CONTEXT_STATE_NONE:
            title = 'Range delete context'
            color = 0x00ff00
        
        elif state == DELETE_RANGE_CONTEXT_STATE_TIMEOUT:
            title = 'Range delete context | Timeout'
            color = 0xff0000
            
        elif state == DELETE_RANGE_CONTEXT_STATE_STARTING:
            title = 'Range delete context | Deleting began'
            color = 0x0000ff
            
        elif state == DELETE_RANGE_CONTEXT_STATE_FINISHED:
            title = 'Range delete context | Deleting done'
            color = 0x0000ff
        
        else:
            title = 'Range delete context'
            color = None
        
        description_parts = [
            'Delete messages by ',
            user.mention,
            '\n Since: ',
            format(self.message_since.created_at, DATETIME_FORMAT_CODE),
        ]
        
        message_till = self.message_till
        if (message_till is not None):
            description_parts.append('\nTill: ')
            description_parts.append(format(self.message_till.created_at, DATETIME_FORMAT_CODE))
        
        description = ''.join(description_parts)
        description_parts = None
        
        return Embed(
            title,
            description,
            color = color,
        ).add_thumbnail(
            user.avatar_url,
        ).add_footer(
            f'This context times out after {DELETE_RANGE_TIMEOUT:.0f} seconds.',
        )
    
    
    async def notify_timeout(self):
        await self.client.interaction_followup_message_create(
            self.event,
            embed = self.get_embed(DELETE_RANGE_CONTEXT_STATE_TIMEOUT),
            show_for_invoking_user_only = True,
        )


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    target = 'message',
    show_for_invoking_user_only = True,
)
async def delete_from(
    client,
    event,
    target,
):
    if not event.user_permissions.can_manage_messages:
        abort('You need manage messages permission to execute this command.')
    
    if (event.user.id, target.channel_id) in DELETE_RANGE_CONTEXTS:
        abort(
            'You already have a context open in the channel.\n'
            'Please close that first.'
        )
    
    context = DeleteRangeContext(client, event, target)
    
    return context.get_embed(DELETE_RANGE_CONTEXT_STATE_NONE)


def match_message_author(user, message):
    return (message.author is user)


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    target = 'message',
    show_for_invoking_user_only = True,
)
async def delete_till(
    client,
    event,
    target,
):
    if not event.user_permissions.can_manage_messages:
        abort('You need manage messages permission to execute this command.')
    
    try:
        context = DELETE_RANGE_CONTEXTS[(event.user.id, target.channel_id)]
    except KeyError:
        pass
    else:
        context.message_till = target
        context.cancel()
        
        yield context.get_embed(DELETE_RANGE_CONTEXT_STATE_STARTING)
        
        before = target.id
        after = context.message_since.id
        
        if before < after:
            before, after = after, before
        
        # This will fix not including issues
        before += 1
        after -= 1
        
        await client.multi_client_message_delete_sequence(
            event.channel,
            after = after,
            before = before,
            filter = partial_func(match_message_author, context.message_since.author),
        )
        
        if not event.is_expired():
            yield context.get_embed(DELETE_RANGE_CONTEXT_STATE_FINISHED)
        
        return
    
    abort('No `since` message defined.')
