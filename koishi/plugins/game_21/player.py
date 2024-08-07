__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .constants import PLAYER_STATE_NONE
from .hand import Hand


class Player(RichAttributeErrorBaseType):
    """
    Represents a player.
    
    Attributes
    ----------
    hand : `Hand`
        The player's hand.
    entry_id : `int`
        Database entry identifier.
    latest_interaction_event : `None | InteractionEvent`
        The latest interaction event the user received.
    state : `int`
        The player's state.
    user : ``ClientUserBase``
        The owner user.
    """
    __slots__ = ('entry_id', 'hand', 'latest_interaction_event', 'state', 'user')
    
    def __new__(cls, user, entry_id, latest_interaction_event):
        self = object.__new__(cls)
        self.entry_id = entry_id
        self.hand = Hand()
        self.latest_interaction_event = latest_interaction_event
        self.state = PLAYER_STATE_NONE
        self.user = user
        return self
    
    
    def __repr__(self):
        """Returns the player's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # user
        repr_parts.append(' user = ')
        repr_parts.append(repr(self.user))
        
        # hand
        repr_parts.append(' hand = ')
        repr_parts.append(repr(self.hand))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
