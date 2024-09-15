import vampytest

from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import get_plugins_page_count

from .helpers import wrap_mock_spec_from_file_location


def test__get_plugins_page_count():
    """
    Tests whether ``get_plugins_page_count`` works as intended.
    """
    page_size = 2
    
    for _ in wrap_mock_spec_from_file_location():
        plugin_0 = Plugin('miau.plugins.land_0019', '/miau/plugins', None, None, False, False, False, None)
        plugin_1 = Plugin('miau.plugins.fumo_0020', '/miau/plugins/fumo', None, None, False, False, False, None)
        plugin_2 = Plugin('miau.plugins.hey_0021', '/miau/plugins/hey', None, None, False, False, False, None)
    
    mocked = vampytest.mock_globals(
        get_plugins_page_count,
        PAGE_SIZE = page_size,
    )
    
    output = mocked([])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    output = mocked([plugin_0])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)
    
    output = mocked([plugin_0, plugin_1])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)
    
    output = mocked([plugin_0, plugin_1, plugin_2])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
