import vampytest
from hata import Embed, Guild, User

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..rendering import build_join_embed_game_started


def _iter_options():
    user_0 = User.precreate(202408050012, name = 'Mountain')
    user_1 = User.precreate(202408050013, name = 'of')
    user_2 = User.precreate(202408050014, name = 'Faith')
    guild = Guild.precreate(202408050015)
    
    yield (
        [user_0, user_1, user_2],
        guild,
        1000,
        Embed(
            'Game 21 multi-player started',
            (
                f'Bet amount: {1000!s} {EMOJI__HEART_CURRENCY}\n'
                f'Creator: {user_0.name}\n'
                f'\n'
                f'Joined users:\n'
                f'{user_1.name}\n'
                f'{user_2.name}'
            ),
            color = COLOR__GAMBLING,
        ).add_footer(
            'The results will show up here when everyone is finished.',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_embed_game_started(users, guild, amount):
    """
    Tests whether ``build_join_embed_game_started`` works as intended.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    
    Returns
    -------
    output : `Embed`
    """
    output = build_join_embed_game_started(users, guild, amount)
    vampytest.assert_instance(output, Embed)
    return output
