import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..embed_builders import build_success_embed


def _iter_options():
    user_id = 202502220050
    guild_id = 202502220051
    user = User.precreate(user_id, name = 'Koishi')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Flower')
    
    yield (
        6000,
        2000,
        1000,
        user,
        0,
        None,
        Embed(
            'Aww, so lovely',
            f'You gifted 1000 {EMOJI__HEART_CURRENCY} to Koishi.',
            color = COLOR__GAMBLING,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'6000 -> 5000\n'
                f'```'
            ),
        ).add_field(
            f'Their {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'2000 -> 3000\n'
                f'```'
            ),
        ),
    )
    
    yield (
        6000,
        2000,
        1000,
        user,
        guild_id,
        'mrrr',
        Embed(
            'Aww, so lovely',
            f'You gifted 1000 {EMOJI__HEART_CURRENCY} to Flower.',
            color = COLOR__GAMBLING,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'6000 -> 5000\n'
                f'```'
            ),
        ).add_field(
            f'Their {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'2000 -> 3000\n'
                f'```'
            ),
        ).add_field(
            'Message',
            'mrrr',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed(source_balance, target_balance, amount, target_user, guild_id, message):
    """
    Tests whether ``build_success_embed`` works as intended.
    
    Parameters
    ----------
    source_balance : `int`
        The source user's balance.
    
    target_balance : `int`
        The target user's balance.
    
    amount : `int`
        The amount of balance gifted.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    message : `None | str`
        Additional message from the gifter.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed(source_balance, target_balance, amount, target_user, guild_id, message)
    vampytest.assert_instance(output, Embed)
    return output
