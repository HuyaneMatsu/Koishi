__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .automation_configuration_saver import AutomationConfigurationSaver
from .constants import (
    AUTOMATION_CONFIGURATIONS, COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)


class AutomationConfiguration(RichAttributeErrorBaseType):
    """
    Automation configuration.
    
    Attributes
    ----------
    community_message_moderation_availability_duration : `int`
        The duration in seconds how of how old messages the feature is available for.
    
    community_message_moderation_down_vote_emoji_id : `int`
        The identifier of the down vote emoji.
    
    community_message_moderation_enabled : `int`
        Whether community message moderation is enabled.
    
    community_message_moderation_up_vote_emoji_id : `int`
        The identifier of the up vote emoji.
    
    community_message_moderation_vote_threshold : `int`
        The required amount of reactions to moderate a message.
    
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
    
    reaction_copy_role_id : `bool`
        Additional role assigned to the `reaction-copy` feature.
    
    touhou_feed_enabled : `bool`
        Whether touhou-feed is enabled in the guild.
    
    welcome_channel_id : `int`
        The channel's identifier where the welcome messages will be sent.
    
    welcome_reply_buttons_enabled : `bool`
        Whether welcome messages should be equipped with a welcome button.
    
    welcome_style_name : `None | str`
        Which welcome style should the client use. By leaving it as `None` the client's default welcome style will be
        used if it has.
    """
    __slots__ = (
        'community_message_moderation_availability_duration', 'community_message_moderation_down_vote_emoji_id',
        'community_message_moderation_enabled', 'community_message_moderation_up_vote_emoji_id', 
        'community_message_moderation_vote_threshold', 'entry_id', 'guild_id', 'log_emoji_channel_id',
        'log_mention_channel_id', 'log_satori_auto_start', 'log_satori_channel_id', 'log_sticker_channel_id',
        'log_user_channel_id', 'reaction_copy_enabled', 'reaction_copy_role_id', 'saver', 'touhou_feed_enabled',
        'welcome_channel_id', 'welcome_reply_buttons_enabled', 'welcome_style_name',
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
        self.community_message_moderation_availability_duration = 0
        self.community_message_moderation_down_vote_emoji_id = 0
        self.community_message_moderation_enabled = False
        self.community_message_moderation_up_vote_emoji_id = 0
        self.community_message_moderation_vote_threshold = 0
        self.entry_id = -1
        self.guild_id = guild_id
        self.log_emoji_channel_id = 0
        self.log_mention_channel_id = 0
        self.log_satori_auto_start = False
        self.log_satori_channel_id = 0
        self.log_sticker_channel_id = 0
        self.log_user_channel_id = 0
        self.reaction_copy_enabled = False
        self.reaction_copy_role_id = 0
        self.saver = None
        self.touhou_feed_enabled = False
        self.welcome_channel_id = 0
        self.welcome_reply_buttons_enabled = False
        self.welcome_style_name = None
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
        
        # community_message_moderation_enabled
        community_message_moderation_enabled = self.community_message_moderation_enabled
        if community_message_moderation_enabled:
            repr_parts.append(', community_message_moderation_enabled = ')
            repr_parts.append(repr(community_message_moderation_enabled))
            
            # community_message_moderation_availability_duration
            community_message_moderation_availability_duration = self.community_message_moderation_availability_duration
            if not community_message_moderation_availability_duration:
                community_message_moderation_availability_duration = (
                    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT
                )
            
            repr_parts.append(', community_message_moderation_availability_duration = ')
            repr_parts.append(repr(community_message_moderation_availability_duration))
            
            # community_message_moderation_down_vote_emoji_id
            community_message_moderation_down_vote_emoji_id = self.community_message_moderation_down_vote_emoji_id
            if not community_message_moderation_down_vote_emoji_id:
                community_message_moderation_down_vote_emoji_id = (
                    COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT
                )
            
            if community_message_moderation_down_vote_emoji_id:
                repr_parts.append(', community_message_moderation_down_vote_emoji_id = ')
                repr_parts.append(repr(community_message_moderation_down_vote_emoji_id))
            
            # community_message_moderation_up_vote_emoji_id
            community_message_moderation_up_vote_emoji_id = self.community_message_moderation_up_vote_emoji_id
            if community_message_moderation_up_vote_emoji_id:
                repr_parts.append(', community_message_moderation_up_vote_emoji_id = ')
                repr_parts.append(repr(community_message_moderation_up_vote_emoji_id))
            
            # community_message_moderation_vote_threshold
            community_message_moderation_vote_threshold = self.community_message_moderation_vote_threshold
            if not community_message_moderation_vote_threshold:
                community_message_moderation_vote_threshold = COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
            
            repr_parts.append(', community_message_moderation_vote_threshold = ')
            repr_parts.append(repr(community_message_moderation_vote_threshold))
        
        
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
            
            reaction_copy_role_id = self.reaction_copy_role_id
            if reaction_copy_role_id:
                repr_parts.append(', reaction_copy_role_id = ')
                repr_parts.append(repr(reaction_copy_role_id))
        
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
            
            # welcome_reply_buttons_enabled
            welcome_reply_buttons_enabled = self.welcome_reply_buttons_enabled
            if welcome_reply_buttons_enabled:
                repr_parts.append(', welcome_reply_buttons_enabled = ')
                repr_parts.append(repr(welcome_reply_buttons_enabled))
            
            welcome_style_name = self.welcome_style_name
            if (welcome_style_name is not None):
                repr_parts.append(', welcome_style_name = ')
                repr_parts.append(repr(welcome_style_name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether any automation configuration is set."""
        community_message_moderation_availability_duration = self.community_message_moderation_availability_duration
        if (
            community_message_moderation_availability_duration != 0 and
            community_message_moderation_availability_duration != COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT
        ):
            return True
        
        community_message_moderation_down_vote_emoji_id = self.community_message_moderation_down_vote_emoji_id
        if (
            community_message_moderation_down_vote_emoji_id != 0 and
            community_message_moderation_down_vote_emoji_id != COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT
        ):
            return True
        
        if self.community_message_moderation_enabled:
            return True
        
        if self.community_message_moderation_up_vote_emoji_id:
            return True
        
        community_message_moderation_vote_threshold = self.community_message_moderation_vote_threshold
        if (
            community_message_moderation_vote_threshold != 0 and
            community_message_moderation_vote_threshold != COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
        ):
            return True
        
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
        
        if self.reaction_copy_role_id:
            return True
        
        if self.touhou_feed_enabled:
            return True
        
        if self.welcome_channel_id:
            return True
        
        if self.welcome_reply_buttons_enabled:
            return True
        
        if self.welcome_style_name is not None:
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
        self.community_message_moderation_availability_duration = entry['community_message_moderation_availability_duration']
        self.community_message_moderation_down_vote_emoji_id = entry['community_message_moderation_down_vote_emoji_id']
        self.community_message_moderation_enabled = entry['community_message_moderation_enabled']
        self.community_message_moderation_up_vote_emoji_id = entry['community_message_moderation_up_vote_emoji_id']
        self.community_message_moderation_vote_threshold = entry['community_message_moderation_vote_threshold']
        self.log_emoji_channel_id = entry['log_emoji_channel_id']
        self.log_mention_channel_id = entry['log_mention_channel_id']
        self.log_satori_auto_start = entry['log_satori_auto_start']
        self.log_satori_channel_id = entry['log_satori_channel_id']
        self.log_sticker_channel_id = entry['log_sticker_channel_id']
        self.log_user_channel_id = entry['log_user_channel_id']
        self.reaction_copy_enabled = entry['reaction_copy_enabled']
        self.reaction_copy_role_id = entry['reaction_copy_role_id']
        self.touhou_feed_enabled = entry['touhou_feed_enabled']
        self.welcome_channel_id = entry['welcome_channel_id']
        self.welcome_reply_buttons_enabled = entry['welcome_reply_buttons_enabled']
        self.welcome_style_name = entry['welcome_style_name']
        
        return self


AUTOMATION_CONFIGURATION_FIELD_SETTERS = {
    'community_message_moderation_availability_duration': (
        AutomationConfiguration.community_message_moderation_availability_duration.__set__
    ),
    'community_message_moderation_down_vote_emoji_id': (
        AutomationConfiguration.community_message_moderation_down_vote_emoji_id.__set__
    ),
    'community_message_moderation_enabled': AutomationConfiguration.community_message_moderation_enabled.__set__,
    'community_message_moderation_up_vote_emoji_id': (
        AutomationConfiguration.community_message_moderation_up_vote_emoji_id.__set__
    ),
    'community_message_moderation_vote_threshold': (
        AutomationConfiguration.community_message_moderation_vote_threshold.__set__
    ),
    
    'log_emoji_channel_id': AutomationConfiguration.log_emoji_channel_id.__set__,
    'log_mention_channel_id': AutomationConfiguration.log_mention_channel_id.__set__,
    'log_sticker_channel_id': AutomationConfiguration.log_sticker_channel_id.__set__,
    'log_user_channel_id': AutomationConfiguration.log_user_channel_id.__set__,
    
    'log_satori_channel_id': AutomationConfiguration.log_satori_channel_id.__set__,
    'log_satori_auto_start': AutomationConfiguration.log_satori_auto_start.__set__,
    
    'reaction_copy_enabled': AutomationConfiguration.reaction_copy_enabled.__set__,
    'reaction_copy_role_id': AutomationConfiguration.reaction_copy_role_id.__set__,
    
    'touhou_feed_enabled': AutomationConfiguration.touhou_feed_enabled.__set__,
    
    'welcome_channel_id': AutomationConfiguration.welcome_channel_id.__set__,
    'welcome_reply_buttons_enabled': AutomationConfiguration.welcome_reply_buttons_enabled.__set__,
    'welcome_style_name': AutomationConfiguration.welcome_style_name.__set__,
}
