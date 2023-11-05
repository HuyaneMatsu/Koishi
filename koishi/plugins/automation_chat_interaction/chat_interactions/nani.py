__all__ = ()

from re import compile as re_compile, I as re_ignore_case

from hata import MessageType

from ..chat_interaction import ChatInteraction


NANI_MATCH = re_compile('omae wa mou', re_ignore_case)
OUTCOME = 'NANI?'


NAME = 'nani'


def nani_check_can_trigger(client, message):
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
    
    message_type = message.type
    if message_type is MessageType.default:
        pass
    
    elif message_type is MessageType.inline_reply:
        referenced_message = message.referenced_message
        if referenced_message is None:
            return None
        
        if referenced_message.author is not client:
            return None
    
    else:
        return None
    
    if NANI_MATCH.match(content) is None:
        return None
    
    return OUTCOME


async def nani_trigger(client, message, outcome):
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
    await client.message_create(message.channel, content = outcome)


CHAT_INTERACTION = ChatInteraction(
    NAME,
    nani_check_can_trigger,
    nani_trigger,
)
