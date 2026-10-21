__all__ = ()

from hata import CLIENTS, KOKORO, Permission
from threading import main_thread
from signal import SIGKILL as SIGNAL_KILL, pthread_kill as  process_thread_kill

from koishi.bots import COMMAND_CLIENT


@COMMAND_CLIENT.interactions(
    is_global = True,
    name = 'shutdown',
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def command_execute(client, interaction_event):
    """
    Shutdowns me.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    while True:
        if not client.is_owner(interaction_event.user):
            error_message = 'Owner only.'
            break
    
        for client_ in CLIENTS.values():
            await client_.disconnect()
        
        await client.interaction_response_message_create(interaction_event, content = 'Clients stopped, stopping process.')
        
        KOKORO.stop()
        process_thread_kill(main_thread().ident, SIGNAL_KILL)
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
