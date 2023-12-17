__all__ = ()

from hata import Channel, ChannelType, Client, Permission, Role
from hata.ext.slash import P, abort

from ...bots import FEATURE_CLIENTS, MAIN_CLIENT

from ..automation_core import (
    clear_satori_channel, delete_automation_configuration_of, discover_satori_channel, get_automation_configuration_for,
    get_log_satori_channel, get_reaction_copy_enabled, get_touhou_feed_enabled
)
from ..automation_reaction_copy import build_reaction_copy_about_response, build_reaction_copy_list_channels_response
from ..automation_touhou_feed import (
    TOUHOU_FEED_ABOUT_BUILDERS, TOUHOU_FEED_ABOUT_FIELDS, TOUHOU_FEED_ABOUT_TOPIC_MAIN,
    build_touhou_feed_listing_response, try_remove_guild as touhou_feed_try_remove_guild,
    try_update_guild as touhou_feed_try_update_guild
)
from ..automation_welcome import WELCOME_STYLE_NAMES

from .constants import CHOICE_DEFAULT, LOG_SATORI_ALLOWED_IDS
from .permission_checks import (
    check_channel_and_client_permissions, check_user_permissions, default_channel_and_check_its_guild
)
from .list_all import build_response_list_all


AUTOMATION_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'automation',
    description = 'Automate with koishi ',
    is_global = True,
    required_permissions = Permission().update_by_keys(administrator = True),
)

AUTOMATION_COMMANDS_SATORI = MAIN_CLIENT.interactions(
    None,
    name = 'automation',
    description = 'Automate with koishi ',
    guild = LOG_SATORI_ALLOWED_IDS,
    required_permissions = Permission().update_by_keys(administrator = True),
)


# Read

@AUTOMATION_COMMANDS.interactions
async def list_all(
    event,
):
    """
    Shows the automation configurations.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_user_permissions(event)
    
    guild = event.guild
    if guild is None:
        return abort('Guild out of cache.')
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    
    return build_response_list_all(automation_configuration, guild)


@AUTOMATION_COMMANDS.interactions
async def disable_all(
    event,
):
    """
    Disables all automation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    guild = event.guild
    if (guild is None):
        abort('Guild out of cache.')
    
    # Disable Satori
    satori_channel = get_log_satori_channel(guild.id)
    if (satori_channel is not None):
        clear_satori_channel(satori_channel)
    
    # Disable touhou-feed
    if get_touhou_feed_enabled(guild.id):
        touhou_feed_try_remove_guild(guild)
    
    # Rest is check as we go, so they are fine.
    
    delete_automation_configuration_of(guild.id)
    return 'All automation has been disabled.'


# Emoji Logging

LOG_EMOJI_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-emoji',
    description = 'Enable or disable emoji logging.',
)


