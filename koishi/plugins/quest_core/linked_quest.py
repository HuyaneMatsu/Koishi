__all__ = ('LinkedQuest',)

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from hata import DATETIME_FORMAT_CODE
from scarletio import RichAttributeErrorBaseType

from ..item_core import get_item_name

from .amount_types import get_amount_type_name
from .linked_quest_completion_states import LINKED_QUEST_COMPLETION_STATE_ACTIVE
from .quest_types import get_quest_type_name
from .utils import get_quest_template


class LinkedQuest(RichAttributeErrorBaseType):
    """
    Represents a quest.
    
    Attributes
    ----------
    amount_required : `int`
        The requested amount of items to submit.
    
    amount_submitted : `int`
        The remaining amount to submit.
    
    batch_id : `int`
        The identifier of the match. Used for deduplication.
    
    completion_count : `int`
        How much times this quest was completed.
    
    completion_state : `int`
        How much times this quest was completed.
    
    entry_id : `int`
        The database entry identifier of the quest.
    
    expires_at : `DateTime`
        When the quest expires.
    
    guild_id : `int`
        The source guild's identifier.
    
    reward_balance : `int`
        The amount of balance to be rewarded.
    
    reward_credibility : `int`
        The amount of credibility to be rewarded.
    
    taken_at : `DateTime`
        When the quest was taken at.
    
    template_id : `int`
        The identifier of the quest's template.
    
    user_id : `int`
        The owner user identifier.
    """
    __slots__ = (
        'amount_required', 'amount_submitted', 'batch_id', 'completion_count', 'completion_state', 'entry_id',
        'expires_at', 'guild_id', 'reward_balance', 'reward_credibility', 'taken_at', 'template_id', 'user_id'
    )
    
    def __new__(cls, user_id, guild_id, batch_id, quest):
        """
        Creates a new linked quest from the given fields.
        
        Parameters
        ----------
        user_id : `int`
            User identifier to bind to.
        
        guild_id : `int`
            The respective guild's identifier.
        
        batch_id : `int`
            The identifier of the batch. Used for deduplication.
        
        quest : ``Quest``
            Quest to link.
        """
        now = DateTime.now(TimeZone.utc)
        
        self = object.__new__(cls)
        self.amount_submitted = 0
        self.amount_required = quest.amount
        self.batch_id = batch_id
        self.completion_count = 0
        self.completion_state = LINKED_QUEST_COMPLETION_STATE_ACTIVE
        self.entry_id = 0
        self.expires_at = now + TimeDelta(seconds = quest.duration)
        self.guild_id = guild_id
        self.reward_balance = quest.reward_balance
        self.reward_credibility = quest.reward_credibility
        self.taken_at = now
        self.template_id = quest.template_id
        self.user_id = user_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # user_id
        repr_parts.append(', guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # entry_id
        entry_id = self.entry_id
        if (entry_id != 0):
            repr_parts.append(', entry_id = ')
            repr_parts.append(repr(entry_id))
        
        # template_id
        repr_parts.append(' template_id = ')
        template_id = self.template_id
        repr_parts.append(repr(template_id))
        
        quest_template = get_quest_template(template_id)
        
        # amount_required
        repr_parts.append(', amount_required = ')
        repr_parts.append(repr(self.amount_required))
        
        # amount_submitted
        repr_parts.append(', amount_submitted = ')
        repr_parts.append(repr(self.amount_submitted))
        
        # completion_count
        repr_parts.append(', completion_count = ')
        repr_parts.append(repr(self.completion_count))
        
        # completion_state
        repr_parts.append(', completion_state = ')
        repr_parts.append(repr(self.completion_state))
        
        # quest_template / amount_type
        if (quest_template is None):
            amount_type = -1
        else:
            amount_type = quest_template.amount_type
        
        repr_parts.append(', amount_type = ')
        repr_parts.append(get_amount_type_name(amount_type))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(amount_type))
        
        # taken_at
        repr_parts.append(', taken_at = ')
        repr_parts.append(format(self.taken_at, DATETIME_FORMAT_CODE))
        
        # expires_at
        repr_parts.append(', expires_at = ')
        repr_parts.append(format(self.expires_at, DATETIME_FORMAT_CODE))
        
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
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates a linked quest from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.amount_required = entry['amount_required']
        self.amount_submitted = entry['amount_submitted']
        self.completion_count = entry['completion_count']
        self.completion_state = entry['completion_state']
        self.batch_id = entry['batch_id']
        self.entry_id = entry['id']
        self.expires_at = entry['expires_at'].replace(tzinfo = TimeZone.utc)
        self.guild_id = entry['guild_id']
        self.reward_balance = entry['reward_balance']
        self.reward_credibility = entry['reward_credibility']
        self.taken_at = entry['taken_at'].replace(tzinfo = TimeZone.utc)
        self.template_id = entry['template_id']
        self.user_id = entry['user_id']
        return self
    
    
    def reset(self):
        """
        Resets the linked quest as it would be started just now.
        """
        now = DateTime.now(TimeZone.utc)
        duration = self.expires_at - self.taken_at
        
        self.amount_submitted = 0
        self.completion_state = LINKED_QUEST_COMPLETION_STATE_ACTIVE
        self.expires_at = now + duration
        self.taken_at = now
