__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .constants import ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE


class TopListActionCounter(RichAttributeErrorBaseType):
    """
    Used to count moderation actions.
    
    Attributes
    ----------
    all : `int`
        The total actions executed.
    
    ban : `int`
        Bans executed.
    
    kick : `int`
        Kicks executed.
    
    mute : `int`
        Mutes executed.
    """
    __slots__ = ('all', 'ban', 'kick', 'mute')
    
    def __new__(cls):
        """
        Creates a new action counter.
        """
        self = object.__new__(cls)
        self.all = 0
        self.ban = 0
        self.kick = 0
        self.mute = 0
        return self
    
    
    def __repr__(self):
        """Returns the action counter's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' all = ')
        repr_parts.append(repr(self.all))
        
        repr_parts.append(', ban = ')
        repr_parts.append(repr(self.ban))
        
        repr_parts.append(', kick = ')
        repr_parts.append(repr(self.kick))
        
        repr_parts.append(', mute = ')
        repr_parts.append(repr(self.mute))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def top_list_action_counter_increment_with(top_list_action_counter, action_type, amount = 1):
    """
    Increments the action counter counter by the given action type.
    
    Parameters
    ----------
    top_list_action_counter : ``TopListActionCounter``
        Action counter to increment.
    
    action_type : `int`
        Action type identifier.
    
    amount : `int` = `1`, Optional
        The amount to increment with.
    """
    top_list_action_counter.all += amount
    
    if action_type == ACTION_TYPE_BAN:
        top_list_action_counter.ban += amount
    
    elif action_type == ACTION_TYPE_KICK:
        top_list_action_counter.kick += amount
    
    elif action_type == ACTION_TYPE_MUTE:
        top_list_action_counter.mute += amount
