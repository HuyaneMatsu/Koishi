import vampytest

from hata import Component, Guild, create_container, create_text_display

from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_MUTE
from ..component_building import build_mod_other_notification_components


def _iter_options():
    guild = Guild.precreate(202607190000, name = 'Moriya shrine')
    
    yield (
        ACTION_TYPE_BAN,
        guild,
        None,
        0,
        [
            create_text_display('You have been banned from Moriya shrine.'),
        ],
    )
    
    yield (
        ACTION_TYPE_BAN,
        guild,
        'frog',
        0,
        [
            create_text_display('You have been banned from Moriya shrine.'),
            create_text_display('Reason:'),
            create_container(create_text_display('frog')),
        ],
    )
    
    yield (
        ACTION_TYPE_MUTE,
        guild,
        'frog',
        3600,
        [
            create_text_display('You have been muted in Moriya shrine.'),
            create_text_display('Reason:'),
            create_container(create_text_display('frog')),
            create_text_display('Duration: 1 hour'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mod_other_notification_components(action_type, guild, reason, duration):
    """
    Tests whether ``build_mod_other_notification_components`` work as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    guild : ``Guild``
        The local guild.
    
    reason : `None | str`
        Reason to use.
    
    duration : `int`
        Duration duration.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_mod_other_notification_components(action_type, guild, reason, duration)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
