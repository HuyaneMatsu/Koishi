import vampytest
from hata import Component, ComponentType

from ..chapters import CHAPTER_DEFAULT
from ..component_building import build_components_end_screen
from ..constants import CHAPTERS
from ..user_state import GameState


def _assert_output_structure(output):
    """
    Checks output structure.
    
    Parameters
    ----------
    output : ``tuple<Component>``
    """
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 6)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    vampytest.assert_is(output[0].type, ComponentType.text_display)
    vampytest.assert_is(output[1].type, ComponentType.separator)
    vampytest.assert_is(output[2].type, ComponentType.text_display)
    vampytest.assert_is(output[3].type, ComponentType.separator)
    vampytest.assert_is(output[4].type, ComponentType.text_display)
    vampytest.assert_is(output[5].type, ComponentType.row)
    
    for nested_0 in output[5 : 6]:
        vampytest.assert_is_not(nested_0.components, None)
        for nested_1 in nested_0.components:
            vampytest.assert_is(nested_1.type, ComponentType.button)


def test__build_components_end_screen():
    """
    Tests whether ``build_components_end_screen`` works as intended.
    """
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    else:
        raise RuntimeError()
    
    stage = chapter.get_first_stage()
    assert stage is not None
    
    game_state = GameState(stage, -1)
    
    output = build_components_end_screen(game_state)
    _assert_output_structure(output)
