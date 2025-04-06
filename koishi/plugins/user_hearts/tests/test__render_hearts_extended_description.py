import vampytest
from hata import InteractionEvent, User

from ....bot_utils.daily import ConditionName, Reward

from ..rendering import render_hearts_extended_description


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
        
    user_0 = User.precreate(202412020041, name = name)
    user_1 = User.precreate(202412020043, name = 'koishi')
    
    yield (
        InteractionEvent.precreate(
            202412020040,
            user = user_0,
        ),
        user_0,
        (reward_1, reward_0),
        12,
        (
            '**Base:**\n'
            'Base: 1\n'
            'Extra limit: 5\n'
            'Extra per streak: 3\n'
            '\n'
            '**Called as `brain`:**\n'
            '+ Base: 1\n'
            '+ Extra limit: 2\n'
            '+ Extra per streak: 3\n'
            '**\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_**\n'
            '\n'
            '**Total**\n'
            'Base: 2\n'
            'Extra limit: 7\n'
            'Extra per streak: 6\n'
            '\n'
            '**Formula:**\n'
            'base + min(extra\\_limit, extra\\_per\\_streak * streak) + streak\n'
            '2 + min(7, 6 * 12) + 12 = 21'
        ),
    )
    
    yield (
        InteractionEvent.precreate(
            202412020042,
            user = user_0,
        ),
        user_1,
        (reward_1, reward_0),
        12,
        (
            '**Base:**\n'
            'Base: 1\n'
            'Extra limit: 5\n'
            'Extra per streak: 3\n'
            '\n'
            '**Formula:**\n'
            'base + min(extra\\_limit, extra\\_per\\_streak * streak) + streak\n'
            '1 + min(5, 3 * 12) + 12 = 18'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_hearts_extended_description(interaction_event, target_user, rewards, streak):
    """
    Tests whether ``render_hearts_extended_description`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        User to calculate the reward of.
    
    rewards : `tuple<Reward>`
        Rewards to render.
    
    streak : `int`
        The user's streak.
    
    Returns
    -------
    output : `str`
    """
    output = render_hearts_extended_description(interaction_event, target_user, rewards, streak)
    vampytest.assert_instance(output, str)
    return output
