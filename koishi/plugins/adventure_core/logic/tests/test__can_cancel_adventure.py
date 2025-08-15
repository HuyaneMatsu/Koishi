import vampytest

from ...adventure import (
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_CANCELLED, ADVENTURE_STATE_DEPARTING, ADVENTURE_STATE_RETURNING,
    ADVENTURE_STATE_FINALIZED, Adventure,
)

from ..helpers import can_cancel_adventure


def _iter_options():
    adventure = Adventure(
        202507290000,
        9999,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_DEPARTING
    
    yield (
        adventure,
        True,
    )
    
    adventure = Adventure(
        202507290001,
        9999,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_ACTIONING
    
    yield (
        adventure,
        True,
    )
    
    adventure = Adventure(
        202507290002,
        9999,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_RETURNING
    
    yield (
        adventure,
        False,
    )
    
    adventure = Adventure(
        202507290003,
        9999,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_FINALIZED
    
    yield (
        adventure,
        False,
    )
    
    adventure = Adventure(
        202507290004,
        9999,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_CANCELLED
    
    yield (
        adventure,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__can_cancel_adventure(adventure):
    """
    Tests whether ``can_cancel_adventure`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to check.
    
    Returns
    -------
    output : `bool`
    """
    output = can_cancel_adventure(adventure)
    vampytest.assert_instance(output, bool)
    return output
