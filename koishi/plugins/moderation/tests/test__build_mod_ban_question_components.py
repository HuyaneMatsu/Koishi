import vampytest
from hata import (
    Component, Icon, IconType, User, create_container, create_section, create_text_display, create_thumbnail_media
)

from ..component_building import build_mod_ban_question_components


def _iter_options():
    user = User.precreate(202608020000, avatar = Icon(IconType.static, 2), name = 'Suwako')
    
    yield (
        user,
        0,
        False,
        None,
        [
            create_section(
                create_text_display(
                    'Suwako is **NOT YET** banned.',
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user.id}/00000000000000000000000000000002.png',
                ),
            ),
        ],
    )
    
    yield (
        user,
        0,
        True,
        None,
        [
            create_section(
                create_text_display(
                    'Suwako is banned.',
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user.id}/00000000000000000000000000000002.png',
                ),
            ),
            create_text_display('Reason: \*none\*'),
        ],
    )
    
    yield (
        user,
        0,
        True,
        'Frog',
        [
            create_section(
                create_text_display(
                    'Suwako is banned.',
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user.id}/00000000000000000000000000000002.png',
                ),
            ),
            create_text_display('Reason:'),
            create_container(
                create_text_display('Frog'),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mod_ban_question_components(target, guild_id, banned, reason):
    """
    Tests whether ``build_mod_ban_question_components`` works as intended.
    
    Parameters
    ----------
    target : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The local guild's identifier.
    
    banned : `bool`
        Whether the user is banned.
    
    reason : `None | str`
        Ban reason.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_mod_ban_question_components(target, guild_id, banned, reason)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
