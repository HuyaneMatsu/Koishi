from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import BUILTIN_EMOJIS

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, ITEM_ID_SCARLET_ONION, ITEM_ID_STRAWBERRY
from ...quest_core import (
    AMOUNT_TYPE_COUNT, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_PEACH, QuestRequirementSerialisableDuration,
    QuestRequirementSerialisableExpiration, QuestRequirementSerialisableItemExact, QuestRewardSerialisableBalance,
    QuestRewardSerialisableCredibility, get_quest_template
)

from ..content_building import produce_linked_quest_detailed_description


def _iter_options():
    quest_template_id = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template = get_quest_template(quest_template_id)
    assert quest_template is not None
    
    user_id = 202505230020
    guild_id = 202505230021
    batch_id = 55555
    
    yield (
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            quest_template_id,
            (
                QuestRequirementSerialisableDuration(3600 * 24),
                QuestRequirementSerialisableExpiration(DateTime.now(TimeZone.utc) + TimeDelta(seconds = 3600 * 24)),
                QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
            ),
            (
                QuestRewardSerialisableBalance(1000),
                QuestRewardSerialisableCredibility(10),
            ),
        ),
        quest_template,
        1,
        (
            f'**Task: Submit 0 / 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.**\n'
            f'\n'
            f'{quest_template.description}\n'
            f'\n'
            f'**Rewards:**\n'
            f'- **1000** {EMOJI__HEART_CURRENCY}\n'
            f'- **10** credibility\n'
            f'**Time available:**\n'
            f'- **1 day**\n'
            f'**Time left:**\n'
            f'- **23 hours, 59 minutes, 59 seconds**\n'
            f'**Completed:**\n'
            f'- **0 / 3** times, cannot be re-accepted anymore'
        ),
    )
    
    yield (
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            quest_template_id,
            (
                QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
                QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 19, 0),
                QuestRequirementSerialisableItemExact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_COUNT, 18, 2),
            ),
            None,
        ),
        quest_template,
        1,
        (
            f'**Task: Submit 0 / 20 {BUILTIN_EMOJIS["peach"]} Peach, 0 / 19 {BUILTIN_EMOJIS["strawberry"]} Strawberry '
            f'and 2 / 18 {BUILTIN_EMOJIS["onion"]} Scarlet onion to Mystia.**\n'
            f'\n'
            f'{quest_template.description}\n'
            f'\n'
            f'**Time available:**\n'
            f'- **unlimited**\n'
            f'**Time left:**\n'
            f'- **unlimited**\n'
            f'**Completed:**\n'
            f'- **0 / 3** times, cannot be re-accepted anymore'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_detailed_description(linked_quest, quest_template, user_level):
    """
    Tests whether ``produce_linked_quest_detailed_description`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest in context.
    
    quest_template : `int`
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_linked_quest_detailed_description(linked_quest, quest_template, user_level)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
