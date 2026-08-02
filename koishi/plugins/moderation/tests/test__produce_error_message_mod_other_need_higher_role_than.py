import vampytest
from hata import User

from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_KICK, ACTION_TYPE_MUTE, ACTION_TYPE_UN_BAN,
    ACTION_TYPE_UN_MUTE
)
from ..content_building import produce_error_message_mod_other_need_higher_role_than


def _iter_options():
    user_0 = User.precreate(202607210002, name = 'Suwako')
    user_1 = User.precreate(202607210003, name = 'Kanako')
    
    yield (
        ACTION_TYPE_BAN,
        True,
        (user_0, user_1),
        0,
        'You need to have higher role than Suwako and Kanako to ban them.',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        True,
        (user_0, user_1),
        0,
        'You need to have higher role than Suwako and Kanako to un-ban them.',
    )
    
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        True,
        (user_0, user_1),
        0,
        'You need to have higher role than Suwako and Kanako to edit their ban reason.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        True,
        (user_0, user_1),
        0,
        'You need to have higher role than Suwako and Kanako to mute them.',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        True,
        (user_0, user_1),
        0,
        'You need to have higher role than Suwako and Kanako to un-mute them.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        True,
        (user_0, user_1),
        0,
        'You need to have higher role than Suwako and Kanako to kick them.',
    )
    
    yield (
        255,
        True,
        (user_0, user_1),
        0,
        'You need to have higher role than Suwako and Kanako to peg them.',
    )
    
    
    yield (
        ACTION_TYPE_BAN,
        False,
        (user_0, user_1),
        0,
        'I require higher role than Suwako and Kanako to ban them.',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        False,
        (user_0, user_1),
        0,
        'I require higher role than Suwako and Kanako to un-ban them.',
    )
    
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        False,
        (user_0, user_1),
        0,
        'I require higher role than Suwako and Kanako to edit their ban reason.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        False,
        (user_0, user_1),
        0,
        'I require higher role than Suwako and Kanako to mute them.',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        False,
        (user_0, user_1),
        0,
        'I require higher role than Suwako and Kanako to un-mute them.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        False,
        (user_0, user_1),
        0,
        'I require higher role than Suwako and Kanako to kick them.',
    )
    
    yield (
        255,
        False,
        (user_0, user_1),
        0,
        'I require higher role than Suwako and Kanako to peg them.',
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_error_message_mod_other_need_higher_role_than(action_type, user_side, targets, guild_id):
    """
    Tests whether ``produce_error_message_mod_other_need_higher_role_than`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    user_side : `bool`
        Whether the lower role is coming from the user's side.
    
    targets : ``tuple<ClientUserBase>``
        The targeted users.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_error_message_mod_other_need_higher_role_than(action_type, user_side, targets, guild_id)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
