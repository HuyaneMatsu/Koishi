import vampytest

from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import get_plugin_list

from .helpers import wrap_mock_spec_from_file_location


def test__get_plugin_list():
    """
    Tests whether ``get_plugin_list`` works as intended.
    """
    for _ in wrap_mock_spec_from_file_location():
        plugin_0 = Plugin('miau.plugins.land_0024', '/miau/plugins', None, None, False, False, False, None)
        plugin_1 = Plugin('miau.plugins.fumo_0025', '/miau/plugins/fumo', None, None, False, False, False, None)
        plugin_2 = Plugin('miau.plugins.hey_0026', '/miau/plugins/hey', None, None, False, False, False, None)
        plugin_3 = Plugin('miau.plugins.hey_0026.mister_0027', '/miau/plugins/hey/mister', None, None, False, False, False, None)
        plugin_4 = Plugin('miau.plugins.hey_0026.sister_0028', '/miau/plugins/hey/sister', None, None, False, False, False, None)
        plugin_5 = Plugin('miau.plugins.eye_0029', '/miau/plugins/eye', None, None, False, False, False, None)
    
    plugins = [
        plugin_0,
        plugin_1,
        plugin_2,
        plugin_3,
        plugin_4,
        plugin_5,
    ]
    
    page = 2
    page_size = 2
    
    output = get_plugin_list(plugins, page, page_size)
    
    vampytest.assert_instance(output, list)
    
    vampytest.assert_eq(
        output,
        [
            plugin_2,
            plugin_3,
        ]
    )
