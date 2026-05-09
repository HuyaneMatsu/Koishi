__all__ = ()

from scarletio import copy_docs

from .option import UserSettingsOption


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
    
    name : `str`
        The field's name.
    """
    __slots__ = ('flag_shift',)
    
    def __new__(cls, field_descriptor, name, display_name, flag_shift):
        """
        Creates a new user settings option with the given parameters.
        
        Parameters
        ----------
        field_descriptor : `member_descriptor`
            Field get-set descriptor.
    
        flag_shift : `bool`
            Shift to apply on the value.
        
        name : `str`
            The field's name.
        
        display_name : `str`
            The field's long name.
        """
        self = UserSettingsOption.__new__(cls, field_descriptor, name, display_name)
        self.flag_shift = flag_shift
        return self
    
    
    @copy_docs(UserSettingsOption.get)
    def get(self, user_settings):
        flag_value = self.field_descriptor.__get__(user_settings, type(user_settings))
        return (flag_value >> self.flag_shift) & 1
    
    
    @copy_docs(UserSettingsOption.set)
    def set(self, user_settings, value):
        field_descriptor = self.field_descriptor
        flag_value = field_descriptor.__get__(user_settings, type(user_settings))
        
        flag_shift = self.flag_shift
        flag_value = (flag_value & ~(1 << flag_shift)) | ((value & 1) << flag_shift)
        
        field_descriptor.__set__(user_settings, flag_value)
