__all__ = (
    'QUEST_REQUIREMENT_SERIALISATION_RESOLUTION', 'QUEST_REWARD_SERIALISATION_RESOLUTION',
    'quest_serialisable_deserialise', 'quest_serialisable_serialise'
)

from .quest_requirement_serialisables import (
    QuestRequirementSerialisableBase, QuestRequirementSerialisableDuration, QuestRequirementSerialisableExpiration,
    QuestRequirementSerialisableItemCategory, QuestRequirementSerialisableItemExact,
    QuestRequirementSerialisableItemGroup
)
from .quest_reward_serialisables import (
    QuestRewardSerialisableBalance, QuestRewardSerialisableBase, QuestRewardSerialisableCredibility,
    QuestRewardSerialisableItemExact
)


QUEST_REWARD_SERIALISATION_RESOLUTION = {
    reward_type.TYPE : reward_type for reward_type in (
        QuestRewardSerialisableBalance,
        QuestRewardSerialisableBase,
        QuestRewardSerialisableCredibility,
        QuestRewardSerialisableItemExact,
    )
}

QUEST_REQUIREMENT_SERIALISATION_RESOLUTION = {
    reward_type.TYPE : reward_type for reward_type in (
        QuestRequirementSerialisableBase,
        QuestRequirementSerialisableDuration,
        QuestRequirementSerialisableExpiration,
        QuestRequirementSerialisableItemCategory,
        QuestRequirementSerialisableItemExact,
        QuestRequirementSerialisableItemGroup,
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
        parts.append(serialisable.TYPE.to_bytes(1, 'little'))
        parts.extend(serialisable.serialise())
    
    return b''.join(parts)


def quest_serialisable_deserialise(resolution, data):
    """
    Deserialises the given serialisable quest sub-types.
    
    Parameters
    ----------
    resolution : ``dict<int, type<QuestSubTypeSerialisable>>``
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
            serialisable_type = resolution[serialisable_type_identifier]
        except KeyError:
            success = False
            break
        
        serialisable_and_end_index = serialisable_type.deserialise(data, index)
        if (serialisable_and_end_index is None):
            success = False
            break
        
        serialisable, index = serialisable_and_end_index
        serialisable_listing.append(serialisable)
        continue
    
    if not serialisable_listing:
        serialisable_listing = None
    
    return success, tuple(serialisable_listing)
