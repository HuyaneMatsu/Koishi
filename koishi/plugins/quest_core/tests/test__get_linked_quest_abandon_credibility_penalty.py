import vampytest

from ..utils import get_linked_quest_abandon_credibility_penalty


def _iter_options():
    yield (
        0,
        3,
        3,
        0.0,
        0,
    )
    
    yield (
        20,
        3,
        3,
        0.0,
        40,
    )
    
    yield (
        20,
        3,
        3,
        1.0,
        20,
    )
    
    yield (
        20,
        0,
        3,
        0.0,
        80,
    )
    
    yield (
        20,
        0,
        3,
        1.0,
        40,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_abandon_credibility_penalty(reward_credibility, quest_rank, entity_rank, completion_ratio):
    """
    Tests whether ``get_linked_quest_abandon_credibility_penalty`` works as intended.
    
    Parameters
    ----------
    reward_credibility : `int`
        The amount of credibility to be rewarded.
    
    quest_rank : `int`
        The quest's rank.
    
    entity_rank : `int`
        The entity's rank to be rewarded.
    
    Returns
    -------
    output : `int`
    """
    output = get_linked_quest_abandon_credibility_penalty(reward_credibility, quest_rank, entity_rank, completion_ratio)
    vampytest.assert_instance(output, int)
    return output
