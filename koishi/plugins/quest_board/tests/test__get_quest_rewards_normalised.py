import vampytest

from ...item_core import ITEM_ID_STRAWBERRY
from ...quest_core import (
    QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_ITEM_EXACT, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, quest_create,
    quest_reward_instantiable_create_credibility, quest_reward_instantiable_create_item_exact,
    quest_sub_type_instantiable_create_base
)

from ..helpers import get_quest_rewards_normalised


def _iter_options():
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            None,
        ),
        0,
        0,
        None,
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                quest_sub_type_instantiable_create_base(),
            ),
        ),
        0,
        0,
        None,
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                quest_reward_instantiable_create_item_exact(ITEM_ID_STRAWBERRY, 100),
                quest_reward_instantiable_create_credibility(20),
            ),
        ),
        0,
        0,
        [
            (QUEST_REWARD_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, 100),
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 20),
        ],
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                quest_reward_instantiable_create_item_exact(ITEM_ID_STRAWBERRY, 500),
                quest_sub_type_instantiable_create_base(),
            ),
        ),
        0,
        4,
        [
            (QUEST_REWARD_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, 500),
        ],
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                quest_reward_instantiable_create_credibility(20),
            ),
        ),
        0,
        3,
        [
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 10),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_rewards_normalised(quest, quest_level, user_level):
    """
    Tests whether ``get_quest_rewards_normalised`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    quest_level : `int`
        The quest's level.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    output : `None | list<(int, int, int)>`
    """
    output = get_quest_rewards_normalised(quest, quest_level, user_level)
    vampytest.assert_instance(output, list, nullable = True)
    return output
