__all__ = ()

from scarletio import RichAttributeErrorBaseType


class UserSettingsOption(RichAttributeErrorBaseType):
    """
    User settings option representing a field.
    
    Attributes
    ----------
    display_name : `str`
        The field's display name.
    
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    name : `str`
        The field's name.
    """
    __slots__ = ('field_descriptor', 'display_name', 'name')
    
    def __new__(cls, field_descriptor, name, display_name):
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
        """
        self = object.__new__(cls)
        self.display_name = display_name
        self.field_descriptor = field_descriptor
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns the user option's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' name = ')
        repr_parts.append(self.name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get(self, user_settings):
        """
        Gets the represented field of the user settings.
        
        Parameters
        ----------
        user_settings : ``UserSettings``
            The user settings to get value of.
        
        Returns
        -------
        value : `object`
        """
        return self.field_descriptor.__get__(user_settings, type(user_settings))
    
    
    def set(self, user_settings, value):
        """
        Sets the represented field of the user settings.
        
        Parameters
        ----------
        user_settings : ``UserSettings``
            The user settings to get value of.
        
        value : `object`
            The value to set.
        """
        self.field_descriptor.__set__(user_settings, value)
