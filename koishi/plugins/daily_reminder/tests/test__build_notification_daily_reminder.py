import vampytest
from hata import Component, ComponentType, Embed


from ..builders import build_notification_daily_reminder


def test__build_notification_daily_reminder__default():
    """
    Tests whether ``build_notification_daily_reminder`` works as intended.
    
    Case: Default.
    """
    client_id = 0
    output = build_notification_daily_reminder(client_id)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    embed, components = output
    vampytest.assert_instance(embed, Embed)
    vampytest.assert_instance(components, Component)


def test__build_notification_daily_reminder__custom():
    """
    Tests whether ``build_notification_daily_reminder`` works as intended.
    
    Case: custom.
    """
    return_embed = Embed(
        'hey mister'
    )
    return_components = Component(
        component_type = ComponentType.button,
        custom_id = 'standby',
        label = 'orin',
    )
    
    def builder():
        nonlocal return_embed
        nonlocal return_components
        return return_embed, return_components
    
    client_id = 202402280000
    
    mocked = vampytest.mock_globals(
        build_notification_daily_reminder,
        NOTIFICATION_BUILDERS_DAILY_REMINDER = {client_id: builder},
    )
    
    output = mocked(client_id)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    embed, components = output
    vampytest.assert_instance(embed, Embed)
    vampytest.assert_instance(components, Component)
    
    vampytest.assert_eq(embed, return_embed)
    vampytest.assert_eq(components, return_components)
