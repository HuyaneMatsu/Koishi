__all__ = ('Game21Session',)

from scarletio import RichAttributeErrorBaseType

from .deck import Deck


class Game21Session(RichAttributeErrorBaseType):
    """
    Represents a session.
    
    Attributes
    ----------
    amount : `int`
        The amount of gambled hearts by user.
    
    deck : ``Deck``
        The session's deck.
    
    guild : ``None | Guild``
        The owner guild.
    
    id : `int`
        The session's identifier.
    
    latest_interaction_event : ``InteractionEvent``
        The latest interaction event the user received.
    
    message : ``None | Message``
        The message of teh session.
    
    user_ids : `None | tuple<int>`
        The joined users' identifiers.
    """
    __slots__ = ('amount', 'deck', 'guild', 'id', 'latest_interaction_event', 'message', 'user_ids')
    
    def __new__(cls, session_id, guild, amount, latest_interaction_event):
        """
        Creates a new session.
        
        Parameters
        ----------
        session_id : `int`
            The session's identifier.
        
        guild : ``None | Guild``
            The owner guild.
        
        amount : `int`
            The amount of gambled hearts by user.
        
        latest_interaction_event : ``InteractionEvent``
            The latest interaction event the user received.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.deck = Deck()
        self.guild = guild
        self.id = session_id
        self.latest_interaction_event = latest_interaction_event
        self.message = None
        self.user_ids = None
        return self
    
    
    def __repr__(self):
        """Returns the session's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # guild
        repr_parts.append(' guild = ')
        repr_parts.append(repr(self.guild))
        
        # deck
        repr_parts.append(' deck = ')
        repr_parts.append(repr(self.deck))
        
        # user_ids
        user_ids = self.user_ids
        if (user_ids is not None):
            repr_parts.append(', user_ids = ')
            repr_parts.append(repr(user_ids))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
