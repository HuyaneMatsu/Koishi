__all__ = ()

from hata import CHANNELS

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


def set_automation_configuration(automation_configuration):
    """
    Sets the automation configuration for the given guild.
    
    Parameters
    ----------
    automation_configuration : ``AutomationConfiguration``
        The configuration to set.
    """
    if automation_configuration:
        AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
    else:
        try:
            del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
        except KeyError:
            pass


def delete_automation_configuration_of(guild_id):
    """
    Removes automation configuration of the given guild.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    """
    try:
        del AUTOMATION_CONFIGURATIONS[guild_id]
    except KeyError:
        pass


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
    
    automation_configuration.log_emoji_channel_id = 0
    set_automation_configuration(automation_configuration)
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
    
    automation_configuration.log_mention_channel_id = 0
    set_automation_configuration(automation_configuration)
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
    
    automation_configuration.log_satori_channel_id = 0
    set_automation_configuration(automation_configuration)
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
    
    automation_configuration.log_satori_channel_id = 0
    set_automation_configuration(automation_configuration)
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
    
    automation_configuration.log_sticker_channel_id = 0
    set_automation_configuration(automation_configuration)
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
    
    automation_configuration.log_user_channel_id = 0
    set_automation_configuration(automation_configuration)
    return None


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
    
    automation_configuration.welcome_channel_id = 0
    set_automation_configuration(automation_configuration)
    return None
