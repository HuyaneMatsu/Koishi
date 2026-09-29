__all__ = (
    'QUEST_REQUIREMENT_SERIALISATION_RESOLUTION', 'QUEST_REWARD_SERIALISATION_RESOLUTION',
    'quest_serialisable_deserialise', 'quest_serialisable_serialise'
)

from .quest_requirement_serialisables import (
    QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_DURATION, QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_EXPIRATION,
    QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_CATEGORY, QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_EXACT,
    QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_GROUP
)
from .quest_reward_serialisables import (
    QUEST_REWARD_SERIALISABLE_BEHAVIOUR_BALANCE, QUEST_REWARD_SERIALISABLE_BEHAVIOUR_CREDIBILITY,
    QUEST_REWARD_SERIALISABLE_BEHAVIOUR_ITEM_EXACT
)


QUEST_REQUIREMENT_SERIALISATION_RESOLUTION = {
    behaviour.type : behaviour for behaviour in (
        QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_DURATION,
        QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_EXPIRATION,
        QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_CATEGORY,
        QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_EXACT,
        QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_GROUP,
    )
}


QUEST_REWARD_SERIALISATION_RESOLUTION = {
    behaviour.type : behaviour for behaviour in (
        QUEST_REWARD_SERIALISABLE_BEHAVIOUR_BALANCE,
        QUEST_REWARD_SERIALISABLE_BEHAVIOUR_CREDIBILITY,
        QUEST_REWARD_SERIALISABLE_BEHAVIOUR_ITEM_EXACT,
    )
}


def quest_serialisable_serialise(serialisable_listing):
    """
    Serialises the given serialisable quest sub-types.
    
    Parameters
    ----------
    serialisable_listing : ``None | tuple<QuestSubTypeSerialisable>``
        To serialise.
    
    Returns
    -------
    data : `None | bytes`
    """
    if (serialisable_listing is None) or (not serialisable_listing):
        return None
    
    parts = []
    
    for serialisable in serialisable_listing:
        behaviour = serialisable.behaviour
        parts.append(behaviour.type.to_bytes(1, 'little'))
        parts.extend(behaviour.serialise(serialisable.configuration))
    
    return b''.join(parts)


def quest_serialisable_deserialise(resolution, data):
    """
    Deserialises the given serialisable quest sub-types.
    
    Parameters
    ----------
    resolution : ``dict<int, QuestSubTypeSerialisableBehaviour>``
        Type identifier to type mapping.
    
    data : `None | bytes`
        Data to deserialise.
    
    Returns
    -------
    success_and_serialisable_listing : ``(bool, None | tuple<QuestSubTypeSerialisable>)``
    """
    if (data is None):
        return True, None
    
    index = 0
    data_length = len(data)
    
    success = True
    serialisable_listing = []
    
    while index < data_length:
        serialisable_type_identifier = data[index]
        index += 1
        
        try:
            behaviour = resolution[serialisable_type_identifier]
        except KeyError:
            success = False
            break
        
        serialisable_and_end_index = behaviour.deserialise(data, index)
        if (serialisable_and_end_index is None):
            success = False
            break
        
        serialisable, index = serialisable_and_end_index
        serialisable_listing.append(serialisable)
        continue
    
    if not serialisable_listing:
        serialisable_listing = None
    
    return success, tuple(serialisable_listing)
