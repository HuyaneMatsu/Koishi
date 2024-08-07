__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .deck import Deck


class Session(RichAttributeErrorBaseType):
    """
    Represents a session.
    
    Attributes
    ----------
    amount : `int`
        The amount of gambled hearts by user.
    deck : ``Deck``
        The session's deck.
    guild : `None | Guild`
        The owner guild.
    latest_interaction_event : ``InteractionEvent``
        The latest interaction event the user received.
    """
    __slots__ = ('amount', 'deck', 'guild', 'latest_interaction_event')
    
    def __new__(cls, guild, amount, latest_interaction_event):
        """
        Creates a new session.
        
        Parameters
        ----------
        guild : `None | Guild`
            The owner guild.
        amount : `int`
            The amount of gambled hearts by user.
        latest_interaction_event : `InteractionEvent`
            The latest interaction event the user received.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.deck = Deck()
        self.guild = guild
        self.latest_interaction_event = latest_interaction_event
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
        
        repr_parts.append('>')
        return ''.join(repr_parts)
