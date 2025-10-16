import vampytest
from hata import BUILTIN_EMOJIS

from ...quest_core import (
    LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH,
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, Quest, get_quest_template
)

from ..content_builders import produce_quest_short_description


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
    
    quest_1 = Quest(
        quest_template_id_1,
        20,
        3600 * 24,
        10,
        1000,
    )
    
    quest_2 = Quest(
        quest_template_id_2,
        20,
        3600 * 24,
        10,
        1000,
    )
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_1,
    )
    linked_quest_1.completion_count = 1
    
    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_2,
    )
    linked_quest_2.completion_count = 1
    
    yield (
        None,
        quest_template_0,
        20,
        (
            f'Required rank: G\n'
            f'Submit 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    yield (
        linked_quest_1,
        quest_template_1,
        500,
        (
            f'Required rank: F      Completed: 1 / 1 times\n'
            f'Submit 0.5 kg {BUILTIN_EMOJIS["strawberry"]} Strawberry to Sakuya.'
        ),
    )
    
    yield (
        linked_quest_2,
        quest_template_2,
        500,
        (
            f'Required rank: F      Completed: 1 times\n'
            f'Submit 0.5 kg {BUILTIN_EMOJIS["grapes"]} Bluefrankish to Sakuya.'
        ),
    )
    
    # No submit items by value quests yet
    # No subjugation quests yet


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_quest_short_description(linked_quest, quest_template, amount_required):
    """
    Tests whether ``produce_quest_short_description`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``None | LinkedQuest``
        The user's linked quest for this entry.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    amount_required : `int`
        The required amount of items to submit.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_quest_short_description(linked_quest, quest_template, amount_required)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
