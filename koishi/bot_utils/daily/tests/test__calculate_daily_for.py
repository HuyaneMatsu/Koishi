import vampytest
from hata import User

from ..utils import calculate_daily_for

from .helpers import _create_dummy_reward_0, _create_dummy_reward_1


def test__calculate_daily_for():
    """
    Tests whether ``calculate_daily_for`` works as intended.
    """
    reward_0 = _create_dummy_reward_0()
    reward_1 = _create_dummy_reward_1()
    streak = 20
    user = User.precreate(202412010004, name = 'brain')
    
    mocked = vampytest.mock_globals(
        calculate_daily_for,
        REWARDS_DAILY = (reward_0, reward_1),
    )
    
    output = mocked(user, streak)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 220)
