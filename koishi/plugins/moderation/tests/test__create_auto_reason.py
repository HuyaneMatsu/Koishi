import vampytest
from hata import InteractionEvent, User

from ..shared_helpers import create_auto_reason


def _iter_options():
    user_id = 202310180000
    user_name = 'Satori'
    
    event = InteractionEvent(user = User.precreate(user_id, name = user_name))
    
    yield event, None, f'Requested by: {user_name} [{user_id}]'
    yield event, 'Ban reimu', f'Ban reimu\nRequested by: {user_name} [{user_id}]'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__create_auto_reason(event, reason):
    """
    Tests whether ``create_auto_reason`` works as intended.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interactions event.
    reason : `None`, `str`
        Reason given.
    
    Returns
    -------
    output : `str`
    """
    return create_auto_reason(event, reason)
