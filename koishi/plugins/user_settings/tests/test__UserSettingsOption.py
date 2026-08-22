from types import FunctionType, MemberDescriptorType

import vampytest

from ..option import (
    UserSettingsOption, UserSettingsOptionBitWithHook, user_settings_option_create_bit,
    user_settings_option_create_bit_with_hook, user_settings_option_create_regular, user_settings_option_getter_bit,
    user_settings_option_getter_regular, user_settings_option_setter_bit, user_settings_option_setter_bit_with_hook,
    user_settings_option_setter_regular
)
from ..user_settings import UserSettings, user_settings_create


def assert_user_settings_option_fields_set(user_settings_option):
    """
    Tests whether the option has every of its fields set.
    
    Parameters
    ----------
    user_settings_option : ``UserSettingsOption``
        The option to check.
    """
    vampytest.assert_instance(user_settings_option, UserSettingsOption)
    vampytest.assert_instance(user_settings_option.display_name, str)
    vampytest.assert_instance(user_settings_option.field_descriptor, MemberDescriptorType)
    vampytest.assert_instance(user_settings_option.name, str)
    vampytest.assert_instance(user_settings_option.getter, FunctionType)
    vampytest.assert_instance(user_settings_option.setter, FunctionType)


def assert_user_settings_option_bit_fields_set(user_settings_option):
    """
    Tests whether the option has every of its fields set.
    
    Parameters
    ----------
    user_settings_option : ``UserSettingsOptionBit``
        The option to check.
    """
    vampytest.assert_instance(user_settings_option, UserSettingsOption)
    vampytest.assert_instance(user_settings_option.display_name, str)
    vampytest.assert_instance(user_settings_option.field_descriptor, MemberDescriptorType)
    vampytest.assert_instance(user_settings_option.flag_shift, int)
    vampytest.assert_instance(user_settings_option.name, str)
    vampytest.assert_instance(user_settings_option.getter, FunctionType)
    vampytest.assert_instance(user_settings_option.setter, FunctionType)


def assert_user_settings_option_bit_with_hook_fields_set(user_settings_option):
    """
    Tests whether the option has every of its fields set.
    
    Parameters
    ----------
    user_settings_option : ``UserSettingsOptionBitWithHook``
        The option to check.
    """
    vampytest.assert_instance(user_settings_option, UserSettingsOption)
    vampytest.assert_instance(user_settings_option.display_name, str)
    vampytest.assert_instance(user_settings_option.field_descriptor, MemberDescriptorType)
    vampytest.assert_instance(user_settings_option.flag_shift, int)
    vampytest.assert_instance(user_settings_option.hook, FunctionType, nullable = True)
    vampytest.assert_instance(user_settings_option.name, str)
    vampytest.assert_instance(user_settings_option.getter, FunctionType)
    vampytest.assert_instance(user_settings_option.setter, FunctionType)


