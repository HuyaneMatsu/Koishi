import vampytest

from ..user_settings import UserSettings
from ..option import UserSettingsOption
from ..utils import set_user_settings_option


async def test__set_user_settings_option__no_change():
    """
    Tests whether ``set_user_settings_option`` works as intended.
    
    Case: No change.
    
    This function is a coroutine.
    """
    saver_called = False
    
    async def saver(user_settings):
        nonlocal saver_called
        saver_called = True
    
    
    option = UserSettingsOption(UserSettings.notification_daily_by_waifu, '', '')
    user_settings = UserSettings(202309260002, notification_daily_by_waifu = False)
    
    mocked = vampytest.mock_globals(
        set_user_settings_option,
        save_one_user_settings = saver,
    )
    
    output = await mocked(user_settings, option, False)
    
    vampytest.assert_false(saver_called)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)



async def test__set_user_settings_option__with_change():
    """
    Tests whether ``set_user_settings_option`` works as intended.
    
    Case: with change.
    
    This function is a coroutine.
    """
    saver_called = False
    saver_called_with_user_settings = False
    
    async def saver(user_settings):
        nonlocal saver_called
        nonlocal saver_called_with_user_settings
        saver_called = True
        saver_called_with_user_settings = user_settings.copy()
    
    option = UserSettingsOption(UserSettings.notification_daily_by_waifu, '', '')
    user_settings = UserSettings(202309260002, notification_daily_by_waifu = False)
    
    mocked = vampytest.mock_globals(
        set_user_settings_option,
        save_one_user_settings = saver,
    )
    
    output = await mocked(user_settings, option, True)
    
    vampytest.assert_true(saver_called)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(user_settings.notification_daily_by_waifu, True)
    vampytest.assert_eq(saver_called_with_user_settings, user_settings)
