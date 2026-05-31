from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    Component, Icon, IconType, User, create_container, create_section, create_text_display, create_thumbnail_media
)

from ..component_building import build_to_do_view
from ..to_do import ToDo


def _iter_options():
    user_id = 202605270004
    user = User.precreate(
        user_id,
        avatar = Icon(IconType.static, 2),
        name = 'Koishi',
    )
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        user_id,
    )
    to_do.entry_id = 100
    
    
    yield (
        to_do,
        user,
        0,
        [
            create_section(
                create_text_display(
                    '## \\#100: shrimp\n'
                    '**By**: Koishi\n'
                    '**At**: 2016-05-14 00:00:00'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id!s}/00000000000000000000000000000002.png'
                ),
            ),
        ],
    )
    
    user_id = 202605270005
    user = User.precreate(
        user_id,
        avatar = Icon(IconType.static, 2),
        name = 'Koishi',
    )
    to_do = ToDo(
        'shrimp',
        'fry',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        user_id,
    )
    to_do.entry_id = 100
    
    
    yield (
        to_do,
        user,
        0,
        [
            create_section(
                create_text_display(
                    '## \\#100: shrimp\n'
                    '**By**: Koishi\n'
                    '**At**: 2016-05-14 00:00:00'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_container(create_text_display('fry')),
        ],
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_to_do_view(to_do, user, guild_id):
    """
    Tests whether ``build_to_do_view`` works as intended.
    
    Parameters
    ----------
    to_do : ``ToDo``
        Todo entry to build view for.
    
    user : ``ClientUserBase``
        The creator user.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_to_do_view(to_do, user, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
