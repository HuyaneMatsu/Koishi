__all__ = ('GOAL_TYPE_ITEM_EXACT', 'Goal', 'goal_create_default', 'goal_create_item_exact')

from struct import Struct

from scarletio import RichType, copy_docs, include

from ...item_core import get_item_nullable
from ...unit_core import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT

adventure_action_listing_accumulate_loot = include('adventure_action_listing_accumulate_loot')


GOAL_ITEM_EXACT_STRUCT = Struct('<LBQ')


GOAL_TYPE_NONE = 0
GOAL_TYPE_ITEM_EXACT = 1


def check_default(configuration, adventure):
    """
    Default check.
    
    Parameters
    ----------
    configuration : ``GoalConfigurationBase``
        Goal configuration.
    
    adventure : ``Adventure``
        Adventure to check.
    
    Returns
    -------
    satisfied : `bool`
    """
    return False


@copy_docs(check_default)
def check_item_exact(configuration, adventure):
    adventure_action_listing = adventure.action_listing
    if adventure_action_listing is None:
        return False
    
    accumulated_loot = adventure_action_listing_accumulate_loot(adventure_action_listing)
    
    item_id = configuration.item_id
    try:
        amount_collected = accumulated_loot[item_id]
    except KeyError:
        return False
    
    amount_type = configuration.amount_type
    
    if (amount_type == AMOUNT_TYPE_VALUE) or (amount_type == AMOUNT_TYPE_WEIGHT):
        item = get_item_nullable(configuration.item_id)
        if (item is not None):
            amount_collected *= item.value if (amount_type == AMOUNT_TYPE_VALUE) else item.weight
    
    return amount_collected >= configuration.amount_required


def deserialise_default(data, start_index):
    """
    Deserialises the given data.
    
    Parameters
    ----------
    data : `memoryview`
        Data to deserialise.
    
    start_index : `int`
        Where serialisation starts at.
    
    Returns
    -------
    configuration_and_end_index : ``None | (Goal, int)``
    """
    return goal_create_default(), start_index


@copy_docs(deserialise_default)
def deserialise_item_exact(data, start_index):
    end_index = start_index + 13
    
    if len(data) < end_index:
        return None
    
    return (
        goal_create_item_exact(
            *GOAL_ITEM_EXACT_STRUCT.unpack(data[start_index : end_index])
        ),
        end_index,
    )


def serialise_default(configuration):
    """
    Base serialiser for configurations.
    
    Parameters
    ----------
    configuration : ``GoalConfigurationBase``
    
    Yields
    ------
    part : `bytes`
    """
    return
    yield


@copy_docs(serialise_default)
def serialise_item_exact(configuration):
    yield GOAL_ITEM_EXACT_STRUCT.pack(
        configuration.item_id,
        configuration.amount_type,
        configuration.amount_required,
    )


class GoalBehaviour(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Goal behaviour.
    
    Attributes
    ----------
    check : `FunctionType`
        Check to call.
    
    deserialise : `FunctionType`
        Deserialiser function.
    
    serialise : `FunctionType`
        Serialiser function`
    
    type : `int`
        Behaviour type.
    """
    __slots__ = ('check', 'deserialise', 'serialise', 'type')


def goal_behaviour_create(goal_type, deserialise, serialise, check):
    """
    Creates a new goal behaviour.
    
    Parameters
    ----------
    goal_type : `int`
        Goal type.
    
    deserialise : `FunctionType`
        Deserialiser function.
    
    serialise : `FunctionType`
        Serialiser function`
    
    check : `FunctionType`
        Check to call.
    
    Returns
    -------
    behaviour : ``GoalBehaviour``
    """
    behaviour =  object.__new__(GoalBehaviour)
    behaviour.type = goal_type
    behaviour.deserialise = deserialise
    behaviour.serialise = serialise
    behaviour.check = check
    return behaviour


GOAL_BEHAVIOUR_DEFAULT = goal_behaviour_create(
    GOAL_TYPE_NONE,
    deserialise_default,
    serialise_default,
    check_default,
)


GOAL_BEHAVIOUR_ITEM_EXACT = goal_behaviour_create(
    GOAL_TYPE_ITEM_EXACT,
    deserialise_item_exact,
    serialise_item_exact,
    check_item_exact,
)


class GoalConfigurationBase(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base configuration.
    """
    __slots__ = ()


class GoalConfigurationItemExact(GoalConfigurationBase):
    """
    Item exact configuration.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount of items.
    
    amount_type : `int`
        The type of items to require.
    
    item_id : `int`
        The required item's identifier.
    """
    __slots__ = ('amount_required', 'amount_type', 'item_id')


class Goal(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    A goal that cancels the adventure when satisfied.
    
    Attributes
    ----------
    behaviour : ``GoalBehaviour``
        Behaviour of the goal.
    
    configuration : ``GoalConfigurationBase``
        Configuration to use.
    """
    __slots__ = ('behaviour', 'configuration')


def goal_create(behaviour, configuration):
    """
    Creates a goal.
    
    Parameters
    ----------
    behaviour : ``GoalBehaviour``
        Behaviour of the goal.
    
    configuration : ``GoalConfigurationBase``
        Configuration to use.
    
    Returns
    -------
    goal : ``Goal``
    """
    goal = object.__new__(Goal)
    goal.behaviour = behaviour
    goal.configuration = configuration
    return goal


def goal_create_default():
    """
    Creates a new default goal.
    
    Returns
    -------
    goal : ``Goal``
    """
    return goal_create(GOAL_BEHAVIOUR_DEFAULT, object.__new__(GoalConfigurationBase))


def goal_create_item_exact(item_id, amount_type, amount_required):
    """
    Creates a new default goal.
    
    Parameters
    ----------
    item_id : `int`
        The required item's identifier.
    
    amount_type : `int`
        The type of items to require.
    
    amount_required : `int`
        The required amount of items.
    
    Returns
    -------
    goal : ``Goal``
    """
    configuration = object.__new__(GoalConfigurationItemExact)
    configuration.amount_required = amount_required
    configuration.amount_type = amount_type
    configuration.item_id = item_id
    
    return goal_create(GOAL_BEHAVIOUR_ITEM_EXACT, configuration)
