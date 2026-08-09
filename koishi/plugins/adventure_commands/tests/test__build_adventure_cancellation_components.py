import vampytest
from hata import Component, create_text_display

from ..component_building import build_adventure_cancellation_components
from ..constants import ADVENTURE_CANCELLATION_MODE_AFTER, ADVENTURE_CANCELLATION_MODE_NOW


def _iter_options():
    yield (
        ADVENTURE_CANCELLATION_MODE_NOW,
        [
            create_text_display('You successfully cancelled your adventure.'),
            create_text_display('You head back home immediately.'),
        ],
    )
    yield (
        ADVENTURE_CANCELLATION_MODE_AFTER,
        [
            create_text_display('You successfully cancelled your adventure.'),
            create_text_display('You will head back after the next action is completed.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_cancellation_components(cancellation_mode):
    """
    Tests whether ``build_adventure_cancellation_components`` works as intended.
    
    Parameters
    ----------
    cancellation_mode : `int`
        How the adventure was cancelled.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_cancellation_components(cancellation_mode)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
