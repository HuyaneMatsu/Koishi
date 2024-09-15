import vampytest

from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import get_elements_truncation_point

from .helpers import wrap_mock_spec_from_file_location


def test__get_elements_truncation_point():
    """
    Tests whether ``get_elements_truncation_point`` works as intended.
    """
    for _ in wrap_mock_spec_from_file_location():
        plugin_0 = Plugin('miau.plugins.land_0034', '/miau/plugins', None, None, False, False, False, None)
        plugin_1 = Plugin('miau.plugins.fumo_0035', '/miau/plugins/fumo', None, None, False, False, False, None)
        plugin_2 = Plugin('miau.plugins.hey_0036', '/miau/plugins/hey', None, None, False, False, False, None)
    
    plugins = [plugin_0, plugin_1, plugin_2]
    length = len(plugin_0.name) + len(plugin_1.name) + 2
    
    output = get_elements_truncation_point(plugins, length)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    
    output = get_elements_truncation_point(plugins, length - 1)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)
    
    output = get_elements_truncation_point(plugins, length + 1)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
