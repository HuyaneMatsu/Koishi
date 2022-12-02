__all__ = ('TouhouHandlerKey',)

from ..constants import SAFE_BOORU_ENDPOINT, SAFE_BOORU_PROVIDER, SOLO_REQUIRED_TAGS, TOUHOU_TAGS_BANNED
from ..image_handler import ImageHandlerBooru, ImageHandlerGroup

from .safe_booru_tags import TOUHOU_SAFE_BOORU_TAGS


TOUHOU_IMAGE_HANDLERS = {}


class TouhouHandlerKey:
    """
    Represents a touhou handler's key.
    
    Attributes
    ----------
    characters : `frozenset` of ``TouhouCharacter``
        The included characters.
    hash_value : `int`
        The has precalculated hash value of the key.
    solo : `bool`
        Whether the selected characters should be solo.
    """
    __slots__ = ('characters', 'hash_value', 'solo')
    
    def __init__(self, character, *characters, solo = True):
        characters = frozenset((character, *characters))
        
        if len(characters) > 1:
            solo = False
        
        hash_value = hash(characters) ^ solo
        
        self.characters = characters
        self.hash_value = hash_value
        self.solo = solo
    
    
    def __repr__(self):
        """Returns the handler key's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' characters=')
        repr_parts.append(repr(self.characters))
        
        repr_parts.append(', solo=')
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
        if len(self.characters) == 1:
            self.solo = True
    
    
    def get_handler(self):
        """
        Gets handler which corresponds to the key.
        
        Returns
        -------
        handler : ``ImageHandlerBooru``
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
        if self.solo:
            if len(self.characters) == 1:
                handler = self.create_solo_single_handler()
            else:
                handler = self.create_solo_poly_handler()
        else:
            handler = self.create_wide_handler()
        
        return handler
    
    
    def create_solo_single_handler(self):
        """
        Creates a solo handler single character handler.
        
        Returns
        -------
        handler : ``HandlerBase``
        """
        return ImageHandlerGroup(*(
            ImageHandlerBooru(
                SAFE_BOORU_PROVIDER,
                SAFE_BOORU_ENDPOINT,
                SOLO_REQUIRED_TAGS,
                TOUHOU_TAGS_BANNED,
                {tag},
                True,
            ) for tag in TOUHOU_SAFE_BOORU_TAGS[next(iter(self.characters))]
        ))
    
    
    def create_solo_poly_handler(self):
        """
        Creates a handler for multiple solo characters.
        
        Returns
        -------
        handler : ``HandlerBase``
        """
        return ImageHandlerGroup(*(
            TouhouHandlerKey(character, solo = True).get_handler() for character in self.characters
        ))
    
    
    def create_wide_handler(self):
        """
        Creates a truly multi-character handler.
        
        Returns
        -------
        handler : ``HandlerBase``
        """
        return ImageHandlerGroup(*(
            ImageHandlerBooru(
                SAFE_BOORU_PROVIDER,
                SAFE_BOORU_ENDPOINT,
                None,
                TOUHOU_TAGS_BANNED,
                tags,
                True,
            ) for tags in iter_combine_character_tags(self.characters)
        ))


def iter_combine_character_tags(characters):
    """
    Combines the tags of the given characters.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    characters : `frozenset` of ``TouhouCharacter``
        The characters to walk through.
    
    Yields
    ------
    tags : `set` of `str`
    """
    tag_groups = tuple(TOUHOU_SAFE_BOORU_TAGS[character] for character in characters)
    
    tags = []
    
    for _ in _walk_tags(tags, tag_groups):
        yield {*tags}


def _walk_tags(tags, tag_groups):
    """
    Walks over the tags of the 1st tag group and of all the rest of tag groups recursively in a loop.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    tags : `list` of `str`
        Tags list to build the group into.
    tag_groups : `tuple` of (`tuple` of `str`)
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
