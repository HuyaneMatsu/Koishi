__all__ = ('UserSettings',)

from warnings import warn

from scarletio import RichAttributeErrorBaseType

from .constants import PREFERRED_IMAGE_SOURCE_NONE


class UserSettings(RichAttributeErrorBaseType):
    """
    A user's user settings.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    user_id : `int`
        The user's identifier.
        
    notification_daily_by_waifu : `bool`
        Whether daily notification should be delivered.
        
    notification_daily_reminder : `bool`
        Whether the user should get reminder about that they forgot to claim their daily reward.
    
    notification_proposal : `bool`
        Whether notification_proposal notification should be delivered.
    
    preferred_client_id : `int`
        The client's identifier who should deliver the notifications.
    
    preferred_image_source : `int`
        The image source the user prefers if multiple choices are available.
    """
    __slots__ = (
        'entry_id', 'user_id', 'notification_daily_by_waifu', 'notification_daily_reminder', 'notification_proposal',
        'preferred_client_id', 'preferred_image_source'
    )
    
    def __new__(
        cls,
        user_id,
        *,
        notification_daily_by_waifu = True,
        notification_daily_reminder = False,
        notification_proposal = True,
        preferred_client_id = 0,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_NONE,
    ):
        """
        Creates a new user settings object.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        
        notification_daily_by_waifu : `bool` = `True`, Optional (Keyword only)
            Whether daily notification should be delivered.
        
        notification_daily_reminder : `bool` = `False`, Optional (Keyword only)
            Whether the user should get reminder about that they forgot to claim their daily reward.
        
        notification_proposal : `bool` = `True`, Optional (Keyword only)
            Whether notification_proposal notification should be delivered.
        
        preferred_client_id : `int` = `0`, Optional (Keyword only)
            The client's identifier who should deliver the notifications.
        
        preferred_image_source : `int` = `PREFERRED_IMAGE_SOURCE_NONE`, Optional (Keyword only)
            The image source the user prefers if multiple choices are available.
        """
        self = object.__new__(cls)
        self.entry_id = -1
        self.user_id = user_id
        self.notification_daily_by_waifu = notification_daily_by_waifu
        self.notification_daily_reminder = notification_daily_reminder
        self.notification_proposal = notification_proposal
        self.preferred_client_id = preferred_client_id
        self.preferred_image_source = preferred_image_source
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
        self.notification_daily_by_waifu = entry['notification_daily_by_waifu']
        self.notification_daily_reminder = entry['notification_daily_reminder']
        self.notification_proposal = entry['notification_proposal']
        self.preferred_client_id = entry['preferred_client_id']
        self.preferred_image_source = entry['preferred_image_source']
        return self
    
    
    def __repr__(self):
        """Returns the user settings' representation."""
        repr_parts = ['<', type(self).__name__]
        
        entry_id = self.entry_id
        if (entry_id != -1):
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append(', notification_daily_by_waifu = ')
        repr_parts.append(repr(self.notification_daily_by_waifu))
        
        repr_parts.append(', notification_daily_reminder = ')
        repr_parts.append(repr(self.notification_daily_reminder))
        
        repr_parts.append(', notification_proposal = ')
        repr_parts.append(repr(self.notification_proposal))
        
        repr_parts.append(', preferred_client_id = ')
        repr_parts.append(repr(self.preferred_client_id))
        
        repr_parts.append(', preferred_image_source = ')
        repr_parts.append(repr(self.preferred_image_source))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two user settings are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.user_id != other.user_id:
            return False
        
        if self.notification_daily_by_waifu != other.notification_daily_by_waifu:
            return False
        
        if self.notification_daily_reminder != other.notification_daily_reminder:
            return False
        
        if self.notification_proposal != other.notification_proposal:
            return False
        
        if self.preferred_client_id != other.preferred_client_id:
            return False
        
        if self.preferred_image_source != other.preferred_image_source:
            return False
        
        return True
    
    
    def __bool__(self):
        """Returns whether the notification setting has anything modified."""
        if self.notification_daily_by_waifu != True:
            return True
        
        if self.notification_daily_reminder != False:
            return True
        
        if self.notification_proposal != True:
            return True
        
        if self.preferred_client_id != 0:
            return True
        
        if self.preferred_image_source != PREFERRED_IMAGE_SOURCE_NONE:
            return True
        
        return False
    
    
    def copy(self):
        """
        Copies the user settings.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.entry_id = self.entry_id
        new.user_id = self.user_id
        new.notification_daily_by_waifu = self.notification_daily_by_waifu
        new.notification_daily_reminder = self.notification_daily_reminder
        new.notification_proposal = self.notification_proposal
        new.preferred_client_id = self.preferred_client_id
        new.preferred_image_source = self.preferred_image_source
        return new
    
    
    @property
    def daily(self):
        warn(
            f'`{type(self).__name__}.daily` has been removed. Use `.notification_daily_by_waifu` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return self.notification_daily_by_waifu

    
    @property
    def daily_by_waifu(self):
        warn(
            f'`{type(self).__name__}.daily_by_waifu` has been removed. Use `.notification_daily_by_waifu` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return self.notification_daily_by_waifu


    @property
    def daily_reminder(self):
        warn(
            f'`{type(self).__name__}.daily_reminder` has been removed. Use `.notification_daily_reminder` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return self.notification_daily_reminder

    
    @property
    def proposal(self):
        warn(
            f'`{type(self).__name__}.proposal` has been removed. Use `.notification_proposal` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return self.notification_proposal
