__all__ = ()

from ...bot_utils.constants import GUILD__SUPPORT
from ...bots import COMMAND_CLIENT

from .logic import build_output, parse_input


@COMMAND_CLIENT.interactions(
    guild = GUILD__SUPPORT,
    target = 'message',
)
async def orange_juice_achievement_parse(client, interaction_event, target):
    """
    Parses your orange juice achievements into a Yes / No list.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction evnet.
    
    target : ``Message``
        The targeted message.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        attachment = target.attachment
        if (attachment is None):
            content = target.content
            if content is None:
                error_message = 'The message does not have content / attachment.'
                break
        
        else:
            if not attachment.name.endswith('.txt'):
                error_message = 'Are you sure whether the message\'s attachment is text?'
                break
            
            if (not attachment.size) or (attachment.size >= 1048576):
                error_message = 'Suspicious attachment size.'
                break
            
            content_raw = await client.download_attachment(attachment)
            
            try:
                content = content_raw.decode()
            except UnicodeDecodeError:
                error_message = 'Could not decide attachment content.'
                break
            
            content_raw = None
        
        user_owned_achievements = parse_input(content)
        content = None
        
        if not user_owned_achievements:
            error_message = 'Empty input.'
            break
        
        output = build_output(user_owned_achievements)
        user_owned_attachments = None
        
        # Respond
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            file = (
                'output.txt',
                output,
            )
        )
        return
    
    await client.interaction_response_message_edit(interaction_event, error_message)
    return
