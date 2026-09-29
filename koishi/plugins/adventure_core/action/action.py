__all__ = ('Action', 'action_create')

from scarletio import RichType


class Action(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Represents a action to adventure at.
    
    Attributes
    ----------
    battle : ``None | tuple<OptionBattle>``
        Options to chose battles from.
    
    duration : `int`
        How long does this action lasts for. Time spent before occurring.
    
    id : `int`
        The identifier of the action.
    
    loot : ``None | tuple<OptionLoot>``
        The loot options of the action.
    
    type : `int`
        The type of the action.
    
    weight : `int`
        The weight of the action representing its chance to be chosen.
    """
    __slots__ = ('battle', 'duration', 'id', 'loot', 'type', 'weight')


def action_create(action_id, action_type, duration, weight, battle, loot):
    """
    Creates a new action.
    
    Parameters
    ----------
    action_id : `int`
        The identifier of the action.
    
    action_type : `int`
        The type of the action.
    
    duration : `int`
        How long does this action lasts for. Time spent before occurring.
    
    weight : `int`
        The weight of the action representing its chance to be chosen.
    
    battle : ``None | tuple<OptionBattle>``
        Options to chose battles from.
    
    loot : ``None | tuple<OptionLoot>``
        The loot options of the action.
    
    Returns
    -------
    action : ``Action``
    """
    action = object.__new__(Action)
    action.battle = battle
    action.duration = duration
    action.id = action_id
    action.loot = loot
    action.type = action_type
    action.weight = weight
    return action
