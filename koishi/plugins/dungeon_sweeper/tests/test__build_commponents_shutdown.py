import vampytest
from hata import Component, ComponentType

from ..component_building import build_components_shutdown


def _assert_output_structure(output):
    """
    Checks output structure.
    
    Parameters
    ----------
    output : ``tuple<Component>``
    """
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 1)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    vampytest.assert_is(output[0].type, ComponentType.section)
    
    nested_0 = output[0]
    vampytest.assert_is_not(nested_0.components, None)
    vampytest.assert_eq(len(nested_0.components), 1)
    for nested_1 in nested_0.components:
        vampytest.assert_is(nested_1.type, ComponentType.text_display)
    
    vampytest.assert_is_not(nested_0.thumbnail, None)
    vampytest.assert_is(nested_0.thumbnail.type, ComponentType.thumbnail_media)


def test__build_components_shutdown():
    """
    Tests whether ``build_components_shutdown`` works as intended.
    """
    output = build_components_shutdown()
    _assert_output_structure(output)
