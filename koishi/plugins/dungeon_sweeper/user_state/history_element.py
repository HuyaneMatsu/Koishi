__all__ = ('HistoryElement',)

from scarletio import RichAttributeErrorBaseType


JSON_KEY_HISTORY_ELEMENT_POSITION = '0'
JSON_KEY_HISTORY_ELEMENT_WAS_SKILL = '1'
JSON_KEY_HISTORY_ELEMENT_CHANGES = '2'


class HistoryElement(RichAttributeErrorBaseType):
    """
    An element of a ``GameState``'s history.
    
    Attributes
    ----------
    changes : `tuple<(int, int)>`
        A tuple containing each changed tile inside of a `position - tile` value pair.
    
    position : `int`
        The character's old position.
    
    was_skill : `bool`
        Whether the step was skill usage.
    """
    __slots__ = ('changes', 'position', 'was_skill')
    
    def __new__(cls, position, was_skill, changes):
        """
        Creates a new history from the given parameters.
        
        Parameters
        ----------
        position : `int`
            The character's old position.
        
        was_skill : `bool`
            Whether the step was skill usage.
        
        changes : `tuple<(int, int)>`
            A tuple containing each changed tile inside of a `position - tile` value pair.
        """
        self = object.__new__(cls)
        self.position = position
        self.was_skill = was_skill
        self.changes = changes
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # position
        repr_parts.append(' position = ')
        repr_parts.append(repr(self.position))
        
        # was_skill
        repr_parts.append(', was_skill = ')
        repr_parts.append(repr(self.was_skill))
        
        # changes
        repr_parts.append(', changes = ')
        repr_parts.append(repr(self.changes))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # position
        if self.position != other.position:
            return False
        
        # was_skill
        if self.was_skill != other.was_skill:
            return False
        
        # changes
        if self.changes != other.changes:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new history element from json data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Decoded json data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.position = data[JSON_KEY_HISTORY_ELEMENT_POSITION]
        self.was_skill = data[JSON_KEY_HISTORY_ELEMENT_WAS_SKILL]
        self.changes = tuple(tuple(change) for change in data[JSON_KEY_HISTORY_ELEMENT_CHANGES])
        return self
    
    
    def to_data(self):
        """
        Converts the history element to json serializable data.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        return {
            JSON_KEY_HISTORY_ELEMENT_POSITION: self.position,
            JSON_KEY_HISTORY_ELEMENT_WAS_SKILL: self.was_skill,
            JSON_KEY_HISTORY_ELEMENT_CHANGES: self.changes,
        }
