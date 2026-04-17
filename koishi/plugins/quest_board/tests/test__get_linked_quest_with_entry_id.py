import vampytest

from ...quest_core import (
    LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_CARROT, QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, get_quest_template_nullable
)

from ..helpers import get_linked_quest_with_entry_id


def _iter_options():
    user_id = 202505240030
    guild_id = 202505240031
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_CARROT
    quest_template_0 = get_quest_template_nullable(quest_template_id_0)
    assert quest_template_0 is not None
    linked_quest_entry_id_0 = 533
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        123,
        quest_template_id_0,
        None,
        None,
    )
    linked_quest_0.entry_id = linked_quest_entry_id_0
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_1 = get_quest_template_nullable(quest_template_id_1)
    assert quest_template_1 is not None
    quest_amount_1 = 18
    linked_quest_entry_id_1 = 534
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        124,
        quest_template_id_1,
        None,
        None,
    )
    linked_quest_1.entry_id = linked_quest_entry_id_1
    
    quest_template_id_2 = QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH
    quest_template_2 = get_quest_template_nullable(quest_template_id_2)
    assert quest_template_2 is not None
    quest_amount_2 = 174000
    linked_quest_entry_id_2 = 535
    
    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id,
        125,
        quest_template_id_2,
        None,
        None,
    )
    linked_quest_2.entry_id = linked_quest_entry_id_2
    
    yield (
        [
            linked_quest_0,
            linked_quest_1,
            linked_quest_2,
        ],
        linked_quest_entry_id_1,
        linked_quest_1,
    )
    
    yield (
        [
            linked_quest_0,
            linked_quest_1,
        ],
        linked_quest_entry_id_2,
        None,
    )
    
    yield (
        None,
        linked_quest_entry_id_0,
        None,
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_with_entry_id(linked_quest_listing, entry_id):
    """
    Tests whether ``get_linked_quest_with_entry_id`` works as intended.
    
    Parameters
    ----------
    linked_quest_listing : ``None | list<LinkedQuest>``
        Linked quests.
    
    entry_id : `int`
        Linked quest entry identifier.
    
    Returns
    -------
    output : ``None | LinkedQuest``
    """
    output = get_linked_quest_with_entry_id(linked_quest_listing, entry_id)
    vampytest.assert_instance(output, LinkedQuest, nullable = True)
    return output
