__all__ = ('QuestTemplate',)

from scarletio import RichAttributeErrorBaseType

from ..item_core import get_item_name

from .amount_types import get_amount_type_name
from .quest_types import get_quest_type_name


class QuestTemplate(RichAttributeErrorBaseType):
    """
    Represents a quest.
    
    Attributes
    ----------
    amount_base : `int`
        The requested amount of items to submit.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_type : `int`
        The amount's type.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    description : `None | str`
        Flavour text.
    
    duration_base : `int`
        The duration of the quest to complete.
    
    duration_require_multiple_of : `int`
        Value to require the duration to be multiple of.
    
    duration_variance_percentage_lower_threshold : `int`
        Lower threshold of for duration variance in percentage.
    
    duration_variance_percentage_upper_threshold : `int`
        Upper threshold of for duration variance in percentage.
    
    id : `int`
        The quest template's identifier.
    
    item_id : `int`
        The item identifier to deliver.
    
    level : `int`
        The quest's level.
    
    requester_id : `int`
        Who requested the action.
    
    reward_balance_base : `int`
        The amount of balance to be rewarded.
    
    reward_balance_require_multiple_of : `int`
        Value to require the reward balance to be multiple of.
    
    reward_balance_variance_percentage_lower_threshold : `int`
        Lower threshold of for reward balance variance in percentage.
    
    reward_balance_variance_percentage_upper_threshold : `int`
        Upper threshold of for reward balance variance in percentage.
    
    reward_credibility : `int`
        The amount of credibility to be rewarded.
    
    type : `int`
        The type of the quest.
    """
    __slots__ = (
        'amount_base', 'amount_require_multiple_of', 'amount_type', 'amount_variance_percentage_lower_threshold',
        'amount_variance_percentage_upper_threshold', 'description', 'duration_base', 'duration_require_multiple_of',
        'duration_variance_percentage_lower_threshold', 'duration_variance_percentage_upper_threshold', 'id',
        'item_id', 'level', 'requester_id', 'reward_balance_base', 'reward_balance_require_multiple_of',
        'reward_balance_variance_percentage_lower_threshold', 'reward_balance_variance_percentage_upper_threshold',
        'reward_credibility', 'type'
    )
    
    def __new__(
        cls,
        quest_template_id,
        description,
        quest_type,
        level,
        item_id,
        requester_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
        amount_type,
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
        reward_credibility,
        reward_balance_base,
        reward_balance_require_multiple_of,
        reward_balance_variance_percentage_lower_threshold,
        reward_balance_variance_percentage_upper_threshold,
    ):
        """
        Creates a new quest with the given parameters.
        
        Parameters
        ----------
        quest_template_id : `int`
            The quest template's identifier.
        
        description : `None | str`
            Flavour text.
        
        quest_type : `int`
            The type of the quest.
        
        level : `int`
            The quest's level.
        
        item_id : `int`
            The item identifier to deliver.
        
        requester_id : `int`
            Who requested the action.
        
        amount_base : `int`
            The requested amount of items to submit.
        
        amount_require_multiple_of : `int`
            Value to require the amount to be multiple of.
        
        amount_variance_percentage_lower_threshold : `int`
            Lower threshold of for amount variance in percentage.
        
        amount_variance_percentage_upper_threshold : `int`
            Upper threshold of for amount variance in percentage.
        
        amount_type : `int`
            The amount's type.
        
        duration_base : `int`
            The duration of the quest to complete.
        
        duration_require_multiple_of : `int`
            Value to require the duration to be multiple of.
        
        duration_variance_percentage_lower_threshold : `int`
            Lower threshold of for duration variance in percentage.
        
        duration_variance_percentage_upper_threshold : `int`
            Upper threshold of for duration variance in percentage.
        
        reward_balance_base : `int`
            The amount of balance to be rewarded.
        
        reward_balance_require_multiple_of : `int`
            Value to require the reward balance to be multiple of.
        
        reward_balance_variance_percentage_lower_threshold : `int`
            Lower threshold of for reward balance variance in percentage.
        
        reward_balance_variance_percentage_upper_threshold : `int`
            Upper threshold of for reward balance variance in percentage.
        
        reward_credibility : `int`
            The amount of credibility to be rewarded.
        """
        self = object.__new__(cls)
        self.amount_base = amount_base
        self.amount_require_multiple_of = amount_require_multiple_of
        self.amount_type = amount_type
        self.amount_variance_percentage_lower_threshold = amount_variance_percentage_lower_threshold
        self.amount_variance_percentage_upper_threshold = amount_variance_percentage_upper_threshold
        self.description = description
        self.duration_base = duration_base
        self.duration_require_multiple_of = duration_require_multiple_of
        self.duration_variance_percentage_lower_threshold = duration_variance_percentage_lower_threshold
        self.duration_variance_percentage_upper_threshold = duration_variance_percentage_upper_threshold
        self.id = quest_template_id
        self.item_id = item_id
        self.level = level
        self.requester_id = requester_id
        self.reward_balance_base = reward_balance_base
        self.reward_balance_require_multiple_of = reward_balance_require_multiple_of
        self.reward_balance_variance_percentage_lower_threshold = reward_balance_variance_percentage_lower_threshold
        self.reward_balance_variance_percentage_upper_threshold = reward_balance_variance_percentage_upper_threshold
        self.reward_credibility = reward_credibility
        self.type = quest_type
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # amount_base
        repr_parts.append(', amount_base = ')
        repr_parts.append(repr(self.amount_base))
        
        # amount_require_multiple_of
        repr_parts.append(', amount_require_multiple_of = ')
        repr_parts.append(repr(self.amount_require_multiple_of))
        
        # amount_type
        repr_parts.append(', amount_type = ')
        amount_type = self.amount_type
        repr_parts.append(get_amount_type_name(amount_type))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(amount_type))
        
        # amount_variance_percentage_lower_threshold
        repr_parts.append(', amount_variance_percentage_lower_threshold = ')
        repr_parts.append(repr(self.amount_variance_percentage_lower_threshold))
        
        # amount_variance_percentage_upper_threshold
        repr_parts.append(', amount_variance_percentage_upper_threshold = ')
        repr_parts.append(repr(self.amount_variance_percentage_upper_threshold))
        
        # description
        repr_parts.append(', description = ')
        repr_parts.append(repr(self.description))
        
        # duration_base
        repr_parts.append(', duration_base = ')
        repr_parts.append(repr(self.duration_base))
        
        # duration_require_multiple_of
        repr_parts.append(', duration_require_multiple_of = ')
        repr_parts.append(repr(self.duration_require_multiple_of))
        
        # duration_variance_percentage_lower_threshold
        repr_parts.append(', duration_variance_percentage_lower_threshold = ')
        repr_parts.append(repr(self.duration_variance_percentage_lower_threshold))
        
        # duration_variance_percentage_upper_threshold
        repr_parts.append(', duration_variance_percentage_upper_threshold = ')
        repr_parts.append(repr(self.duration_variance_percentage_upper_threshold))
        
        # item_id
        repr_parts.append(', item = ')
        item_id = self.item_id
        repr_parts.append(get_item_name(item_id))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(item_id))
        
        # level
        repr_parts.append(', level = ')
        repr_parts.append(repr(self.level))
        
        # requester_id
        repr_parts.append(', requester = ')
        requester_id = self.requester_id
        repr_parts.append(get_item_name(requester_id))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(requester_id))
        
        # reward_balance_base
        repr_parts.append(', reward_balance_base = ')
        repr_parts.append(repr(self.reward_balance_base))
        
        # reward_balance_require_multiple_of
        repr_parts.append(', reward_balance_require_multiple_of = ')
        repr_parts.append(repr(self.reward_balance_require_multiple_of))
        
        # reward_balance_variance_percentage_lower_threshold
        repr_parts.append(', reward_balance_variance_percentage_lower_threshold = ')
        repr_parts.append(repr(self.reward_balance_variance_percentage_lower_threshold))
        
        # reward_balance_variance_percentage_upper_threshold
        repr_parts.append(', reward_balance_variance_percentage_upper_threshold = ')
        repr_parts.append(repr(self.reward_balance_variance_percentage_upper_threshold))
        
        # reward_credibility
        repr_parts.append(', reward_credibility = ')
        repr_parts.append(repr(self.reward_credibility))
        
        # type
        repr_parts.append(', type = ')
        quest_type = self.type
        repr_parts.append(get_quest_type_name(quest_type))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(quest_type))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
