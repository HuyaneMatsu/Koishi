from types import MemberDescriptorType

import vampytest

from ..user_settings import UserSettings
from ..option import UserSettingsOption


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
    field_descriptor = UserSettings.preferred_client_id
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


def test__UserSettingsOption__repr():
    """
    Tests whether ``UserSettingsOption.__repr__`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
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
    field_descriptor = UserSettings.preferred_client_id
    client_id = 202604250000
    
    option = UserSettingsOption(field_descriptor, '', '')
    
    user_settings = UserSettings(202309260000)
    user_settings.notification_flags = 0
    
    output = option.get(user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    user_settings.preferred_client_id = client_id
    
    output = option.get(user_settings)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, client_id)


def test__UserSettingsOption__set():
    """
    Tests whether ``UserSettingsOption.set`` works as intended.
    """
    field_descriptor = UserSettings.preferred_client_id
    client_id = 202604250001
    
    option = UserSettingsOption(field_descriptor, '', '')
    
    user_settings = UserSettings(202309260001)
    user_settings.preferred_client_id = 0
    
    option.set(user_settings, client_id)
    vampytest.assert_instance(user_settings.preferred_client_id, int)
    vampytest.assert_eq(user_settings.preferred_client_id, client_id)
    
    option.set(user_settings, 0)
    vampytest.assert_instance(user_settings.preferred_client_id, int)
    vampytest.assert_eq(user_settings.preferred_client_id, 0)
