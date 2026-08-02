import vampytest
from hata import Guild, User

from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE
from ..content_building import produce_mod_self_completion_header


def _iter_options():
    user = User.precreate(202607260009, name = 'Suwako')
    
    yield (
        ACTION_TYPE_BAN,
        user,
        0,
        '### Hecatia Yeah!\n\nSuwako have banned themselves!',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        user,
        0,
        '### Hecatia Yeah!\n\nSuwako have muted themselves!',
    )
    
    yield (
        ACTION_TYPE_KICK,
        user,
        0,
        '### Hecatia Yeah!\n\nSuwako have kicked themselves!',
    )
    
    yield (
        255,
        user,
        0,
        '### Hecatia Yeah!\n\nSuwako have pegged themselves!',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_mod_self_completion_header(action_type, user, guild_id):
    """
    Tests whether ``produce_mod_self_completion_header`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    targets : ``None | tuple<ClientUserBase>``
        Targeted users.
    
    guild_id : ``Guild``
        The local guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_mod_self_completion_header(action_type, user, guild_id)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
