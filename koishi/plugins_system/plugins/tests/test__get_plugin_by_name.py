import vampytest

from hata.ext.plugin_loader.plugin import Plugin
from hata.ext.slash import InteractionAbortedError

from ..helpers import get_plugin_by_name

from .helpers import wrap_mock_spec_from_file_location


def test__get_plugin_by_name__no_plugin():
    """
    Returns the plugin with the given name.
    
    Case: no plugin.
    """
    name = 'keine_0031'
    
    def get_plugin_like_mock(input_name):
        nonlocal name
        
        vampytest.assert_eq(input_name, name)
        return None
    
    mocked = vampytest.mock_globals(
        get_plugin_by_name,
        get_plugin_like = get_plugin_like_mock,
    )
    
    with vampytest.assert_raises(InteractionAbortedError):
        mocked(name)
    

def test__get_plugin_by_name__locked():
    """
    Returns the plugin with the given name.
    
    Case: locked plugin.
    """
    name = 'keine_0032'
    
    for _ in wrap_mock_spec_from_file_location():
        plugin = Plugin(name, '/hey/mister', None, None, False, True, False, None)
    
    def get_plugin_like_mock(input_name):
        nonlocal name
        nonlocal plugin
        
        vampytest.assert_eq(input_name, name)
        
        return plugin
    
    mocked = vampytest.mock_globals(
        get_plugin_by_name,
        get_plugin_like = get_plugin_like_mock,
    )
    
    with vampytest.assert_raises(InteractionAbortedError):
        mocked(name)
    


def test__get_plugin_by_name__success():
    """
    Returns the plugin with the given name.
    
    Case: locked plugin.
    """
    name = 'keine_0033'
    
    for _ in wrap_mock_spec_from_file_location():
        plugin = Plugin(name, '/hey/mister', None, None, False, False, False, None)
    
    def get_plugin_like_mock(input_name):
        nonlocal name
        nonlocal plugin
        
        vampytest.assert_eq(input_name, name)
        
        return plugin
    
    mocked = vampytest.mock_globals(
        get_plugin_by_name,
        get_plugin_like = get_plugin_like_mock,
    )
    
    output = mocked(name)
    vampytest.assert_instance(output, Plugin)
    vampytest.assert_is(output, plugin)
    
