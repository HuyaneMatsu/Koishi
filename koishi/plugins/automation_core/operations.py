__all__ = (
    'delete_automation_configuration_of', 'get_automation_configuration_for', 'get_log_emoji_channel',
    'get_log_mention_channel', 'get_log_user_channel', 'get_log_satori_channel', 'get_log_satori_channel_if_auto_start',
    'get_log_sticker_channel', 'get_reaction_copy_enabled', 'get_reaction_copy_enabled_and_role',
    'get_touhou_feed_enabled', 'get_welcome_channel'
)

from hata import CHANNELS, ROLES

from .automation_configuration import AutomationConfiguration
from .constants import AUTOMATION_CONFIGURATIONS


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
    
    log_emoji_channel_id = automation_configuration.log_emoji_channel_id
    if not log_emoji_channel_id:
        return None
    
    try:
        return CHANNELS[log_emoji_channel_id]
    except KeyError:
        pass
    
    automation_configuration.set('log_emoji_channel_id', 0)
    return None


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
    
    log_mention_channel_id = automation_configuration.log_mention_channel_id
    if not log_mention_channel_id:
        return None
    
    try:
        return CHANNELS[log_mention_channel_id]
    except KeyError:
        pass
    
    automation_configuration.set('log_mention_channel_id', 0)
    return None


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
    
    log_satori_channel_id = automation_configuration.log_satori_channel_id
    if not log_satori_channel_id:
        return None
    
    try:
        return CHANNELS[log_satori_channel_id]
    except KeyError:
        pass
    
    automation_configuration.set('log_satori_channel_id', 0)
    return None


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
    
    if not automation_configuration.log_satori_auto_start:
        return None
    
    log_satori_channel_id = automation_configuration.log_satori_channel_id
    if not log_satori_channel_id:
        return None
    
    try:
        return CHANNELS[log_satori_channel_id]
    except KeyError:
        pass
    
    automation_configuration.set('log_satori_channel_id', 0)
    return None


def iter_log_satori_channels():
    """
    Iterates over the satori channels. Will not remove them if they arent found.
    
    This function is an iterable generator.
    
    Yields
    ------
    channel : ``Channel``
    """
    for automation_configuration in AUTOMATION_CONFIGURATIONS.values():
        log_satori_channel_id = automation_configuration.log_satori_channel_id
        if log_satori_channel_id:
            try:
                channel = CHANNELS[log_satori_channel_id]
            except KeyError:
                pass
            else:
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
    
    log_sticker_channel_id = automation_configuration.log_sticker_channel_id
    if not log_sticker_channel_id:
        return None
    
    try:
        return CHANNELS[log_sticker_channel_id]
    except KeyError:
        pass
    
    automation_configuration.set('log_sticker_channel_id', 0)
    return None


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
    
    log_user_channel_id = automation_configuration.log_user_channel_id
    if not log_user_channel_id:
        return None
    
    try:
        return CHANNELS[log_user_channel_id]
    except KeyError:
        pass
    
    automation_configuration.set('log_user_channel_id', 0)
    return None


def get_reaction_copy_enabled(guild_id):
    """
    Gets whether reaction-copy is enabled for the given guild.
    
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
    
    return automation_configuration.reaction_copy_enabled


def get_reaction_copy_enabled_and_role(guild_id):
    """
    Gets whether reaction-copy is enabled for the given guild and the role it is limited to.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    enabled : `bool`
    role : `None`, ``Role``
    """
    try:
        automation_configuration = AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        return False
    
    enabled = automation_configuration.reaction_copy_enabled
    if enabled:
        role_id = automation_configuration.reaction_copy_role_id
        if role_id:
            role = ROLES.get(role_id, None)
        else:
            role = None
    else:
        role = None
    
    return enabled, role


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


def get_welcome_channel(guild_id):
    """
    Gets welcome channel for the given guild.
    
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
    
    welcome_channel_id = automation_configuration.welcome_channel_id
    if not welcome_channel_id:
        return None
    
    try:
        return CHANNELS[welcome_channel_id]
    except KeyError:
        pass
    
    automation_configuration.set('welcome_channel_id', 0)
    return None
