__all__ = ()

from hata import Client

from ...bots import FEATURE_CLIENTS

from .command_helpers_snipe_whole_message import respond_snipe_whole_message


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    target = 'message',
)
async def snipe(client, event, target):
    """
    Snipes the emojis, reactions and stickers of the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    target : ``Message``
        the targeted message by the user.
    """
    return await respond_snipe_whole_message(client, event, target, True, False)
