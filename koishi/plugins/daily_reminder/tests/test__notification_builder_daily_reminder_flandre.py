import vampytest
from hata import Component, ComponentType, Embed

from ...user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE

from ..builders import _notification_builder_daily_reminder_flandre, IMAGE_FLANDRE_HAPPY


def test__notification_builder_daily_reminder_flandre():
    """
    Tests whether ``_notification_builder_daily_reminder_flandre`` works as intended.
    """
    output = _notification_builder_daily_reminder_flandre()
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    embed, components = output
    vampytest.assert_instance(embed, Embed)
    vampytest.assert_instance(components, Component)
    
    vampytest.assert_eq(
        embed,
        Embed(
            description = 'Onee-sama, did you forget your daily?',
        ).add_thumbnail(
            IMAGE_FLANDRE_HAPPY,
        )
    )
    
    vampytest.assert_eq(
        components,
        Component(
            component_type = ComponentType.button,
            label = 'Go back to your basement!!',
            custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE,
        ),
    )
