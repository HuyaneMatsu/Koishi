__all__ = ('ImageDetail',)


from .constants import CHARACTER_DIRECTION_ANY, CHARACTER_DIRECTION_SOURCE, CHARACTER_DIRECTION_TARGET


class ImageDetail:
    """
    Represents an image.
    
    Attributes
    ----------
    characters : `None | (set<str>, set<str>)`
        Image character info. used for constant images.
    provider : `None | str`
        The provider of the image.
    tags : `None | frozenset<str>`
        Additional tags for the image.
    url : `str`
        Url to the image.
    """
    __slots__ = ('characters', 'provider', 'tags', 'url')
    
    def __new__(cls, url, provider = None):
        """
        Creates a new image detail.
        
        Parameters
        ----------
        url : `str`
            Url to the image.
        provider : `None, `str` = `None`, Optional
            Provider of the image.
        """
        self = object.__new__(cls)
        self.characters = None
        self.url = url
        self.tags = None
        self.provider = provider
        return self
    
    
    def with_tags(self, tags):
        """
        Returns an image detail with the given tags.
        
        Parameters
        ----------
        tags : `None`, `frozenset<str>`
            Additional tags for the image.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.tags = tags
        return self
    
    
    def with_source(self, character):
        """
        Returns a new image handler detail with the given source character.
        
        Parameters
        ----------
        character : ``TouhouCharacter``
            Touhou character to add as a source.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self._add_character(CHARACTER_DIRECTION_SOURCE, character)
        return self
    
    
    def with_target(self, character):
        """
        Returns a new image handler detail with the given target character.
        
        Parameters
        ----------
        character : ``TouhouCharacter``
            Touhou character to add as a target.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self._add_character(CHARACTER_DIRECTION_TARGET, character)
        return self
    
    
    def with_any(self, character):
        """
        Returns a new image handler detail with the given any directional character.
        
        Parameters
        ----------
        character : ``TouhouCharacter``
            Touhou character to add with any direction.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self._add_character(CHARACTER_DIRECTION_ANY, character)
        return self
    
    
    def _add_character(self, direction, character):
        """
        Adds a character info to self.
        
        Parameters
        ----------
        direction : `int`
            Direction flag.
        character : ``TouhouCharacter``
            Touhou character to add.
        """
        character_info = (direction, character.system_name)
        
        characters = self.characters
        if characters is None:
            characters = (character_info,)
        else:
            characters = (*characters, character_info)
        self.characters = characters
    
    
    def iter_source_character_system_names(self):
        """
        Iterates over the source system names.
        
        This method is an iterable generator.
        
        Yields
        ------
        system_name : `str`
        """
        characters = self.characters
        if (characters is not None):
            for direction, system_name in characters:
                if direction & CHARACTER_DIRECTION_SOURCE:
                    yield system_name
    
    
    def iter_target_character_system_names(self):
        """
        Iterates over the target system names.
        
        This method is an iterable generator.
        
        Yields
        ------
        system_name : `str`
        """
        characters = self.characters
        if (characters is not None):
            for direction, system_name in characters:
                if direction & CHARACTER_DIRECTION_TARGET:
                    yield system_name
    
    
    def __repr__(self):
        """Returns the image handler's representation."""
        repr_parts = ['<', self.__class__.__name__, ' url = ', repr(self.url)]
        
        provider = self.provider
        if (provider is not None):
            repr_parts.append(', ')
            repr_parts.append(repr(provider))
        
        tags = self.tags
        if (tags is not None):
            repr_parts.append(', tags = ')
            repr_parts.append(repr(tags))
        
        
        characters = self.characters
        if (characters is not None):
            repr_parts.append(', characters = ')
            repr_parts.append(repr(characters))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the image detail's hash value."""
        hash_value = 0
        
        characters = self.characters
        if (characters is not None):
            hash_value ^= hash(characters)
        
        tags = self.tags
        if (tags is not None):
            hash_value ^= hash(tags)
        
        provider = self.provider
        if (provider is not None):
            hash_value ^= hash(provider)
        
        hash_value ^= hash(self.url)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two image details are equal."""
        if type(self) is not type(other):
            return False
        
        if self.characters != other.characters:
            return False
        
        if self.provider != other.provider:
            return False
        
        if self.tags != other.tags:
            return False
        
        if self.url != other.url:
            return False
        
        return True
