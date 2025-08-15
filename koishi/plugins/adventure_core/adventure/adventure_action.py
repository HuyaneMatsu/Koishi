__all__ = ('AdventureAction',)

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import RichAttributeErrorBaseType


class AdventureAction(RichAttributeErrorBaseType):
    """
    Represents an action of an adventure.
    
    Attributes
    ----------
    action_id : `int`
        The represented action's identifier.
    
    adventure_entry_id : `int`
        The owner adventure's identifier.
    
    battle_data : `None | bytes`
        Metadata about the battle of the action.
    
    created_at : ``DateTime``
        When the action was created.
    
    entry_id : `int`
        The adventure action's identifier in the database.
    
    loot_data : `None | bytes`
        Loot metadata of the action.
    
    energy_exhausted : `int`
        The amount of energy used while completing the action.
    
    health_exhausted : `int`
        The amount of health used while completing the action.
    """
    __slots__ = (
        'action_id', 'adventure_entry_id', 'battle_data', 'created_at', 'entry_id', 'loot_data', 'energy_exhausted',
        'health_exhausted',
    )
    
    def __new__(
        cls,
        adventure_entry_id,
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
        adventure_entry_id : `int`
            The owner adventure's identifier.
        
        action_id : `int`
            The represented action's identifier.
        
        created_at : ``None | DateTime``
            When the action was created.
        
        battle_data : `None | bytes`
            Metadata data.
        
        loot_data : `None | bytes`
            Loot data.
        
        health_exhausted : `int`
            The amount of health used while completing the action.
        
        energy_exhausted : `int`
            The amount of energy used while completing the action.
        """
        if action_id is None:
            action_id = DateTime.now(tz = TimeZone.utc)
        
        self = object.__new__(cls)
        self.action_id = action_id
        self.adventure_entry_id = adventure_entry_id
        self.battle_data = battle_data
        self.created_at = created_at
        self.entry_id = 0
        self.loot_data = loot_data
        self.health_exhausted = health_exhausted
        self.energy_exhausted = energy_exhausted
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # adventure
        repr_parts.append(' adventure_entry_id = ')
        repr_parts.append(repr(self.adventure_entry_id))
        
        # action_id
        repr_parts.append(', action_id = ')
        repr_parts.append(repr(self.action_id))
        
        # entry_id
        repr_parts.append(', entry_id = ')
        repr_parts.append(repr(self.entry_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an adventure action from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.action_id = entry['action_id']
        self.adventure_entry_id = entry['adventure_entry_id']
        self.battle_data = entry['battle_data']
        self.created_at = entry['created_at'].replace(tzinfo = TimeZone.utc)
        self.entry_id = entry['id']
        self.loot_data = entry['loot_data']
        self.health_exhausted = entry['health_exhausted']
        self.energy_exhausted = entry['energy_exhausted']
        return self
