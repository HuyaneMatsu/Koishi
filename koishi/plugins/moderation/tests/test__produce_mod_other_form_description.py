import vampytest
from hata import Guild, User

from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_INVITES_DISABLE, ACTION_TYPE_INVITES_ENABLE,
    ACTION_TYPE_KICK, ACTION_TYPE_MUTE, ACTION_TYPE_UN_BAN, ACTION_TYPE_UN_MUTE
)
from ..content_building import produce_mod_other_form_description


def _iter_options():
    user = User.precreate(202607260000, name = 'Suwako')
    guild = Guild.precreate(202607260001, name = 'Moriya shrine')
    
    yield (
        ACTION_TYPE_BAN,
        user,
        guild,
        '### Banning Suwako from Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        user,
        guild,
        '### Un-banning Suwako from Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        user,
        guild,
        '### Edit ban reason of Suwako in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        user,
        guild,
        '### Muting Suwako in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        user,
        guild,
        '### Un-muting Suwako in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        user,
        guild,
        '### Kicking Suwako from Moriya shrine.',
    )


    yield (
        ACTION_TYPE_BAN,
        None,
        guild,
        '### Banning user(s) from Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        None,
        guild,
        '### Un-banning user(s) from Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        None,
        guild,
        '### Edit ban reason of user(s) in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        None,
        guild,
        '### Muting user(s) in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        None,
        guild,
        '### Un-muting user(s) in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        None,
        guild,
        '### Kicking user(s) from Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_INVITES_DISABLE,
        None,
        guild,
        '### Disabling invites of Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_INVITES_ENABLE,
        None,
        guild,
        '### Enabling invites of Moriya shrine.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_mod_other_form_description(action_type, target, guild):
    """
    Tests whether ``produce_mod_other_form_description`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    target : ``None | ClientUserBase``
        The targeted user if any.
    
    guild : ``Guild``
        The local guild.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_mod_other_form_description(action_type, target, guild)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
