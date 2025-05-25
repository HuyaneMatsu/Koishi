__all__ = ('Quest',)

from scarletio import RichAttributeErrorBaseType

from ..item_core import get_item_name

from .amount_types import get_amount_type_name
from .quest_types import get_quest_type_name
from .utils import get_quest_template


class Quest(RichAttributeErrorBaseType):
    """
    Represents a quest.
    
    Attributes
    ----------
    amount : `int`
        The requested amount of items to submit.
    
    duration : `int`
        The duration of the quest to complete.
    
    reward_balance : `int`
        The amount of balance to be rewarded.
    
    reward_credibility : `int`
        The amount of credibility to be rewarded.
    
    template_id : `int`
        The identifier of the quest's template.
    """
    __slots__ = ('amount', 'duration', 'reward_balance', 'reward_credibility', 'template_id')
    
    def __new__(
        cls,
        quest_template_id,
        amount,
        duration,
        reward_credibility,
        reward_balance,
    ):
        """
        Creates a new quest with the given parameters.
        
        Parameters
        ----------
        quest_template_id : `int`
            The identifier of the quest's template.
        
        amount : `int`
            The requested amount of items to submit.
        
        duration : `int`
            The duration of the quest to complete.
        
        reward_credibility : `int`
            The amount of credibility to be rewarded.
        
        reward_balance : `int`
            The amount of balance to be rewarded.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.duration = duration
        self.reward_balance = reward_balance
        self.reward_credibility = reward_credibility
        self.template_id = quest_template_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # template_id
        repr_parts.append(' template_id = ')
        template_id = self.template_id
        repr_parts.append(repr(template_id))
        
        quest_template = get_quest_template(template_id)
        
        # amount
        repr_parts.append(', amount = ')
        repr_parts.append(repr(self.amount))
        
        # quest_template / amount_type
        if (quest_template is None):
            amount_type = -1
        else:
            amount_type = quest_template.amount_type
        
        repr_parts.append(', amount_type = ')
        repr_parts.append(get_amount_type_name(amount_type))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(amount_type))
        
        # duration
        repr_parts.append(', duration = ')
        repr_parts.append(repr(self.duration))
        
        # quest_template / item_id
        if (quest_template is None):
            item_id = -1
        else:
            item_id = quest_template.item_id
        
        repr_parts.append(', item = ')
        repr_parts.append(get_item_name(item_id))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(item_id))
        
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
        repr_parts.append(get_item_name(requester_id))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(requester_id))
        
        # reward_balance
        repr_parts.append(', reward_balance = ')
        repr_parts.append(repr(self.reward_balance))
        
        # reward_credibility
        repr_parts.append(', reward_credibility = ')
        repr_parts.append(repr(self.reward_credibility))
        
        # quest_template / type
        if (quest_template is None):
            quest_type = -1
        else:
            quest_type = quest_template.type
        
        repr_parts.append(', type = ')
        repr_parts.append(get_quest_type_name(quest_type))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(quest_type))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
