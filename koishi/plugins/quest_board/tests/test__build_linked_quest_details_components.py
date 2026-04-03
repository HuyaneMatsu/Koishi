import vampytest

from hata import (
    BUILTIN_EMOJIS, ButtonStyle, Component, create_button, create_row, create_separator, create_text_display
)
from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from ...item_core import ITEM_ID_CARROT, ITEM_ID_PEACH
from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT,
    QuestRequirementSerialisableDuration, QuestRequirementSerialisableExpiration,
    QuestRequirementSerialisableItemExact, QuestRewardSerialisableBalance, QuestRewardSerialisableCredibility
)
from ...user_stats_core import UserStats

from ..component_building import build_linked_quest_details_components


def _iter_options():
    user_id = 202505240020
    guild_id = 202505240021
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        5666,
        QUEST_TEMPLATE_ID_MYSTIA_CARROT,
        (
            QuestRequirementSerialisableDuration(3600),
            QuestRequirementSerialisableExpiration(DateTime.now(TimeZone.utc) + TimeDelta(seconds = 3600)),
            QuestRequirementSerialisableItemExact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, 3600, 0),
        ),
        (
            QuestRewardSerialisableBalance(1000),
            QuestRewardSerialisableCredibility(10),
        ),
    )
    linked_quest_entry_id_0 = 123
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        5666,
        QUEST_TEMPLATE_ID_MYSTIA_CARROT,
        (
            QuestRequirementSerialisableDuration(3600),
            QuestRequirementSerialisableExpiration(DateTime.now(TimeZone.utc) + TimeDelta(seconds = 3600)),
            QuestRequirementSerialisableItemExact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, 3600, 0),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
        ),
        (
            QuestRewardSerialisableBalance(1000),
            QuestRewardSerialisableCredibility(10),
        ),
    )
    linked_quest_entry_id_1 = 124
    linked_quest_1.entry_id = linked_quest_entry_id_1
    
    page_index = 1
    
    yield (
        linked_quest_0,
        user_id,
        1 << 10,
        page_index,
        [
            create_text_display(
                f'**Task: Submit 0.00 / {3600 / 1000} kg {BUILTIN_EMOJIS["carrot"]} Carrot to Mystia.**\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **5** credibility\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Time left:**\n'
                f'- **59 minutes, 59 seconds**\n'
                f'**Completed:**\n'
                f'- **0 / 3** times, cannot be re-accepted anymore'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{page_index:x}',
                ),
                create_button(
                    'Abandon',
                    custom_id = f'linked_quest.abandon.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'Auto submit items',
                    custom_id = f'linked_quest.submit_auto.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Select requirement to submit for',
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{page_index:x}.{linked_quest_entry_id_0:x}.'
                        f'{0:x}'
                    ),
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )
    
    yield (
        linked_quest_1,
        user_id,
        1 << 10,
        page_index,
        [
            create_text_display(
                f'**Task: Submit 0.00 / {3600 / 1000} kg {BUILTIN_EMOJIS["carrot"]} Carrot and '
                f'0 / 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.**\n'
                f'\n'
                f'I am running low on some vegetables for soups.\n'
                f'\nRequesting a basketful of Carrot.\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **5** credibility\n'
                f'**Time available:**\n'
                f'- **1 hour**\n'
                f'**Time left:**\n'
                f'- **59 minutes, 59 seconds**\n'
                f'**Completed:**\n'
                f'- **0 / 3** times, cannot be re-accepted anymore'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{page_index:x}',
                ),
                create_button(
                    'Abandon',
                    custom_id = f'linked_quest.abandon.{user_id:x}.{page_index:x}.{linked_quest_entry_id_1:x}',
                    style = ButtonStyle.red,
                ),
                create_button(
                    'Auto submit items',
                    custom_id = f'linked_quest.submit_auto.{user_id:x}.{page_index:x}.{linked_quest_entry_id_1:x}',
                    style = ButtonStyle.green,
                ),
                create_button(
                'Select requirement to submit for',
                    custom_id = (
                        f'linked_quest.submit_select_requirement.{user_id:x}.{page_index:x}.'
                        f'{linked_quest_entry_id_1:x}.{0:x}'
                    ),
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_details_components(linked_quest, user_id, credibility, page_index):
    """
    Tests whether ``build_linked_quest_details_components`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest to describe.
    
    user_id : `int`
        The guild's identifier.
    
    credibility : `int`
        The user's  credibility.
    
    Returns
    -------
    output : ``list<Component>``
    """
    user_stats = UserStats(user_id)
    user_stats.modify_credibility_by(credibility)

    output = build_linked_quest_details_components(linked_quest, user_stats, page_index)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
