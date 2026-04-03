import vampytest
from hata import Client, StringSelectOption, create_button, create_row, create_string_select
from hata.ext.plugin_loader.plugin import Plugin

from ..helpers import (
    CUSTOM_ID_PAGE_CLOSE, EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT, create_custom_id_page_n, create_custom_switch_client,
    create_plugins_page_components
)

from .helpers import wrap_mock_spec_from_file_location


def test__create_plugins_page_components():
    """
    Tests whether ``create_plugins_page_components`` works as intended.
    """
    for _ in wrap_mock_spec_from_file_location():
        plugin_0 = Plugin('miau.plugins.eye_0041', '/miau/plugins/eye', None, None, False, False, True, None)
        plugin_1 = Plugin('miau.plugins.hey_0042', '/miau/plugins/hey', None, None, False, False, False, None)
        plugín_2 = Plugin('miau.plugins.hey_0042.mister_0043', '/miau/plugins/hey/mister', None, None, False, False, False, None)
        plugin_3 = Plugin('miau.plugins.hey_0042.sister_0044', '/miau/plugins/hey/sister', None, None, False, False, False, None)

    mocked = vampytest.mock_globals(
        create_plugins_page_components,
        CLIENTS = {},
    )
    
    output = mocked(None, [plugin_0, plugin_1, plugín_2, plugin_3], 1)
    
    vampytest.assert_instance(output, list)
    
    vampytest.assert_eq(
        output,
        [
            create_row(
                create_button(
                    'Page 0',
                    EMOJI_LEFT,
                    custom_id = create_custom_id_page_n(0, 0),
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    EMOJI_RIGHT,
                    custom_id = create_custom_id_page_n(0, 2),
                    enabled = False,
                ),
                create_button(
                    None,
                    EMOJI_CLOSE,
                    custom_id = CUSTOM_ID_PAGE_CLOSE,
                ),
            ),
        ]
    )


def test__create_plugins_page_components__with_client():
    """
    Tests whether ``create_plugins_page_components`` works as intended.
    
    Case: with client.
    """
    client_id = 202409150001
    client_name = 'resolution'
    
    client = Client('token_' + str(client_id), client_id = client_id, name = client_name)
    
    try:
        for _ in wrap_mock_spec_from_file_location():
            plugin_0 = Plugin('miau.plugins.eye_0037', '/miau/plugins/eye', None, None, False, False, True, None)
            plugin_1 = Plugin('miau.plugins.hey_0038', '/miau/plugins/hey', None, None, False, False, False, None)
            plugin_2 = Plugin('miau.plugins.hey_0038.mister_0039', '/miau/plugins/hey/mister', None, None, False, False, False, None)
            plugin_3 = Plugin('miau.plugins.hey_0038.sister_0040', '/miau/plugins/hey/sister', None, None, False, False, False, None)
        
        mocked = vampytest.mock_globals(
            create_plugins_page_components,
            CLIENTS = {client_id : client},
        )
        
        output = mocked(client, [plugin_0, plugin_1, plugin_2, plugin_3], 1)
        
        vampytest.assert_instance(output, list)
        
        vampytest.assert_eq(
            output,
            [
                create_row(
                    create_button(
                        'Page 0',
                        EMOJI_LEFT,
                        custom_id = create_custom_id_page_n(client_id, 0),
                        enabled = False,
                    ),
                    create_button(
                        'Page 2',
                        EMOJI_RIGHT,
                        custom_id = create_custom_id_page_n(client_id, 2),
                        enabled = False,
                    ),
                    create_button(
                        None,
                        EMOJI_CLOSE,
                        custom_id = CUSTOM_ID_PAGE_CLOSE,
                    ),
                ),
                create_row(
                    create_string_select(
                        [
                            StringSelectOption(
                                format(client_id, 'x'),
                                client_name,
                                default = True,
                            ),
                        ],
                        custom_id = create_custom_switch_client(1),
                        placeholder = 'Select a client',
                    ),
                ),
            ]
        )
    
    finally:
        client._delete()
        client = None
