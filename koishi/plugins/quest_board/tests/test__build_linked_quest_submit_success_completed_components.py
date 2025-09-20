import vampytest

from hata import Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT

from ..component_building import build_linked_quest_submit_success_completed_components


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    user_id = 202509160003
    
    yield (
        user_id,
        1,
        202509150000,
        item,
        AMOUNT_TYPE_COUNT,
        50,
        12,
        900,
        0,
        [
            create_text_display(
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'For a total of **50** and finished the quest.\n'
                f'\n'
                f'**You received:**\n'
                f'- **900** {EMOJI__HEART_CURRENCY}'
            ),
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
        item,
        AMOUNT_TYPE_COUNT,
        50,
        12,
        900,
        0,
        [
            create_text_display(
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'For a total of **50** and finished the quest.\n'
                f'\n'
                f'**You received:**\n'
                f'- **900** {EMOJI__HEART_CURRENCY}'
            ),
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
def test__build_linked_quest_submit_success_completed_components(
    user_id, page_index, guild_id, item, amount_type, amount_required, amount_used, reward_balance, reward_credibility,
):
    """
    Tests whether ``build_linked_quest_submit_success_completed_components`` works as intended.
    
    Parameters
    ----------
    page_index : `int`
        The linked quests' current page's index.
    
    guild_id : `int`
        The local guild's identifier.
    
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    reward_balance : `int`
        The amount of balance the user receives.
    
    reward_credibility : `int`
        The amount of credibility the user receives.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_submit_success_completed_components(
        user_id,
        page_index,
        guild_id,
        item,
        amount_type,
        amount_required,
        amount_used,
        reward_balance,
        reward_credibility,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
