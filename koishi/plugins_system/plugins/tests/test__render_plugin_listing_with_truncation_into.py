import vampytest

from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import render_plugin_listing_with_truncation_into

from .helpers import wrap_mock_spec_from_file_location


def test__render_plugin_listing_with_truncation_into():
    """
    Tests whether ``render_plugin_listing_with_truncation_into`` works as intended.
    """
    for _ in wrap_mock_spec_from_file_location():
        plugin_0 = Plugin('miau.plugins.eye_0015', '/miau/plugins/eye', None, None, False, False, True, None)
        plugin_1 = Plugin('miau.plugins.hey_0016', '/miau/plugins/hey', None, None, False, False, False, None)
        plugin_2 = Plugin('miau.plugins.hey_0016.mister_0017', '/miau/plugins/hey/mister', None, None, False, False, False, None)
        plugin_3 = Plugin('miau.plugins.hey_0016.sister_0018', '/miau/plugins/hey/sister', None, None, False, False, False, None)
    
    into = render_plugin_listing_with_truncation_into(
        [plugin_0, plugin_1, plugin_2, plugin_3],
        len(plugin_0.name) + len(plugin_1.name) + 2 + 30,
        [],
    )
    output = ''.join(into)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            '```\n'
            'miau.plugins.eye_0015\n'
            'miau.plugins.hey_0016\n'
            '```\n'
            '2 truncated.'
        ),
    )
