import vampytest
from hata import Message, MessageType, User

from ..owo import get_reply_from_content, owo_check_can_trigger


def _iter_options__get_reply_from_content():
    yield 'random', 'OwO'
    yield 'owo', 'OwO'
    yield 'Uwu', 'UwU'
    yield '0w0', '0w0'
    yield 'OWO', 'OwO'


@vampytest._(vampytest.call_from(_iter_options__get_reply_from_content()).returning_last())
def test__get_reply_from_content(content):
    """
    Tests whether ``get_reply_from_content`` works as intended.
    
    Parameters
    ----------
    content : `str`
        Content to translate.
    
    Returns
    -------
    content : `str`
    """
    return get_reply_from_content(content)


def _iter_options__owo_check_can_trigger():
    user_0 = User.precreate(202311050000)
    
    yield (
        user_0,
        Message.precreate(
            202311050001,
            content = None,
            message_type = MessageType.default,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311050002,
            content = 'owo',
            message_type = MessageType.default,
        ),
        'owo',
    )

    yield (
        user_0,
        Message.precreate(
            202311050003,
            content = 'owo',
            message_type = MessageType.inline_reply,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311050004,
            content = 'owO',
            message_type = MessageType.default,
        ),
        'owO',
    )

    yield (
        user_0,
        Message.precreate(
            202311050005,
            content = '0w0',
            message_type = MessageType.default,
        ),
        '0w0',
    )

    yield (
        user_0,
        Message.precreate(
            202311050006,
            content = 'Uwu',
            message_type = MessageType.default,
        ),
        'Uwu',
    )


@vampytest._(vampytest.call_from(_iter_options__owo_check_can_trigger()).returning_last())
def test__owo_check_can_trigger(client, message):
    """
    Tests whether ``owo_check_can_trigger`` works as intended.
    
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
    return owo_check_can_trigger(client, message)
