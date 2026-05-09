from types import FunctionType, MemberDescriptorType

import vampytest

from ..user_settings import UserSettings
from ..option_bit_with_hook import UserSettingsOptionBitWithHook


def _assert_fields_set(option):
    """
    Tests whether the option has every of its fields set.
    
    Parameters
    ----------
    option : ``UserSettingsOptionBitWithHook``
        The option to check.
    """
    vampytest.assert_instance(option, UserSettingsOptionBitWithHook)
    vampytest.assert_instance(option.display_name, str)
    vampytest.assert_instance(option.field_descriptor, MemberDescriptorType)
    vampytest.assert_instance(option.flag_shift, int)
    vampytest.assert_instance(option.hook, FunctionType, nullable = True)
    vampytest.assert_instance(option.name, str)


def test__UserSettingsOptionBitWithHook__new():
    """
    Tests whether ``UserSettingsOptionBitWithHook.__new__`` works as intended.
    """
    field_descriptor = UserSettings.notification_flags
    name = 'daily'
    display_name = 'daily-by-waifu'
    flag_shift = 5
    
    option = UserSettingsOptionBitWithHook(
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


def test__UserSettingsOptionBitWithHook__set():
    """
    Tests whether ``UserSettingsOptionBitWithHook.set`` works as intended.
    """
    field_descriptor = UserSettings.notification_flags
    flag_shift = 5
    hook_called = False
    
    def hook(input_user_settings, input_value):
        nonlocal expected_value
        nonlocal user_settings
        nonlocal hook_called
        vampytest.assert_is(input_user_settings, user_settings)
        vampytest.assert_eq(input_value, expected_value)
        hook_called = True
    
    option = UserSettingsOptionBitWithHook(field_descriptor, '', '', flag_shift)
    
    user_settings = UserSettings(202605080002)
    user_settings.notification_flags = 0 << flag_shift
    option.hook = hook
    
    expected_value = 1
    option.set(user_settings, expected_value)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 1 << 5)
    vampytest.assert_true(hook_called)
    hook_called = False
    
    option.set(user_settings, expected_value)
    vampytest.assert_false(hook_called)
    
    expected_value = 0
    option.set(user_settings, expected_value)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 0)
    vampytest.assert_true(hook_called)
    hook_called = False
    
    option.set(user_settings, expected_value)
    vampytest.assert_false(hook_called)
