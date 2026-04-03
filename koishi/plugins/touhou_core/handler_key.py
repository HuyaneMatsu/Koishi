__all__ = ('TouhouHandlerKey',)

from scarletio import RichAttributeErrorBaseType

from ..image_handling_core import ImageHandlerSafeBooru, ImageHandlerGroup, SOLO_REQUIRED_TAGS, TOUHOU_TAGS_BANNED

from .character import TOUHOU_CHARACTERS
from .safe_booru_tags import TOUHOU_SAFE_BOORU_TAGS


TOUHOU_IMAGE_HANDLERS = {}


class TouhouHandlerKey(RichAttributeErrorBaseType):
    """
    Represents a touhou handler's key.
    
    Attributes
    ----------
    characters : `None | frozenset<TouhouCharacter>`
        The included characters.
    hash_value : `int`
        The has precalculated hash value of the key.
    solo : `bool`
        Whether the selected characters should be solo.
    """
    __slots__ = ('characters', 'hash_value', 'solo')
    
    def __new__(cls, *characters, solo = True):
        # Process characters
        if characters:
            characters = frozenset(characters)
        else:
            characters = None
        
        # Process solo
        if (characters is not None) and (len(characters) > 1):
            solo = False
        
        # calculate hash value
        hash_value = 0
        
        if characters is not None:
            hash_value = hash(characters)
        
        hash_value ^= solo
        
        # Construct
        self = object.__new__(cls)
        self.characters = characters
        self.hash_value = hash_value
        self.solo = solo
        return self
    
    
    def __repr__(self):
        """Returns the handler key's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' characters = ')
        repr_parts.append(repr(self.characters))
        
        repr_parts.append(', solo = ')
        repr_parts.append(repr(self.solo))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
        
        
    def __hash__(self):
        """Returns the hash value of the object."""
        return self.hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two objects are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.solo != other.solo:
            return False
        
        if self.characters != other.characters:
            return False
        
        return True
    
    
    def apply_solo_preference(self):
        """
        Applies solo preference if applicable.
        """
        characters = self.characters
        if (characters is not None) and (len(characters) == 1):
            self.solo = True
        
    
    def get_handler(self):
        """
        Gets handler which corresponds to the key.
        
        Returns
        -------
        handler : ``ImageHandlerSafeBooru``
        """
        try:
            handler = TOUHOU_IMAGE_HANDLERS[self]
        except KeyError:
            handler = self.create_handler()
            TOUHOU_IMAGE_HANDLERS[self] = handler
        
        return handler
    
    
    def create_handler(self):
        """
        Creates an image handler of the key.
        
        Returns
        -------
        handler : ``HandlerBase``
        """
        characters = self.characters
        solo = self.solo
        
        if characters is None:
            return _create_all_handler(solo)
        
        if not solo:
            return _create_wide_handler(characters)
            
        if len(characters) == 1:
            return _create_solo_single_handler(next(iter(characters)))
        
        return _create_solo_group_handler(characters)


def _create_all_handler(solo):
    """
    Creates an all character handler.
    
    Parameters
    ----------
    solo : `bool`
        Whether the selected characters should be solo.
    
    Returns
    -------
    handler : ``HandlerBase``
    """
    return ImageHandlerGroup(*(
        TouhouHandlerKey(character, solo = solo).get_handler() for character in TOUHOU_CHARACTERS.values()
    ))


def _create_solo_single_handler(character):
    """
    Creates a solo handler single character handler.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        Character to create the handler for.
    
    Returns
    -------
    handler : ``HandlerBase``
    """
    return ImageHandlerGroup(*(
        ImageHandlerSafeBooru(
            SOLO_REQUIRED_TAGS,
            TOUHOU_TAGS_BANNED,
            {(True, tag)},
            True,
        ) for tag in TOUHOU_SAFE_BOORU_TAGS[character]
    ))


def _create_solo_group_handler(characters):
    """
    Creates a handler for multiple solo characters.
    
    Parameters
    ----------
    characters : `frozenset<TouhouCharacter>`
        Characters to create handler for.
    
    Returns
    -------
    handler : ``HandlerBase``
    """
    return ImageHandlerGroup(*(
        TouhouHandlerKey(character, solo = True).get_handler() for character in characters
    ))


def _create_wide_handler(characters):
    """
    Creates a truly multi-character handler.
    
    Parameters
    ----------
    characters : `frozenset<TouhouCharacter>`
        Characters to create handler for.
    
    Returns
    -------
    handler : ``HandlerBase``
    """
    return ImageHandlerGroup(*(
        ImageHandlerSafeBooru(
            None,
            TOUHOU_TAGS_BANNED,
            tags,
            True,
        ) for tags in _iter_combine_character_tags(characters)
    ))


def _iter_combine_character_tags(characters):
    """
    Combines the tags of the given characters.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    characters : `frozenset<TouhouCharacter>`
        The characters to walk through.
    
    Yields
    ------
    tags : `set<(bool, str)>`
    """
    tag_groups = tuple(TOUHOU_SAFE_BOORU_TAGS[character] for character in characters)
    
    tags = []
    
    for _ in _walk_tags(tags, tag_groups):
        yield {(True, tag) for tag in tags}


def _walk_tags(tags, tag_groups):
    """
    Walks over the tags of the 1st tag group and of all the rest of tag groups recursively in a loop.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    tags : `list` of `str`
        Tags list to build the group into.
    tag_groups : `tuple<tuple<str>>`
        Tag groups to walk.
    """
    if not tag_groups:
        yield
        return
    
    tag_group, *tag_groups = tag_groups
    for tag in tag_group:
        tags.append(tag)
        yield from _walk_tags(tags, tag_groups)
        del tags[-1]
