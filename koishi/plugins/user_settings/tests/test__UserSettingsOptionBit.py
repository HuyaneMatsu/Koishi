from types import MemberDescriptorType

import vampytest

from ..user_settings import UserSettings
from ..option_bit import UserSettingsOptionBit


def _assert_fields_set(option):
    """
    Tests whether the option has every of its fields set.
    
    Parameters
    ----------
    option : ``UserSettingsOptionBit``
        The option to check.
    """
    vampytest.assert_instance(option, UserSettingsOptionBit)
    vampytest.assert_instance(option.display_name, str)
    vampytest.assert_instance(option.field_descriptor, MemberDescriptorType)
    vampytest.assert_instance(option.flag_shift, int)
    vampytest.assert_instance(option.name, str)


def test__UserSettingsOptionBit__new():
    """
    Tests whether ``UserSettingsOptionBit.__new__`` works as intended.
    """
    field_descriptor = UserSettings.notification_flags
    name = 'daily'
    display_name = 'daily-by-waifu'
    flag_shift = 5
    
    option = UserSettingsOptionBit(
        field_descriptor,
        name,
        display_name,
        flag_shift,
    )
    
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.display_name, display_name)
    vampytest.assert_is(option.field_descriptor, field_descriptor)
    vampytest.assert_is(option.flag_shift, flag_shift)
    vampytest.assert_eq(option.name, name)


def test__UserSettingsOptionBit__get():
    """
    Tests whether ``UserSettingsOptionBit.get`` works as intended.
    """
    field_descriptor = UserSettings.notification_flags
    flag_shift = 5
    
    option = UserSettingsOptionBit(field_descriptor, '', '', flag_shift)
    
    user_settings = UserSettings(202605080000)
    user_settings.notification_flags = 0 << flag_shift
    
    output = option.get(user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    user_settings.notification_flags = 1 << flag_shift
    
    output = option.get(user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__UserSettingsOptionBit__set():
    """
    Tests whether ``UserSettingsOptionBit.set`` works as intended.
    """
    field_descriptor = UserSettings.notification_flags
    flag_shift = 5
    
    option = UserSettingsOptionBit(field_descriptor, '', '', flag_shift)
    
    user_settings = UserSettings(202605080001)
    user_settings.notification_flags = 0 << flag_shift
    
    option.set(user_settings, 1)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 1 << 5)
    
    option.set(user_settings, 0)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 0)
