__all__ = (
    'AdventureAction', 'adventure_action_create', 'adventure_action_listing_deserialise',
    'adventure_action_listing_serialise',
)

from struct import Struct

from scarletio import RichAttributeErrorBaseType

from ....bot_utils.time import unix_time_seconds_get


ADVENTURE_ACTION_STRUCT = Struct('<IQIIQQ')
ADVENTURE_ACTION_STRUCT_SIZE = ADVENTURE_ACTION_STRUCT.size


class AdventureAction(RichAttributeErrorBaseType):
    """
    Represents an action of an adventure.
    
    Attributes
    ----------
    action_id : `int`
        The represented action's identifier.
    
    battle_data : `None | bytes`
        Metadata about the battle of the action.
    
    created_at : `int`
        When the action was created.
    
    loot_data : `None | bytes`
        Loot metadata of the action.
    
    energy_exhausted : `int`
        The amount of energy used while completing the action.
    
    health_exhausted : `int`
        The amount of health used while completing the action.
    """
    __slots__ = (
        'action_id', 'battle_data', 'created_at', 'loot_data', 'energy_exhausted', 'health_exhausted',
    )
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # action_id
        repr_parts.append(' action_id = ')
        repr_parts.append(repr(self.action_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
def adventure_action_create(
    action_id,
    created_at,
    battle_data,
    loot_data,
    health_exhausted,
    energy_exhausted,
):
    """
    Creates an adventure action from the given fields.
    
    Parameters
    ----------
    action_id : `int`
        The represented action's identifier.
    
    created_at : `int`
        When the action was created.
    
    battle_data : `None | bytes`
        Metadata data.
    
    loot_data : `None | bytes`
        Loot data.
    
    health_exhausted : `int`
        The amount of health used while completing the action.
    
    energy_exhausted : `int`
        The amount of energy used while completing the action.
    
    Returns
    -------
    adventure_action : ``AdventureAction``
    """
    if not created_at:
        created_at = unix_time_seconds_get()
    
    adventure_action = object.__new__(AdventureAction)
    adventure_action.action_id = action_id
    adventure_action.battle_data = battle_data
    adventure_action.created_at = created_at
    adventure_action.loot_data = loot_data
    adventure_action.health_exhausted = health_exhausted
    adventure_action.energy_exhausted = energy_exhausted
    return adventure_action


def adventure_action_listing_serialise(adventure_action_listing):
    """
    Serailises the adventure action listing.
    
    Parameters
    ----------
    adventure_action_listing : ``list<AdventureAction>``
        Adventure actions to serialise.
    
    Returns
    -------
    data : `bytes`
    """
    data_parts = []
    
    for adventure_action in adventure_action_listing:
        battle_data = adventure_action.battle_data
        loot_data = adventure_action.loot_data
        
        data_parts.append(ADVENTURE_ACTION_STRUCT.pack(
            adventure_action.action_id,
            adventure_action.created_at,
            (0 if battle_data is None else len(battle_data)),
            (0 if loot_data is None else len(loot_data)),
            adventure_action.health_exhausted,
            adventure_action.energy_exhausted,
        ))
        
        if (battle_data is not None):
            data_parts.append(battle_data)
        
        if (loot_data is not None):
            data_parts.append(loot_data)
    
    return b''.join(data_parts)


def adventure_action_listing_deserialise(data):
    """
    Deserialises an adventure action listing.
    
    Parameters
    ----------
    data : `bytes`
        Data to deserialise.
    
    Returns
    -------
    adventure_action_listing : ``list<AdventureAction>``
    """
    adventure_action_listing = []
    chunk_start = 0
    data_length = len(data)
    
    while True:
        chunk_end = chunk_start + ADVENTURE_ACTION_STRUCT_SIZE
        (
            action_id,
            created_at,
            battle_data_length,
            loot_data_length,
            health_exhausted,
            energy_exhausted,
        ) = ADVENTURE_ACTION_STRUCT.unpack(data[chunk_start : chunk_end])
        chunk_start = chunk_end
        
        if not battle_data_length:
            battle_data = None
        else:
            chunk_end = chunk_start + battle_data_length
            battle_data = data[chunk_start : chunk_end]
            chunk_start = chunk_end
        
        if not loot_data_length:
            loot_data = None
        else:
            chunk_end = chunk_start + loot_data_length
            loot_data = data[chunk_start : chunk_end]
            chunk_start = chunk_end
        
        adventure_action = object.__new__(AdventureAction)
        adventure_action.action_id = action_id
        adventure_action.battle_data = battle_data
        adventure_action.created_at = created_at
        adventure_action.loot_data = loot_data
        adventure_action.health_exhausted = health_exhausted
        adventure_action.energy_exhausted = energy_exhausted
        
        adventure_action_listing.append(adventure_action)
        
        # If we ar at the end of the data, break out.
        if chunk_start >= data_length:
            break
    
    return adventure_action_listing
