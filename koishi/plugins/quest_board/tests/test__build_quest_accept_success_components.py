import vampytest

from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ..component_building import build_quest_accept_success_components


def _iter_options():
    user_id = 202509160002
    
    yield (
        user_id,
        1,
        999,
        [
            create_text_display('You successfully accepted the quest.'),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{1:x}',
                ),
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{0:x}',
                ),
                create_button(
                    'View the quest',
                    custom_id = f'linked_quest.details.{user_id:x}.{0:x}.{999:x}',
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_accept_success_components(user_id, page_index, linked_quest_entry_id):
    """
    Tests whether ``build_quest_accept_success_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The page's index to show.
    
    linked_quest_entry_id : `int`
        The currently selected quest's entry's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_quest_accept_success_components(user_id, page_index, linked_quest_entry_id)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
