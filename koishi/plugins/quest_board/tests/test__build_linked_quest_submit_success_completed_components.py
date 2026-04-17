from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import ButtonStyle, Component, create_button, create_row, create_separator, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_FROG, get_item_nullable
from ...quest_core import (
    AMOUNT_TYPE_COUNT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, QUEST_REWARD_TYPE_BALANCE,
    QUEST_TEMPLATE_ID_CHIRUNO_FROG, QuestRequirementSerialisableDuration, QuestRequirementSerialisableExpiration,
    QuestRequirementSerialisableItemExact, QuestRewardSerialisableBalance, get_quest_template_nullable
)
from ...user_stats_core import UserStats

from ..component_building import build_linked_quest_submit_success_completed_components


def _iter_options():
    item = get_item_nullable(ITEM_ID_FROG)
    assert item is not None
    
    quest_template_0 = get_quest_template_nullable(QUEST_TEMPLATE_ID_CHIRUNO_FROG)
    assert quest_template_0 is not None
    
    user_id = 202510140000
    guild_id_0 = 202510140001
    guild_id_1 = 202510260003
    batch_id = 5997
    
    duration = 3600 * 24 * 3
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id_0,
        batch_id,
        QUEST_TEMPLATE_ID_CHIRUNO_FROG,
        (
            QuestRequirementSerialisableDuration(duration),
            QuestRequirementSerialisableExpiration(DateTime.now(TimeZone.utc) + TimeDelta(seconds = duration)),
            QuestRequirementSerialisableItemExact(ITEM_ID_FROG, AMOUNT_TYPE_COUNT, 50, 50),
        ),
        (
            QuestRewardSerialisableBalance(2600),
        ),
    )
    linked_quest_0.entry_id = 5
    linked_quest_0.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    linked_quest_0.completion_count = 1
    
    
    yield (
        0,
        user_id,
        0,
        1,
        guild_id_0,
        linked_quest_0,
        quest_template_0,
        1 << 12,
        5,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 38, 12),
        ],
        [
            (QUEST_REWARD_TYPE_BALANCE, 0, 2600),
        ],
        1,
        [
            create_text_display(
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'For a total of **50**.\n'
                f'By doing so, you completed the quest.\n'
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
                    custom_id = (
                        f'quest_board.accept.{user_id:x}.{guild_id_0:x}.{0:x}.{QUEST_TEMPLATE_ID_CHIRUNO_FROG:x}'
                    ),
                    enabled = True,
                    style = ButtonStyle.green,
                ),
            ),
        ],
    )
    
    yield (
        0,
        user_id,
        0,
        1,
        guild_id_1,
        linked_quest_0,
        quest_template_0,
        1 << 0,
        0,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 38, 12),
        ],
        [
            (QUEST_REWARD_TYPE_BALANCE, 0, 2600),
        ],
        1,
        [
            create_text_display(
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'For a total of **50**.\n'
                f'By doing so, you completed the quest.\n'
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
                    custom_id = (
                        f'quest_board.accept.{user_id:x}.{guild_id_0:x}.{0:x}.{QUEST_TEMPLATE_ID_CHIRUNO_FROG:x}'
                    ),
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_success_completed_components(
    client_id,
    user_id,
    page_index_quest_board,
    page_index_linked_quests,
    local_guild_id,
    linked_quest,
    quest_template,
    user_credibility,
    user_level_old,
    submissions_normalised,
    rewards_normalised,
    executed_completion_count,
):
    """
    Tests whether ``build_linked_quest_submit_success_completed_components`` works as intended.
    
    Parameters
    ----------
    client_id : `int`
        The client's identifier who is rendering this message.
    
    user_id : `int`
        The invoking user's identifier.
    
    page_index_quest_board : `int`
        The quest board's current page's index.
    
    page_index_linked_quests : `int`
        The linked quests' current page's index.
    
    local_guild_id : `int`
        The local guild's identifier.
    
    linked_quest : : ``LinkedQuest``
        The finished quest.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    user_credibility : `int`
        The user's credibility.
    
    user_level_old : `int`
        The user's adventurer rank before completing the quest.
    
    submissions_normalised : ``list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    rewards_normalised : `None | list<(int, int, int)>`
        The rewards given by the quest in a normalised form.
    
    executed_completion_count : `int`
        How much times completion was executed.
    
    Returns
    -------
    output : ``list<Component>``
    """
    user_stats = UserStats(user_id)
    user_stats.modify_credibility_by(user_credibility)
    
    output = build_linked_quest_submit_success_completed_components(
        client_id,
        user_id,
        page_index_quest_board,
        page_index_linked_quests,
        local_guild_id,
        linked_quest,
        quest_template,
        user_stats,
        user_level_old,
        submissions_normalised,
        rewards_normalised,
        executed_completion_count,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
