import vampytest
from hata import Embed, Guild, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..constants import GAME_21_EMOJI_ENTER, PLAYERS_MAX
from ..rendering import build_join_embed_base


def _iter_options():
    user_0 = User.precreate(202408050000, name = 'Mountain')
    user_1 = User.precreate(202408050001, name = 'of')
    user_2 = User.precreate(202408050002, name = 'Faith')
    guild = Guild.precreate(202408050003)
    
    yield (
        [user_0, user_1, user_2],
        guild,
        1000,
        'Hey mister',
        True,
        Embed(
            'Hey mister',
            (
                f'Bet amount: {1000!s} {EMOJI__HEART_CURRENCY}\n'
                f'Creator: {user_0.name}\n'
                f'\n'
                f'Joined users:\n'
                f'{user_1.name}\n'
                f'{user_2.name}\n'
                f'\n'
                f'Click on {GAME_21_EMOJI_ENTER} to join.'
            ),
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_embed_base(users, guild, amount, title, ask_to_join):
    """
    Tests whether ``build_join_embed_base`` works as intended.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    title : `str`
        Embed title.
    ask_to_join : `bool`
        Whether the embed should ask the users to join.
    
    Returns
    -------
    output : `Embed`
    """
    output = build_join_embed_base(users, guild, amount, title, ask_to_join)
    vampytest.assert_instance(output, Embed)
    return output
