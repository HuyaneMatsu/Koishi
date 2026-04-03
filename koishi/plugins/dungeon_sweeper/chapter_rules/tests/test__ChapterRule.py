from types import FunctionType

import vampytest
from hata import create_text_display

from ..chapter_rule import ChapterRule


def _assert_fields_set(chapter_rule):
    """
    Asserts whether all fields are set of the given chapter rule.
    
    Parameters
    ----------
    chapter_rule : ``ChapterRule``
        The chapter rule to test.
    """
    vampytest.assert_instance(chapter_rule, ChapterRule)
    vampytest.assert_instance(chapter_rule.component_builder, FunctionType)
    vampytest.assert_instance(chapter_rule.id, int)
    

def test__ChapterRule__new():
    """
    Tests whether ``ChapterRule.__new__`` works as intended.
    """
    def component_builder(chapter, style):
        return create_text_display('test')
    
    chapter_rule_id = 9999
    
    
    chapter_rule = ChapterRule(chapter_rule_id, component_builder)
    _assert_fields_set(chapter_rule)
    
    vampytest.assert_is(chapter_rule.component_builder, component_builder)
    vampytest.assert_eq(chapter_rule.id, chapter_rule_id)


def test__ChapterRule__repr():
    """
    Tests whether ``ChapterRule.__repr__`` works as intended.
    """
    def component_builder(chapter, style):
        return create_text_display('test')
    
    chapter_rule_id = 9999
    
    
    chapter_rule = ChapterRule(chapter_rule_id, component_builder)
    
    output = repr(chapter_rule)
    vampytest.assert_instance(output, str)
