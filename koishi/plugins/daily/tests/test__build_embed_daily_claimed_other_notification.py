import vampytest
from hata import Embed, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..embed_builders import build_embed_daily_claimed_other_notification


def _iter_options():
    yield (
        123,
        1566,
        21,
        User.precreate(202412110004, name = 'Remilia'),
        0,
        Embed(
            'Remilia claimed daily hearts for you.',
            (
                f'You received 123 {EMOJI__HEART_CURRENCY} and now you have 1566 {EMOJI__HEART_CURRENCY}\n'
                f'You are on a 21 day streak.'
            ),
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_daily_claimed_other_notification(received, balance_new, streak_new, source_user, guild_id):
    """
    Tests whether ``build_embed_daily_claimed_other_notification`` works as intended.
    
    Parameters
    ----------
    received : `int`
        The amount of received balance.
    
    balance_new : `int`
        The user's new balance.
    
    streak_new : `int`
        The user's new streak.
    
    source_user : ``ClientUserBase``
        The source user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_embed_daily_claimed_other_notification(received, balance_new, streak_new, source_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