@LOG_EMOJI_COMMANDS.interactions(name = 'enable')
async def log_emoji_enable(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Enables emoji logging in the specified channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : `None`, ``Channel`` = `None`, Optional
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    channel = default_channel_and_check_its_guild(event, channel)
    check_channel_and_client_permissions(client, channel)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_emoji_channel_id', channel.id)
    
    return f'Emoji log messages will be sent to {channel:m}.'


@LOG_EMOJI_COMMANDS.interactions(name = 'disable')
async def log_emoji_disable(
    event,
):
    """
    Disables emoji logging.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_emoji_channel_id', 0)
    
    return f'Emoji log messages will not be sent anymore.'


# Mention Logging

LOG_MENTION_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-mention',
    description = 'Enable or disable mention logging.',
)


@LOG_MENTION_COMMANDS.interactions(name = 'enable')
async def log_mention_enable(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Enables mention logging in the specified channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : `None`, ``Channel`` = `None`, Optional
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    channel = default_channel_and_check_its_guild(event, channel)
    check_channel_and_client_permissions(client, channel)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_mention_channel_id', channel.id)
    
    return f'Mention log messages will be sent to {channel:m}.'


@LOG_MENTION_COMMANDS.interactions(name = 'disable')
async def log_mention_disable(
    event,
):
    """
    Disables mention logging.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    This function is a coroutine.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_mention_channel_id', 0)
    
    return f'Mention log messages will not be sent anymore.'

# Satori Logging

LOG_SATORI_COMMANDS = AUTOMATION_COMMANDS_SATORI.interactions(
    None,
    name = 'log-satori',
    description = 'Enable or disable satori logging.',
)


@LOG_SATORI_COMMANDS.interactions(name = 'enable')
async def log_satori_enable(
    event,
    channel: P(
        Channel,
        'Select the category channel to log to.',
        channel_types = [ChannelType.guild_category],
    ),
):
    """
    Enables satori (presence) logging in the specified category.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    channel : `None`, ``Channel``
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    if channel.guild_id != event.guild_id:
        abort('The selected channel\'s guild is from an other guild.')
    
    if not channel.is_guild_category():
        abort('Please select a guild category channel.')
    
    satori_channel = get_log_satori_channel(event.guild_id)
    if (satori_channel is not channel):
        if (satori_channel is not None):
            clear_satori_channel(satori_channel)
        
        discover_satori_channel(channel)
        
        automation_configuration = get_automation_configuration_for(event.guild_id)
        automation_configuration.set('log_satori_channel_id', channel.id)
    
    return f'Satori (presence) log messages will be sent to {channel:m}.'


@LOG_SATORI_COMMANDS.interactions(name = 'disable')
async def log_satori_disable(
    event,
):
    """
    Disables satori logging.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    satori_channel = get_log_satori_channel(event.guild_id)
    if (satori_channel is not None):
        clear_satori_channel(satori_channel)
        
        automation_configuration = get_automation_configuration_for(event.guild_id)
        automation_configuration.set('log_satori_channel_id', 0)
    
    return 'Satori (presence) log messages will not be sent anymore.'


@LOG_SATORI_COMMANDS.interactions(name = 'auto-start')
async def log_satori_auto_start(
    event,
    value: (bool, 'Whether satori channels should be auto started.'),
):
    """
    Enable or disable auto starting satori channels when a user joins.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    value : `bool`
        Whether auto start should be enabled.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_satori_auto_start', value)
    
    return f'Satori channels {"will" if value else "wont"} be auto started when a user joins.'


# Sticker Logging

LOG_STICKER_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-sticker',
    description = 'Enable or disable sticker logging.',
)


@LOG_STICKER_COMMANDS.interactions(name = 'enable')
async def log_sticker_enable(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Enables sticker logging in the specified channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : `None`, ``Channel`` = `None`, Optional
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    channel = default_channel_and_check_its_guild(event, channel)
    check_channel_and_client_permissions(client, channel)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_sticker_channel_id', channel.id)
    
    return f'Sticker log messages will be sent to {channel:m}.'


@LOG_STICKER_COMMANDS.interactions(name = 'disable')
async def log_sticker_disable(
    event,
):
    """
    Disables sticker logging.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_sticker_channel_id', 0)
    
    return f'Sticker log messages will not be sent anymore.'


# User Logging

LOG_USER_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-user',
    description = 'Enable or disable user logging.',
)


