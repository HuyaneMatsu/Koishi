import vampytest
from hata import Component, ComponentType, Embed

from ...notification_settings import NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_REMINDER_DISABLE

from ..builders import _notification_builder_daily_reminder_default, IMAGE_ORIN_POKE



def test__notification_builder_daily_reminder_default():
    """
    Tests whether ``_notification_builder_daily_reminder_default`` works as intended.
    """
    output = _notification_builder_daily_reminder_default()
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    embed, components = output
    vampytest.assert_instance(embed, Embed)
    vampytest.assert_instance(components, Component)
    
    vampytest.assert_eq(
        embed,
        Embed(
            description = 'Hey mister, did you forget your daily?',
        ).add_thumbnail(
            IMAGE_ORIN_POKE,
        )
    )
    
    vampytest.assert_eq(
        components,
        Component(
            component_type = ComponentType.button,
            label = 'I don\'t want notifs, nya!!',
            custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_REMINDER_DISABLE,
        ),
    )
