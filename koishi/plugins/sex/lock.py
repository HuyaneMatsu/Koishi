__all__ = ()

from hata import KOKORO

from .constants import SEX_RESET_AFTER

SEX_SPAM_LOCK = {}


class SexSpamLock:
    """
    Sex spam lock used to avoid sex spam. Or you could say to promote it by not giving.
    
    Attributes
    -----------
    entity_id : `int`
        The locked entity's identifier.
    expires_at : `float`
        When the lock expires in monotonic time.
    max_level : `int`
        The max allowed sex rarity level.
    """
    __slots__ = ('entity_id', 'expires_at', 'max_level')
    
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
        self.expires_at = 0.0
        
        KOKORO.call_after(SEX_RESET_AFTER, self)
        return self
    
    
    def __call__(self):
        """
        Called when sex lock expires. Sets itself back on cooldown if required. or removes itself from the locks.
        """
        expires_at = self.expires_at
        if expires_at:
            KOKORO.call_at(expires_at + SEX_RESET_AFTER, self)
        else:
            try:
                del SEX_SPAM_LOCK[self.entity_id]
            except KeyError:
                pass
    
    
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
            level = max_level
        elif level < max_level:
            self.max_level = level
        
        return level



def check_lock_and_limit_level(event, level):
    """
    Checks whether the event's entities are locked and limits their rarity level.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    level : `int`
        The sex rarity level after limiting.
    """
    channel_id = event.channel_id
    try:
        spam_lock = SEX_SPAM_LOCK[channel_id]
    except KeyError:
        SEX_SPAM_LOCK[channel_id] = SexSpamLock(channel_id, level)
    else:
        level = spam_lock.set_max_level(level)
    
    return level
