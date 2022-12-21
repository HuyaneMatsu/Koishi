__all__ = (
    'TOUHOU_CHARACTERS_UNIQUE', 'TouhouCharacter', 'get_familiar_touhou_matches', 'get_touhou_character_like',
    'get_touhou_character_names_like',
)

from difflib import get_close_matches
from re import compile as re_compile, I as re_ignore_case, U as re_unicode, escape as re_escape


TOUHOU_CHARACTER_NAMES = []
TOUHOU_CHARACTER_LOOKUP = {}
TOUHOU_CHARACTERS_UNIQUE = set()


class TouhouCharacter:
    """
    Represents a touhou character.
    
    Attributes
    ----------
    system_name : `str`
        The character's system name. Used to identify the character.
    name : `str`
        The character's name.
    nicks : `tuple` of `str`
        Additional nick names of the character.
    """
    __slots__ = ('system_name', 'name', 'nicks')
    
    def __new__(cls, system_name, name, nicks):
        """
        Creates a new touhou character.
        
        Parameters
        ----------
        system_name : `str`
            The character's system name. Used to identify the character.
        name : `str`
            The character's name.
        nicks : `tuple` of `str`
            Additional nick names of the character.
        """
        self = object.__new__(cls)
        self.system_name = system_name
        self.name = name
        self.nicks = nicks
        
        for name in self.iter_names():
            name = name.casefold()
            
            TOUHOU_CHARACTER_NAMES.append(name)
            TOUHOU_CHARACTER_LOOKUP[name] = self
        
        TOUHOU_CHARACTERS_UNIQUE.add(self)
        
        return self
    
    
    def __repr__(self):
        """Returns the touhou character's representation."""
        return ''.join(['<', self.__class__.__name__, ' name=', repr(self.name), '>'])
    
    
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
        yield from self.nicks


def get_touhou_character_like(name):
    """
    Gets the touhou character's name with the most familiar name.
    
    Parameters
    ----------
    name : `str`
        Input value.
    
    Returns
    -------
    matched : `None`, ``TouhouCharacter``
    """
    name_length = len(name)
    if name_length == 0:
        return None
    
    name = name.replace('-', ' ').replace('_', ' ').casefold()
    
    if name_length > 10:
        name_length = 10
    
    diversity = 0.2 + (10 - name_length) * 0.02
    
    matcheds = get_close_matches(
        name,
        TOUHOU_CHARACTER_NAMES,
        n = 1,
        cutoff = 1.0 - diversity,
    )
    
    if matcheds:
        return TOUHOU_CHARACTER_LOOKUP[matcheds[0]]



def _iter_names_like(name):
    """
    Iterates over familiar names to the given one.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Names to match.
    
    Yields
    ------
    character_name : `str`
    """
    matcher = re_compile(re_escape(name), re_ignore_case | re_unicode)
    
    for character_name in TOUHOU_CHARACTER_NAMES:
        if (matcher.match(character_name) is not None):
            yield character_name

    value_length = len(name)
    if value_length < 3:
        return
    
    if len(name) > 10:
        value_length = 10
    
    diversity = 0.2 + (10 - value_length) * 0.02
    
    yield from get_close_matches(
        name,
        TOUHOU_CHARACTER_NAMES,
        n = 25,
        cutoff = 1.0 - diversity,
    )


def get_touhou_character_names_like(name):
    """
    Gets the touhou characters' names who's name match the given input.
    
    Parameters
    ----------
    name : `str`
        Input value.
    
    Returns
    -------
    unique : `list`, `str`
    """
    unique = []
    characters = set()
    
    for name in _iter_names_like(name):
        character = TOUHOU_CHARACTER_LOOKUP[name]
        if character in characters:
            continue
        
        characters.add(character)
        unique.append(name)
        if len(unique) < 25:
            continue
        
        break
    
    return unique


def get_familiar_touhou_matches(name):
    """
    Gets familiar names to the given one.
    
    Parameters
    ----------
    name : `str`
        Input value.
    
    Returns
    -------
    touhou_characters : `list` of `tuple` (``TouhouCharacter``, `str`)
    """
    name_length = len(name)
    if name_length > 10:
        name_length = 10
    
    diversity = 0.2 + (10 - name_length) * 0.02
    
    matcheds = get_close_matches(
        name,
        TOUHOU_CHARACTER_NAMES,
        n = 10,
        cutoff = 1.0 - diversity,
    )
    
    return [(TOUHOU_CHARACTER_LOOKUP[matched], matched) for matched in matcheds]


def freeze(*characters):
    """
    Freezes the given character's system name into a frozenlist.
    
    Parameters
    ----------
    *characters : ``TouhouCharacter``
        The touhou characters to freeze.
    
    Returns
    -------
    frozen : `frozenset`
    """
    return frozenset(character.system_name for character in characters)
