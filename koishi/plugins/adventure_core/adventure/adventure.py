__all__ = ('Adventure',)


from datetime import datetime as DateTime, timezone as TimeZone
from random import random
from math import floor

from scarletio import RichAttributeErrorBaseType

from .adventure_states import ADVENTURE_STATE_DEPARTING


class Adventure(RichAttributeErrorBaseType):
    """
    Represents an adventure.
    
    Attributes
    ----------
    action_count : `int`
        How much actions does the adventure has. Used for seed shifting.
    
    auto_cancellation_id : `int`
        Flags determining how the adventure should be auto cancelled if necessary.
    
    created_at : ``DateTime``
        When the action was created at.
    
    energy_exhausted : `int`
        The amount of energy exhausted in the adventure.
    
    energy_initial : `int`
        The user's starting energy.
    
    entry_id : `int`
        The adventure's identifier in the database.
    
    handle : ``None | TimerHandle``
        Call-back handle. Used while the adventure is active.
    
    health_exhausted : `int`
        The amount of health exhausted.
    
    health_initial : `int`
        The user's starting health.
    
    initial_duration : `int`
        The duration with what the user initialized the adventure with.
    
    location_id : `int`
        The location's identifier.
    
    return_id : `int`
        Return logic identifier.
    
    seed : `int`
        Initial seeding for the adventure allowing it to be regenerated.
    
    state : `int`
        The state of the adventure.
    
    target_id : `int`
        Target actions identifier.
    
    updated_at : `DateTime`
        When the adventure was last updated.
    
    user_id : `int`
        The owner user's identifier.
    """
    __slots__ = (
        '__weakref__', 'action_count', 'auto_cancellation_id', 'created_at', 'energy_exhausted', 'energy_initial',
        'entry_id', 'handle', 'health_exhausted', 'health_initial', 'initial_duration', 'location_id', 'return_id',
        'seed', 'state', 'target_id', 'updated_at', 'user_id', 
    )
    
    def __new__(
        cls,
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        
        initial_duration,
        health_initial,
        energy_initial,
    ):
        """
        Creates a new adventure.
        
        Parameters
        ----------
        user_id : `int`
            The owner user's identifier.
        
        location_id : `int`
            The location's identifier.
        
        target_id : `int`
            Target actions identifier.
        
        return_id : `int`
            Return logic identifier.
        
        auto_cancellation_id : `int`
            Auto cancellation logic identifier.
        
        initial_duration : `int`
            The duration with what the user initialized the adventure with.
        
        health_initial : `int`
            The user's starting health.
        
        energy_initial : `int`
            The user's starting energy.
        """
        self = object.__new__(cls)
        self.entry_id = 0
        self.user_id = user_id
        self.handle = None
        
        self.location_id = location_id
        self.target_id = target_id
        self.return_id = return_id
        self.auto_cancellation_id = auto_cancellation_id
        self.state = ADVENTURE_STATE_DEPARTING
        
        self.initial_duration = initial_duration
        self.created_at = self.updated_at = DateTime.now(tz = TimeZone.utc)
        self.action_count = 0
        self.seed = floor(random() * (1 << 63))
        
        self.health_initial = health_initial
        self.health_exhausted = 0
        
        self.energy_initial = energy_initial
        self.energy_exhausted = 0
        
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # entry_id
        repr_parts.append(', entry_id = ')
        repr_parts.append(repr(self.entry_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an adventure from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.entry_id = entry['id']
        self.user_id = entry['user_id']
        self.handle = None
        
        self.location_id = entry['location_id']
        self.target_id = entry['target_id']
        self.return_id = entry['return_id']
        self.auto_cancellation_id = entry['auto_cancellation_id']
        self.state = entry['state']
        
        self.initial_duration = entry['initial_duration']
        self.created_at = entry['created_at'].replace(tzinfo = TimeZone.utc)
        self.updated_at = entry['updated_at'].replace(tzinfo = TimeZone.utc)
        self.action_count = entry['action_count']
        self.seed = entry['seed']
        
        self.health_initial = entry['health_initial']
        self.health_exhausted = entry['health_exhausted']
        
        self.energy_initial = entry['energy_initial']
        self.energy_exhausted = entry['energy_exhausted']
        
        return self
