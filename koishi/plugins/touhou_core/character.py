__all__ = ('TOUHOU_CHARACTERS', 'TouhouCharacter')

from scarletio import RichAttributeErrorBaseType


TOUHOU_CHARACTER_NAMES = []
TOUHOU_CHARACTER_LOOKUP = {}
TOUHOU_CHARACTERS = {}


class TouhouCharacter(RichAttributeErrorBaseType):
    """
    Represents a touhou character.
    
    Attributes
    ----------
    name : `str`
        The character's name.
    nicks : `None | tuple<str>`
        Additional nick names of the character.
    system_name : `str`
        The character's system name. Used to identify the character.
    """
    __slots__ = ('name', 'nicks', 'system_name')
    
    def __new__(cls, system_name, name, nicks):
        """
        Creates a new touhou character.
        
        Parameters
        ----------
        system_name : `str`
            The character's system name. Used to identify the character.
        name : `str`
            The character's name.
        nicks : `None | tuple<str>`
            Additional nick names of the character.
        """
        if (nicks is not None) and (not nicks):
            nicks = None
        
        self = object.__new__(cls)
        self.system_name = system_name
        self.name = name
        self.nicks = nicks
        
        register_character(self)
        
        return self
    
    
    def __repr__(self):
        """Returns the touhou character's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' system_name = ')
        repr_parts.append(repr(self.system_name))
        
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        
        nicks = self.nicks
        if (nicks is not None):
            length = len(nicks)
            repr_parts.append(', nicks = [')
            
            index = 0
            while True:
                nick = nicks[index]
                index += 1
                
                repr_parts.append(repr(nick))
                
                if index >= length:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the touhou character's hash value."""
        return hash(self.system_name)
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.system_name > other.system_name
    
    
    def iter_names(self):
        """
        Iterates over the names of the touhou character.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
        """
        yield self.name
        
        nicks = self.nicks
        if (nicks is not None):
            yield from nicks


def register_character(touhou_character):
    """
    Registers the touhou character into the lookup tables.
    
    Parameters
    ----------
    touhou_character : ``TouhouCharacter``
        The touhou character to register.
    """
    for name in touhou_character.iter_names():
        name = name.casefold()
        
        TOUHOU_CHARACTER_NAMES.append(name)
        TOUHOU_CHARACTER_LOOKUP[name] = touhou_character
    
    TOUHOU_CHARACTERS[touhou_character.system_name] = touhou_character


def remove_character(touhou_character):
    """
    Registers the touhou character into the lookup tables.
    
    Parameters
    ----------
    touhou_character : ``TouhouCharacter``
        The touhou character to register.
    """
    for name in touhou_character.iter_names():
        name = name.casefold()
        
        if TOUHOU_CHARACTER_LOOKUP.get(name, None) is touhou_character:
            del TOUHOU_CHARACTER_LOOKUP[name]
            
            # Only remove name, if it references the current character.
            TOUHOU_CHARACTER_NAMES.remove(name)
        
    
    system_name = touhou_character.system_name
    if TOUHOU_CHARACTERS.get(system_name, None) is touhou_character:
        del TOUHOU_CHARACTERS[system_name]
