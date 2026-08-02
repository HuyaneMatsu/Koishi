import vampytest

from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_INVITES_DISABLE, ACTION_TYPE_INVITES_ENABLE,
    ACTION_TYPE_KICK, ACTION_TYPE_MUTE, ACTION_TYPE_UN_BAN, ACTION_TYPE_UN_MUTE, ACTION_TYPE_TOP_LIST_CLIENT,
    ACTION_TYPE_TOP_LIST_USER
)
from ..content_building import produce_error_message_missing_permission


def _iter_options():
    yield (
        ACTION_TYPE_BAN,
        True,
        'You must have ban users permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        True,
        'You must have ban users permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        True,
        'You must have ban users permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        True,
        'You must have moderate users permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        True,
        'You must have moderate users permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        True,
        'You must have kick users permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_TOP_LIST_USER,
        True,
        'You must have ban, kick, moderate users and view audit logs permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_INVITES_DISABLE,
        True,
        'You must have manage guild permission to use this command.',
    )
    
    yield (
        ACTION_TYPE_INVITES_ENABLE,
        True,
        'You must have manage guild permission to use this command.',
    )
    
    yield (
        255,
        True,
        'You must have administrator permission to use this command.',
    )
    
    
    yield (
        ACTION_TYPE_BAN,
        False,
        'I require ban users permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        False,
        'I require ban users permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        False,
        'I require ban users permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        False,
        'I require moderate users permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        False,
        'I require moderate users permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        False,
        'I require kick users permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_TOP_LIST_CLIENT,
        False,
        'I require view audit logs permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_INVITES_DISABLE,
        False,
        'I require manage guild permission to execute this action.',
    )
    
    yield (
        ACTION_TYPE_INVITES_ENABLE,
        False,
        'I require manage guild permission to execute this action.',
    )
    
    yield (
        255,
        False,
        'I require administrator permission to execute this action.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_error_message_missing_permission(action_type, user_side):
    """
    Tests whether ``produce_error_message_missing_permission`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    user_side : `bool`
        Whether the missing permission issue comes from the user's side.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_error_message_missing_permission(action_type, user_side)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
