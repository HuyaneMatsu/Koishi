__all__ = ('AutomationConfiguration',)

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxy

from .automation_configuration_saver import AutomationConfigurationSaver
from .constants import (
    AUTOMATION_CONFIGURATIONS, COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)


class AutomationConfiguration(EntryProxy):
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
    
    community_message_moderation_log_enabled : `bool`
        Whether community message moderation actions should be logged.
    
    community_message_moderation_log_channel_id : `int`
        Where should community message moderation actions be logged.
    
    community_message_moderation_up_vote_emoji_id : `int`
        The identifier of the up vote emoji.
    
    community_message_moderation_vote_threshold : `int`
        The required amount of reactions to moderate a message.
    
    entry_id : `int`
        The entry's identifier in the database.
    
    farewell_channel_id : `int`
        The channel's identifier where farewell messages should be ent.
    
    farewell_enabled : `bool`
        Whether farewell messages are enabled.
    
    farewell_style_name : `None | str`
        Which farewell style should the client use. By leaving it as `None` the client's default farewell style will be
        used if it has.
    
    guild_id : `int`
        The automation's parent guild identifier.
    
    log_emoji_channel_id : `int`
        The channel's identifier where the emoji log messages will be sent.
    
    log_emoji_enabled : `bool`
        Whether emoji logging is enabled.
    
    log_mention_channel_id : `int`
        The channel's identifier where the mention log messages will be sent.
    
    log_mention_enabled : `bool`
        Whether mention logging is enabled.
    
    log_satori_auto_start : `bool`
        Whether satori channels should be automatically started.
    
    log_satori_channel_id : `int`
        The channel's identifier where the satori log messages will be sent. Must be a guild category channel.
    
    log_satori_enabled : `bool`
        Whether satori logging is enabled.
    
    log_sticker_channel_id : `int`
        The channel's identifier where the sticker log messages will be sent.
    
    log_sticker_enabled : `bool`
        Whether sticker logging is enabled.
    
    log_user_channel_id : `int`
        The channel's identifier where the user log messages will be sent.
    
    log_user_enabled : `bool`
        Whether user logging is enabled.
    
    reaction_copy_enabled : `bool`
        Whether reaction-copy feature is enabled in the guild.
    
    reaction_copy_flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    reaction_copy_role_id : `bool`
        Additional role assigned to the `reaction-copy` feature.
    
    saver : `None | AutomationConfigurationSaver`
        Saver responsible for save synchronization.
    
    touhou_feed_enabled : `bool`
        Whether touhou-feed is enabled in the guild.
    
    welcome_channel_id : `int`
        The channel's identifier where the welcome messages will be sent.
    
    welcome_enabled : `bool`
        Whether welcoming is enabled.
    
    welcome_reply_buttons_enabled : `bool`
        Whether welcome messages should be equipped with a welcome button.
    
    welcome_style_name : `None | str`
        Which welcome style should the client use. By leaving it as `None` the client's default welcome style will be
        used if it has.
    """
    __slots__ = (
        'community_message_moderation_availability_duration', 'community_message_moderation_down_vote_emoji_id',
        'community_message_moderation_enabled', 'community_message_moderation_log_enabled',
        'community_message_moderation_log_channel_id', 'community_message_moderation_up_vote_emoji_id', 
        'community_message_moderation_vote_threshold', 'farewell_channel_id', 'farewell_enabled',
        'farewell_style_name', 'guild_id', 'log_emoji_channel_id', 'log_emoji_enabled', 'log_mention_channel_id',
        'log_mention_enabled', 'log_satori_auto_start', 'log_satori_channel_id', 'log_satori_enabled',
        'log_sticker_channel_id', 'log_sticker_enabled', 'log_user_channel_id', 'log_user_enabled',
        'reaction_copy_enabled', 'reaction_copy_flags', 'reaction_copy_role_id', 'touhou_feed_enabled',
        'welcome_channel_id', 'welcome_enabled', 'welcome_reply_buttons_enabled', 'welcome_style_name',
    )
    
    saver_type = AutomationConfigurationSaver
    
    
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
        self.community_message_moderation_log_enabled = False
        self.community_message_moderation_log_channel_id = 0
        self.community_message_moderation_up_vote_emoji_id = 0
        self.community_message_moderation_vote_threshold = 0
        self.entry_id = 0
        self.farewell_channel_id = 0
        self.farewell_enabled = False
        self.farewell_style_name = None
        self.guild_id = guild_id
        self.log_emoji_channel_id = 0
        self.log_emoji_enabled = False
        self.log_mention_channel_id = 0
        self.log_mention_enabled = False
        self.log_satori_auto_start = False
        self.log_satori_channel_id = 0
        self.log_satori_enabled = False
        self.log_sticker_channel_id = 0
        self.log_sticker_enabled = False
        self.log_user_channel_id = 0
        self.log_user_enabled = False
        self.reaction_copy_enabled = False
        self.reaction_copy_flags = 0
        self.reaction_copy_role_id = 0
        self.saver = None
        self.touhou_feed_enabled = False
        self.welcome_channel_id = 0
        self.welcome_enabled = False
        self.welcome_reply_buttons_enabled = False
        self.welcome_style_name = None
        return self
    
    
    @copy_docs(EntryProxy._put_repr_parts)
    def _put_repr_parts(self, repr_parts, field_added):
        if field_added:
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
            
            # community_message_moderation_log_enabled
            community_message_moderation_log_enabled = self.community_message_moderation_log_enabled
            if community_message_moderation_log_enabled:
                repr_parts.append(', community_message_moderation_log_enabled = ')
                repr_parts.append(repr(community_message_moderation_log_enabled))
                
                # community_message_moderation_log_channel_id
                community_message_moderation_log_channel_id = self.community_message_moderation_log_channel_id
                if community_message_moderation_log_channel_id:
                    repr_parts.append(', community_message_moderation_log_channel_id = ')
                    repr_parts.append(repr(community_message_moderation_log_channel_id))
        
        
        # log_emoji_enabled
        log_emoji_enabled = self.log_emoji_enabled
        if log_emoji_enabled:
            repr_parts.append(', log_emoji_enabled = ')
            repr_parts.append(repr(log_emoji_enabled))
            
            # log_emoji_channel_id
            log_emoji_channel_id = self.log_emoji_channel_id
            if log_emoji_channel_id:
                repr_parts.append(', log_emoji_channel_id = ')
                repr_parts.append(repr(log_emoji_channel_id))
        
        # log_mention_enabled
        log_mention_enabled = self.log_mention_enabled
        if log_mention_enabled:
            repr_parts.append(', log_mention_enabled = ')
            repr_parts.append(repr(log_mention_enabled))
            
            # log_mention_channel_id
            log_mention_channel_id = self.log_mention_channel_id
            if log_mention_channel_id:
                repr_parts.append(', log_mention_channel_id = ')
                repr_parts.append(repr(log_mention_channel_id))
        
        # log_satori_enabled
        log_satori_enabled = self.log_satori_enabled
        if log_satori_enabled:
            repr_parts.append(', log_satori_enabled = ')
            repr_parts.append(repr(log_satori_enabled))
            
            # log_satori_channel_id
            log_satori_channel_id = self.log_satori_channel_id
            if log_satori_channel_id:
                repr_parts.append(', log_satori_channel_id = ')
                repr_parts.append(repr(log_satori_channel_id))
            
            # log_satori_auto_start
            log_satori_auto_start = self.log_satori_auto_start
            if log_satori_auto_start:
                repr_parts.append(', log_satori_auto_start = ')
                repr_parts.append(repr(log_satori_auto_start))
        
        # log_sticker_enabled
        log_sticker_enabled = self.log_sticker_enabled
        if log_sticker_enabled:
            repr_parts.append(', log_sticker_enabled = ')
            repr_parts.append(repr(log_sticker_enabled))
            
            # log_sticker_channel_id
            log_sticker_channel_id = self.log_sticker_channel_id
            if log_sticker_channel_id:
                repr_parts.append(', log_sticker_channel_id = ')
                repr_parts.append(repr(log_sticker_channel_id))
        
        # log_user_enabled
        log_user_enabled = self.log_user_enabled
        if log_user_enabled:
            repr_parts.append(', log_user_enabled = ')
            repr_parts.append(repr(log_user_enabled))
            
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
            
            reaction_copy_flags = self.reaction_copy_flags
            if reaction_copy_flags:
                repr_parts.append(', reaction_copy_flags = ')
                repr_parts.append(repr(reaction_copy_flags))
            
            reaction_copy_role_id = self.reaction_copy_role_id
            if reaction_copy_role_id:
                repr_parts.append(', reaction_copy_role_id = ')
                repr_parts.append(repr(reaction_copy_role_id))
        
        # touhou_feed_enabled
        touhou_feed_enabled = self.touhou_feed_enabled
        if touhou_feed_enabled:
            repr_parts.append(', touhou_feed_enabled = ')
            repr_parts.append(repr(touhou_feed_enabled))
        
        # welcome_enabled
        welcome_enabled = self.welcome_enabled
        if welcome_enabled:
            repr_parts.append(', welcome_enabled = ')
            repr_parts.append(repr(welcome_enabled))
            
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
        
        # farewell_enabled
        farewell_enabled = self.farewell_enabled
        if farewell_enabled:
            repr_parts.append(', farewell_enabled = ')
            repr_parts.append(repr(farewell_enabled))
            
            # farewell_channel_id
            farewell_channel_id = self.farewell_channel_id
            if farewell_channel_id:
                repr_parts.append(', farewell_channel_id = ')
                repr_parts.append(repr(farewell_channel_id))
            
            farewell_style_name = self.farewell_style_name
            if (farewell_style_name is not None):
                repr_parts.append(', farewell_style_name = ')
                repr_parts.append(repr(farewell_style_name))
    
    
    @copy_docs(EntryProxy.__bool__)
    def __bool__(self):
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
        
        if self.community_message_moderation_log_enabled:
            return True
        
        if self.community_message_moderation_log_channel_id:
            return True
        
        if self.community_message_moderation_up_vote_emoji_id:
            return True
        
        community_message_moderation_vote_threshold = self.community_message_moderation_vote_threshold
        if (
            community_message_moderation_vote_threshold != 0 and
            community_message_moderation_vote_threshold != COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
        ):
            return True
        
        if self.farewell_channel_id:
            return True
        
        if self.farewell_enabled:
            return True
        
        if (self.farewell_style_name is not None):
            return True
        
        if self.log_emoji_channel_id:
            return True
        
        if self.log_emoji_enabled:
            return True
        
        if self.log_mention_channel_id:
            return True
        
        if self.log_mention_enabled:
            return True
        
        if self.log_satori_auto_start:
            return True
        
        if self.log_satori_channel_id:
            return True
        
        if self.log_satori_enabled:
            return True
        
        if self.log_sticker_channel_id:
            return True
        
        if self.log_sticker_enabled:
            return True
        
        if self.log_user_channel_id:
            return True
        
        if self.log_user_enabled:
            return True
        
        if self.reaction_copy_enabled:
            return True
        
        if self.reaction_copy_flags:
            return True
        
        if self.reaction_copy_role_id:
            return True
        
        if self.touhou_feed_enabled:
            return True
        
        if self.welcome_channel_id:
            return True
        
        if self.welcome_enabled:
            return True
        
        if self.welcome_reply_buttons_enabled:
            return True
        
        if self.welcome_style_name is not None:
            return True
        
        return False
    
    
    @copy_docs(EntryProxy._store_in_cache)
    def _store_in_cache(self):
        AUTOMATION_CONFIGURATIONS[self.guild_id] = self
    
    
    @copy_docs(EntryProxy._pop_from_cache)
    def _pop_from_cache(self):
        try:
            del AUTOMATION_CONFIGURATIONS[self.guild_id]
        except KeyError:
            pass
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
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
        self.community_message_moderation_log_enabled = entry['community_message_moderation_log_enabled']
        self.community_message_moderation_log_channel_id = entry['community_message_moderation_log_channel_id']
        self.community_message_moderation_up_vote_emoji_id = entry['community_message_moderation_up_vote_emoji_id']
        self.community_message_moderation_vote_threshold = entry['community_message_moderation_vote_threshold']
        self.farewell_channel_id = entry['farewell_channel_id']
        self.farewell_enabled = entry['farewell_enabled']
        self.farewell_style_name = entry['farewell_style_name']
        self.log_emoji_channel_id = entry['log_emoji_channel_id']
        self.log_emoji_enabled = entry['log_emoji_enabled']
        self.log_mention_channel_id = entry['log_mention_channel_id']
        self.log_mention_enabled = entry['log_mention_enabled']
        self.log_satori_auto_start = entry['log_satori_auto_start']
        self.log_satori_channel_id = entry['log_satori_channel_id']
        self.log_satori_enabled = entry['log_satori_enabled']
        self.log_sticker_channel_id = entry['log_sticker_channel_id']
        self.log_sticker_enabled = entry['log_sticker_enabled']
        self.log_user_channel_id = entry['log_user_channel_id']
        self.log_user_enabled = entry['log_user_enabled']
        self.reaction_copy_enabled = entry['reaction_copy_enabled']
        self.reaction_copy_flags = entry['reaction_copy_flags']
        self.reaction_copy_role_id = entry['reaction_copy_role_id']
        self.touhou_feed_enabled = entry['touhou_feed_enabled']
        self.welcome_channel_id = entry['welcome_channel_id']
        self.welcome_enabled = entry['welcome_enabled']
        self.welcome_reply_buttons_enabled = entry['welcome_reply_buttons_enabled']
        self.welcome_style_name = entry['welcome_style_name']
        
        return self
