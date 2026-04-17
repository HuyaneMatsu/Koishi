import vampytest

from ..helpers import get_allowed_completion_count

from ...quest_core import (
    LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
    QUEST_TEMPLATE_ID_MYSTIA_PEACH, get_quest_template_nullable
)


def _iter_options():
    quest_template_mystia_peach = get_quest_template_nullable(QUEST_TEMPLATE_ID_MYSTIA_PEACH)
    assert quest_template_mystia_peach is not None
    
    quest_template_mystia_firewood = get_quest_template_nullable(QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD)
    assert quest_template_mystia_firewood is not None
    
    user_id = 202604140000
    guild_id = 202604140001
    batch_id = 55555
    
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        QUEST_TEMPLATE_ID_MYSTIA_PEACH,
        None,
        None,
    )
    linked_quest_0.completion_count = 1
    linked_quest_0.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
        None,
        None,
    )
    linked_quest_1.completion_count = 1
    linked_quest_1.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    
    yield (
        'No linked quest, limited',
        None,
        quest_template_mystia_peach,
        6,
        3,
    )
    
    yield (
        'No linked quest, unlimited',
        None,
        quest_template_mystia_firewood,
        6,
        6,
    )
    
    yield (
        'No linked quest, limited, low',
        None,
        quest_template_mystia_peach,
        1,
        1,
    )
    
    yield (
        'No linked quest, unlimited, low',
        None,
        quest_template_mystia_firewood,
        1,
        1,
    )
    
    yield (
        'With linked quest, limited',
        linked_quest_0,
        quest_template_mystia_peach,
        6,
        2,
    )
    
    yield (
        'With linked quest, unlimited',
        linked_quest_1,
        quest_template_mystia_firewood,
        6,
        6,
    )
    
    yield (
        'With linked quest, limited, low',
        linked_quest_0,
        quest_template_mystia_peach,
        1,
        1,
    )
    
    yield (
        'With linked quest, unlimited, low',
        linked_quest_1,
        quest_template_mystia_firewood,
        1,
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__get_allowed_completion_count(linked_quest, quest_template, possession_count):
    """
    Tests whether ``get_allowed_completion_count`` works as intended.
    
    Parameters
    ----------
    linked_quest : : ``None | LinkedQuest``
        The linked quest if the user already completed this quest before.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    possession_count : `int`
        How much times the required items are possessed by the user.
    
    Returns
    -------
    output : `int`
    """
    output = get_allowed_completion_count(linked_quest, quest_template, possession_count)
    vampytest.assert_instance(output, int)
    return output
