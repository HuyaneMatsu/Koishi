__all__ = ()

from scarletio import RichAttributeErrorBaseType, copy_docs


class UserSettingsOption(RichAttributeErrorBaseType):
    """
    User settings option representing a field.
    
    Attributes
    ----------
    display_name : `str`
        The field's display name.
    
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    getter : `FunctionType`
        Getter function.
    
    name : `str`
        The field's name.
    
    setter : `FUnctionType`
        Setter function.
    """
    __slots__ = ('field_descriptor', 'display_name', 'getter', 'name', 'setter')
    
    def __repr__(self):
        """Returns the user option's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' name = ')
        repr_parts.append(self.name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)


class UserSettingsOptionBit(UserSettingsOption):
    """
    User settings option representing a field.
    
    Attributes
    ----------
    display_name : `str`
        The field's display name.
    
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    flag_shift : `bool`
        Shift to apply on the value.
    
    getter : `FunctionType`
        Getter function.
    
    name : `str`
        The field's name.
    
    setter : `FUnctionType`
        Setter function.
    """
    __slots__ = ('flag_shift',)



class UserSettingsOptionBitWithHook(UserSettingsOptionBit):
    """
    User settings option representing a field.
    
    Attributes
    ----------
    display_name : `str`
        The field's display name.
    
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    flag_shift : `bool`
        Shift to apply on the value.
    
    getter : `FunctionType`
        Getter function.
    
    hook : `book`
        Hook to call upon being changed.
    
    name : `str`
        The field's name.
    
    setter : `FUnctionType`
        Setter function.
    """
    __slots__ = ('hook',)


def user_settings_option_create_regular(field_descriptor, name, display_name):
    """
    Creates a new user settings option with the given parameters.
    
    Parameters
    ----------
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    name : `str`
        The field's name.
    
    display_name : `str`
        The field's long name.
    
    Returns
    -------
    user_settings_option : ``UserSettingsOption``
    """
    user_settings_option = object.__new__(UserSettingsOption)
    user_settings_option.display_name = display_name
    user_settings_option.field_descriptor = field_descriptor
    user_settings_option.name = name
    user_settings_option.getter = user_settings_option_getter_regular
    user_settings_option.setter = user_settings_option_setter_regular
    return user_settings_option


def user_settings_option_getter_regular(user_settings_option, user_settings):
    """
    Gets the represented field of the user settings.
    
    Parameters
    ----------
    user_settings_option : ``UserSettingsOption``
        The owner user settings.
    
    user_settings : ``UserSettings``
        The user settings to get value of.
    
    Returns
    -------
    value : `object`
    """
    return user_settings_option.field_descriptor.__get__(user_settings, type(user_settings))


def user_settings_option_setter_regular(user_settings_option, user_settings, value):
    """
    Sets the represented field of the user settings.
    
    Parameters
    ----------
    user_settings_option : ``UserSettingsOption``
        The owner user settings.
    
    user_settings : ``UserSettings``
        The user settings to get value of.
    
    value : `object`
        The value to set.
    """
    user_settings_option.field_descriptor.__set__(user_settings, value)


def user_settings_option_create_bit(field_descriptor, name, display_name, flag_shift):
    """
    Creates a new user settings option with the given parameters.
    
    Parameters
    ----------
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    name : `str`
        The field's name.
    
    display_name : `str`
        The field's long name.
    
    Returns
    -------
    user_settings_option : ``UserSettingsOptionBit``
    """
    user_settings_option = object.__new__(UserSettingsOptionBit)
    user_settings_option.display_name = display_name
    user_settings_option.field_descriptor = field_descriptor
    user_settings_option.name = name
    user_settings_option.flag_shift = flag_shift
    user_settings_option.getter = user_settings_option_getter_bit
    user_settings_option.setter = user_settings_option_setter_bit
    return user_settings_option


@copy_docs(user_settings_option_getter_regular)
def user_settings_option_getter_bit(user_settings_option, user_settings):
    flag_value = user_settings_option.field_descriptor.__get__(user_settings, type(user_settings))
    return (flag_value >> user_settings_option.flag_shift) & 1


@copy_docs(user_settings_option_setter_regular)
def user_settings_option_setter_bit(user_settings_option, user_settings, value):
    field_descriptor = user_settings_option.field_descriptor
    flag_value = field_descriptor.__get__(user_settings, type(user_settings))
    
    flag_shift = user_settings_option.flag_shift
    flag_value = (flag_value & ~(1 << flag_shift)) | ((value & 1) << flag_shift)
    
    field_descriptor.__set__(user_settings, flag_value)


def user_settings_option_create_bit_with_hook(field_descriptor, name, display_name, flag_shift):
    """
    Creates a new user settings option with the given parameters.
    
    Parameters
    ----------
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    name : `str`
        The field's name.
    
    display_name : `str`
        The field's long name.
    
    Returns
    -------
    user_settings_option : ``UserSettingsOptionBitWithHook``
    """
    user_settings_option = object.__new__(UserSettingsOptionBitWithHook)
    user_settings_option.display_name = display_name
    user_settings_option.field_descriptor = field_descriptor
    user_settings_option.name = name
    user_settings_option.flag_shift = flag_shift
    user_settings_option.hook = None
    user_settings_option.getter = user_settings_option_getter_bit
    user_settings_option.setter = user_settings_option_setter_bit_with_hook
    return user_settings_option


@copy_docs(user_settings_option_setter_regular)
def user_settings_option_setter_bit_with_hook(user_settings_option, user_settings, value):
    field_descriptor = user_settings_option.field_descriptor
    flag_value = field_descriptor.__get__(user_settings, type(user_settings))
    flag_shift = user_settings_option.flag_shift
    
    old_value = (flag_value >> flag_shift) & 1
    new_value = value & 1
    
    # If there is no change, do not call the hook.
    if old_value == new_value:
        return
    
    flag_value = (flag_value & ~(1 << flag_shift)) | (new_value << flag_shift)
    
    field_descriptor.__set__(user_settings, flag_value)
    
    hook = user_settings_option.hook
    if (hook is not None):
        hook(user_settings, value)
