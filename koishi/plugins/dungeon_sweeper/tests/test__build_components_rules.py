import vampytest
from hata import Component, ComponentType

from ..chapters import CHAPTER_DEFAULT
from ..component_building import build_components_rules
from ..constants import CHAPTERS


def _assert_output_structure(output):
    """
    Checks output structure.
    
    Parameters
    ----------
    output : ``tuple<Component>``
    """
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    vampytest.assert_is(output[0].type, ComponentType.text_display)
    vampytest.assert_is(output[1].type, ComponentType.row)
    
    nested_0 = output[1]
    vampytest.assert_is_not(nested_0.components, None)
    vampytest.assert_eq(len(nested_0.components), 1)
    
    nested_1 = nested_0.components[0]
    vampytest.assert_is(nested_1.type, ComponentType.string_select)
    vampytest.assert_is_not(nested_1.options, None)
    vampytest.assert_eq(len(nested_1.options), len(CHAPTERS))


def test__build_components_rules__default():
    """
    Tests whether ``build_components_rules`` works as intended.
    
    Case: default.
    """
    chapter = None
    
    output = build_components_rules(chapter)
    _assert_output_structure(output)
    
    for index, option in enumerate(output[1].components[0].options):
        vampytest.assert_eq(option.default, index == 0)


def test__build_components_rules__chapter_2():
    """
    Tests whether ``build_components_rules`` works as intended.
    
    Case: chapter 2.
    """
    for chapter in CHAPTERS.values():
        if (chapter is not CHAPTER_DEFAULT) and (not chapter.unlock_prerequisite_stage_id):
            break
    else:
        raise RuntimeError('Could not get satisfactory chapter.')
    
    chapter = chapter.get_next_chapter()
    assert chapter is not None
    
    output = build_components_rules(chapter)
    _assert_output_structure(output)
    
    for index, option in enumerate(output[1].components[0].options):
        vampytest.assert_eq(option.default, index == 2)
