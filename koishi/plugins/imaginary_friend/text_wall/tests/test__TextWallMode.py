from types import FunctionType

import vampytest

from ..mode import TextWallMode


def _assert_fields_set(text_wall_mode):
    """
    Asserts whether all fields are set of the given text wall mode.
    
    Parameters
    ----------
    text_wall_mode : ``TextWallMode``
        Instance to check.
    """
    vampytest.assert_instance(text_wall_mode, TextWallMode)
    vampytest.assert_instance(text_wall_mode.builder, FunctionType)
    vampytest.assert_instance(text_wall_mode.name, str)
    vampytest.assert_instance(text_wall_mode.splitter, FunctionType)


def test__TextWallMode__new():
    """
    Tests whether ``TextWallMode.__new__`` works as intended.
    """
    name = 'pudding'
    
    def splitter(text):
        return text
    
    def builder(text):
        return text
    
    text_wall_mode = TextWallMode(
        name,
        splitter,
        builder,
    )
    _assert_fields_set(text_wall_mode)
    
    vampytest.assert_eq(text_wall_mode.builder, builder)
    vampytest.assert_eq(text_wall_mode.name, name)
    vampytest.assert_eq(text_wall_mode.splitter, splitter)


def test__TextWallMode__repr():
    """
    Tests whether ``TextWallMode.__repr__`` works as intended.
    """
    name = 'pudding',
    
    def splitter(text):
        return text
    
    def builder(text):
        return text
    
    text_wall_mode = TextWallMode(
        name,
        splitter,
        builder,
    )
    
    output = repr(text_wall_mode)
    vampytest.assert_instance(output, str)
