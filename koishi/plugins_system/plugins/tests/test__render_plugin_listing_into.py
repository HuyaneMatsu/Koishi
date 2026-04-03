import vampytest

from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import render_plugin_listing_into

from .helpers import wrap_mock_spec_from_file_location


def test__render_plugin_listing_into():
    """
    Tests whether ``render_plugin_listing_into`` works as intended.
    """
    for _ in wrap_mock_spec_from_file_location():
        plugin_0 = Plugin('miau.plugins.eye_0002', '/miau/plugins/eye', None, None, False, False, True, None)
        plugin_1 = Plugin('miau.plugins.hey_0003', '/miau/plugins/hey', None, None, False, False, False, None)
        plugin_2 = Plugin('miau.plugins.hey_0003.mister_0004', '/miau/plugins/hey/mister', None, None, False, False, False, None)
        plugin_3 = Plugin('miau.plugins.hey_0003.sister_0005', '/miau/plugins/hey/sister', None, None, False, False, False, None)
    
    into = render_plugin_listing_into([plugin_0, plugin_1, plugin_2, plugin_3], [])
    output = ''.join(into)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            '```\n'
            'miau.plugins.eye_0002\n'
            'miau.plugins.hey_0003\n'
            'miau.plugins.hey_0003.mister_0004\n'
            'miau.plugins.hey_0003.sister_0005\n'
            '```'
        ),
    )
