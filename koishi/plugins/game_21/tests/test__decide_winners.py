import vampytest

from hata import InteractionEvent, User

from ..constants import PLAYER_STATE_FINISH, PLAYER_STATE_CANCELLED_TIMEOUT
from ..helpers import decide_winners
from ..player import Player


def _iter_options():
    player_0 = Player(User.precreate(202408040015), InteractionEvent.precreate(202408040016))
    player_0.state = PLAYER_STATE_FINISH
    player_0.hand.add_card(8)
    player_0.hand.add_card(8)
    
    player_1 = Player(User.precreate(202408040017), InteractionEvent.precreate(202408040018))
    player_1.state = PLAYER_STATE_FINISH
    player_1.hand.add_card(8)
    player_1.hand.add_card(8)
    
    player_2 = Player(User.precreate(202408040019), InteractionEvent.precreate(202408040020))
    player_2.state = PLAYER_STATE_FINISH
    player_2.hand.add_card(8)
    player_2.hand.add_card(6)
    
    player_3 = Player(User.precreate(202408040021), InteractionEvent.precreate(202408040022))
    player_3.state = PLAYER_STATE_FINISH
    player_3.hand.add_card(8)
    player_3.hand.add_card(6)
    player_3.hand.add_card(4)
    
    player_4 = Player(User.precreate(202408040023), InteractionEvent.precreate(202408040024))
    player_4.state = PLAYER_STATE_FINISH
    player_4.hand.add_card(8)
    player_4.hand.add_card(6)
    player_4.hand.add_card(4)
    
    player_5 = Player(User.precreate(202408040024), InteractionEvent.precreate(202408040025))
    player_5.state = PLAYER_STATE_CANCELLED_TIMEOUT
    player_5.hand.add_card(8)
    player_5.hand.add_card(6)
    
    yield (
        [],
        (
            None,
            None,
        ),
    )
    
    yield (
        [player_0, player_1],
        (
            [player_0, player_1],
            None,
        ),
    )
    
    yield (
        [player_0, player_2],
        (
            [player_0],
            [player_2],
        ),
    )
    
    yield (
        [player_3, player_4],
        (
            None,
            [player_3, player_4],
        ),
    )
    
    yield (
        [player_0, player_2, player_4],
        (
            [player_0],
            [player_2, player_4],
        ),
    )

    yield (
        [player_2, player_5],
        (
            [player_2],
            [player_5],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__decide_winners(players):
    """
    Tests whether ``decide_winners`` works as intended.
    
    Parameters
    ----------
    players : `list<Player>`
        Players to decide about.
    
    output
    -------
    output : `(None | list<Player> | None | list<Player>)`
    """
    return decide_winners(players)
