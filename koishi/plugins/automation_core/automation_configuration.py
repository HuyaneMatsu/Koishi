__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .automation_configuration_saver import AutomationConfigurationSaver
from .constants import AUTOMATION_CONFIGURATIONS


class AutomationConfiguration(RichAttributeErrorBaseType):
    """
    Automation configuration.
    
    Attributes
    ----------
    entry_id : `int`
        The entry's identifier in the database.
    
    guild_id : `int`
        The automation's parent guild identifier.
    
    log_emoji_channel_id : `int`
        The channel's identifier where the emoji log messages will be sent.
    
    log_mention_channel_id : `int`
        The channel's identifier where the mention log messages will be sent.
    
    log_satori_auto_start : `bool`
        Whether satori channels should be automatically started.
    
    log_satori_channel_id : `int`
        The channel's identifier where the satori log messages will be sent. Must be a guild category channel.
    
    log_sticker_channel_id : `int`
        The channel's identifier where the sticker log messages will be sent.
    
    log_user_channel_id : `int`
        The channel's identifier where the user log messages will be sent.
    
    reaction_copy_enabled : `bool`
        Whether reaction-copy feature is enabled in the guild.
    
    touhou_feed_enabled : `bool`
        Whether touhou-feed is enabled in the guild.
    
    welcome_channel_id : `int`
        The channel's identifier where the welcome messages will be sent.
    """
    __slots__ = (
        'entry_id', 'guild_id', 'log_emoji_channel_id', 'log_mention_channel_id', 'log_satori_auto_start',
        'log_satori_channel_id', 'log_sticker_channel_id', 'log_user_channel_id', 'reaction_copy_enabled', 'saver',
        'touhou_feed_enabled', 'welcome_channel_id'
    )
    
    def __new__(cls, guild_id):
        """
        Creates a new automation config.
        
        Parameters
        ----------
        guild_id : `int`
            The parent guild identifier.
        """
        self = object.__new__(cls)
        self.entry_id = -1
        self.log_emoji_channel_id = 0
        self.guild_id = guild_id
        self.log_mention_channel_id = 0
        self.log_satori_auto_start = False
        self.log_satori_channel_id = 0
        self.log_sticker_channel_id = 0
        self.log_user_channel_id = 0
        self.reaction_copy_enabled = False
        self.saver = None
        self.touhou_feed_enabled = False
        self.welcome_channel_id = 0
        return self
    
    
    def __repr__(self):
        """Returns the automation configuration's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # entry_id
        entry_id = self.entry_id
        if entry_id != -1:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # log_emoji_channel_id
        log_emoji_channel_id = self.log_emoji_channel_id
        if log_emoji_channel_id:
            repr_parts.append(', log_emoji_channel_id = ')
            repr_parts.append(repr(log_emoji_channel_id))
        
        # log_mention_channel_id
        log_mention_channel_id = self.log_mention_channel_id
        if log_mention_channel_id:
            repr_parts.append(', log_mention_channel_id = ')
            repr_parts.append(repr(log_mention_channel_id))
        
        # log_satori_channel_id
        log_satori_channel_id = self.log_satori_channel_id
        if log_satori_channel_id:
            repr_parts.append(', log_satori_channel_id = ')
            repr_parts.append(repr(log_satori_channel_id))
            
            log_satori_auto_start = self.log_satori_auto_start
            if log_satori_auto_start:
                repr_parts.append(', log_satori_auto_start = ')
                repr_parts.append(repr(log_satori_auto_start))
        
        # log_sticker_channel_id
        log_sticker_channel_id = self.log_sticker_channel_id
        if log_sticker_channel_id:
            repr_parts.append(', log_sticker_channel_id = ')
            repr_parts.append(repr(log_sticker_channel_id))
        
        # log_user_channel_id
        log_user_channel_id = self.log_user_channel_id
        if log_user_channel_id:
            repr_parts.append(', log_user_channel_id = ')
            repr_parts.append(repr(log_user_channel_id))
        
        # reaction_copy_enabled
        reaction_copy_enabled = self.reaction_copy_enabled
        if reaction_copy_enabled:
            repr_parts.append(', reaction_copy_enabled = ')
            repr_parts.append(repr(reaction_copy_enabled))
        
        # touhou_feed_enabled
        touhou_feed_enabled = self.touhou_feed_enabled
        if touhou_feed_enabled:
            repr_parts.append(', touhou_feed_enabled = ')
            repr_parts.append(repr(touhou_feed_enabled))
        
        # welcome_channel_id
        welcome_channel_id = self.welcome_channel_id
        if welcome_channel_id:
            repr_parts.append(', welcome_channel_id = ')
            repr_parts.append(repr(welcome_channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether any automation configuration is set."""
        if self.log_emoji_channel_id:
            return True
        
        if self.log_mention_channel_id:
            return True
        
        if self.log_satori_channel_id:
            return True
        
        if self.log_satori_auto_start:
            return True
        
        if self.log_sticker_channel_id:
            return True
        
        if self.log_user_channel_id:
            return True
        
        if self.reaction_copy_enabled:
            return True
        
        if self.touhou_feed_enabled:
            return True
        
        if self.welcome_channel_id:
            return True
        
        return False
    
    
    def get_saver(self):
        """
        Gets or creates a new saver for the configuration.
        """
        saver = self.saver
        if (saver is None):
            saver = AutomationConfigurationSaver(self)
            self.saver = saver
        
        return saver
    
        
    def set(self, field_name, field_value):
        """
        Sets a value of the auto moderation configuration.
        
        Parameters
        ----------
        field_name : `str`
            The field's name.
        field_value : `object`
            The new value of the field.
        """
        AUTOMATION_CONFIGURATION_FIELD_SETTERS[field_name](self, field_value)
        
        saver = self.get_saver()
        
        if self:
            AUTOMATION_CONFIGURATIONS[self.guild_id] = self
            
            saver.add_modification(field_name, field_value)
        
        else:
            try:
                del AUTOMATION_CONFIGURATIONS[self.guild_id]
            except KeyError:
                pass
            
            saver.ensure_deletion()
        
        saver.begin()
    
    
    def delete(self):
        """
        Deletes the entry.
        """
        saver = self.get_saver()
        saver.ensure_deletion()
        saver.begin()
        
        try:
            del AUTOMATION_CONFIGURATIONS[self.guild_id]
        except KeyError:
            pass
    
    
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
        guild_id = entry['guild_id']
        
        try:
            self = AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            self = object.__new__(cls)
            self.guild_id = guild_id
            self.saver = None
            AUTOMATION_CONFIGURATIONS[guild_id] = self
        
        self.entry_id = entry['id']
        self.log_emoji_channel_id = entry['log_emoji_channel_id']
        self.log_mention_channel_id = entry['log_mention_channel_id']
        self.log_satori_auto_start = entry['log_satori_auto_start']
        self.log_satori_channel_id = entry['log_satori_channel_id']
        self.log_sticker_channel_id = entry['log_sticker_channel_id']
        self.log_user_channel_id = entry['log_user_channel_id']
        self.reaction_copy_enabled = entry['reaction_copy_enabled']
        self.touhou_feed_enabled = entry['touhou_feed_enabled']
        self.welcome_channel_id = entry['welcome_channel_id']
        
        return self


AUTOMATION_CONFIGURATION_FIELD_SETTERS = {
    'log_emoji_channel_id': AutomationConfiguration.log_emoji_channel_id.__set__,
    'log_mention_channel_id': AutomationConfiguration.log_mention_channel_id.__set__,
    'log_sticker_channel_id': AutomationConfiguration.log_sticker_channel_id.__set__,
    'log_user_channel_id': AutomationConfiguration.log_user_channel_id.__set__,
    
    'log_satori_channel_id': AutomationConfiguration.log_satori_channel_id.__set__,
    'log_satori_auto_start': AutomationConfiguration.log_satori_auto_start.__set__,
    
    'welcome_channel_id': AutomationConfiguration.welcome_channel_id.__set__,
    'touhou_feed_enabled': AutomationConfiguration.touhou_feed_enabled.__set__,
    'reaction_copy_enabled': AutomationConfiguration.reaction_copy_enabled.__set__,
}
