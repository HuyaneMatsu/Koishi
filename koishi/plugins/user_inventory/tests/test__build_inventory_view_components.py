import vampytest
from hata import (
    Component, User, create_button, create_row, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from ...inventory_core import ItemEntry
from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item

from ..component_building import build_inventory_view_components
from ..constants import EMOJI_CLOSE, EMOJI_LEFT, EMOJI_REFRESH, EMOJI_RIGHT


def _iter_options():
    user_id = 202511110021
    user = User.precreate(user_id, name = 'Label')
    
    item_peach = get_item(ITEM_ID_PEACH)
    item_strawberry = get_item(ITEM_ID_STRAWBERRY)
    
    yield (
        user,
        0,
        None,
        1,
        3,
        0,
        0,
        0,
        0,
        [
            create_section(
                create_text_display(
                    f'# {user.name}\'s inventory\n'
                    f'\n'
                    f'Page: 1; Sort by: amount; Sort order: increasing\n'
                    f'Weight: 0.000 / 0.000 kg'
                ),
                thumbnail = create_thumbnail_media(user.avatar_url_at(0)),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = f'inventory.page.{user_id:x}.1.3.0',
                ),
                create_button(
                    'Page 0',
                    EMOJI_LEFT,
                    custom_id = 'inventory.page.D',
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_RIGHT,
                    custom_id = 'inventory.page.I',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = 'inventory.page.close',
                ),
            ),
        ],
    )
    
    yield (
        user,
        0,
        [
            ItemEntry(item_peach, 4),
            ItemEntry(item_strawberry, 5),
        ],
        1,
        3,
        1,
        3,
        1335,
        63122,
        [
            create_section(
                create_text_display(
                    f'# {user.name}\'s inventory\n'
                    f'\n'
                    f'Page: 2; Sort by: amount; Sort order: increasing\n'
                    f'Weight: 1.335 / 63.122 kg'
                ),
                thumbnail = create_thumbnail_media(user.avatar_url_at(0)),
            ),
            create_separator(),
            create_text_display(
                f'{item_peach.emoji} {item_peach.name} x4 (0.{4 * item_peach.weight:0>3} kg)\n'
                f'{item_strawberry.emoji} {item_strawberry.name} x5 (0.{5 * item_strawberry.weight:0>3} kg)'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    custom_id = f'inventory.page.{user_id:x}.1.3.1',
                ),
                create_button(
                    'Page 1',
                    EMOJI_LEFT,
                    custom_id = f'inventory.page.{user_id:x}.1.3.0',
                ),
                create_button(
                    'Page 3',
                    EMOJI_RIGHT,
                    custom_id = f'inventory.page.{user_id:x}.1.3.2',
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = 'inventory.page.close',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_inventory_view_components(
    user, guild_id, item_entries, sort_by, sort_order, page_index, page_count, weight, capacity
):
    """
    Tests whether ``build_inventory_view_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's inventory is being rendered.
    
    guild_id : `int`
        The local guild's identifier.
    
    item_entries : `None | dict<int, ItemEntry>`
        The items of the user.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_index : `int`
        The current page's index.
    
    page_count : `int`
        Amount of pages.
    
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Returns
    -------
    components : ``listComponent>``
    """
    output = build_inventory_view_components(
        user, guild_id, item_entries, sort_by, sort_order, page_index, page_count, weight, capacity
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
