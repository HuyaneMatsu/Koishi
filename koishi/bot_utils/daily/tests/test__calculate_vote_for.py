import vampytest
from hata import User

from ..utils import calculate_vote_for

from .helpers import _create_dummy_reward_0, _create_dummy_reward_1


def test__calculate_vote_for():
    """
    Tests whether ``calculate_vote_for`` works as intended.
    """
    reward_0 = _create_dummy_reward_0()
    reward_1 = _create_dummy_reward_1()
    streak = 20
    user = User.precreate(202412010005, name = 'brain')
    
    mocked = vampytest.mock_globals(
        calculate_vote_for,
        REWARDS_VOTE = (reward_0, reward_1),
    )
    
    output = mocked(user, streak)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 220)
