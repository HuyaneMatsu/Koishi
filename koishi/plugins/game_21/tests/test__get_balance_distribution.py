import vampytest
from hata import InteractionEvent, User

from ..helpers import get_balance_distribution
from ..player import Player


def _iter_options():
    user_id_0 = 202412080000
    user_id_1 = 202412080001
    user_id_2 = 202412080002
    user_id_3 = 202412080003
    
    player_0 = Player(User.precreate(user_id_0), InteractionEvent.precreate(202412080004))
    player_1 = Player(User.precreate(user_id_1), InteractionEvent.precreate(202412080005))
    player_2 = Player(User.precreate(user_id_2), InteractionEvent.precreate(202412080006))
    player_3 = Player(User.precreate(user_id_3), InteractionEvent.precreate(202412080007))
    
    
    yield (
        None,
        [player_0, player_1, player_2, player_3],
        1000,
        [
            (user_id_0, 1000, 0.0),
            (user_id_1, 1000, 0.0),
            (user_id_2, 1000, 0.0),
            (user_id_3, 1000, 0.0),
        ],
    )

    yield (
        [player_0, player_1],
        [player_2, player_3],
        1000,
        [
            (user_id_0, 1000,  1.0),
            (user_id_1, 1000,  1.0),
            (user_id_2, 1000, -1.0),
            (user_id_3, 1000, -1.0),
        ],
    )

    yield (
        [player_1],
        [player_0, player_2, player_3],
        1000,
        [
            (user_id_1, 1000,  3.0),
            (user_id_0, 1000, -1.0),
            (user_id_2, 1000, -1.0),
            (user_id_3, 1000, -1.0),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_balance_distribution(winners, losers, amount):
    """
    Tests whether ``get_balance_distribution`` works as intended.
    
    Parameters
    ----------
    winners : `None | list<Player>`
        The winning players.
    losers : `None | list<Player>`
        The losing players.
    amount : `int`
        The bet amount.
    
    Returns
    -------
    output : `list<(int, int, int)>`
    """
    output = get_balance_distribution(winners, losers, amount)
    vampytest.assert_instance(output, list)
    return output
