import vampytest

from ..notification_settings import NotificationSettings
from ..option import NotificationSettingsOption

from types import MemberDescriptorType


def _assert_fields_set(option):
    """
    Tests whether the option has every of its fields set.
    
    Parameters
    ----------
    option : ``NotificationSettingsOption``
        The option to check.
    """
    vampytest.assert_instance(option, NotificationSettingsOption)
    vampytest.assert_instance(option.field_descriptor, MemberDescriptorType)
    vampytest.assert_instance(option.name, str)
    vampytest.assert_instance(option.long_name, str)


def test__NotificationSettingsOption__new():
    """
    Tests whether ``NotificationSettingsOption.__new__`` works as intended.
    """
    field_descriptor = NotificationSettings.daily
    name = 'daily'
    long_name = 'daily-by-waifu'
    
    option = NotificationSettingsOption(
        field_descriptor,
        name,
        long_name,
    )
    
    _assert_fields_set(option)
    
    vampytest.assert_is(option.field_descriptor, field_descriptor)
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.long_name, long_name)


def test__NotificationSettingsOption__system_name():
    """
    Tests whether ``NotificationSettingsOption.system_name`` works as intended.
    """
    field_descriptor = NotificationSettings.daily
    
    option = NotificationSettingsOption(field_descriptor, '', '')
    
    output = option.system_name
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, 'daily')


def test__NotificationSettingsOption__repr():
    """
    Tests whether ``NotificationSettingsOption.__repr__`` works as intended.
    """
    field_descriptor = NotificationSettings.daily
    name = 'daily'
    long_name = 'daily-by-waifu'
    
    option = NotificationSettingsOption(
        field_descriptor,
        name,
        long_name,
    )
    
    output = repr(option)
    vampytest.assert_instance(output, str)


def test__NotificationSettingsOption__get():
    """
    Tests whether ``NotificationSettingsOption.get`` works as intended.
    """
    field_descriptor = NotificationSettings.daily
    
    option = NotificationSettingsOption(field_descriptor, '', '')
    
    notification_settings = NotificationSettings(202309260000, daily = False)
    
    output = option.get(notification_settings)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, notification_settings.daily)
    
    notification_settings.daily = True
    
    output = option.get(notification_settings)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, notification_settings.daily)


def test__NotificationSettingsOption__set():
    """
    Tests whether ``NotificationSettingsOption.set`` works as intended.
    """
    field_descriptor = NotificationSettings.daily
    
    option = NotificationSettingsOption(field_descriptor, '', '')
    
    notification_settings = NotificationSettings(202309260001)
    
    option.set(notification_settings, True)
    vampytest.assert_instance(notification_settings.daily, bool)
    vampytest.assert_eq(notification_settings.daily, True)
    
    option.set(notification_settings, False)
    vampytest.assert_instance(notification_settings.daily, bool)
    vampytest.assert_eq(notification_settings.daily, False)
