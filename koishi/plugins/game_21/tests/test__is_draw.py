import vampytest
from hata import InteractionEvent, User

from ..helpers import is_draw
from ..player import Player


def _iter_options():
    player_0 = Player(User.precreate(202408040030), -1, InteractionEvent.precreate(202408040031))
    player_1 = Player(User.precreate(202408040032), -1, InteractionEvent.precreate(202408040033))
    
    yield (None, None, True)
    yield (None, [player_1], True)
    yield ([player_0], None, True)
    yield ([player_0], [player_1], False)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_draw(winners, losers):
    """
    Tests whether ``is_draw`` works as intended.
    
    Parameters
    ----------
    winners : `None | list`
        The winning players.
    losers : `None | list`
        The losing players.
    
    Returns
    -------
    output : `bool`
    """
    output = is_draw(winners, losers)
    vampytest.assert_instance(output, bool)
    return output
