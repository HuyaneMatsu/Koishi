__all__ = ('Action',)

from scarletio import RichAttributeErrorBaseType


class Action(RichAttributeErrorBaseType):
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
    
    def __new__(cls, action_id, action_type, duration, weight, battle, loot):
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
        """
        self = object.__new__(cls)
        self.battle = battle
        self.duration = duration
        self.id = action_id
        self.loot = loot
        self.type = action_type
        self.weight = weight
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # type
        repr_parts.append(', type = ')
        repr_parts.append(repr(self.type))
        
        # duration
        repr_parts.append(', duration = ')
        repr_parts.append(repr(self.duration))
        
        # weight
        repr_parts.append(', weight = ')
        repr_parts.append(repr(self.weight))
        
        # battle
        repr_parts.append(', battle = ')
        repr_parts.append(repr(self.battle))
        
        # loot
        repr_parts.append(', loot = ')
        repr_parts.append(repr(self.loot))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
