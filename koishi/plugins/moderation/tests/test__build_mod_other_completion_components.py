import vampytest
from hata import (
    Component, Guild, Icon, IconType, MediaInfo, MediaItem, User, create_container, create_media_gallery,
    create_section, create_text_display, create_thumbnail_media
)

from ..component_building import build_mod_other_completion_components
from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_MUTE
from ..easter_eggs import IMAGE_URL_NAZRIN, IMAGE_URL_ORIN


def _iter_options():
    guild = Guild.precreate(202607190003, name = 'Moriya shrine', icon = Icon(IconType.static, 2))
    
    user_0 = User.precreate(202607190001, avatar = Icon(IconType.static, 2), name = 'Suwako')
    user_1 = User.precreate(202607190002, avatar = Icon(IconType.static, 2), name = 'Kanako')
    
    yield (
        ACTION_TYPE_BAN,
        [user_0],
        guild,
        None,
        False,
        0,
        0,
        False,
        [
            create_section(
                create_text_display(
                    '### Hecatia Yeah!\n'
                    '\n'
                    'Suwako has been banned!',
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_0.id}/00000000000000000000000000000002.png',
                ),
            ),
            create_text_display('Reason: \*none\*'),
            create_text_display('Notify user: no'),
            create_text_display('Delete messages duration: 0 second'),
        ],
    )
    
    yield (
        ACTION_TYPE_BAN,
        [user_0, user_1],
        guild,
        'Frog',
        True,
        4 * 3600,
        0,
        True,
        [
            create_text_display(
                '### Hecatia Yeah!\n'
                '\n'
                'Suwako and Kanako have been banned!',
            ),
            create_text_display('Reason:'),
            create_container(
                create_text_display('Frog'),
            ),
            create_text_display('Notify user: yes'),
            create_text_display('Delete messages duration: 4 hours'),
            create_media_gallery(
                MediaItem(
                    MediaInfo(
                        IMAGE_URL_ORIN,
                    ),
                ),
            ),
        ],
    )
    
    yield (
        ACTION_TYPE_MUTE,
        [user_0, user_1],
        guild,
        'Frog',
        True,
        0,
        4 * 3600,
        True,
        [
            create_text_display(
                '### Hecatia Yeah!\n'
                '\n'
                'Suwako and Kanako have been muted!',
            ),
            create_text_display('Reason:'),
            create_container(
                create_text_display('Frog'),
            ),
            create_text_display('Notify user: yes'),
            create_text_display('Duration: 4 hours'),
            create_media_gallery(
                MediaItem(
                    MediaInfo(
                        IMAGE_URL_NAZRIN,
                    ),
                ),
            ),
        ],
    )
    
    yield (
        ACTION_TYPE_BAN_REASON_EDIT,
        [user_0, user_1],
        guild,
        'Frog',
        False,
        0,
        0,
        True,
        [
            create_text_display(
                '### Hecatia Yeah!\n'
                '\n'
                'Ban reason of Suwako and Kanako have been edited!',
            ),
            create_text_display('Reason:'),
            create_container(
                create_text_display('Frog'),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mod_other_completion_components(
    action_type, targets, guild, reason, notify_user, delete_message_duration, duration, easter_egg_mode
):
    """
    Tests whether ``build_mod_other_completion_components`` works as intended.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    targets : ``None | tuple<ClientUserBase>``
        Targeted users.
    
    guild : ``Guild``
        The local guild.
    
    reason : `None | str`
        Reason to use.
    
    notify_user : `bool`
        Whether the user has been notified.
    
    delete_message_duration : `int`
        How old messages to delete.
    
    duration : `int`
        Duration duration.
    
    easter_egg_mode : `bool`
        Whether easter egg image should be shown.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_mod_other_completion_components(
        action_type, targets, guild, reason, notify_user, delete_message_duration, duration, easter_egg_mode
    )
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
