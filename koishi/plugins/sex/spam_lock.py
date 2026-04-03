__all__ = ()

from hata import KOKORO
from scarletio import RichAttributeErrorBaseType
from time import monotonic

from .constants import SEX_RESET_AFTER, SEX_SPAM_LOCKS


class SexSpamLock(RichAttributeErrorBaseType):
    """
    Sex spam lock used to avoid sex spam. Or you could say to promote it by not giving.
    
    Attributes
    -----------
    entity_id : `int`
        The locked entity's identifier.
    
    handle : `None | TimerHandle`
        Handle to update the lock on expiration.
    
    last_set : `float`
        When the lock was set last time. Set as `0.0` by default.
    
    max_level : `int`
        The max allowed sex rarity level.
    """
    __slots__ = ('entity_id', 'handle', 'last_set', 'max_level')
    
    def __new__(cls, entity_id, max_level):
        """
        Creates a new sex spam lock.
        
        Parameters
        ----------
        entity_id : `int`
            The locked entity's identifier.
        max_level : `int`
            The max allowed sex rarity level.
        """
        self = object.__new__(cls)
        self.entity_id = entity_id
        self.max_level = max_level
        self.last_set = 0.0
        self.handle = KOKORO.call_after(SEX_RESET_AFTER, self)
        return self
    
    
    def __repr__(self):
        """Returns the spam lock's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # entity_id
        repr_parts.append(' entity_id = ')
        repr_parts.append(repr(self.entity_id))
        
        # max_level
        repr_parts.append(', max_level = ')
        repr_parts.append(repr(self.max_level))
        
        # expires_at
        repr_parts.append(', expires_at = ')
        repr_parts.append(repr(self.expires_at))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __call__(self):
        """
        Called when sex lock expires. Sets itself back on cooldown if required. or removes itself from the locks.
        """
        last_set = self.last_set
        if last_set:
            self.last_set = 0.0
            handle = KOKORO.call_at(last_set + SEX_RESET_AFTER, self)
        
        else:
            try:
                del SEX_SPAM_LOCKS[self.entity_id]
            except KeyError:
                pass
            handle = None
        
        self.handle = handle
    
    
    def set_max_level(self, level):
        """
        Sets the max available level of the lock. If level is greater than the current one returns the current one.
        If it is lower then lowers the set one to it.
        
        Parameters
        ----------
        level : `int`
            Sex rarity level.
        
        Returns
        -------
        level : `int`
        """
        max_level = self.max_level
        if level > max_level:
            level = 0
        elif level < max_level:
            self.max_level = level
        
        self.last_set = monotonic()
        return level
    
    
    @property
    def expires_at(self):
        """
        Returns when the lock expires.
        
        Returns
        -------
        expires_at : `float`
        """
        last_set = self.last_set
        if last_set:
            return last_set + SEX_RESET_AFTER
        
        handle = self.handle
        if (handle is not None):
            return handle.when
        
        return 0.0
    
    
    def cancel(self):
        """
        Cancels the spam lock.
        """
        handle = self.handle
        if (handle is not None):
            self.handle = None
            handle.cancel()
        
        self.last_set = 0.0


def check_lock_and_limit_level(event, level):
    """
    Checks whether the event's entities are locked and limits their rarity level.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    level : `int`
        The sex rarity level before limiting.
    
    Returns
    -------
    level : `int`
        The sex rarity level after limiting.
    """
    for entity_id in (event.channel_id, event.user_id):
        try:
            spam_lock = SEX_SPAM_LOCKS[entity_id]
        except KeyError:
            SEX_SPAM_LOCKS[entity_id] = SexSpamLock(entity_id, level)
        else:
            level = spam_lock.set_max_level(level)
    
    return level
