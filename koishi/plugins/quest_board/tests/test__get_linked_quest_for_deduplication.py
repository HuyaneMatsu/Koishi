import vampytest

from ...quest_core import (
    LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT, QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, Quest, get_quest_template
)

from ..helpers import get_linked_quest_for_deduplication


def _iter_options():
    user_id = 202505240040
    guild_id = 202505240041
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template(quest_template_id_0)
    assert quest_template_0 is not None
    quest_amount_0 = 36
    linked_quest_entry_id_0 = 533
    linked_quest_batch_id_0 = 123
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        linked_quest_batch_id_0,
        Quest(
            quest_template_id_0,
            quest_amount_0,
            3600,
            2,
            1000,
        ),
    )
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_1 = get_quest_template(quest_template_id_1)
    assert quest_template_1 is not None
    quest_amount_1 = 18
    linked_quest_entry_id_1 = 534
    linked_quest_batch_id_1 = 124
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        linked_quest_batch_id_1,
        Quest(
            quest_template_id_1,
            quest_amount_1,
            3600,
            2,
            1000,
        ),
    )
    linked_quest_1.entry_id = linked_quest_entry_id_1
    
    quest_template_id_2 = QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH
    quest_template_2 = get_quest_template(quest_template_id_2)
    assert quest_template_2 is not None
    quest_amount_2 = 174000
    linked_quest_entry_id_2 = 535
    linked_quest_batch_id_2 = 125
    
    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id,
        linked_quest_batch_id_2,
        Quest(
            quest_template_id_2,
            quest_amount_2,
            3600,
            2,
            1000,
        ),
    )
    linked_quest_2.entry_id = linked_quest_entry_id_2
    
    yield (
        [
            linked_quest_0,
            linked_quest_1,
            linked_quest_2,
        ],
        guild_id,
        linked_quest_batch_id_1,
        quest_template_id_1,
        linked_quest_1,
    )
    
    yield (
        [
            linked_quest_0,
            linked_quest_1,
            linked_quest_2,
        ],
        0,
        linked_quest_batch_id_1,
        quest_template_id_1,
        None,
    )
    
    yield (
        [
            linked_quest_0,
            linked_quest_1,
            linked_quest_2,
        ],
        guild_id,
        linked_quest_batch_id_0,
        quest_template_id_1,
        None,
    )
    
    yield (
        [
            linked_quest_0,
            linked_quest_1,
            linked_quest_2,
        ],
        guild_id,
        linked_quest_batch_id_1,
        quest_template_id_0,
        None,
    )
    
    yield (
        None,
        guild_id,
        linked_quest_batch_id_1,
        quest_template_id_1,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_for_deduplication(linked_quest_listing, guild_id, quest_batch_id, quest_template_id):
    """
    Tests whether ``get_linked_quest_for_deduplication`` works as intended.
    
    Parameters
    ----------
    linked_quest_listing : ``None | list<LinkedQuest>``
        Linked quests.
    
    guild_id : `int`
        The guild's identifier is quest is from.
    
    quest_batch_id : `int`
        The identifier of the batch the quest is from.
    
    quest_template_id : `int`
        The quest's template's identifier.
    
    Returns
    -------
    output : ``None | LinkedQuest``
    """
    output = get_linked_quest_for_deduplication(linked_quest_listing, guild_id, quest_batch_id, quest_template_id)
    vampytest.assert_instance(output, LinkedQuest, nullable = True)
    return output
