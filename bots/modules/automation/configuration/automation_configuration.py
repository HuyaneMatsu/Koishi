__all__ = ()


from scarletio import RichAttributeErrorBaseType


class AutomationConfiguration(RichAttributeErrorBaseType):
    """
    Automation configuration.
    
    Attributes
    ----------
    guild_id : `int`
        The automation's parent guild identifier.
    log_emoji_channel_id : `int`
        The channel's identifier where the emoji log messages will be sent.
    log_mention_channel_id : `int`
        The channel's identifier where the mention log messages will be sent.
    log_satori_channel_id : `int`
        The channel's identifier where the satori log messages will be sent. Must be a guild category channel.
    log_sticker_channel_id : `int`
        The channel's identifier where the sticker log messages will be sent.
    log_user_channel_id : `int`
        The channel's identifier where the user log messages will be sent.
    welcome_channel_id : `int`
        The channel's identifier where the welcome messages will be sent.
    """
    __slots__ = (
        'guild_id', 'log_emoji_channel_id', 'log_mention_channel_id', 'log_satori_channel_id', 'log_sticker_channel_id',
        'log_user_channel_id', 'welcome_channel_id'
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
        self.log_emoji_channel_id = 0
        self.guild_id = guild_id
        self.log_mention_channel_id = 0
        self.log_satori_channel_id = 0
        self.log_sticker_channel_id = 0
        self.log_user_channel_id = 0
        self.welcome_channel_id = 0
        return self
    
    
    def __repr__(self):
        """Returns the automation configuration's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # log_emoji_channel_id
        log_mention_channel_id = self.log_mention_channel_id
        if log_mention_channel_id:
            repr_parts.append(', log_mention_channel_id = ')
            repr_parts.append(repr(log_mention_channel_id))
        
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
        
        # welcome_channel_id
        welcome_channel_id = self.welcome_channel_id
        if welcome_channel_id:
            repr_parts.append(', welcome_channel_id = ')
            repr_parts.append(repr(welcome_channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether any automation configuration is set."""
        if self.log_mention_channel_id:
            return True
        
        if self.log_mention_channel_id:
            return True
        
        if self.log_satori_channel_id:
            return True
        
        if self.log_sticker_channel_id:
            return True
        
        if self.log_user_channel_id:
            return True
        
        if self.welcome_channel_id:
            return True
        
        return False
