import vampytest
from hata import Client
from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import render_plugins_page

from .helpers import wrap_mock_spec_from_file_location


def test__render_plugins_page():
    """
    Tests whether ``render_plugins_page`` works as intended.
    """
    for _ in wrap_mock_spec_from_file_location():
        plugin_0 = Plugin('miau.plugins.eye_0007', '/miau/plugins/eye', None, None, False, False, True, None)
        plugin_1 = Plugin('miau.plugins.hey_0008', '/miau/plugins/hey', None, None, False, False, False, None)
        plugin_2 = Plugin('miau.plugins.hey_0008.mister_0009', '/miau/plugins/hey/mister', None, None, False, False, False, None)
        plugin_3 = Plugin('miau.plugins.hey_0008.sister_0010', '/miau/plugins/hey/sister', None, None, False, False, False, None)
    
    output = render_plugins_page(None, [plugin_0, plugin_1, plugin_2, plugin_3], 1)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_eq(
        output,
        (
            '```\n'
            'miau.plugins.eye_0007\n'
            'miau.plugins.hey_0008\n'
            'miau.plugins.hey_0008.mister_0009\n'
            'miau.plugins.hey_0008.sister_0010\n'
            '```\n'
            'Page 1 / 1'
        )
    )


def test__render_plugins_page__with_client():
    """
    Tests whether ``render_plugins_page`` works as intended.
    
    Case: with client.
    """
    client_id = 202409150000
    client_name = 'resolution'
    
    client = Client('token_' + str(client_id), client_id = client_id, name = client_name)
    
    try:
        for _ in wrap_mock_spec_from_file_location():
            plugin_0 = Plugin('miau.plugins.eye_0011', '/miau/plugins/eye', None, None, False, False, True, None)
            plugin_1 = Plugin('miau.plugins.hey_0012', '/miau/plugins/hey', None, None, False, False, False, None)
            plugin_2 = Plugin('miau.plugins.hey_0012.mister_0013', '/miau/plugins/hey/mister', None, None, False, False, False, None)
            plugin_3 = Plugin('miau.plugins.hey_0012.sister_0014', '/miau/plugins/hey/sister', None, None, False, False, False, None)
        
        output = render_plugins_page(client, [plugin_0, plugin_1, plugin_2, plugin_3], 1)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_eq(
            output,
            (
                f'Plugins for {client_name!s} ({client_id!s})\n'
                f'```\n'
                f'miau.plugins.eye_0011\n'
                f'miau.plugins.hey_0012\n'
                f'miau.plugins.hey_0012.mister_0013\n'
                f'miau.plugins.hey_0012.sister_0014\n'
                f'```\n'
                f'Page 1 / 1'
            )
        )
    
    finally:
        client._delete()
        client = None
