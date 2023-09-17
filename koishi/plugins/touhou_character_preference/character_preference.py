__all__ = ('CharacterPreference',)

from scarletio import RichAttributeErrorBaseType

from ..touhou_core import TOUHOU_CHARACTERS


class CharacterPreference(RichAttributeErrorBaseType):
    """
    A user's character preference.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    user_id : `int`
        The user's identifier.
    system_name : `str`
        The character's system name.
    """
    __slots__ = ('entry_id', 'user_id', 'system_name')
    
    def __new__(cls, user_id, system_name):
        """
        Creates a new character preference object.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        system_name : `str`
            The character's system name.
        """
        self = object.__new__(cls)
        self.entry_id = -1
        self.user_id = user_id
        self.system_name = system_name
        return self
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an automation configuration from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.entry_id = entry['id']
        self.user_id = entry['user_id']
        self.system_name = entry['system_name']
        return self
    
    
    def __repr__(self):
        """Returns the character preference's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        entry_id = self.entry_id
        if (entry_id != -1):
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append(', system_name = ')
        repr_parts.append(repr(self.system_name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two character entries are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.user_id != other.user_id:
            return False
        
        if self.system_name != other.system_name:
            return False
        
        return True
    
    
    def get_character(self):
        """
        Returns the reference's character
        
        Returns
        -------
        character : `None`, ``TouhouCharacter``
        """
        return TOUHOU_CHARACTERS.get(self.system_name, None)
