import vampytest
from hata import Component, ComponentType

from ..component_building import build_components_in_menu
from ..user_state import UserState


def _assert_output_structure(output):
    """
    Checks output structure.
    
    Parameters
    ----------
    output : ``tuple<Component>``
    """
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 4)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    vampytest.assert_is(output[0].type, ComponentType.section)
    vampytest.assert_is(output[1].type, ComponentType.row)
    vampytest.assert_is(output[2].type, ComponentType.row)
    vampytest.assert_is(output[3].type, ComponentType.row)
    
    nested_0 = output[0]
    vampytest.assert_is_not(nested_0.components, None)
    vampytest.assert_eq(len(nested_0.components), 2)
    for nested_1 in nested_0.components:
        vampytest.assert_is(nested_1.type, ComponentType.text_display)
    
    vampytest.assert_is_not(nested_0.thumbnail, None)
    vampytest.assert_is(nested_0.thumbnail.type, ComponentType.thumbnail_media)
    
    for nested_0 in output[1 : 4]:
        vampytest.assert_is_not(nested_0.components, None)
        for nested_1 in nested_0.components:
            vampytest.assert_is(nested_1.type, ComponentType.button)
    

def test__build_components_in_menu():
    """
    Tests whether ``build_components_in_menu`` works as intended.
    """
    user_state = UserState(202506150001)
    
    output = build_components_in_menu(user_state)
    _assert_output_structure(output)