def test__UserSettingsOption__repr():
    """
    Tests whether ``UserSettingsOption.__repr__`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
    name = 'daily'
    display_name = 'daily-by-waifu'
    
    user_settings_option = user_settings_option_create_regular(
        field_descriptor,
        name,
        display_name,
    )
    
    output = repr(user_settings_option)
    vampytest.assert_instance(output, str)


def test__user_settings_option_create_regular():
    """
    Tests whether ``user_settings_option_create_regular`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
    name = 'daily'
    display_name = 'daily-by-waifu'
    
    user_settings_option = user_settings_option_create_regular(
        field_descriptor,
        name,
        display_name,
    )
    
    assert_user_settings_option_fields_set(user_settings_option)
    
    vampytest.assert_eq(user_settings_option.display_name, display_name)
    vampytest.assert_is(user_settings_option.field_descriptor, field_descriptor)
    vampytest.assert_eq(user_settings_option.name, name)
    vampytest.assert_is(user_settings_option.getter, user_settings_option_getter_regular)
    vampytest.assert_is(user_settings_option.setter, user_settings_option_setter_regular)


def test__user_settings_option_getter_regular():
    """
    Tests whether ``UserSettingsOption.get`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
    client_id = 202604250000
    
    user_settings_option = user_settings_option_create_regular(
        field_descriptor,
        '',
        '',
    )
    
    user_settings = user_settings_create(202309260000)
    user_settings.notification_flags = 0
    
    output = user_settings_option_getter_regular(user_settings_option, user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    user_settings.preferred_client_id = client_id
    
    output = user_settings_option_getter_regular(user_settings_option, user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, client_id)
    

def test__UserSettingsOption__set():
    """
    Tests whether ``user_settings_option_setter_regular`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
    client_id = 202604250001
    
    user_settings_option = user_settings_option_create_regular(
        field_descriptor,
        '',
        '',
    )
    
    user_settings = user_settings_create(202309260001)
    user_settings.preferred_client_id = 0
    
    user_settings_option_setter_regular(user_settings_option, user_settings, client_id)
    vampytest.assert_instance(user_settings.preferred_client_id, int)
    vampytest.assert_eq(user_settings.preferred_client_id, client_id)
    
    user_settings_option_setter_regular(user_settings_option, user_settings, 0)
    vampytest.assert_instance(user_settings.preferred_client_id, int)
    vampytest.assert_eq(user_settings.preferred_client_id, 0)


def test__user_settings_option_create_bit():
    """
    Tests whether ``user_settings_option_create_bit`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
    name = 'daily'
    display_name = 'daily-by-waifu'
    flag_shift = 5
    
    user_settings_option = user_settings_option_create_bit(
        field_descriptor,
        name,
        display_name,
        flag_shift,
    )
    
    assert_user_settings_option_bit_fields_set(user_settings_option)
    
    vampytest.assert_eq(user_settings_option.display_name, display_name)
    vampytest.assert_is(user_settings_option.field_descriptor, field_descriptor)
    vampytest.assert_eq(user_settings_option.name, name)
    vampytest.assert_is(user_settings_option.getter, user_settings_option_getter_bit)
    vampytest.assert_is(user_settings_option.setter, user_settings_option_setter_bit)


def test__user_settings_option_getter_bit():
    """
    Tests whether ``user_settings_option_getter_bit`` works as intended.
    """
    field_descriptor = UserSettings.notification_flags
    flag_shift = 5
    
    user_settings_option = user_settings_option_create_bit(
        field_descriptor,
        '',
        '',
        flag_shift,
    )
    
    user_settings = user_settings_create(202605080000)
    user_settings.notification_flags = 0 << flag_shift
    
    output = user_settings_option_getter_bit(user_settings_option, user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    user_settings.notification_flags = 1 << flag_shift
    
    output = user_settings_option_getter_bit(user_settings_option, user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__user_settings_option_setter_bit():
    """
    Tests whether ``user_settings_option_setter_bit`` works as intended.
    """
    field_descriptor = UserSettings.notification_flags
    flag_shift = 5
    
    user_settings_option = user_settings_option_create_bit(
        field_descriptor,
        '',
        '',
        flag_shift,
    )
    
    user_settings = user_settings_create(202605080001)
    user_settings.notification_flags = 0 << flag_shift
    
    user_settings_option_setter_bit(user_settings_option, user_settings, 1)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 1 << 5)
    
    user_settings_option_setter_bit(user_settings_option, user_settings, 0)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 0)


def test__user_settings_option_create_bit_with_hook():
    """
    Tests whether ``user_settings_option_create_bit_with_hook`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
    name = 'daily'
    display_name = 'daily-by-waifu'
    flag_shift = 5
    
    user_settings_option = user_settings_option_create_bit_with_hook(
        field_descriptor,
        name,
        display_name,
        flag_shift,
    )
    
    assert_user_settings_option_bit_with_hook_fields_set(user_settings_option)
    
    vampytest.assert_eq(user_settings_option.display_name, display_name)
    vampytest.assert_is(user_settings_option.field_descriptor, field_descriptor)
    vampytest.assert_eq(user_settings_option.name, name)
    vampytest.assert_is(user_settings_option.getter, user_settings_option_getter_bit)
    vampytest.assert_is(user_settings_option.setter, user_settings_option_setter_bit_with_hook)


def test__user_settings_option_setter_bit_with_hook():
    """
    Tests whether ``user_settings_option_setter_bit_with_hook`` works as intended.
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
    
    user_settings_option = user_settings_option_create_bit_with_hook(
        field_descriptor,
        '',
        '',
        flag_shift,
    )
    
    user_settings = user_settings_create(202605080002)
    user_settings.notification_flags = 0 << flag_shift
    user_settings_option.hook = hook
    
    expected_value = 1
    user_settings_option_setter_bit_with_hook(user_settings_option, user_settings, expected_value)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 1 << 5)
    vampytest.assert_true(hook_called)
    hook_called = False
    
    user_settings_option_setter_bit_with_hook(user_settings_option, user_settings, expected_value)
    vampytest.assert_false(hook_called)
    
    expected_value = 0
    user_settings_option_setter_bit_with_hook(user_settings_option, user_settings, expected_value)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_eq(user_settings.notification_flags, 0)
    vampytest.assert_true(hook_called)
    hook_called = False
    
    user_settings_option_setter_bit_with_hook(user_settings_option, user_settings, expected_value)
    vampytest.assert_false(hook_called)
