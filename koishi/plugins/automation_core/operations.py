__all__ = (
    'delete_automation_configuration_of', 'get_automation_configuration_for', 'get_community_message_moderation_fields',
    'get_farewell_fields', 'get_log_emoji_channel', 'get_log_mention_channel', 'get_log_user_channel',
    'get_log_satori_channel', 'get_log_satori_channel_if_auto_start', 'get_log_sticker_channel',
    'get_reaction_copy_fields', 'get_reaction_copy_fields_forced', 'get_touhou_feed_enabled', 'get_welcome_fields',
    'get_welcome_style_name'
)

from hata import CHANNELS, ROLES

from .automation_configuration import AutomationConfiguration
from .constants import (
    AUTOMATION_CONFIGURATIONS, COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)


def get_automation_configuration_for(guild_id):
    """
    Gets automation configuration logic for the given guild identifier.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    automation_configuration : ``AutomationConfiguration``
    """
    try:
        return AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return AutomationConfiguration(guild_id)


def delete_automation_configuration_of(guild_id):
    """
    Removes automation configuration of the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        pass
    else:
        automation_configuration.delete()


def get_log_emoji_channel(guild_id):
    """
    Gets emoji log channel for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    channel : `None`, ``Channel``
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.log_emoji_enabled:
        return None
    
    log_emoji_channel_id = automation_configuration.log_emoji_channel_id
    if not log_emoji_channel_id:
        return None
    
    try:
        channel = CHANNELS[log_emoji_channel_id]
    except KeyError:
        automation_configuration.set('log_emoji_channel_id', 0)
        return None
    
    return channel


def get_log_mention_channel(guild_id):
    """
    Gets mention log channel for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    channel : `None`, ``Channel``
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.log_mention_enabled:
        return None
    
    log_mention_channel_id = automation_configuration.log_mention_channel_id
    if not log_mention_channel_id:
        return None
    
    try:
        channel = CHANNELS[log_mention_channel_id]
    except KeyError:
        automation_configuration.set('log_mention_channel_id', 0)
        return None
    
    return channel


def get_log_satori_channel(guild_id):
    """
    Gets satori log channel for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    channel : `None`, ``Channel``
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.log_satori_enabled:
        return None
    
    log_satori_channel_id = automation_configuration.log_satori_channel_id
    if not log_satori_channel_id:
        return None
    
    try:
        channel = CHANNELS[log_satori_channel_id]
    except KeyError:
        automation_configuration.set('log_satori_channel_id', 0)
        return None
    
    return channel


def get_log_satori_channel_if_auto_start(guild_id):
    """
    Gets satori log channel for the given guild if they should be auto created.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    channel : `None`, ``Channel``
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.log_satori_enabled:
        return None
    
    if not automation_configuration.log_satori_auto_start:
        return None
    
    log_satori_channel_id = automation_configuration.log_satori_channel_id
    if not log_satori_channel_id:
        return None
    
    try:
        channel = CHANNELS[log_satori_channel_id]
    except KeyError:
        automation_configuration.set('log_satori_channel_id', 0)
        return None
    
    return channel


def iter_log_satori_channels():
    """
    Iterates over the satori channels. Will not remove them if they arent found.
    
    This function is an iterable generator.
    
    Yields
    ------
    channel : ``Channel``
    """
    for automation_configuration in AUTOMATION_CONFIGURATIONS.values():
        if not automation_configuration.log_satori_enabled:
            continue
        
        log_satori_channel_id = automation_configuration.log_satori_channel_id
        if not log_satori_channel_id:
            continue
        
        try:
            channel = CHANNELS[log_satori_channel_id]
        except KeyError:
            continue
        
        yield channel


def get_log_sticker_channel(guild_id):
    """
    Gets sticker log channel for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    channel : `None`, ``Channel``
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.log_sticker_enabled:
        return None
    
    log_sticker_channel_id = automation_configuration.log_sticker_channel_id
    if not log_sticker_channel_id:
        return None
    
    try:
        channel = CHANNELS[log_sticker_channel_id]
    except KeyError:
        automation_configuration.set('log_sticker_channel_id', 0)
        return None
    
    return channel


