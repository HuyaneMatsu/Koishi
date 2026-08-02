import vampytest
from hata import User

from ..content_building import produce_user_listing


def _iter_options():
    user_0 = User.precreate(202607200000, name = 'Suwako')
    user_1 = User.precreate(202607200001, name = 'Kanako')
    user_2 = User.precreate(202607200002, name = 'Sanae')
    
    yield (
        (user_0,),
        0,
        'Suwako',
    )
    
    yield (
        (user_0, user_1),
        0,
        'Suwako and Kanako',
    )
    
    yield (
        (user_0, user_1, user_2,),
        0,
        'Suwako, Kanako and Sanae',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_user_listing(users, guild_id):
    """
    Tests whether ``produce_user_listing`` works as intended.
    
    Parameters
    ----------
    users : ``tuple<ClientUserBase>``
        Users to produce their names of.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_user_listing(users, guild_id)]
    for part in parts:
        vampytest.assert_instance(part, str)
    
    return ''.join(parts)