@LOG_USER_COMMANDS.interactions(name = 'enable')
async def log_user_enable(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Enables user logging in the specified channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : `None`, ``Channel`` = `None`, Optional
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    channel = default_channel_and_check_its_guild(event, channel)
    check_channel_and_client_permissions(client, channel)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_user_channel_id', channel.id)
    
    return f'User log messages will be sent to {channel:m}.'


@LOG_USER_COMMANDS.interactions(name = 'disable')
async def log_user_disable(
    event,
):
    """
    Disables user logging.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_user_channel_id', 0)
    
    return 'User log messages will not be sent anymore.'

# Reaction copy

REACTION_COPY_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'reaction-copy',
    description = 'Copy messages with reactions',
)


@REACTION_COPY_COMMANDS.interactions(name = 'about')
async def reaction_copy_about(client, event):
    """
    Shows reaction-copy functionality description.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_user_permissions(event)
    return build_reaction_copy_about_response(client, event)


@REACTION_COPY_COMMANDS.interactions(name = 'list-channels')
async def reaction_copy_list_channels(client, event):
    """
    Shows the targetable channels by reaction-copy.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_user_permissions(event)
    
    guild = event.guild
    if guild is None:
        return abort('Guild out of cache.')
    
    return build_reaction_copy_list_channels_response(client, guild, get_reaction_copy_enabled(guild.id))


@REACTION_COPY_COMMANDS.interactions(name = 'enable')
async def reaction_copy_enable(event):
    """
    Enables reaction-copy in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('reaction_copy_enabled', True)
    
    return 'Reaction-copy has been enabled.'


@REACTION_COPY_COMMANDS.interactions(name = 'disable')
async def reaction_copy_disable(event):
    """
    Disables reaction-copy in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('reaction_copy_enabled', False)
    
    return f'Reaction-copy has been disabled.'


@REACTION_COPY_COMMANDS.interactions(name = 'role-set')
async def reaction_copy_role_set(
    event,
    role: (Role, 'select a role.'),
):
    """
    Sets a role for who reaction-copy is additional enabled.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    role : ``Role``
        The role to set.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('reaction_copy_role_id', role.id)
    
    return f'Reaction-copy can be used by users with role {role.name} as well.'


@REACTION_COPY_COMMANDS.interactions(name = 'role-remove')
async def reaction_copy_role_set(
    event,
):
    """
    Sets a role for who reaction-copy is additional enabled.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('reaction_copy_role_id', 0)
    
    return f'Reaction-copy will no logger be additionally available for users with any role.'


# Touhou feed

TOUHOU_FEED_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'touhou-feed',
    description = 'Manage touhou feed.',
)

@TOUHOU_FEED_COMMANDS.interactions(name = 'about')
async def touhou_feed_about(
    client,
    event,
    topic : (TOUHOU_FEED_ABOUT_FIELDS, 'Select a topic to show') = TOUHOU_FEED_ABOUT_TOPIC_MAIN,
):
    """
    Want some help setting up touhou feed?
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    topic : `str` = `TOUHOU_FEED_ABOUT_TOPIC_MAIN`, Optional
        The topic to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_user_permissions(event)
    return TOUHOU_FEED_ABOUT_BUILDERS[topic](client, event)


@TOUHOU_FEED_COMMANDS.interactions(name = 'list-channels')
async def touhou_feed_list_channels(
    client,
    event,
    page: P('int', 'Select a page', min_value = 1, max_value = 100) = 1,
):
    """
    Lists the touhou feed channels.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    page : `int` = `1`, Optional (Keyword only)
        The page to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_user_permissions(event)
    
    guild = event.guild
    if (guild is None):
        abort('Guild out of cache.')
    
    return build_touhou_feed_listing_response(client, guild, page, get_touhou_feed_enabled(guild.id))


@TOUHOU_FEED_COMMANDS.interactions(name = 'enable')
async def touhou_feed_enable(client, event):
    """
    Enables touhou-feed in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    guild = event.guild
    if (guild is None):
        abort('Guild out of cache.')
    
    automation_configuration = get_automation_configuration_for(guild.id)
    automation_configuration.set('touhou_feed_enabled', True)
    
    touhou_feed_try_update_guild(client, guild)
    
    return f'Touhou feed has been enabled.'


@TOUHOU_FEED_COMMANDS.interactions(name = 'disable')
async def touhou_feed_disable(event):
    """
    Disables touhou-feed in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    guild = event.guild
    if (guild is None):
        abort('Guild out of cache.')
    
    automation_configuration = get_automation_configuration_for(guild.id)
    automation_configuration.set('touhou_feed_enabled', False)
    
    touhou_feed_try_remove_guild(guild)
    
    return f'Touhou feed has been disabled.'


# Welcome messages

WELCOME_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'welcome',
    description = 'Enable or disable welcome messages.',
)


@WELCOME_COMMANDS.interactions(name = 'enable')
async def welcome_enable(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to welcome at.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Enables welcome messages in the specified channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : `None`, ``Channel`` = `None`, Optional
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    channel = default_channel_and_check_its_guild(event, channel)
    check_channel_and_client_permissions(client, channel)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('welcome_channel_id', channel.id)
    
    return f'Welcome messages will be sent to {channel:m}.'


@WELCOME_COMMANDS.interactions(name = 'disable')
async def welcome_disable(
    event,
):
    """
    Disables welcome messages.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('welcome_channel_id', 0)
    
    return f'Welcome messages will not be sent anymore.'


@WELCOME_COMMANDS.interactions(name = 'reply-buttons')
async def welcome_reply_buttons(
    event,
    value: (bool, 'Whether reply buttons should shown under welcome messages to reply.'),
):
    """
    Enable or disable putting reply buttons under welcome messages.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    value : `bool`
        Whether auto start should be enabled.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('welcome_reply_buttons_enabled', value)
    
    return f'Welcome reply buttons {"will" if value else "wont"} be put under welcome messages.'


WELCOME_STYLE_CHOICES = [CHOICE_DEFAULT, *WELCOME_STYLE_NAMES]


@WELCOME_COMMANDS.interactions(name = 'style')
async def welcome_style_name(
    event,
    value: (WELCOME_STYLE_CHOICES, 'The welcome style to use to use.'),
):
    """
    Select a custom welcome to use over the default one.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    value : `bool`
        Whether auto start should be enabled.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('welcome_style_name', None if value == CHOICE_DEFAULT else value)
    
    return f'Welcome style set to {value!s}.'
