import vampytest
from hata import Message, MessageType, User

from ..nani import OUTCOME, nani_check_can_trigger


def _iter_options__nani_check_can_trigger():
    user_0 = User.precreate(202311040019)
    user_1 = User.precreate(202311040020)
    
    yield (
        user_0,
        Message.precreate(
            202311040012,
            content = None,
            message_type = MessageType.default,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311040013,
            content = 'Omae wa mou shindeiru!!!',
            message_type = MessageType.default,
        ),
        OUTCOME,
    )

    yield (
        user_0,
        Message.precreate(
            202311040014,
            content = 'omae wa mou',
            message_type = MessageType.inline_reply,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311040015,
            content = 'omae wa mou',
            message_type = MessageType.inline_reply,
            referenced_message = Message.precreate(
                202311040016,
                author = user_1,
            )
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311040017,
            content = 'omae wa mou',
            message_type = MessageType.inline_reply,
            referenced_message = Message.precreate(
                202311040018,
                author = user_0,
            )
        ),
        OUTCOME,
    )

    
@vampytest._(vampytest.call_from(_iter_options__nani_check_can_trigger()).returning_last())
def test__nani_check_can_trigger(client, message):
    """
    Tests whether ``nani_check_can_trigger`` works as intended.
    
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
    return nani_check_can_trigger(client, message)
