__all__ = ('ImageDetailBase',)

from scarletio import RichAttributeErrorBaseType

from .action import ImageDetailAction
from .helpers import _merge_values_with_value, _merge_values_with_values


class ImageDetailBase(RichAttributeErrorBaseType):
    """
    Base class to represent an image.
    
    Attributes
    ----------
    url : `str`
        Url to the image.
    """
    __slots__ = ('url',)
    
    def __new__(cls, url):
        """
        Creates a new image detail.
        
        Parameters
        ----------
        url : `str`
            Url to the image.
        """
        self = object.__new__(cls)
        self.url = url
        return self
    
    
    def __repr__(self):
        """Returns the image detail's representation."""
        repr_parts = ['<', type(self).__name__, ' url = ', repr(self.url)]
        self._put_repr_parts_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts_into(self, repr_parts):
        """
        Appends the representation parts.
        
        Parameters
        ----------
        repr_parts : `list<str>`
        """
        pass
    
    
    def __hash__(self):
        """Returns the image detail's hash value."""
        return hash(self.url)
    
    
    def __eq__(self, other):
        """Returns whether the two image details are equal."""
        if type(self) is not type(other):
            return False
        
        if self.url != other.url:
            return False
        
        return True

    
    @property
    def provider(self):
        """
        The provider of the image.
        
        Returns
        -------
        provider : `None | str`
        """
        return None
    
    @provider.setter
    def provider(self, value):
        pass
    
    
    def with_provider(self, provider):
        """
        Returns an image detail with the given provider.
        
        Parameters
        ----------
        provider : `None | str`
            The provider of the image.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.provider = provider
        return self
    
    
    @property
    def tags(self):
        """
        Additional tags for the image.
        
        Returns
        -------
        tags : `None | frozenset<str>`
        """
        return None
    
    @tags.setter
    def tags(self, value):
        pass
    
    
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
    
    
    @property
    def actions(self):
        """
        The actions of the image.
        
        Returns
        -------
        action : `None | tuple<ImageDetailAction>`
        """
        return None
    
    @actions.setter
    def actions(self, value):
        pass
    
    
    def with_action(self, action_tag, source, target):
        """
        Returns an image detail with the given action.
        
        Parameters
        ----------
        action_tag : `str`
            The done action.
        source : `None | TouhouCharacter`
            Source character.
        target : `None | TouhouCharacter`
            Target character.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        action = ImageDetailAction(action_tag, source, target)
        self.actions = _merge_values_with_value(self.actions, action)
        
        characters = [*action.iter_characters()]
        self.characters = _merge_values_with_values(self.characters, characters)
        
        return self
    
    
    def with_actions(self, *actions):
        """
        Returns an image detail with the given actions.
        
        Parameters
        ----------
        *action : `ImageDetailAction | (str, None | TouhouCharacter, None | TouhouCharacter)`
            The actions to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        actions = [ImageDetailAction(*action) for action in actions]
        self.actions = _merge_values_with_values(self.actions, actions)
                
        characters = []
        for action in actions:
            characters.extend(action.iter_characters())
        self.characters = _merge_values_with_values(self.characters, characters)
        
        return self


    @property
    def characters(self):
        """
        The characters of the image.
        
        Returns
        -------
        character : `None | tuple<TouhouCharacter>`
        """
        return None
    
    @characters.setter
    def characters(self, value):
        pass
    
    
    def with_character(self, character):
        """
        Returns an image detail with the given character.
        
        Parameters
        ----------
        character : `TouhouCharacter`
            The characters to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.characters = _merge_values_with_value(self.characters, character)
        return self
    
    
    def with_characters(self, *characters):
        """
        Returns an image detail with the given characters.
        
        Parameters
        ----------
        *character : `TouhouCharacter`
            The characters to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.characters = _merge_values_with_values(self.characters, characters)
        return self



    @property
    def creators(self):
        """
        The creators of the image.
        
        Returns
        -------
        creator : `None | tuple<str>`
        """
        return None
    
    @creators.setter
    def creators(self, value):
        pass
    
    
    def with_creator(self, creator):
        """
        Returns an image detail with the given creator.
        
        Parameters
        ----------
        creator : `str`
            The creators to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.creators = _merge_values_with_value(self.creators, creator)
        return self
    
    
    def with_creators(self, *creators):
        """
        Returns an image detail with the given creators.
        
        Parameters
        ----------
        *creator : `str`
            The creators to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.creators = _merge_values_with_values(self.creators, creators)
        return self
    
    
    @property
    def editors(self):
        """
        The editors of the image.
        
        Returns
        -------
        editor : `None | tuple<str>`
        """
        return None
    
    @editors.setter
    def editors(self, value):
        pass
    
    
    def with_editor(self, editor):
        """
        Returns an image detail with the given editor.
        
        Parameters
        ----------
        editor : `str`
            The editors to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.editors = _merge_values_with_value(self.editors, editor)
        return self
    
    
    def with_editors(self, *editors):
        """
        Returns an image detail with the given editors.
        
        Parameters
        ----------
        *editor : `str`
            The editors to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.editors = _merge_values_with_values(self.editors, editors)
        return self
    
    
    def iter_actions(self):
        """
        Iterates over the actions of the image detail.
        
        This method is an iterable generator.
        
        Yields
        ------
        action : ``ImageDetailAction``
        """
        actions = self.actions
        if (actions is not None):
            yield from actions
    
    
    def has_action_tag(self, action_tag):
        """
        Returns whether the image detail has the given `action_tag`.
        
        Parameters
        ----------
        action_tag : `str`
            Action tag to check for.
        
        Returns
        -------
        has_action_tag : `bool`
        """
        for action in self.iter_actions():
            if action.tag == action_tag:
                return True
        
        return False
    
    
    def copy(self):
        """
        Copies the image detail.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.url = self.url
        return new
    
    
    def create_action_subset(self, action_tag):
        """
        Creates a subset of self matching the given `action_tag`. Excludes every other action.
        
        Parameters
        ----------
        action_tag : `str`
            Action tag to subset for.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        matched_actions = None
        
        for action in self.iter_actions():
            if action.tag != action_tag:
                continue
            
            if matched_actions is None:
                matched_actions = []
            
            matched_actions.append(action)
        
        if matched_actions is None:
            return None
        
        new = self.copy()
        new.actions = tuple(matched_actions)
        return new
    
    
    @property
    def name(self):
        """
        Returns the image detail's name.
        
        Returns
        -------
        name : str
        """
        url = self.url
        name_start = url.rfind('/') + 1
        name_end = url.find('.', name_start)
        return url[name_start : name_end]
