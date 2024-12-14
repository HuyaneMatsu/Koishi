import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY, URL__KOISHI_TOP_GG

from ..embed_builders import build_embed_daily_claimed_self


def _iter_options():
    yield (
        123,
        1566,
        20,
        21,
        True,
        Embed(
            'Here, some hearts for you~\nCome back tomorrow !',
            (
                f'You received 123 {EMOJI__HEART_CURRENCY} and now have 1566 {EMOJI__HEART_CURRENCY}\n'
                f'You are on a 21 day streak! Keep up the good work!\n'
                f'\n'
                f'Please vote for me on [top.gg]({URL__KOISHI_TOP_GG}) for extra {EMOJI__HEART_CURRENCY} <3'
            ),
            color = COLOR__GAMBLING,
        ),
    )
    
    yield (
        123,
        1566,
        20,
        20,
        False,
        Embed(
            'Here, some hearts for you~\nCome back tomorrow !',
            (
                f'You received 123 {EMOJI__HEART_CURRENCY} and now have 1566 {EMOJI__HEART_CURRENCY}\n'
                f'You did not claim daily for 1 day, your daily stands at 20.'
            ),
            color = COLOR__GAMBLING,
        ),
    )
    
    yield (
        123,
        1566,
        20,
        18,
        False,
        Embed(
            'Here, some hearts for you~\nCome back tomorrow !',
            (
                f'You received 123 {EMOJI__HEART_CURRENCY} and now have 1566 {EMOJI__HEART_CURRENCY}\n'
                f'You did not claim daily for more than 1 day, you lost 2 streak, and now you are at 18.'
            ),
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_daily_claimed_self(received, balance_new, streak_old, streak_new, top_gg_notify):
    """
    Tests whether ``build_embed_daily_claimed_self`` works as intended.
    
    Parameters
    ----------
    received : `int`
        The amount of received balance.
    
    balance_new : `int`
        The user's new balance.
    
    streak_old : `int`
        The user's previous streak.
    
    streak_new : `int`
        The user's new streak.
    
    top_gg_notify : `bool`
        Whether the user should be encouraged to vote on top.gg.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_embed_daily_claimed_self(received, balance_new, streak_old, streak_new, top_gg_notify)
    vampytest.assert_instance(output, Embed)
    return output
