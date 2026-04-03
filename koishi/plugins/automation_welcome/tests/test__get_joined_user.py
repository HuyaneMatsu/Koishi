import vampytest
from hata import InteractionEvent, Message, User

from ..interactions import get_joined_user


def _iter_options():
    yield InteractionEvent(), None
    yield InteractionEvent(message = Message()), None
    
    user = User.precreate(202312140000)
    yield InteractionEvent(message = Message(mentioned_users = [user])), user


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_joined_user(input_value):
    """
    Tests whether ``get_joined_user`` works as intended.
    
    Parameters
    ----------
    input_value : ``InteractionEvent``
        Event to test with.
    
    Returns
    -------
    output : `None | ClientUserBase`
    """
    return get_joined_user(input_value)
