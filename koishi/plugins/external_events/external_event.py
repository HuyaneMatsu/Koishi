__all__ = ()

from datetime import timezone as TimeZone
from json import JSONDecodeError

from hata import DATETIME_FORMAT_CODE
from scarletio import RichAttributeErrorBaseType, from_json


class ExternalEvent(RichAttributeErrorBaseType):
    """
    Represents an event happening outside the bot.
    
    Attributes
    ----------
    client_id : `int`
        The client's identifier to who this event is related to.
    
    entry_id : `int`
        The database entry's identifier.
    
    event_data : `None | object`
        Additional event data.
    
    event_type : `int`
        The event's type.
    
    guild_id : `int`
        The guild identifier the event is bound to.
    
    trigger_after : `None | DateTime`
        After when the event should be triggered.
    
    user_id : `int`
        The user to who this event is related to.
    """
    __slots__ = ('client_id', 'entry_id', 'event_data', 'event_type', 'guild_id', 'trigger_after', 'user_id')
    
    def __new__(
        cls,
        *,
        client_id = 0,
        event_data = None,
        event_type = 0,
        guild_id = 0,
        trigger_after = None,
        user_id = 0,
    ):
        """
        Creates a new external event object.
        
        Parameters
        ----------
        client_id : `int` = `0`, Optional (Keyword only)
            The client's identifier to who this event is related to.
        
        event_data : `None | object` = `None`, Optional (Keyword only)
            Additional event data.
        
        event_type : `int` = `0`, Optional (Keyword only)
            The event's type.
        
        guild_id : `int`
            The guild identifier the event is bound to.
        
        trigger_after : `None | DateTime` = `None`, Optional (Keyword only)
            After when the event should be triggered.
        
        user_id : `int` = `0`, Optional (Keyword only)
            The user to who this event is related to.
        """
        self = object.__new__(cls)
        self.client_id = client_id
        self.entry_id = 0
        self.event_data = event_data
        self.event_type = event_type
        self.guild_id = guild_id
        self.trigger_after = trigger_after
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an external event from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        event_data = entry['event_data']
        if (event_data is not None):
            try:
                event_data = from_json(event_data)
            except JSONDecodeError:
                event_data = None
        
        trigger_after = entry['trigger_after']
        if (trigger_after is not None):
            trigger_after = trigger_after.replace(tzinfo = TimeZone.utc)
        
        self = object.__new__(cls)
        self.client_id = entry['client_id']
        self.entry_id = entry['id']
        self.event_data = event_data
        self.event_type = entry['event_type']
        self.guild_id = entry['guild_id']
        self.trigger_after = trigger_after
        self.user_id = entry['user_id']
        return self
    
    
    def __repr__(self):
        """Returns the user settings' representation."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        entry_id = self.entry_id
        if (entry_id != 0):
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # event_type
        repr_parts.append(' event_type = ')
        repr_parts.append(repr(self.event_type))
            
        # client_id
        client_id = self.client_id
        if client_id:
            repr_parts.append(', client_id = ')
            repr_parts.append(repr(client_id))
        
        # user_id
        user_id = self.user_id
        if user_id:
            repr_parts.append(', user_id = ')
            repr_parts.append(repr(user_id))
        
        # guild_id
        guild_id = self.guild_id
        if guild_id:
            repr_parts.append(', guild_id = ')
            repr_parts.append(repr(guild_id))
        
        # event_data
        event_data = self.event_data
        if (event_data is not None):
            repr_parts.append(', event_data = ')
            repr_parts.append(repr(event_data))
        
        # trigger_after
        trigger_after = self.trigger_after
        if (trigger_after is not None):
            repr_parts.append(', trigger_after = ')
            repr_parts.append(format(trigger_after, DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two external events are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # client_id
        if self.client_id != other.client_id:
            return False
        
        # entry_id | ignore
        
        # event_data
        if self.event_data != other.event_data:
            return False
        
        # event_type
        if self.event_type != other.event_type:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # trigger_after
        if self.trigger_after != other.trigger_after:
            return False
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        return True
