__all__ = ('Quest',)

from scarletio import RichAttributeErrorBaseType

from ..item_core import produce_item_id_with_name

from .helpers import get_quest_template_nullable


class Quest(RichAttributeErrorBaseType):
    """
    Represents a quest.
    
    Attributes
    ----------
    requirements : ``None | tuple<QuestRequirementInstantiable>``
        Requirements.
    
    rewards : ``None | tuple<QuestRewardInstantiable>``
        Rewards.
    
    template_id : `int`
        The identifier of the quest's template.
    """
    __slots__ = ('requirements', 'rewards', 'template_id')
    
    def __new__(
        cls,
        quest_template_id,
        requirements,
        rewards,
    ):
        """
        Creates a new quest with the given parameters.
        
        Parameters
        ----------
        quest_template_id : `int`
            The identifier of the quest's template.
        
        requirements : ``None | tuple<QuestRequirementInstantiable>``
            Requirements.
        
        rewards : ``None | tuple<QuestRewardInstantiable>``
            Rewards.
        """
        self = object.__new__(cls)
        self.requirements = requirements
        self.rewards = rewards
        self.template_id = quest_template_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # template_id
        repr_parts.append(' template_id = ')
        template_id = self.template_id
        repr_parts.append(repr(template_id))
        
        quest_template = get_quest_template_nullable(template_id)
        
        # quest_template / level
        if (quest_template is None):
            level = -1
        else:
            level = quest_template.level
        
        repr_parts.append(', level = ')
        repr_parts.append(repr(level))
        
        # quest_template / requester_id
        if (quest_template is None):
            requester_id = -1
        else:
            requester_id = quest_template.requester_id
        
        repr_parts.append(', requester = ')
        repr_parts.extend(produce_item_id_with_name(requester_id))
        
        # requirements
        requirements = self.requirements
        if (requirements is not None):
            repr_parts.append(', requirements = ')
            repr_parts.append(repr(requirements))
        
        # rewards
        rewards = self.rewards
        if (rewards is not None):
            repr_parts.append(', rewards = ')
            repr_parts.append(repr(rewards))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
