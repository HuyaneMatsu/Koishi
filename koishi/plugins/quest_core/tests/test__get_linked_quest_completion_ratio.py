import vampytest

from .test__get_linked_quest_listing import _create_test_quest

from ..linked_quest import LinkedQuest
from ..utils import get_linked_quest_completion_ratio


def _iter_options():
    quest_0 = _create_test_quest()
    user_id_0 = 202511080060
    guild_id_0 = 202511080061
    batch_id_0 = 5666
    
    quest_1 = _create_test_quest()
    user_id_1 = 202511080062
    guild_id_1 = 202511080063
    batch_id_1 = 5666
    
    quest_2 = _create_test_quest()
    user_id_2 = 202511080064
    guild_id_2 = 202511080065
    batch_id_2 = 5666
    
    linked_quest_0 = LinkedQuest(
        user_id_0,
        guild_id_0,
        batch_id_0,
        quest_0,
    )
    linked_quest_0.amount_required = 10
    linked_quest_0.amount_submitted = 0
    
    linked_quest_1 = LinkedQuest(
        user_id_1,
        guild_id_1,
        batch_id_1,
        quest_1,
    )
    linked_quest_1.amount_required = 10
    linked_quest_1.amount_submitted = 5
    
    linked_quest_2 = LinkedQuest(
        user_id_2,
        guild_id_2,
        batch_id_2,
        quest_2,
    )
    linked_quest_2.amount_required = 10
    linked_quest_2.amount_submitted = 10
    
    yield (
        linked_quest_0,
        0.0,
    )
    
    yield (
        linked_quest_1,
        0.5,
    )
    
    yield (
        linked_quest_2,
        1.0,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_completion_ratio(linked_quest):
    """
    Returns in what ratio is the quest completed at.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        inked quest to get ratio of.
    
    Returns
    -------
    completion_ratio : `float`
    """
    output = get_linked_quest_completion_ratio(linked_quest)
    vampytest.assert_instance(output, float)
    return output
