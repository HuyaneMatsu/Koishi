import vampytest
from hata import (
    Component, Icon, IconType, User, create_container, create_section, create_text_display, create_thumbnail_media
)

from ..component_building import build_mod_self_completion_components
from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_MUTE


def _iter_options():
    user = User.precreate(202607260010, avatar = Icon(IconType.static, 2), name = 'Suwako')
    
    yield (
        ACTION_TYPE_BAN,
        user,
        0,
        None,
        0,
        [
            create_section(
                create_text_display(
                    '### Hecatia Yeah!\n'
                    '\n'
                    'Suwako have banned themselves!',
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user.id}/00000000000000000000000000000002.png',
                ),
            ),
            create_text_display('Reason: \*none\*'),
        ],
    )
    
    yield (
        ACTION_TYPE_MUTE,
        user,
        0,
        'Frog',
        4 * 3600,
        [
            create_section(
                create_text_display(
                    '### Hecatia Yeah!\n'
                    '\n'
                    'Suwako have muted themselves!',
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user.id}/00000000000000000000000000000002.png',
                ),
            ),
            create_text_display('Reason:'),
            create_container(
                create_text_display('Frog'),
            ),
            create_text_display('Duration: 4 hours'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mod_self_completion_components(
    action_type, user, guild_id, reason, duration
):
    """
    Tests whether ``build_mod_self_completion_components`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    user : ``ClientUserBase``
        The user actioning themselves.
    
    guild_id : `int`
        The local guild's identifier.
    
    reason : `None | str`
        Reason to use.
    
    duration : `int`
        Duration.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_mod_self_completion_components(
        action_type, user, guild_id, reason, duration
    )
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
