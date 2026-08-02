import vampytest
from hata import User

from ..content_building import produce_user_banned


def _iter_options():
    user = User.precreate(202607180000, name = 'Suwako')
    
    yield (
        user,
        0,
        False,
        'Suwako is **NOT YET** banned.',
    )
    
    yield (
        user,
        0,
        True,
        'Suwako is banned.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_user_banned(user, guild_id, banned):
    """
    Tests whether ``produce_user_banned`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    
    guild_id : `int`
        The local guild's identifier.
    
    banned : `bool`
        Whether the user is banned.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_user_banned(user, guild_id, banned)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
