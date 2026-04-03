__all__ = ('ImageDetailMatcherBase',)

from scarletio import RichAttributeErrorBaseType


class ImageDetailMatcherBase(RichAttributeErrorBaseType):
    """
    Base class for image detail matching.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new image detail matcher.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the image detail matcher's representation."""
        repr_parts = ['<', type(self).__name__]
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
        """Returns the image detail matcher hash value."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two image detail matchers are equal."""
        if type(self) is not type(other):
            return False
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two instances are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `type(self)`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    def get_match_rate(self, image_detail):
        """
        Gets the match rate for the given image detail.
        
        Parameters
        ----------
        image_detail : ``ImageDetailBase``
            The image detail to match.
        
        Returns
        -------
        match_rate : `int`
        """
        match_rate = 0
        for image_detail_action in image_detail.iter_actions():
            match_rate = max(match_rate, self.get_match_rate_action(image_detail_action))
        
        return match_rate
    
    
    def get_match_rate_action(self, image_detail_action):
        """
        Gets the match rate for the given image detail action.
        
        Parameters
        ----------
        image_detail_action : ``ImageDetailAction``
            Action to match.
        
        Returns
        -------
        match_rate : `int`
        """
        return 0