def get_log_user_channel(guild_id):
    """
    Gets user log channel for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    channel : `None`, ``Channel``
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.log_user_enabled:
        return None
    
    log_user_channel_id = automation_configuration.log_user_channel_id
    if not log_user_channel_id:
        return None
    
    try:
        channel = CHANNELS[log_user_channel_id]
    except KeyError:
        automation_configuration.set('log_user_channel_id', 0)
        return None
    
    return channel


def get_reaction_copy_fields(guild_id):
    """
    Gets whether reaction-copy fields. Returns `None` if reaction-copy is disabled.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    fields : `None | (None | Role, int)`
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    enabled = automation_configuration.reaction_copy_enabled
    if not enabled:
        return None
    
    flags = automation_configuration.reaction_copy_flags
    if not flags:
        return None
    
    role_id = automation_configuration.reaction_copy_role_id
    if not role_id:
        role = None
    
    else:
        try:
            role = ROLES[role_id]
        except KeyError:
            automation_configuration.set('reaction_copy_role_id', 0)
            role = None
        
    return role, flags


def get_reaction_copy_fields_forced(guild_id):
    """
    Gets all reaction-copy fields even if disabled.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    fields : `(bool, None | Role, int)`
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return False, None, 0
    
    role_id = automation_configuration.reaction_copy_role_id
    if not role_id:
        role = None
    
    else:
        try:
            role = ROLES[role_id]
        except KeyError:
            automation_configuration.set('reaction_copy_role_id', 0)
            role = None
    
    return (
        automation_configuration.reaction_copy_enabled,
        role,
        automation_configuration.reaction_copy_flags,
    )


def get_touhou_feed_enabled(guild_id):
    """
    Gets whether touhou-feed is enabled for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    enabled : `bool`
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return False
    
    return automation_configuration.touhou_feed_enabled


def get_welcome_fields(guild_id):
    """
    Gets welcome channel, whether the welcome button is enabled and the farewell style for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    welcome_fields : `None | (Channel, bool, None | str)`
        Returns `None` if disabled. A tuple of `welcome_channel`, `welcome_reply_buttons_enabled`, `welcome_style_name`
        if enabled.
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.welcome_enabled:
        return None
    
    welcome_channel_id = automation_configuration.welcome_channel_id
    if not welcome_channel_id:
        return None
    
    try:
        channel = CHANNELS[welcome_channel_id]
    except KeyError:
        automation_configuration.set('welcome_channel_id', 0)
        return None
    
    return (
        channel,
        automation_configuration.welcome_reply_buttons_enabled,
        automation_configuration.welcome_style_name,
    )


def get_welcome_style_name(guild_id):
    """
    Returns the selected welcome style's name of the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    welcome_style_name : `None | str`
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    return automation_configuration.welcome_style_name


def get_community_message_moderation_fields(guild_id):
    """
    Gets community message moderation fields for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    community_message_moderation_fields : `None | (int, int, int, int, None | Channel)`
        Returns `None` if disabled. A tuple of `down_vote_emoji_id`, `up_vote_emoji_id`, `availability_duration`,
        `vote_threshold`, `log_channel` if enabled.
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.community_message_moderation_enabled:
        return None
    
    community_message_moderation_log_enabled = automation_configuration.community_message_moderation_log_enabled
    if not community_message_moderation_log_enabled:
        log_channel = None
    else:
        community_message_moderation_log_channel_id = automation_configuration.community_message_moderation_log_channel_id
        if not community_message_moderation_log_channel_id:
            log_channel = None
        else:
            try:
                log_channel = CHANNELS[community_message_moderation_log_channel_id]
            except KeyError:
                automation_configuration.set('community_message_moderation_log_channel_id', 0)
                log_channel = None
    
    return (
        (
            automation_configuration.community_message_moderation_down_vote_emoji_id or 
            COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT
        ),
        automation_configuration.community_message_moderation_up_vote_emoji_id,
        (
            automation_configuration.community_message_moderation_availability_duration or
            COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT
        ),
        (
            automation_configuration.community_message_moderation_vote_threshold or
            COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
        ),
        log_channel,
    )


def get_farewell_fields(guild_id):
    """
    Gets farewell channel and the farewell style for the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    farewell_fields : `None | (Channel, None | str)`
        Returns `None` if disabled. A tuple of `farewell_channel`, `farewell_style_name` if enabled.
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return None
    
    if not automation_configuration.farewell_enabled:
        return None
    
    farewell_channel_id = automation_configuration.farewell_channel_id
    if not farewell_channel_id:
        return None
    
    try:
        channel = CHANNELS[farewell_channel_id]
    except KeyError:
        automation_configuration.set('farewell_channel_id', 0)
        return None
    
    return (
        channel,
        automation_configuration.farewell_style_name,
    )
