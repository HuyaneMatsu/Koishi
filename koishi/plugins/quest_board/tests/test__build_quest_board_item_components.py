import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import QUEST_TEMPLATE_ID_MYSTIA_PEACH

from ..component_building import build_quest_board_item_components


def _iter_options():
    page_index = 1
    quest_template_id = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    user_id = 202509160001
    guild_id_0 = 202510250002
    guild_id_1 = 202510260001
    
    yield (
        user_id,
        guild_id_0,
        guild_id_1,
        page_index,
        quest_template_id,
        item_id,
        [
            create_text_display(
                f'**Item information: {item.emoji} {item.name}**\n'
                f'\n'
                f'{item.description}'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{page_index:x}',
                    enabled = False,
                ),
                create_button(
                    'Back to the quest',
                    custom_id = f'quest_board.details.{user_id:x}.{guild_id_0:x}.{page_index:x}.{quest_template_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_board_item_components(user_id, guild_id, local_guild_id, page_index, quest_template_id, item_id):
    """
    Tests whether ``build_quest_board_item_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The quest's source guild's identifier.
    
    local_guild_id : `int`
        The local guild's identifier.
    
    page_index : `int`
        The quest board's current page's index.
    
    quest_template_id : `int`
        The currently selected quest detail's template's identifier.
    
    item_id : `int`
        The item's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_quest_board_item_components(
        user_id, guild_id, local_guild_id, page_index, quest_template_id, item_id
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
