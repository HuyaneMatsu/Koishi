import vampytest
from hata import User

from ..helpers import build_reason


def _iter_options():
    user = User.precreate(202607180004, name = 'Suwako')
    
    yield (
        user,
        0,
        None,
        f'Requested by: Suwako [{user.id}]',
    )
    
    yield (
        user,
        0,
        'frog',
        f'frog\nRequested by: Suwako [{user.id}]',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_reason(user, guild_id, reason):
    """
    Tests whether ``build_reason`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The invoking user.
    
    guild_id : `int`
        The local guild's identifier.
    
    reason : `None | str`
        Reason given.
    
    Returns
    -------
    output : `str`
    """
    output = build_reason(user, guild_id, reason)
    vampytest.assert_instance(output, str)
    return output
