__all__ = ('UserSettings',)

from scarletio import RichAttributeErrorBaseType

from .constants import (
    PREFERRED_IMAGE_SOURCE_NONE, USER_SETTINGS_FEATURE_FLAG_DEFAULT,
    USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX, USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE
)


class UserSettings(RichAttributeErrorBaseType):
    """
    A user's user settings.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    feature_flags : `int`
        Feature flags describing what features the user has access to.
    
    notification_flags : `int`
        Notification flags.
    
    preferred_client_id : `int`
        The client's identifier who should deliver the notifications.
    
    preferred_image_source : `int`
        The image source the user prefers if multiple choices are available.
    
    user_id : `int`
        The user's identifier.
    """
    __slots__ = (
        'entry_id', 'feature_flags', 'notification_flags', 'preferred_client_id', 'preferred_image_source', 'user_id'
    )
    
    def __new__(
        cls,
        user_id,
    ):
        """
        Creates a new user settings object.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        """
        self = object.__new__(cls)
        self.entry_id = 0
        self.feature_flags = USER_SETTINGS_FEATURE_FLAG_DEFAULT
        self.notification_flags = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT
        self.preferred_client_id = 0
        self.preferred_image_source = PREFERRED_IMAGE_SOURCE_NONE
        self.user_id = user_id
        return self
    
    
    @classmethod
    def create_with_specification(
        cls,
        user_id,
        *,
        feature_market_place_inbox = USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX,
        notification_adventure_recovery_over = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER,
        notification_daily_by_waifu = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU,
        notification_daily_reminder = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER,
        notification_gift = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT,
        notification_market_place_item_finalisation = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION,
        notification_proposal = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL,
        notification_vote = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE,
        preferred_client_id = 0,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_NONE,
    ):
        """
        Creates user settings with the given specifications.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        
        feature_market_place_inbox : `int` = `USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX`, Optional (Keyword only)
            Whether the user has access to market place inbox.
        
        notification_adventure_recovery_over : `int` = `USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER`, Optional (Keyword only)
            Whether notification should be delivered when a user's recovered and can engage on a new adventure.
        
        notification_daily_by_waifu : `int` = `USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU`, Optional (Keyword only)
            Whether daily notification should be delivered.
        
        notification_daily_reminder : `int` = `USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER`, Optional (Keyword only)
            Whether the user should get reminder about that they forgot to claim their daily reward.
        
        notification_gift : `int` = `USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT`, Optional (Keyword only)
            Whether the user should get gift notifications.
        
        notification_market_place_item_finalisation : `int` = `USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION`, Optional (Keyword only)
            Whether market place item finalisation should be delivered.
        
        notification_proposal : `int` = `USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL`, Optional (Keyword only)
            Whether notification_proposal notification should be delivered.
        
        notification_vote : `int` = `USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE`, Optional (Keyword only)
            Whether vote notification should be delivered.
        
        preferred_client_id : `int` = `0`, Optional (Keyword only)
            The client's identifier who should deliver the notifications.
        
        preferred_image_source : `int` = `PREFERRED_IMAGE_SOURCE_NONE`, Optional (Keyword only)
            The image source the user prefers if multiple choices are available.
        """
        self = object.__new__(cls)
        self.entry_id = 0
        self.feature_flags = (
             (feature_market_place_inbox << USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX)
        )
        self.notification_flags = (
            (notification_adventure_recovery_over << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER) |
            (notification_daily_by_waifu << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU) |
            (notification_daily_reminder << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER) |
            (notification_gift << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT) |
            (notification_market_place_item_finalisation << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION) |
            (notification_proposal << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL) |
            (notification_vote << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE)
        )
        self.preferred_client_id = preferred_client_id
        self.preferred_image_source = preferred_image_source
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates a user settings from the given entry.
        
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
        self.feature_flags = entry['feature_flags']
        self.notification_flags = entry['notification_flags']
        self.preferred_client_id = entry['preferred_client_id']
        self.preferred_image_source = entry['preferred_image_source']
        self.user_id = entry['user_id']
        return self
    
    
    def __repr__(self):
        """Returns the user settings' representation."""
        repr_parts = ['<', type(self).__name__]
        
        entry_id = self.entry_id
        if (entry_id != 0):
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # feature_flags
        repr_parts.append(', feature_flags = ')
        repr_parts.append(repr(self.feature_flags))
        
        # notification_flags
        repr_parts.append(', notification_flags = ')
        repr_parts.append(repr(self.notification_flags))
        
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
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        # feature_flags
        if self.feature_flags != other.feature_flags:
            return False
        
        # notification_flags
        if self.notification_flags != other.notification_flags:
            return False
        
        # preferred_client_id
        if self.preferred_client_id != other.preferred_client_id:
            return False
        
        # preferred_image_source
        if self.preferred_image_source != other.preferred_image_source:
            return False
        
        return True
    
    
    def __bool__(self):
        """Returns whether the notification setting has anything modified."""
        # feature_flags
        if self.feature_flags != USER_SETTINGS_FEATURE_FLAG_DEFAULT:
            return True
        
        # notification_flags
        if self.notification_flags != USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT:
            return True
        
        # preferred_client_id
        if self.preferred_client_id != 0:
            return True
        
        # preferred_image_source
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
        new.feature_flags = self.feature_flags
        new.notification_flags = self.notification_flags
        new.preferred_client_id = self.preferred_client_id
        new.preferred_image_source = self.preferred_image_source
        new.user_id = self.user_id
        return new
