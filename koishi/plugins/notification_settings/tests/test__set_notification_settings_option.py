import vampytest

from ..notification_settings import NotificationSettings
from ..option import NotificationSettingsOption
from ..utils import set_notification_settings_option


async def test__set_notification_settings_option__no_change():
    """
    Tests whether ``set_notification_settings_option`` works as intended.
    
    Case: No change.
    
    This function is a coroutine.
    """
    saver_called = False
    
    async def saver(notification_settings):
        nonlocal saver_called
        saver_called = True
    
    
    option = NotificationSettingsOption(NotificationSettings.daily, '', '')
    notification_settings = NotificationSettings(202309260002, daily = False)
    
    mocked = vampytest.mock_globals(
        set_notification_settings_option,
        save_one_notification_settings = saver,
    )
    
    output = await mocked(notification_settings, option, False)
    
    vampytest.assert_false(saver_called)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)



async def test__set_notification_settings_option__with_change():
    """
    Tests whether ``set_notification_settings_option`` works as intended.
    
    Case: with change.
    
    This function is a coroutine.
    """
    saver_called = False
    saver_called_with_notification_settings = False
    
    async def saver(notification_settings):
        nonlocal saver_called
        nonlocal saver_called_with_notification_settings
        saver_called = True
        saver_called_with_notification_settings = notification_settings.copy()
    
    option = NotificationSettingsOption(NotificationSettings.daily, '', '')
    notification_settings = NotificationSettings(202309260002, daily = False)
    
    mocked = vampytest.mock_globals(
        set_notification_settings_option,
        save_one_notification_settings = saver,
    )
    
    output = await mocked(notification_settings, option, True)
    
    vampytest.assert_true(saver_called)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(notification_settings.daily, True)
    vampytest.assert_eq(saver_called_with_notification_settings, notification_settings)
