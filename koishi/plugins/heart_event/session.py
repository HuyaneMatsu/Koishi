__all__ = ()

from scarletio import LOOP_TIME, RichAttributeErrorBaseType


class Session(RichAttributeErrorBaseType):
    """
    Represents a heart event session.
    
    Attributes
    ----------
    amount : `int`
        Reward amount.
    
    client : ``Client``
        The client executing the event.
    
    ends_at_loop_time : `float`
        When the event ends in loop time.
    
    event_mode : `int`
        The event's mode.

    message : ``Message``
        The message to update.
    
    update_handle : ``None | TimerHandle``
        Call-back handle. Used to update the message regularly.
    
    user_ids : `None | set<int>`
        User identifiers.
    
    user_limit : `int`
        The maximal amount of users allowed to receive reward.
    """
    __slots__ = (
        'amount', 'client', 'ends_at_loop_time', 'event_mode', 'message', 'update_handle', 'user_ids', 'user_limit'
    )
    
    def __new__(cls, client, message, event_mode, duration, amount, user_limit):
        """
        Creates a new heart event session.
        
        Parameters
        ----------
        client : ``Client``
            The client executing the event.
        
        message : ``Message``
            The message to update.
        
        event_mode : `int`
            The event's mode.
        
        duration : `TimeDelta`
            The duration of the event.
        
        amount : `int`
            Reward amount.
        
        user_limit : `int`
            The maximal amount of users allowed to receive reward.
        """
        self = object.__new__(cls)
        self.amount = amount
        self.client = client
        self.ends_at_loop_time = LOOP_TIME() + duration.total_seconds()
        self.event_mode = event_mode
        self.message = message
        self.update_handle = None
        self.user_ids = None
        self.user_limit = user_limit
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # event_mode
        repr_parts.append(' event_mode = ')
        repr_parts.append(repr(self.event_mode))
        
        # amount
        repr_parts.append(', amount = ')
        repr_parts.append(repr(self.amount))
        
        # user_limit
        repr_parts.append(', user_limit = ')
        repr_parts.append(repr(self.user_limit))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
