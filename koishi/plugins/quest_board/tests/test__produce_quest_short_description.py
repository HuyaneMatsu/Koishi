from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import BUILTIN_EMOJIS

from ...item_core import ITEM_ID_BLUEFRANKISH, ITEM_ID_PEACH, ITEM_ID_STRAWBERRY
from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, Quest,
    QuestRequirementInstantiableDuration, QuestRequirementInstantiableItemExact, QuestRequirementSerialisableDuration,
    QuestRequirementSerialisableExpiration, QuestRequirementSerialisableItemExact, get_quest_template
)

from ..content_building import produce_quest_short_description


def _iter_options():
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_0 = get_quest_template(quest_template_id_0)
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    quest_template_1 = get_quest_template(quest_template_id_1)
    
    quest_template_id_2 = QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH
    quest_template_2 = get_quest_template(quest_template_id_2)
    
    user_id = 202510130002
    guild_id = 202510130003
    batch_id = 5999
    
    quest_0 = Quest(
        quest_template_id_0,
        (
            QuestRequirementInstantiableDuration(3600 * 24),
            QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20),
        ),
        None,
    )
    
    quest_1 = Quest(
        quest_template_id_1,
        (
            QuestRequirementInstantiableDuration(3600 * 24),
            QuestRequirementInstantiableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500),
        ),
        None,
    )
    
    quest_2 = Quest(
        quest_template_id_2,
        (
            QuestRequirementInstantiableDuration(3600 * 24),
            QuestRequirementInstantiableItemExact(ITEM_ID_BLUEFRANKISH, AMOUNT_TYPE_WEIGHT, 500),
        ),
        None,
    )
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_template_id_1,
        (
            QuestRequirementSerialisableDuration(3600 * 24),
            QuestRequirementSerialisableExpiration(DateTime.now(TimeZone.utc) + TimeDelta(seconds = 3600 * 24)),
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 0),
        ),
        None,
    )
    linked_quest_1.completion_count = 1
    
    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_template_id_2,
        (
            QuestRequirementSerialisableDuration(3600 * 24),
            QuestRequirementSerialisableExpiration(DateTime.now(TimeZone.utc) + TimeDelta(seconds = 3600 * 24)),
            QuestRequirementSerialisableItemExact(ITEM_ID_BLUEFRANKISH, AMOUNT_TYPE_WEIGHT, 500, 0),
        ),
        None,
    )
    linked_quest_2.completion_count = 1
    
    yield (
        None,
        quest_0,
        quest_template_0,
        (
            f'Required rank: E\n'
            f'Submit 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    yield (
        linked_quest_1,
        quest_1,
        quest_template_1,
        (
            f'Required rank: E      Completed: 1 / 1 times\n'
            f'Submit 0.5 kg {BUILTIN_EMOJIS["strawberry"]} Strawberry to Sakuya.'
        ),
    )
    
    yield (
        linked_quest_2,
        quest_2,
        quest_template_2,
        (
            f'Required rank: F      Completed: 1 times\n'
            f'Submit 0.5 kg {BUILTIN_EMOJIS["grapes"]} Bluefrankish to Sakuya.'
        ),
    )
    
    # No submit items by value quests yet
    # No subjugation quests yet


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_quest_short_description(linked_quest, quest, quest_template):
    """
    Tests whether ``produce_quest_short_description`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``None | LinkedQuest``
        The user's linked quest for this entry.
    
    quest : ``Quest``
        The quest to produce description for.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_quest_short_description(linked_quest, quest, quest_template)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
