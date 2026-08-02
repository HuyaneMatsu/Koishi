import vampytest
from hata import Guild

from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_KICK, ACTION_TYPE_MUTE, ACTION_TYPE_UN_BAN,
    ACTION_TYPE_UN_MUTE
)
from ..content_building import produce_mod_other_notification_header


def _iter_options():
    guild = Guild.precreate(202607260002, name = 'Moriya shrine')
    
    yield (
        ACTION_TYPE_BAN,
        guild,
        'You have been banned from Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_UN_BAN,
        guild,
        'You have been un-banned from Moriya shrine.',
    )
    
    # Invalid for this action.
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        guild,
        'You have been pegged in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        guild,
        'You have been muted in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_UN_MUTE,
        guild,
        'You have been un-muted in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        guild,
        'You have been kicked from Moriya shrine.',
    )
    
    yield (
        255,
        guild,
        'You have been pegged in Moriya shrine.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_mod_other_notification_header(action_type, guild):
    """
    Tests whether ``produce_mod_other_notification_header`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    guild : ``Guild``
        The local guild.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_mod_other_notification_header(action_type, guild)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
