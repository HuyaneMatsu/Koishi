__all__ = ('ImageDetailMatcherContextSensitive',)

from scarletio import copy_docs

from .base import ImageDetailMatcherBase
from .constants import WEIGHT_DIRECT_MATCH, WEIGHT_NONE_MATCH


class ImageDetailMatcherContextSensitive(ImageDetailMatcherBase):
    """
    Context sensitive image detail matcher.
    
    Attributes
    ----------
    sources : `None | set<str>`
        Touhou character source system names to match.
    targets : `None | set<str>`
        Touhou character target system names to match.
    """
    __slots__ = ('sources', 'targets')
    
    def __new__(cls, sources, targets):
        """
        Creates a new context sensitive image detail matcher.
        
        Parameters
        ----------
        sources : `None | set<str>`
            Touhou character source system names to match.
        targets : `None | set<str>`
            Touhou character target system names to match.
        """
        self = object.__new__(cls)
        self.sources = sources
        self.targets = targets
        return self
    
    
    @copy_docs(ImageDetailMatcherBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # sources
        sources = self.sources
        if (sources is not None):
            repr_parts.append(' sources = ')
            repr_parts.append(repr(sources))
            
            fields_added = True
        else:
            fields_added = False
        
        # targets
        targets = self.targets
        if (targets is not None):
            if fields_added:
                repr_parts.append(',')
            
            repr_parts.append(' targets = ')
            repr_parts.append(repr(targets))
    
    
    @copy_docs(ImageDetailMatcherBase._put_repr_parts_into)
    def __hash__(self):
        hash_value = 0
        
        # sources
        sources = self.sources
        if (sources is not None):
            hash_value ^= len(sources)
            for source in sources:
                hash_value ^= hash(source)
        
        # targets
        targets = self.targets
        if (targets is not None):
            hash_value ^= len(targets) << 8
            for target in targets:
                hash_value ^= hash(target)
        
        return hash_value
    
    
    @copy_docs(ImageDetailMatcherBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # sources
        if self.sources != other.sources:
            return False
        
        # targets
        if self.targets != other.targets:
            return False
        
        return True
    
    
    @copy_docs(ImageDetailMatcherBase.get_match_rate)
    def get_match_rate(self, image_detail):
        match_rate = 0
        for image_detail_action in image_detail.iter_actions():
            match_rate = max(match_rate, self.get_match_rate_action(image_detail_action))
        
        return match_rate
    
    
    @copy_docs(ImageDetailMatcherBase.get_match_rate_action)
    def get_match_rate_action(self, image_detail_action):
        match_rate = 0
        
        # source
        source = image_detail_action.source
        if source is None:
            match_rate += WEIGHT_NONE_MATCH
        else:
            sources = self.sources
            if (sources is not None) and (source.system_name in sources):
                match_rate += WEIGHT_DIRECT_MATCH
        
        # target
        target = image_detail_action.target
        if target is None:
            match_rate += WEIGHT_NONE_MATCH
        else:
            targets = self.targets
            if (targets is not None) and (target.system_name in targets):
                match_rate += WEIGHT_DIRECT_MATCH
        
        return match_rate
