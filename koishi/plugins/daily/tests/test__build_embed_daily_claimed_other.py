import vampytest
from hata import Embed, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..embed_builders import build_embed_daily_claimed_other


def _iter_options():
    yield (
        123,
        1566,
        20,
        21,
        User.precreate(202412110001, name = 'Remilia'),
        0,
        Embed(
            'How sweet, you claimed my hearts for your chosen one !',
            (
                f'Remilia received 123 {EMOJI__HEART_CURRENCY} and now they have 1566 {EMOJI__HEART_CURRENCY}\n'
                f'They are on a 21 day streak! Keep up the good work for them!'
            ),
            color = COLOR__GAMBLING,
        ),
    )
    
    yield (
        123,
        1566,
        20,
        20,
        User.precreate(202412110002, name = 'Remilia'),
        0,
        Embed(
            'How sweet, you claimed my hearts for your chosen one !',
            (
                f'Remilia received 123 {EMOJI__HEART_CURRENCY} and now they have 1566 {EMOJI__HEART_CURRENCY}\n'
                f'They did not claim daily for 1 day, their daily stands at 20.'
            ),
            color = COLOR__GAMBLING,
        ),
    )
    
    yield (
        123,
        1566,
        20,
        18,
        User.precreate(202412110003, name = 'Remilia'),
        0,
        Embed(
            'How sweet, you claimed my hearts for your chosen one !',
            (
                f'Remilia received 123 {EMOJI__HEART_CURRENCY} and now they have 1566 {EMOJI__HEART_CURRENCY}\n'
                f'They did not claim daily for more than 1 day, they lost 2 streak, and now they have 18.'
            ),
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_daily_claimed_other(received, balance_new, streak_old, streak_new, target_user, guild_id):
    """
    Tests whether ``build_embed_daily_claimed_other`` works as intended.
    
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
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_embed_daily_claimed_other(received, balance_new, streak_old, streak_new, target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
