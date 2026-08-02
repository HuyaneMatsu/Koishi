import vampytest
from hata import Guild, User

from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_INVITES_DISABLE, ACTION_TYPE_INVITES_ENABLE,
    ACTION_TYPE_KICK, ACTION_TYPE_MUTE, ACTION_TYPE_UN_BAN, ACTION_TYPE_UN_MUTE
)
from ..content_building import produce_mod_other_completion_header


def _iter_options():
    user_0 = User.precreate(202607260004, name = 'Suwako')
    user_1 = User.precreate(202607260005, name = 'Kanako')
    
    guild = Guild.precreate(202607260006, name = 'Moriya shrine')
    
    yield (
        ACTION_TYPE_BAN,
        (user_0, user_1),
        guild,
        '### Hecatia Yeah!\n\nSuwako and Kanako have been banned!',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        (user_0, user_1),
        guild,
        '### Hecatia Yeah!\n\nSuwako and Kanako have been un-banned!',
    )
    
    # Invalid for this action.
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        (user_0, user_1),
        guild,
        '### Hecatia Yeah!\n\nBan reason of Suwako and Kanako have been edited!',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        (user_0, user_1),
        guild,
        '### Hecatia Yeah!\n\nSuwako and Kanako have been muted!',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        (user_0, user_1),
        guild,
        '### Hecatia Yeah!\n\nSuwako and Kanako have been un-muted!',
    )
    
    yield (
        ACTION_TYPE_KICK,
        (user_0, user_1),
        guild,
        '### Hecatia Yeah!\n\nSuwako and Kanako have been kicked!',
    )
    
    yield (
        ACTION_TYPE_INVITES_DISABLE,
        None,
        guild,
        '### Hecatia Yeah!\n\nInvites of Moriya shrine have been disabled!',
    )
    
    yield (
        ACTION_TYPE_INVITES_ENABLE,
        None,
        guild,
        '### Hecatia Yeah!\n\nInvites of Moriya shrine have been enabled!',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_mod_other_completion_header(action_type, targets, guild):
    """
    Tests whether ``produce_mod_other_completion_header`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    targets : ``None | tuple<ClientUserBase>``
        Targeted users.
    
    guild : ``Guild``
        The local guild.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_mod_other_completion_header(action_type, targets, guild)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
