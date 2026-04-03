__all__ = ('QuestTemplate',)

from scarletio import RichAttributeErrorBaseType

from ..item_core import get_item_name


class QuestTemplate(RichAttributeErrorBaseType):
    """
    Represents a quest.
    
    Attributes
    ----------
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    description : `None | str`
        Flavour text.
    
    id : `int`
        The quest template's identifier.
    
    level : `int`
        The quest's level.
    
    mutually_exclusive_with_ids : `None | tuple<int>`
        Other quest template's identifiers
    
    repeat_count : `int`
        The amount of times this quest can be repeated.
    
    requester_id : `int`
        Who requested the action.
    
    requirements : ``None | tuple<QuestRequirementGeneratorBase>``
        Quest requirements.
    
    rewards : ``None | tuple<QuestRewardGeneratorBase>``
        Quest rewards.
    """
    __slots__ = (
        'chance_in', 'chance_out', 'description', 'id', 'level', 'mutually_exclusive_with_ids',
        'repeat_count', 'requester_id', 'requirements', 'rewards',
    )
    
    def __new__(
        cls,
        quest_template_id,
        mutually_exclusive_with_ids,
        chance_in,
        chance_out,
        description,
        level,
        repeat_count,
        requester_id,
        requirements,
        rewards,
    ):
        """
        Creates a new quest with the given parameters.
        
        Parameters
        ----------
        quest_template_id : `int`
            The quest template's identifier.
        
        mutually_exclusive_with_ids : `None | tuple<int>`
            An tuple of quest template identifiers that this one is mutually exclusive with.
        
        chance_in : `int`
            The chance to be chosen in.
        
        chance_out : `int`
            The chance to be chosen out of.
        
        description : `None | str`
            Flavour text.
        
        level : `int`
            The quest's level.
    
        repeat_count : `int`
            The amount of times this quest can be repeated.
        
        requester_id : `int`
            Who requested the action.
        
        requirements : ``None | tuple<QuestRequirementGeneratorBase>``
            Quest requirements.
        
        rewards : ``None | tuple<QuestRewardGeneratorBase>``
            Quest rewards.
        """
        self = object.__new__(cls)
        self.chance_in = chance_in
        self.chance_out = chance_out
        self.description = description
        self.id = quest_template_id
        self.level = level
        self.mutually_exclusive_with_ids = mutually_exclusive_with_ids
        self.repeat_count = repeat_count
        self.requester_id = requester_id
        self.requirements = requirements
        self.rewards = rewards
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # mutually_exclusive_with_ids
        repr_parts.append(', mutually_exclusive_with_ids = ')
        repr_parts.append(repr(self.mutually_exclusive_with_ids))
        
        # chance_in
        repr_parts.append(', chance_in = ')
        repr_parts.append(repr(self.chance_in))
        
        # chance_out
        repr_parts.append(', chance_out = ')
        repr_parts.append(repr(self.chance_out))
        
        # description
        repr_parts.append(', description = ')
        repr_parts.append(repr(self.description))
        
        # level
        repr_parts.append(', level = ')
        repr_parts.append(repr(self.level))
        
        # repeat_count
        repr_parts.append(', repeat_count = ')
        repr_parts.append(repr(self.repeat_count))
        
        # requester_id
        repr_parts.append(', requester = ')
        requester_id = self.requester_id
        repr_parts.append(get_item_name(requester_id))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(requester_id))
        
        # requirements
        repr_parts.append(', requirements = ')
        repr_parts.append(repr(self.requirements))
        
        # rewards
        repr_parts.append(', rewards = ')
        repr_parts.append(repr(self.rewards))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
