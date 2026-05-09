__all__ = ()

from scarletio import copy_docs

from .option_bit import UserSettingsOptionBit


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
    
    hook : `book`
        Hook to call upon being changed.
    
    name : `str`
        The field's name.
    """
    __slots__ = ('hook',)
    
    @copy_docs(UserSettingsOptionBit.__new__)
    def __new__(cls, field_descriptor, name, display_name, flag_shift):
        self = UserSettingsOptionBit.__new__(cls, field_descriptor, name, display_name, flag_shift)
        self.hook = None
        return self
    
    
    @copy_docs(UserSettingsOptionBit.set)
    def set(self, user_settings, value):
        field_descriptor = self.field_descriptor
        flag_value = field_descriptor.__get__(user_settings, type(user_settings))
        flag_shift = self.flag_shift
        
        old_value = (flag_value >> flag_shift) & 1
        new_value = value & 1
        
        # If there is no change, do not call the hook.
        if old_value == new_value:
            return
        
        flag_value = (flag_value & ~(1 << flag_shift)) | (new_value << flag_shift)
        
        field_descriptor.__set__(user_settings, flag_value)
        
        hook = self.hook
        if (hook is not None):
            hook(user_settings, value)
