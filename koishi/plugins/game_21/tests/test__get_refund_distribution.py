import vampytest
from hata import InteractionEvent, User

from ..helpers import get_refund_distribution
from ..player import Player


def _iter_options():
    player_0 = Player(User.precreate(202408040038), -1, InteractionEvent.precreate(202408040039))
    player_1 = Player(User.precreate(202408040040), 1, InteractionEvent.precreate(202408040041))
    player_2 = Player(User.precreate(202408040041), 2, InteractionEvent.precreate(202408040042))
    
    
    yield (
        [player_0, player_1, player_2],
        1000,
        [
            (1, 1000, 0.0, True),
            (2, 1000, 0.0, True),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_refund_distribution(players, amount):
    """
    Tests whether ``get_refund_distribution`` works as intended.
    
    Parameters
    ----------
    players : `iterable<Player>`
        Players to create distribution for.
    amount : `int`
        The bet amount.
    
    Returns
    -------
    output : `list<(int, int, int, bool)>`
    """
    output = get_refund_distribution(players, amount)
    vampytest.assert_instance(output, list)
    return output
