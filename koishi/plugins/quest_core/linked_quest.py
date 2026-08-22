__all__ = ('LinkedQuest', 'linked_quest_create', 'linked_quest_create_from_entry')

from scarletio import RichAttributeErrorBaseType

from ...bot_utils.time import get_unix_time_nano_seconds

from ..item_core import produce_item_id_with_name

from .flags import QUEST_FLAG_INITIALISATION_FAILURE
from .helpers import get_quest_template_nullable
from .linked_quest_completion_states import LINKED_QUEST_COMPLETION_STATE_ACTIVE
from .serialisation import (
    QUEST_REQUIREMENT_SERIALISATION_RESOLUTION, QUEST_REWARD_SERIALISATION_RESOLUTION, quest_serialisable_deserialise
)


class LinkedQuest(RichAttributeErrorBaseType):
    """
    Represents a quest.
    
    Attributes
    ----------
    batch_id : `int`
        The identifier of the match. Used for deduplication.
    
    completion_count : `int`
        How much times this quest was completed.
    
    completion_state : `int`
        How much times this quest was completed.
    
    created_at : `int`
        When the linked quest was created.
    
    entry_id : `int`
        The database entry identifier of the quest.
    
    guild_id : `int`
        The source guild's identifier.
    
    requirements : ``None | tuple<QuestRequirementSerialisable>``
        Quest requirements.
    
    rewards : ``None | tuple<QuestRewardSerialisable>``
        Quest rewards.
    
    template_id : `int`
        The identifier of the quest's template.
    
    user_id : `int`
        The owner user identifier.
    """
    __slots__ = (
        'batch_id', 'completion_count', 'completion_state', 'created_at', 'entry_id', 'flags', 'guild_id',
        'requirements', 'rewards', 'template_id', 'user_id'
    )
    
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
        
        # completion_count
        repr_parts.append(', completion_count = ')
        repr_parts.append(repr(self.completion_count))
        
        # completion_state
        repr_parts.append(', completion_state = ')
        repr_parts.append(repr(self.completion_state))
        
        
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
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def linked_quest_create(user_id, guild_id, batch_id, template_id, requirements, rewards):
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
    
    template_id : `int`
        The identifier of the quest's template.
    
    requirements : ``None | tuple<QuestRequirementSerialisable>``
        Quest requirements.
    
    rewards : ``None | tuple<QuestRewardSerialisable>``
        Quest rewards.
    
    Returns
    -------
    linked_quest : ``LinkedQuest``
    """
    linked_quest = object.__new__(LinkedQuest)
    linked_quest.batch_id = batch_id
    linked_quest.completion_count = 0
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_ACTIVE
    linked_quest.created_at = get_unix_time_nano_seconds()
    linked_quest.entry_id = 0
    linked_quest.guild_id = guild_id
    linked_quest.flags = 0
    linked_quest.requirements = requirements
    linked_quest.rewards = rewards
    linked_quest.template_id = template_id
    linked_quest.user_id = user_id
    return linked_quest


def linked_quest_create_from_entry(entry):
    """
    Creates a linked quest from the given entry.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy`
        The entry to create the instance from.
    
    Returns
    -------
    linked_quest : ``LinkedQuest``
    """
    flags = 0
    
    success_0, requirements = quest_serialisable_deserialise(
        QUEST_REQUIREMENT_SERIALISATION_RESOLUTION, entry['requirements']
    )
    success_1, rewards = quest_serialisable_deserialise(
        QUEST_REWARD_SERIALISATION_RESOLUTION, entry['rewards']
    )
    if not (success_0 and success_1):
        flags |= QUEST_FLAG_INITIALISATION_FAILURE
    
    linked_quest = object.__new__(LinkedQuest)
    linked_quest.completion_count = entry['completion_count']
    linked_quest.completion_state = entry['completion_state']
    linked_quest.created_at = entry['created_at']
    linked_quest.batch_id = entry['batch_id']
    linked_quest.entry_id = entry['id']
    linked_quest.flags = flags
    linked_quest.guild_id = entry['guild_id']
    linked_quest.template_id = entry['template_id']
    linked_quest.user_id = entry['user_id']
    linked_quest.requirements = requirements
    linked_quest.rewards = rewards
    
    return linked_quest
