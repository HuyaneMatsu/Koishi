import vampytest
from hata import Guild

from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE
from ..content_building import produce_mod_self_form_title


def _iter_options():
    guild = Guild.precreate(202607260008, name = 'Moriya shrine')
    
    yield (
        ACTION_TYPE_BAN,
        guild,
        'Banning yourself from Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_MUTE,
        guild,
        'Muting yourself in Moriya shrine.',
    )
    
    yield (
        ACTION_TYPE_KICK,
        guild,
        'Kicking yourself from Moriya shrine.',
    )
    
    yield (
        255,
        guild,
        'Pegging yourself in Moriya shrine.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_mod_self_form_title(action_type, guild):
    """
    Tests whether ``produce_mod_self_form_title`` works as intended.
    
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
    parts = [*produce_mod_self_form_title(action_type, guild)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
