__all__ = ()

from scarletio import RichAttributeErrorBaseType


class NotificationSettingsOption(RichAttributeErrorBaseType):
    """
    Notification settings option representing a field.
    
    Attributes
    ----------
    field_descriptor : `member_descriptor`
        Field get-set descriptor.
    
    long_name : `str`
        The field's long name.
    
    name : `str`
        The field's name.
    """
    __slots__ = ('field_descriptor', 'long_name', 'name')
    
    def __new__(cls, field_descriptor, name, long_name):
        """
        Creates a new notification settings option with the given parameters.
        
        Parameters
        ----------
        field_descriptor : `member_descriptor`
            Field get-set descriptor.
        
        name : `str`
            The field's name.
        
        long_name : `str`
            The field's long name.
        """
        self = object.__new__(cls)
        self.field_descriptor = field_descriptor
        self.long_name = long_name
        self.name = name
        return self
    
    
    @property
    def system_name(self):
        """
        Returns the option's system name-
        
        Returns
        -------
        system_name : `str`
        """
        return self.field_descriptor.__name__
    
    
    def __repr__(self):
        """Returns the notification option's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' system_name = ')
        repr_parts.append(self.system_name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get(self, notification_settings):
        """
        Gets the represented field of the notification settings.
        
        Parameters
        ----------
        notification_settings : ``NotificationSettings``
            The notification settings to get value of.
        
        Returns
        -------
        value : `bool`
        """
        return self.field_descriptor.__get__(notification_settings, type(notification_settings))
    
    
    def set(self, notification_settings, value):
        """
        Sets the represented field of the notification settings.
        
        Parameters
        ----------
        notification_settings : ``NotificationSettings``
            The notification settings to get value of.
        value : `bool`
            The value to set.
        """
        self.field_descriptor.__set__(notification_settings, value)
