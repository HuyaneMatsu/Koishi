__all__ = ()

from re import compile as re_compile, I as re_ignore_case

from hata import MessageType

from ..chat_interaction import ChatInteraction


OWO_DEFAULT = 'OwO'
OWO_MAP = {
    'owo': 'OwO',
    'uwu': 'UwU',
    '0w0': '0w0',
}

MATCH_OWO = re_compile('(owo|0w0|uwu)', re_ignore_case)


NAME = 'owo'


def get_reply_from_content(content):
    """
    Gets the owo reply.
    
    Parameters
    ----------
    content : `str`
        Content to translate.
    
    Returns
    -------
    content : `str`
    """
    return OWO_MAP.get(content.casefold(), OWO_DEFAULT)


def owo_check_can_trigger(client, message):
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
    
    if message.type is not MessageType.default:
        return None
    
    if MATCH_OWO.fullmatch(content) is None:
        return None
    
    return content


async def owo_trigger(client, message, outcome):
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
    content = get_reply_from_content(outcome)
    await client.message_create(message.channel, content = content)


CHAT_INTERACTION = ChatInteraction(
    NAME,
    owo_check_can_trigger,
    owo_trigger,
)
