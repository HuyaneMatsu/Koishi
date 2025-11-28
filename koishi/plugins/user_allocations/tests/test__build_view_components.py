import vampytest
from hata import (
    Component, Icon, IconType, User, create_button, create_row, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from ...user_balance import ALLOCATION_FEATURE_ID_GAME_21, ALLOCATION_FEATURE_ID_NONE

from ..component_building import build_view_components
from ..constants import EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, EMOJI_REFRESH


def _iter_options():
    user_id = 202511230020
    
    user = User.precreate(
        user_id,
        name = 'Remilia',
        avatar = Icon(IconType.static, 2),
    )
    
    page_index = 0
    page_count = 0
    guild_id = 202511230021
    
    yield (
        user,
        page_index,
        page_count,
        guild_id,
        [],
        [
            create_section(
                create_text_display(
                    '# Remilia\'s allocations'
                ),
                thumbnail = create_thumbnail_media(
                    'https://cdn.discordapp.com/avatars/202511230020/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = f'allocations.view.{user_id:x}.{page_index:x}'
                ),
                create_button(
                    'Page 0',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = 'allocations.view.disabled.d',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'allocations.view.disabled.i',
                    enabled = False,
                ),
            ),
        ],
    )
    
    page_index = 1
    page_count = 3
    
    yield (
        user,
        page_index,
        page_count,
        guild_id,
        [
            (ALLOCATION_FEATURE_ID_NONE, 123, 10),
            (ALLOCATION_FEATURE_ID_GAME_21, 124, 20),
        ],
        [
            create_section(
                create_text_display(
                    '# Remilia\'s allocations'
                ),
                thumbnail = create_thumbnail_media(
                    'https://cdn.discordapp.com/avatars/202511230020/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_section(
                create_text_display(
                    '`unknown` allocating 10'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'allocations.details.{user_id:x}.{page_index:x}.{ALLOCATION_FEATURE_ID_NONE:x}.{123:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    '`/21` allocating 20'
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = (
                        f'allocations.details.{user_id:x}.{page_index:x}.{ALLOCATION_FEATURE_ID_GAME_21:x}.{124:x}'
                    ),
                    enabled = True,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = f'allocations.view.{user_id:x}.{page_index:x}'
                ),
                create_button(
                    'Page 1',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = f'allocations.view.{user_id:x}.{page_index - 1:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_NEXT,
                    custom_id = f'allocations.view.{user_id:x}.{page_index + 1:x}',
                    enabled = True,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_view_components(user, page_index, page_count, guild_id, allocations):
    """
    Tests whether ``build_view_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The invoking user.
    
    page_index : `int`
        The current page's index.
    
    page_count : `int`
        The amount of pages.
    
    guild_id : `int`
        The local guild's identifier.
    
    allocations : `list<(int, int, int)>`
        The user's allocations.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_view_components(user, page_index, page_count, guild_id, allocations)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
