import vampytest

from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE
from ..content_building import produce_error_message_mod_self_need_higher_role_than


def _iter_options():
    yield (
        ACTION_TYPE_BAN,
        'I require higher role than you to ban you.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        'I require higher role than you to mute you.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        'I require higher role than you to kick you.',
    )
    
    yield (
        255,
        'I require higher role than you to peg you.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_error_message_mod_self_need_higher_role_than(action_type):
    """
    Tests whether ``produce_error_message_mod_self_need_higher_role_than`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_error_message_mod_self_need_higher_role_than(action_type)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
