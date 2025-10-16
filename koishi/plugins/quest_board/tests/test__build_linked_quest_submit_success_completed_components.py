import vampytest

from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import (
    AMOUNT_TYPE_COUNT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest,
    get_quest_template
)
from ...user_stats_core import UserStats

from ..component_building import build_linked_quest_submit_success_completed_components


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_0 = get_quest_template(quest_template_id_0)
    
    user_id = 202510140000
    guild_id = 202510140001
    batch_id = 5997
    
    duration = 3600 * 24 * 3
    amount_required = 20
    reward_balance = 2600
    reward_credibility = 4
    
    quest_0 = Quest(
        quest_template_id_0,
        amount_required,
        duration,
        reward_credibility,
        reward_balance,
    )
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_0,
    )
    linked_quest_0.entry_id = 5
    linked_quest_0.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    linked_quest_0.completion_count = 1
    
    
    user_id = 202509160003
    
    yield (
        user_id,
        1,
        guild_id,
        linked_quest_0,
        quest_template_0,
        1 << 12,
        1,
        item,
        AMOUNT_TYPE_COUNT,
        50,
        12,
        0,
        [
            create_text_display(
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'For a total of **50** and finished the quest.\n'
                f'\n'
                f'**You received:**\n'
                f'- **2600** {EMOJI__HEART_CURRENCY}'
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
                create_button(
                    'Repeat',
                    custom_id = f'quest_board.accept.{user_id:x}.{0:x}.{quest_template_id_0}',
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        1,
        0,
        linked_quest_0,
        quest_template_0,
        1 << 0,
        0,
        item,
        AMOUNT_TYPE_COUNT,
        50,
        12,
        0,
        [
            create_text_display(
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'For a total of **50** and finished the quest.\n'
                f'\n'
                f'**You received:**\n'
                f'- **2600** {EMOJI__HEART_CURRENCY}'
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
                create_button(
                    'Repeat',
                    custom_id = f'quest_board.accept.{user_id:x}.{0:x}.{quest_template_id_0}',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_success_completed_components(
    user_id,
    page_index,
    guild_id,
    linked_quest,
    quest_template,
    user_credibility,
    user_level_old,
    item,
    amount_type,
    amount_required,
    amount_used,
    reward_credibility,
):
    """
    Tests whether ``build_linked_quest_submit_success_completed_components`` works as intended.
    
    Parameters
    ----------
    page_index : `int`
        The linked quests' current page's index.
    
    guild_id : `int`
        The local guild's identifier.
    
    linked_quest : : ``LinkedQuest``
        The finished quest.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    user_credibility : `int`
        The user's credibility.
    
    user_level_old : `int`
        The user's adventurer rank before completing the quest.
    
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    reward_credibility : `int`
        The amount of credibility the user receives.
    
    Returns
    -------
    output : ``list<Component>``
    """
    user_stats = UserStats(user_id)
    user_stats.set('credibility', user_credibility)
    
    output = build_linked_quest_submit_success_completed_components(
        user_id,
        page_index,
        guild_id,
        linked_quest,
        quest_template,
        user_stats,
        user_level_old,
        item,
        amount_type,
        amount_required,
        amount_used,
        reward_credibility,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
