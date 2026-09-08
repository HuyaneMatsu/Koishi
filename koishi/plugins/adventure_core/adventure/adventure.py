__all__ = (
    'Adventure', 'adventure_add_action', 'adventure_collect_modifications', 'adventure_count_actions_for_seeding',
    'adventure_create', 'adventure_create_from_entry', 'adventure_increase_energy_exhausted',
    'adventure_increase_health_exhausted', 'adventure_set_updated_at', 'adventure_set_state'
)

from scarletio import RichAttributeErrorBaseType

from ....bot_utils.time import unix_time_seconds_get

from ...seeding import create_seed

from .adventure_action import adventure_action_listing_deserialise, adventure_action_listing_serialise
from .adventure_states import ADVENTURE_STATE_DEPARTING


ADVENTURE_MODIFICATION_FLAG_STATE = 1 << 0
ADVENTURE_MODIFICATION_FLAG_UPDATED_AT = 1 << 1
ADVENTURE_MODIFICATION_FLAG_ACTION_LISTING = 1 << 2
ADVENTURE_MODIFICATION_FLAG_ENERGY_EXHAUSTED = 1 << 3
ADVENTURE_MODIFICATION_FLAG_HEALTH_EXHAUSTED = 1 << 4


class Adventure(RichAttributeErrorBaseType):
    """
    Represents an adventure.
    
    Attributes
    ----------
    action_listing : ``None | list<AdventureAction>``
        How much actions does the adventure has. Used for seed shifting.
    
    auto_cancellation_id : `int`
        Flags determining how the adventure should be auto cancelled if necessary.
    
    created_at : `int`
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
    
    initial_duration_seconds : `int`
        The duration with what the user initialized the adventure with.
    
    location_id : `int`
        The location's identifier.
    
    modification_flags : `int`
        Bit flags describing which fields were modified.
    
    return_id : `int`
        Return logic identifier.
    
    seed : `int`
        Initial seeding for the adventure allowing it to be regenerated.
    
    state : `int`
        The state of the adventure.
    
    target_id : `int`
        Target actions identifier.
    
    updated_at : `int`
        When the adventure was last updated.
    
    user_id : `int`
        The owner user's identifier.
    """
    __slots__ = (
        '__weakref__', 'action_listing', 'auto_cancellation_id', 'created_at', 'energy_exhausted', 'energy_initial',
        'entry_id', 'handle', 'health_exhausted', 'health_initial', 'initial_duration_seconds', 'location_id',
        'modification_flags', 'return_id', 'seed', 'state', 'target_id', 'updated_at', 'user_id', 
    )
    
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
    

