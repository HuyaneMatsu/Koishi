__all__ = ()

from scarletio import RichAttributeErrorBaseType


class CalendarEvent(RichAttributeErrorBaseType):
    """
    Represents a calendar event.
    
    Attributes
    ----------
    day : `int`
        The day's value.
    month : `int`
        The month's value.
    name : `str`
        The event's name.
    color_code : `str`
        Color code to use to highlight the event's name.
    """
    __slots__ = ('color_code', 'day', 'month', 'name',)
    
    def __init__(self, month, day, name, color_code):
        """
        Creates a new calendar event.
        
        Parameters
        ----------
        month : `int`
            The month's value.
        day : `int`
            The day's value.
        name : `str`
            The event's name.
        color_code : `str`
            Color code to use to highlight the event's name.
        """
        self.color_code = color_code
        self.day = day
        self.month = month
        self.name = name
    
    
    def __eq__(self, other):
        """Returns whether the two calendar events are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.day != other.day:
            return False
        
        if self.month != other.month:
            return False
        
        if self.name != other.name:
            return False
        
        if self.color_code != other.color_code:
            return False
        
        return True
    
    
    def __gt__(self, other):
        """
        Returns whether self is greater than other.
        """
        if type(self) is not type(other):
            return NotImplemented
        
        # Month has priority over day.
        self_month = self.month
        other_month = other.month
        
        if self_month > other_month:
            return True
        
        if self_month < other_month:
            return False
        
        self_day = self.day
        other_day = other.day
        
        if self_day > other_day:
            return True
        
        if self_day < other_day:
            return False
        
        # And lastly the name
        self_name = self.name
        other_name = other.name
        
        if self_name > other_name:
            return True
        
        if self_name < other_name:
            return False
        
        if self.color_code > other.color_code:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the calendar event's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' month = ')
        repr_parts.append(repr(self.month))
        
        repr_parts.append(' day = ')
        repr_parts.append(repr(self.day))
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append(' color_code = ')
        repr_parts.append(repr(self.color_code))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
