__all__ = ('QuestTemplate', 'quest_template_create')

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


def quest_template_create(
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
    Creates a new quest template with the given parameters.
    
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
    
    Returns
    -------
    quest_template : ``QuestTemplate``
    """
    linked_quest = object.__new__(QuestTemplate)
    linked_quest.chance_in = chance_in
    linked_quest.chance_out = chance_out
    linked_quest.description = description
    linked_quest.id = quest_template_id
    linked_quest.level = level
    linked_quest.mutually_exclusive_with_ids = mutually_exclusive_with_ids
    linked_quest.repeat_count = repeat_count
    linked_quest.requester_id = requester_id
    linked_quest.requirements = requirements
    linked_quest.rewards = rewards
    return linked_quest
