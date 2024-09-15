import vampytest

from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import VALUE_LOCKED, get_plugin_listing_element_length

from .helpers import wrap_mock_spec_from_file_location


def test__get_plugin_listing_element_length():
    """
    Tests whether ``get_plugin_listing_element_length`` works as intended.
    """
    plugin_name = 'miau.plugins.land_0022'
    
    for _ in wrap_mock_spec_from_file_location():
        plugin = Plugin(plugin_name, '/miau/plugins', None, None, False, False, False, None)
    
    output = get_plugin_listing_element_length(plugin)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, len(plugin_name) + 1)


def test__get_plugin_listing_element_length__locked():
    """
    Tests whether ``get_plugin_listing_element_length`` works as intended.
    
    Case: plugin locked.
    """
    plugin_name = 'miau.plugins.land_0023'
    
    for _ in wrap_mock_spec_from_file_location():
        plugin = Plugin(plugin_name, '/miau/plugins', None, None, False, True, False, None)
    
    output = get_plugin_listing_element_length(plugin)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, len(plugin_name) + 1 + len(VALUE_LOCKED) + 1)
