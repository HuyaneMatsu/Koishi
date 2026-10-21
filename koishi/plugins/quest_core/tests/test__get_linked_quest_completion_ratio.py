import vampytest

from ...item_core import ITEM_ID_STRAWBERRY
from ...unit_core import AMOUNT_TYPE_WEIGHT

from ..linked_quest import LinkedQuest, linked_quest_create
from ..quest_requirement_serialisables import (
    quest_requirement_serialisable_create_duration, quest_requirement_serialisable_create_expiration,
    quest_requirement_serialisable_create_item_exact
)
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
from ..utils import get_linked_quest_completion_ratio


def _iter_options():
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    user_id_0 = 202511080060
    guild_id_0 = 202511080061
    batch_id_0 = 5666
    
    linked_quest_0 = linked_quest_create(
        user_id_0,
        guild_id_0,
        batch_id_0,
        quest_template_id,
        (
            quest_requirement_serialisable_create_duration(3600 * 24 * 3),
            quest_requirement_serialisable_create_expiration(1000000 + 3600 * 24 * 3),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 0),
        ),
        None,
    )
    
    yield (
        linked_quest_0,
        0.0,
    )
    
    user_id_1 = 202511080062
    guild_id_1 = 202511080063
    batch_id_1 = 5666
    
    linked_quest_1 = linked_quest_create(
        user_id_1,
        guild_id_1,
        batch_id_1,
        quest_template_id,
        (
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 500),
        ),
        None,
    )
    
    yield (
        linked_quest_1,
        0.5,
    )
    
    user_id_2 = 202511080064
    guild_id_2 = 202511080065
    batch_id_2 = 5666
    
    linked_quest_2 = linked_quest_create(
        user_id_2,
        guild_id_2,
        batch_id_2,
        quest_template_id,
        (
            quest_requirement_serialisable_create_duration(3600 * 24 * 3),
            quest_requirement_serialisable_create_expiration(1000000 + 3600 * 24 * 3),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 1200),
        ),
        None,
    )
    
    yield (
        linked_quest_2,
        1.0,
    )
    
    user_id_3 = 202602240000
    guild_id_3 = 202602240001
    batch_id_3 = 5666
    
    linked_quest_3 = linked_quest_create(
        user_id_3,
        guild_id_3,
        batch_id_3,
        quest_template_id,
        (
            quest_requirement_serialisable_create_duration(3600 * 24 * 3),
            quest_requirement_serialisable_create_expiration(1000000 + 3600 * 24 * 3),
        ),
        None,
    )
    
    yield (
        linked_quest_3,
        1.0,
    )
    
    user_id_4 = 202602240002
    guild_id_4 = 202602240003
    batch_id_4 = 5666
    
    linked_quest_4 = linked_quest_create(
        user_id_4,
        guild_id_4,
        batch_id_4,
        quest_template_id,
        (
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 1200),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 500),
        ),
        None,
    )
    
    yield (
        linked_quest_4,
        0.75,
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
