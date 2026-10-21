__all__ = ()

from hata import Permission, attachment_request_create_regular_create

from .execution import LOCK, run
from .helpers import STRIP_STATE_EMPTY, STRIP_STATE_UNCLOSED, strip_content

from koishi.bots import COMMAND_CLIENT


@COMMAND_CLIENT.interactions(
    is_global = True,
    name = 'execute',
    required_permissions = Permission().update_by_keys(administrator = True),
    target = 'message',
)
async def command_execute(client, interaction_event, target):
    """
    Execute code through me. Owner only!!!
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``Message``
        The targeted message.
    """
    while True:
        if not client.is_owner(interaction_event.user):
            error_message = 'Owner only.'
            break
        
        if LOCK.is_locked():
            error_message = 'An execution is already running.'
            break
        
        attachments = target.attachments
        if (attachments is not None):
            if len(attachments) != 1:
                error_message = 'Multiple attachments.'
                break
            
            attachment = attachments[0]
            if attachment.content_type not in (
                'text/plain',
                'text/plain; charset=utf-8',
                'text/x-python',
                'ext/x-python; charset=utf-8',
            ):
                error_message = 'Attachment has invalid content type.'
                break
            
            async with client.http.get(attachment.url) as response:
                if response.status != 200:
                    error_message = 'failed to download attachment.'
                    break
                
                content = await response.text()
        
        else:
            content = target.content
            if content is None:
                error_message = 'No content.'
                break
        
        strip_state, content = strip_content(content)
        if strip_state == STRIP_STATE_EMPTY:
            error_message = 'Empty content.'
            break
        
        if strip_state == STRIP_STATE_UNCLOSED:
            error_message = 'Unclosed grave or code block.'
            break
        
        await client.interaction_response_message_create(
            interaction_event,
            content = 'Execution began.'
        )
        
        output = await run(content)
        if len(output) < 1992:
            await client.message_create(interaction_event.channel, content = f'```\n{output}\n```')
        else:
            await client.message_create(
                interaction_event.channel,
                attachments = [attachment_request_create_regular_create('response.txt', output)]
            )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
