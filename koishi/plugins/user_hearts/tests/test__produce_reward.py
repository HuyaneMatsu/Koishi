import vampytest
from hata import InteractionEvent, User

from ....bot_utils.daily import ConditionName, Reward

from ..rendering import produce_reward


def _iter_options():
    name = 'brain'
    
    class reward_0(Reward):
        base = 1
        extra_limit = 2
        extra_per_streak = 3
        condition = ConditionName(name)
    
    class reward_1(Reward):
        base = 1
        extra_limit = 5
        extra_per_streak = 3
    
    
    yield (
        InteractionEvent.precreate(
            202412020020,
            user = User.precreate(202412020021, name = name)
        ),
        reward_0,
        (
            '**Called as `brain`:**\n'
            '+ Base: 1\n'
            '+ Extra limit: 2\n'
            '+ Extra per streak: 3\n'
        ),
    )
    
    
    yield (
        InteractionEvent.precreate(
            202412020022,
            user = User.precreate(202412020023, name = name)
        ),
        reward_1,
        (
            '**Base:**\n'
            'Base: 1\n'
            'Extra limit: 5\n'
            'Extra per streak: 3\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_reward(interaction_even, reward):
    """
    Tests whether ``produce_reward`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    reward : ``Reward``
        Reward to render.
    
    Returns
    -------
    output : `str`
    """
    return ''.join(produce_reward(interaction_even, reward))
