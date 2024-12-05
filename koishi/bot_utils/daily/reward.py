__all__ = ('Reward',)

from scarletio import RichAttributeErrorBaseType

from ..instantiate_inheritance import InstantiateInheritanceMeta


class Reward(RichAttributeErrorBaseType, metaclass = InstantiateInheritanceMeta):
    """
    Represents a reward.
    
    Attributes
    ----------
    base : `int`
        Base reward.
    
    condition : `None | ConditionBase`
        Condition to check whether to apply the reward.
    
    extra_limit : `int`
        Extra reward extra_limit.
    
    extra_per_streak : `int`
        Extra reward for each streak.
    """
    __slots__ = ('base', 'condition', 'extra_limit', 'extra_per_streak')
    
    base = 0
    extra_per_streak = 0
    extra_limit = 0
    condition = None

    
    def __repr__(self):
        """Returns repr(self)"""
        repr_parts = ['<', type(self).__name__]
        
        # base
        repr_parts.append(' base = ')
        repr_parts.append(repr(self.base))
        
        # extra_per_streak
        repr_parts.append(', extra_per_streak = ')
        repr_parts.append(repr(self.extra_per_streak))
        
        # extra_limit
        repr_parts.append(', extra_limit = ')
        repr_parts.append(repr(self.extra_limit))
        
        # condition
        condition = self.condition
        if (condition is not None):
            repr_parts.append(', condition = ')
            repr_parts.append(repr(condition))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
