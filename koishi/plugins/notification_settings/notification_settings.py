__all__ = ('NotificationSettings',)

from warnings import warn

from scarletio import RichAttributeErrorBaseType


class NotificationSettings(RichAttributeErrorBaseType):
    """
    A user's notification settings.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    user_id : `int`
        The user's identifier.
        
    daily_by_waifu : `bool`
        Whether daily notification should be delivered.
        
    daily_reminder : `bool`
        Whether the user should get reminder about that they forgot to claim their daily reward.
    
    notifier_client_id : `int`
        The client's identifier who should deliver the notifications.
    
    proposal : `bool`
        Whether proposal notification should be delivered.
    """
    __slots__ = ('entry_id', 'user_id', 'daily_by_waifu', 'daily_reminder', 'notifier_client_id', 'proposal')
    
    def __new__(
        cls,
        user_id,
        *,
        daily_by_waifu = True,
        daily_reminder = False,
        notifier_client_id = 0,
        proposal = True,
    ):
        """
        Creates a new notification settings object.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        
        daily_by_waifu : `bool` = `True`, Optional (Keyword only)
            Whether daily notification should be delivered.
        
        daily_reminder : `bool` = `False`, Optional (Keyword only)
            Whether the user should get reminder about that they forgot to claim their daily reward.
        
        notifier_client_id : `int` = `0`, Optional (Keyword only)
            The client's identifier who should deliver the notifications.
        
        proposal : `bool` = `True`, Optional (Keyword only)
            Whether proposal notification should be delivered.
        """
        self = object.__new__(cls)
        self.entry_id = -1
        self.user_id = user_id
        self.daily_by_waifu = daily_by_waifu
        self.daily_reminder = daily_reminder
        self.notifier_client_id = notifier_client_id
        self.proposal = proposal
        return self
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an automation configuration from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.entry_id = entry['id']
        self.user_id = entry['user_id']
        self.daily_by_waifu = entry['daily_by_waifu']
        self.daily_reminder = entry['daily_reminder']
        self.notifier_client_id = entry['notifier_client_id']
        self.proposal = entry['proposal']
        return self
    
    
    def __repr__(self):
        """Returns the notification settings' representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        entry_id = self.entry_id
        if (entry_id != -1):
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append(', daily_by_waifu = ')
        repr_parts.append(repr(self.daily_by_waifu))
        
        repr_parts.append(', daily_reminder = ')
        repr_parts.append(repr(self.daily_reminder))
        
        repr_parts.append(', notifier_client_id = ')
        repr_parts.append(repr(self.notifier_client_id))
        
        repr_parts.append(', proposal = ')
        repr_parts.append(repr(self.proposal))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two notification settings are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.user_id != other.user_id:
            return False
        
        if self.daily_by_waifu != other.daily_by_waifu:
            return False
        
        if self.daily_reminder != other.daily_reminder:
            return False
        
        if self.notifier_client_id != other.notifier_client_id:
            return False
        
        if self.proposal != other.proposal:
            return False
        
        return True
    
    
    def __bool__(self):
        """Returns whether the notification setting has anything modified."""
        if self.daily_by_waifu != True:
            return True
        
        if self.daily_reminder != False:
            return True
        
        if self.notifier_client_id != 0:
            return True
        
        if self.proposal != True:
            return True
        
        return False
    
    
    def copy(self):
        """
        Copies the notification settings.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.entry_id = self.entry_id
        new.user_id = self.user_id
        new.daily_by_waifu = self.daily_by_waifu
        new.daily_reminder = self.daily_reminder
        new.notifier_client_id = self.notifier_client_id
        new.proposal = self.proposal
        return new
    
    
    @property
    def daily(self):
        warn(
            f'`{type(self).__name__}.daily` has been removed. Use `.daily_by_waifu` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return self.daily_by_waifu
