import vampytest

from ..utils import calculate_received_reward_credibility


def _iter_options():
    yield (10, 0, 0, 10)
    yield (10, 1, 0, 10)
    yield (10, 2, 0, 10)
    yield (10, 0, 1, 7)
    yield (10, 0, 2, 6)
    yield (10, 0, 3, 5)
    yield (10, 1, 1, 10)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_received_reward_credibility(reward_credibility, quest_rank, entity_rank):
    """
    Tests whether ``calculate_received_reward_credibility`` works as intended.
    
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
    output = calculate_received_reward_credibility(reward_credibility, quest_rank, entity_rank)
    vampytest.assert_instance(output, int)
    return output
