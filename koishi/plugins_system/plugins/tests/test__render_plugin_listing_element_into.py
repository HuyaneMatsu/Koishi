import vampytest

from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import VALUE_LOCKED, render_plugin_listing_element_into

from .helpers import wrap_mock_spec_from_file_location


def test__render_plugin_listing_element_into():
    """
    Tests whether ``render_plugin_listing_element_into`` works as intended.
    """
    plugin_name = 'miau.plugins.land_0001'
    
    for _ in wrap_mock_spec_from_file_location():
        plugin = Plugin(plugin_name, '/miau/plugins', None, None, False, False, False, None)
    
    into = render_plugin_listing_element_into(plugin, [])
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'{plugin_name}\n')


def test__render_plugin_listing_element_into__locked():
    """
    Tests whether ``render_plugin_listing_element_into`` works as intended.
    
    Case: plugin locked.
    """
    plugin_name = 'miau.plugins.land_0000'
    
    for _ in wrap_mock_spec_from_file_location():
        plugin = Plugin(plugin_name, '/miau/plugins', None, None, False, True, False, None)
    
    into = render_plugin_listing_element_into(plugin, [])
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'{plugin_name} {VALUE_LOCKED}\n')
