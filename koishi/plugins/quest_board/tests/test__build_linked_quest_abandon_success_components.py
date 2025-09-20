import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ..component_building import build_linked_quest_abandon_success_components


def _iter_options():
    user_id = 202509190000
    
    yield (
        user_id,
        1,
        6556655656,
        [
            create_text_display('You successfully abandoned the quest.'),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{0:x}',
                    enabled = True,
                ),
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{1:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        1,
        0,
        [
            create_text_display('You successfully abandoned the quest.'),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{0:x}',
                    enabled = False,
                ),
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{1:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_abandon_success_components(user_id, page_index, guild_id):
    """
    Tests whether ``build_linked_quest_abandon_success_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_abandon_success_components(user_id, page_index, guild_id)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
