import vampytest

from ...adventure import (
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_ACTIONING_CANCEL_AFTER, ADVENTURE_STATE_CANCELLED,
    ADVENTURE_STATE_DEPARTING, ADVENTURE_STATE_RETURNING, ADVENTURE_STATE_FINALISED, adventure_create
)

from ..helpers import can_cancel_adventure_now


def _iter_options():
    adventure = adventure_create(
        202507290000,
        9999,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_DEPARTING
    
    yield (
        adventure,
        True,
    )
    
    adventure = adventure_create(
        202507290001,
        9999,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_ACTIONING
    
    yield (
        adventure,
        True,
    )
    
    adventure = adventure_create(
        202507290002,
        9999,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_RETURNING
    
    yield (
        adventure,
        False,
    )
    
    adventure = adventure_create(
        202507290003,
        9999,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_FINALISED
    
    yield (
        adventure,
        False,
    )
    
    adventure = adventure_create(
        202507290004,
        9999,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_CANCELLED
    
    yield (
        adventure,
        False,
    )
    
    adventure = adventure_create(
        202507290005,
        9999,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure.state = ADVENTURE_STATE_ACTIONING_CANCEL_AFTER
    
    yield (
        adventure,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__can_cancel_adventure_now(adventure):
    """
    Tests whether ``can_cancel_adventure_now`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to check.
    
    Returns
    -------
    output : `bool`
    """
    output = can_cancel_adventure_now(adventure)
    vampytest.assert_instance(output, bool)
    return output
