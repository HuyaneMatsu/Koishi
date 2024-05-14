__all__ = ('ImageDetailMatcherCustom',)

from scarletio import copy_docs

from .base import ImageDetailMatcherBase


class ImageDetailMatcherCustom(ImageDetailMatcherBase):
    """
    Custom image detail matcher.
    
    Attributes
    ----------
    action_tag : `None | str`
        Action tag to match.
    source : `None | TouhouCharacter`
        Source user to match.
    name : `None | str`
        Name to match.
    target : `None | TouhouCharacter`
        Target user to match.
    """
    __slots__ = ('action_tag', 'source', 'name', 'target')
    
    def __new__(cls, action_tag, source, target, name):
        """
        Creates a new custom image detail matcher.
        
        Parameters
        ----------
        action_tag : `None | str`
            Action tag to match.
        source : `None | TouhouCharacter`
            Source user to match.
        target : `None | TouhouCharacter`
            Target user to match.
        name : `None | str`
            Name to match.
        """
        self = object.__new__(cls)
        self.action_tag = action_tag
        self.source = source
        self.target = target
        self.name = name
        return self
    
    
    @copy_docs(ImageDetailMatcherBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # action_tag
        action_tag = self.action_tag
        if (action_tag is not None):
            repr_parts.append(' action_tag = ')
            repr_parts.append(repr(action_tag))
            
            fields_added = True
        else:
            fields_added = False
        
        # source
        source = self.source
        if (source is not None):
            if fields_added:
                repr_parts.append(',')
            else:
                fields_added = True
            
            repr_parts.append(' source = ')
            repr_parts.append(repr(source))
        
        # target
        target = self.target
        if (target is not None):
            if fields_added:
                repr_parts.append(',')
            else:
                fields_added = True
            
            repr_parts.append(' target = ')
            repr_parts.append(repr(target))
        
        # name
        name = self.name
        if (name is not None):
            if fields_added:
                repr_parts.append(',')
            
            repr_parts.append(' name = ')
            repr_parts.append(repr(name))
    
    
    @copy_docs(ImageDetailMatcherBase._put_repr_parts_into)
    def __hash__(self):
        hash_value = 0
        
        # action_tag
        action_tag = self.action_tag
        if (action_tag is not None):
            hash_value ^= hash(action_tag)
        
        # source
        source = self.source
        if (source is not None):
            hash_value ^= hash(source)
        
        # name
        name = self.name
        if (name is not None):
            hash_value ^= hash(name)
        
        # target
        target = self.target
        if (target is not None):
            hash_value ^= hash(target)
        
        return hash_value
    
    
    @copy_docs(ImageDetailMatcherBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # action_tag
        if self.action_tag != other.action_tag:
            return False
        
        # source
        if self.source != other.source:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # target
        if self.target != other.target:
            return False
        
        return True
    
    
    @copy_docs(ImageDetailMatcherBase.get_match_rate)
    def get_match_rate(self, image_detail):
        if not ImageDetailMatcherBase.get_match_rate(self, image_detail):
            return 0
        
        # name
        name = self.name
        if (name is not None) and (not image_detail.name.startswith(name)):
            return 0
        
        return 1
    
    
    @copy_docs(ImageDetailMatcherBase.get_match_rate_action)
    def get_match_rate_action(self, image_detail_action):
        # action_tag
        action_tag = self.action_tag
        if (action_tag is not None) and (action_tag != image_detail_action.tag):
            return 0
        
        # source
        source = self.source
        if (source is not None) and (source is not image_detail_action.source):
            return 0
        
        # target
        target = self.target
        if (target is not None) and (target is not image_detail_action.target):
            return 0
        
        return 1