def adventure_create(
    user_id,
    
    location_id,
    target_id,
    return_id,
    auto_cancellation_id,
    
    initial_duration_seconds,
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
    
    initial_duration_seconds : `int`
        The duration with what the user initialized the adventure with.
    
    health_initial : `int`
        The user's starting health.
    
    energy_initial : `int`
        The user's starting energy.
    
    Returns
    -------
    adventure : ``Adventure``
    """
    adventure = object.__new__(Adventure)
    adventure.entry_id = 0
    adventure.user_id = user_id
    adventure.handle = None
    adventure.modification_flags = 0
    
    adventure.location_id = location_id
    adventure.target_id = target_id
    adventure.return_id = return_id
    adventure.auto_cancellation_id = auto_cancellation_id
    adventure.state = ADVENTURE_STATE_DEPARTING
    
    adventure.initial_duration_seconds = initial_duration_seconds
    adventure.created_at = adventure.updated_at = unix_time_seconds_get()
    adventure.action_listing = None
    adventure.seed = create_seed()
    
    adventure.health_initial = health_initial
    adventure.health_exhausted = 0
    
    adventure.energy_initial = energy_initial
    adventure.energy_exhausted = 0
    
    return adventure


def adventure_create_from_entry(entry):
    """
    Creates an adventure from the given entry.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy`
        The entry to create the instance based on.
    
    Returns
    -------
    adventure : ``Adventure``
    """
    action_listing_data = entry['action_listing_data']
    if (action_listing_data is None):
        action_listing = None
    else:
        action_listing = adventure_action_listing_deserialise(action_listing_data)
    
    adventure = object.__new__(Adventure)
    adventure.entry_id = entry['id']
    adventure.user_id = entry['user_id']
    adventure.handle = None
    adventure.modification_flags = 0
    
    adventure.location_id = entry['location_id']
    adventure.target_id = entry['target_id']
    adventure.return_id = entry['return_id']
    adventure.auto_cancellation_id = entry['auto_cancellation_id']
    adventure.state = entry['state']
    
    adventure.initial_duration_seconds = entry['initial_duration_seconds']
    adventure.created_at = entry['created_at']
    adventure.updated_at = entry['updated_at']
    adventure.action_listing = action_listing
    adventure.seed = entry['seed']
    
    adventure.health_initial = entry['health_initial']
    adventure.health_exhausted = entry['health_exhausted']
    
    adventure.energy_initial = entry['energy_initial']
    adventure.energy_exhausted = entry['energy_exhausted']
    
    return adventure


def adventure_set_state(adventure, state):
    """
    Sets the adventure's state.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to modify.
    
    state : `int`
        The new adventure state.
    """
    adventure.state = state
    adventure.modification_flags |= ADVENTURE_MODIFICATION_FLAG_STATE


def adventure_set_updated_at(adventure, updated_at):
    """
    Sets when the adventure was updated at.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to modify.
    
    updated_at : `int`
        The new updated at.
    """
    adventure.updated_at = updated_at
    adventure.modification_flags |= ADVENTURE_MODIFICATION_FLAG_UPDATED_AT


def adventure_add_action(adventure, adventure_action):
    """
    Adds an action to the adventure.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to modify.
    
    adventure_action : ``AdventureAction``
        The action to add.
    """
    action_listing = adventure.action_listing
    if (action_listing is None):
        action_listing = []
        adventure.action_listing = action_listing
    
    action_listing.append(adventure_action)
    adventure.modification_flags |= ADVENTURE_MODIFICATION_FLAG_ACTION_LISTING
    

def adventure_increase_energy_exhausted(adventure, energy_exhausted):
    """
    Increases the energy exhausted by the adventure.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to modify.
    
    energy_exhausted : `int`
        Energy exhaust to add.
    """
    adventure.energy_exhausted += energy_exhausted
    adventure.modification_flags |= ADVENTURE_MODIFICATION_FLAG_ENERGY_EXHAUSTED


def adventure_increase_health_exhausted(adventure, health_exhausted):
    """
    Increases the health exhausted by the adventure.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to modify.
    
    health_exhausted : `int`
        Energy exhaust to add.
    """
    adventure.health_exhausted += health_exhausted
    adventure.modification_flags |= ADVENTURE_MODIFICATION_FLAG_HEALTH_EXHAUSTED


def adventure_collect_modifications(adventure):
    """
    Collects the modifications done to the adventure.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to collect of.
    
    Returns
    -------
    modifications : `None | dict<str, object>`
    """
    modification_flags = adventure.modification_flags
    if not modification_flags:
        return None
    
    adventure.modification_flags = 0
    
    modifications = {}
    
    if modification_flags & ADVENTURE_MODIFICATION_FLAG_STATE:
        modifications['state'] = adventure.state
    
    if modification_flags & ADVENTURE_MODIFICATION_FLAG_UPDATED_AT:
        modifications['updated_at'] = adventure.updated_at
    
    if modification_flags & ADVENTURE_MODIFICATION_FLAG_ACTION_LISTING:
        action_listing = adventure.action_listing
        if action_listing is None:
            action_listing_data = None
        else:
            action_listing_data = adventure_action_listing_serialise(action_listing)
        modifications['action_listing_data'] = action_listing_data
    
    if modification_flags & ADVENTURE_MODIFICATION_FLAG_ENERGY_EXHAUSTED:
        modifications['energy_exhausted'] = adventure.energy_exhausted
        
    if modification_flags & ADVENTURE_MODIFICATION_FLAG_HEALTH_EXHAUSTED:
        modifications['health_exhausted'] = adventure.health_exhausted
    
    return modifications


def adventure_count_actions_for_seeding(adventure):
    """
    Counts how much actions the adventure had for seeding.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to count their actions of.
    
    Returns
    -------
    action_count : `int`
    """
    action_listing = adventure.action_listing
    if (action_listing is None):
        return 0
    
    # Ignore all action under 100, since they are system actions.
    return sum(action.action_id >= 100 for action in action_listing)
