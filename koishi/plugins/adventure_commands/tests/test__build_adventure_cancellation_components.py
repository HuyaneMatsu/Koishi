import vampytest
from hata import Component, create_text_display

from ..component_builders import build_adventure_cancellation_components


def _iter_options():
    yield (
        [
            create_text_display('You successfully cancelled your adventure.'),
            create_text_display('You head back home immediately.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_cancellation_components():
    """
    Tests whether ``build_adventure_cancellation_components`` works as intended.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_cancellation_components()
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
