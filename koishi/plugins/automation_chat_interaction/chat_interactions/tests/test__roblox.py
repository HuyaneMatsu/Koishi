import vampytest
from hata import Message, User

from ..roblox import roblox_check_can_trigger


def _iter_options__roblox_check_can_trigger():
    user_0 = User.precreate(202311050008)
    
    yield (
        user_0,
        Message.precreate(
            202311050009,
            content = None,
        ),
        None,
    )

    yield (
        user_0,
        Message.precreate(
            202311050010,
            content = 'Only kids play roblox.',
        ),
        '',
    )

    yield (
        user_0,
        Message.precreate(
            202311050011,
            content = 'KC people selling their soul for robux be like.',
        ),
        '',
    )

    yield (
        user_0,
        Message.precreate(
            202311050012,
            content = 'Weird lego people.',
        ),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options__roblox_check_can_trigger()).returning_last())
def test__roblox_check_can_trigger(client, message):
    """
    Tests whether ``roblox_check_can_trigger`` works as intended.
    
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
    return roblox_check_can_trigger(client, message)
