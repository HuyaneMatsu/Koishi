__all__ = ()

from scarletio import ReuAsyncIO

from os.path import join as join_paths
from re import compile as re_compile, I as re_ignore_case

from ..chat_interaction import ChatInteraction
from ..constants import PATH_ASSETS


MATCH_ROBLOX = re_compile('rob(?:lox|ux)', re_ignore_case)
PATH_IMAGE = join_paths(PATH_ASSETS, 'only-kids-play-roblox-meme.png')


NAME = 'roblox'


def roblox_check_can_trigger(client, message):
    """
    Returns whether the chat interaction can be triggered.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who received the message.
    message : ``Message``
        The received message.
    
    Returns
    -------
    outcome : `None | str`
    """
    content = message.content
    if content is None:
        return None
    
    if MATCH_ROBLOX.search(content) is None:
        return None
    
    return ''


async def roblox_trigger(client, message, outcome):
    """
    Triggers the chat interaction.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    message : ``Message``
        The received message.
    outcome : `str`
        Output of the can trigger check.
    """
    with await ReuAsyncIO(PATH_IMAGE) as file:
        await client.message_create(message.channel, file = file)


CHAT_INTERACTION = ChatInteraction(
    NAME,
    roblox_check_can_trigger,
    roblox_trigger,
)
