import vampytest

from ..love_option import LoveOption


def _assert_fields_set(love_option):
    """
    Asserts whether every fields are set of the given love option.
    
    Parameters
    ----------
    love_option : ``LoveOption``
        The love option to test.
    """
    vampytest.assert_instance(love_option, LoveOption)
    vampytest.assert_instance(love_option.name, str)
    vampytest.assert_instance(love_option.text, str)
    vampytest.assert_instance(love_option.titles, tuple)


def test__LoveOption__new():
    """
    Tests whether ``LoveOption.__new__`` works as intended.
    """
    name = 'brain'
    titles = ('empty', 'big')
    text = 'You should derp now!'
    
    love_option = LoveOption(name, titles, text)
    _assert_fields_set(love_option)
    
    vampytest.assert_eq(love_option.name, name)
    vampytest.assert_eq(love_option.text, text)
    vampytest.assert_eq(love_option.titles, titles)


def test__LoveOption__repr():
    """
    Tests whether ``LoveOption.__repr__`` works as intended.
    """
    name = 'brain'
    titles = ('empty', 'big')
    text = 'You should derp now!'
    
    love_option = LoveOption(name, titles, text)
    
    output = repr(love_option)
    vampytest.assert_instance(output, str)
