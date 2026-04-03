import vampytest

from ..user_settings import UserSettings
from ..option import UserSettingsOption

from types import MemberDescriptorType


def _assert_fields_set(option):
    """
    Tests whether the option has every of its fields set.
    
    Parameters
    ----------
    option : ``UserSettingsOption``
        The option to check.
    """
    vampytest.assert_instance(option, UserSettingsOption)
    vampytest.assert_instance(option.display_name, str)
    vampytest.assert_instance(option.field_descriptor, MemberDescriptorType)
    vampytest.assert_instance(option.name, str)


def test__UserSettingsOption__new():
    """
    Tests whether ``UserSettingsOption.__new__`` works as intended.
    """
    field_descriptor = UserSettings.notification_daily_by_waifu
    name = 'daily'
    display_name = 'daily-by-waifu'
    
    option = UserSettingsOption(
        field_descriptor,
        name,
        display_name,
    )
    
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.display_name, display_name)
    vampytest.assert_is(option.field_descriptor, field_descriptor)
    vampytest.assert_eq(option.name, name)


def test__UserSettingsOption__system_name():
    """
    Tests whether ``UserSettingsOption.system_name`` works as intended.
    """
    field_descriptor = UserSettings.notification_daily_by_waifu
    
    option = UserSettingsOption(field_descriptor, '', '')
    
    output = option.system_name
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, 'notification_daily_by_waifu')


def test__UserSettingsOption__repr():
    """
    Tests whether ``UserSettingsOption.__repr__`` works as intended.
    """
    field_descriptor = UserSettings.notification_daily_by_waifu
    name = 'daily'
    display_name = 'daily-by-waifu'
    
    option = UserSettingsOption(
        field_descriptor,
        name,
        display_name,
    )
    
    output = repr(option)
    vampytest.assert_instance(output, str)


def test__UserSettingsOption__get():
    """
    Tests whether ``UserSettingsOption.get`` works as intended.
    """
    field_descriptor = UserSettings.notification_daily_by_waifu
    
    option = UserSettingsOption(field_descriptor, '', '')
    
    user_settings = UserSettings(202309260000, notification_daily_by_waifu = False)
    
    output = option.get(user_settings)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, user_settings.notification_daily_by_waifu)
    
    user_settings.notification_daily_by_waifu = True
    
    output = option.get(user_settings)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, user_settings.notification_daily_by_waifu)


def test__UserSettingsOption__set():
    """
    Tests whether ``UserSettingsOption.set`` works as intended.
    """
    field_descriptor = UserSettings.notification_daily_by_waifu
    
    option = UserSettingsOption(field_descriptor, '', '')
    
    user_settings = UserSettings(202309260001)
    
    option.set(user_settings, True)
    vampytest.assert_instance(user_settings.notification_daily_by_waifu, bool)
    vampytest.assert_eq(user_settings.notification_daily_by_waifu, True)
    
    option.set(user_settings, False)
    vampytest.assert_instance(user_settings.notification_daily_by_waifu, bool)
    vampytest.assert_eq(user_settings.notification_daily_by_waifu, False)
