__all__ = ()

from hata import CHANNELS, Channel, ChannelType, Client, Permission, Role, parse_emoji
from hata.ext.slash import P, abort

from ...bots import FEATURE_CLIENTS, MAIN_CLIENT

from ..automation_core import (
    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT, COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_MAX,
    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_MIN, COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MAX,
    COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MIN, clear_satori_channel, delete_automation_configuration_of,
    discover_satori_channel, get_automation_configuration_for, get_log_satori_channel, get_reaction_copy_fields_forced,
    get_touhou_feed_enabled
)
from ..automation_farewell import FAREWELL_STYLE_NAMES
from ..automation_reaction_copy import (
    MASK_PARSE_NAME_UNICODE, MASK_PARSE_TOPIC_CUSTOM, MASK_PARSE_TOPIC_UNICODE, build_reaction_copy_about_response,
    build_reaction_copy_list_channels_response, get_reaction_copy_flag_parse_names
)
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
from .representation_getters import get_duration_representation, get_emoji_representation


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


@LOG_EMOJI_COMMANDS.interactions(name = 'state')
async def log_emoji_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Set emoji logging state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_emoji_enabled', state == 'enabled')
    
    return f'Emoji logging has been {state!s}.'


@LOG_EMOJI_COMMANDS.interactions(name = 'channel')
async def log_emoji_set_channel(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Define to which channel should emoji log messages be sent to.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
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


# Mention Logging

LOG_MENTION_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-mention',
    description = 'Enable or disable mention logging.',
)


@LOG_MENTION_COMMANDS.interactions(name = 'state')
async def log_mention_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Set mention logging state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_mention_enabled', state == 'enabled')
    
    return f'Mention logging has been {state!s}.'


@LOG_MENTION_COMMANDS.interactions(name = 'channel')
async def log_mention_set_channel(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Define to which channel should mention log messages be sent to.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
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


# Satori Logging

LOG_SATORI_COMMANDS = AUTOMATION_COMMANDS_SATORI.interactions(
    None,
    name = 'log-satori',
    description = 'Enable or disable satori logging.',
)


@LOG_SATORI_COMMANDS.interactions(name = 'state')
async def log_satori_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Set satori (presence) logging state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    enable = state == 'enabled'
    automation_configuration = get_automation_configuration_for(event.guild_id)
    if enable != automation_configuration.log_satori_enabled:
        log_satori_channel_id = automation_configuration.log_satori_channel_id
        if not log_satori_channel_id:
            log_satori_channel = None
        else:
            log_satori_channel = CHANNELS.get(log_satori_channel_id, None)
        
        if (log_satori_channel is not None):
            if enable:
                discover_satori_channel(log_satori_channel)
            else:
                clear_satori_channel(log_satori_channel)
        
        automation_configuration.set('log_satori_enabled', enable)
    
    return f'Satori logging has been {state!s}.'


@LOG_SATORI_COMMANDS.interactions(name = 'channel')
async def log_satori_set_channel(
    event,
    channel: P(
        Channel,
        'Select the category channel to log to.',
        channel_types = [ChannelType.guild_category],
    ),
):
    """
    Define in which category should satori work in.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
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
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    if automation_configuration.log_satori_enabled:
        log_satori_channel_id = automation_configuration.log_satori_channel_id
        if not log_satori_channel_id:
            log_satori_channel = None
        else:
            log_satori_channel = CHANNELS.get(log_satori_channel_id, None)
        
        if (log_satori_channel is not None):
            clear_satori_channel(log_satori_channel)
        
        discover_satori_channel(log_satori_channel)
    
    automation_configuration.set('log_satori_channel_id', channel.id)
    
    return f'Satori log messages will be sent under {channel:m}.'


@LOG_SATORI_COMMANDS.interactions(name = 'auto-start')
async def log_satori_auto_start(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Enable or disable auto starting satori channels when a user joins.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    enabled = state == 'enabled'
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_satori_auto_start', enabled)
    
    return f'Satori channels {"will" if enabled else "wont"} be auto started when a user joins.'


# Sticker Logging

LOG_STICKER_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-sticker',
    description = 'Enable or disable sticker logging.',
)


@LOG_STICKER_COMMANDS.interactions(name = 'state')
async def log_sticker_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Set sticker logging state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_sticker_enabled', state == 'enabled')
    
    return f'Sticker logging has been {state!s}.'


@LOG_STICKER_COMMANDS.interactions(name = 'channel')
async def log_sticker_set_channel(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Define to which channel should sticker log messages be sent to.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
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


# User Logging

LOG_USER_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-user',
    description = 'Enable or disable user logging.',
)


@LOG_USER_COMMANDS.interactions(name = 'state')
async def log_user_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Set user logging state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('log_user_enabled', state == 'enabled')
    
    return f'User logging has been {state!s}.'


@LOG_USER_COMMANDS.interactions(name = 'channel')
async def log_user_set_channel(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Define to which channel should user log messages be sent to.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
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
    
    enabled, role, flags = get_reaction_copy_fields_forced(guild.id)
    return build_reaction_copy_list_channels_response(guild, enabled, flags)


@REACTION_COPY_COMMANDS.interactions(name = 'state')
async def reaction_copy_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Enables reaction-copy in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('reaction_copy_enabled', state == 'enabled')
    
    return f'Reaction-copy has been {state!s}.'


@REACTION_COPY_COMMANDS.interactions(name = 'role')
async def reaction_copy_set_role(
    event,
    role: (Role, 'select a role.') = None,
):
    """
    Sets a role for who reaction-copy is additional enabled.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    role : `None | Role` = `None`, Optional
        The role to set.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    
    automation_configuration.set('reaction_copy_role_id', 0 if role is None else role.id)
    
    if role is None:
        return f'Reaction-copy will no logger be additionally available for users with any role.'
    
    return f'Reaction-copy can be used by users with role {role.name} as well.'



@REACTION_COPY_COMMANDS.interactions(name = 'parse')
async def reaction_copy_set_parse(
    event,
    name_unicode : (bool, 'Whether to parse unicode emojis from name.') = None,
    topic_custom : (bool, 'Whether to parse custom emojis from topic.') = None,
    topic_unicode : (bool, 'Whether to parse unicode emojis from topic.') = None,
):
    """
    Sets parse rules.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    name_unicode : `None | bool` = `None`, Optional
        Whether to parse unicode emojis from name.
    topic_custom : `None | bool` = `None`, Optional
        Whether to parse custom emojis from topic.
    topic_unicode : `None | bool` = `None`, Optional
        Whether to parse unicode emojis from topic.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    flags = automation_configuration.reaction_copy_flags
    
    # calculate new flags value
    for value, mask in (
        (name_unicode, MASK_PARSE_NAME_UNICODE),
        (topic_custom, MASK_PARSE_TOPIC_CUSTOM),
        (topic_unicode, MASK_PARSE_TOPIC_UNICODE),
    ):
        if value is None:
            continue
        
        if value:
            flags |= mask
        else:
            flags &= ~mask
    
    automation_configuration.set('reaction_copy_flags', flags)
    
    return f'Reaction-copy has been set to: {get_reaction_copy_flag_parse_names(flags)!s}.'


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


@TOUHOU_FEED_COMMANDS.interactions(name = 'state')
async def touhou_feed_set_state(
    client,
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Enables touhou-feed in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    guild = event.guild
    if (guild is None):
        abort('Guild out of cache.')
    
    enable = state == 'enabled'
    
    automation_configuration = get_automation_configuration_for(guild.id)
    automation_configuration.set('touhou_feed_enabled', enable)
    
    if state == enable:
        touhou_feed_try_update_guild(client, guild)
    else:
        touhou_feed_try_remove_guild(guild)
    
    return f'Touhou feed has been {state!s}.'

# Welcome messages

WELCOME_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'welcome',
    description = 'Enable or disable welcome messages.',
)


@WELCOME_COMMANDS.interactions(name = 'state')
async def welcome_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Sets welcoming state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('welcome_enabled', state == 'enabled')
    
    return f'Welcoming has been {state!s}.'


@WELCOME_COMMANDS.interactions(name = 'channel')
async def welcome_set_channel(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to welcome at.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Define to which channel should welcome messages be sent to.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
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



@WELCOME_COMMANDS.interactions(name = 'reply-buttons')
async def welcome_set_reply_buttons(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Enable or disable putting reply buttons under welcome messages.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    enabled = state == 'enabled'
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('welcome_reply_buttons_enabled', enabled)
    
    return f'Welcome reply buttons {"will" if enabled else "wont"} be put under welcome messages.'


WELCOME_STYLE_CHOICES = [CHOICE_DEFAULT, *WELCOME_STYLE_NAMES]


@WELCOME_COMMANDS.interactions(name = 'style')
async def welcome_set_style_name(
    event,
    value: (WELCOME_STYLE_CHOICES, 'The welcome style to use to use.'),
):
    """
    Select a custom welcome to use over the default one.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    value : `str`
        Welcome style name.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('welcome_style_name', None if value == CHOICE_DEFAULT else value)
    
    return f'Welcome style set to {value!s}.'


# Farewell messages

FAREWELL_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'farewell',
    description = 'Enable or disable farewell messages.',
)


@FAREWELL_COMMANDS.interactions(name = 'state')
async def farewell_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Sets farewelling state.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('farewell_enabled', state == 'enabled')
    
    return f'Welcoming has been {state!s}.'


@FAREWELL_COMMANDS.interactions(name = 'channel')
async def farewell_set_channel(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to farewell at.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Define to which channel should farewell messages be sent to.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    channel = default_channel_and_check_its_guild(event, channel)
    check_channel_and_client_permissions(client, channel)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('farewell_channel_id', channel.id)
    
    return f'Farewell messages will be sent to {channel:m}.'


FAREWELL_STYLE_CHOICES = [CHOICE_DEFAULT, *FAREWELL_STYLE_NAMES]


@FAREWELL_COMMANDS.interactions(name = 'style')
async def farewell_set_style_name(
    event,
    value: (FAREWELL_STYLE_CHOICES, 'The farewell style to use to use.'),
):
    """
    Select a custom farewell to use over the default one.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    value : `str`
        Farewell style name.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('farewell_style_name', None if value == CHOICE_DEFAULT else value)
    
    return f'Farewell style set to {value!s}.'


# Community message moderation

COMMUNITY_MESSAGE_MODERATION_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'community-message-moderation',
    description = 'Configure community message moderation.',
)

@COMMUNITY_MESSAGE_MODERATION_COMMANDS.interactions(name = 'state')
async def community_message_moderation_set_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Enable or disable community message moderation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `bool`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('community_message_moderation_enabled', state == 'enabled')
    
    return f'Community message moderation has been {state!s}.'


@COMMUNITY_MESSAGE_MODERATION_COMMANDS.interactions(name = 'availability-duration')
async def community_message_moderation_set_availability_duration(
    event,
    hours : P(int, 'Duration in hours.', min_value = 0, max_value = 24) = 0,
    minutes : P(int, 'Duration in minutes.', min_value = 0, max_value = 60) = 0,
    seconds : P(int, 'Duration in seconds.', min_value = 0, max_value = 60) = 0,
):
    """
    Sets the availability duration of community message moderation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    hours : `int` = `0`, Optional
        Duration in hours.
    minutes : `int` = `0`, Optional
        Duration in minutes.
    seconds : `int` = `0`, Optional
        Duration in seconds.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    duration = seconds + minutes * 60 + hours * 3600
    
    if duration == 0:
        duration = COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT
        case = ' (default value)'
    elif duration >= COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_MAX:
        duration = COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_MAX
        case = ' (max value)'
    elif duration <= COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_MIN:
        duration = COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_MIN
        case = ' (min value)'
    else:
        case = ''
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('community_message_moderation_availability_duration', duration)
    
    return (
        f'Community message moderation availability duration has been set to: '
        f'{get_duration_representation(duration)!s}{case}.'
    )


@COMMUNITY_MESSAGE_MODERATION_COMMANDS.interactions(name = 'down-vote-emoji')
async def community_message_moderation_set_down_vote_emoji_id(
    event,
    emoji_value : P(str, 'The emoji to set to.', name = 'emoji') = None,
):
    """
    Sets the down vote emoji of community message moderation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    emoji_value : `None | str` = `None`, Optional
        The emoji to set to.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    if emoji_value is None:
        emoji = COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_DEFAULT
    else:
        emoji = parse_emoji(emoji_value)
        if emoji is None:
            abort(f'Could not identify {emoji_value!s} as an emoji.')
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('community_message_moderation_down_vote_emoji_id', emoji.id)
    
    return f'Community message moderation down vote emoji set to: {get_emoji_representation(emoji)!s}.'


@COMMUNITY_MESSAGE_MODERATION_COMMANDS.interactions(name = 'up-vote-emoji')
async def community_message_moderation_set_up_vote_emoji_id(
    event,
    emoji_value : P(str, 'The emoji to set to.', name = 'emoji') = None,
):
    """
    Sets the up vote emoji of community message moderation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    emoji_value : `None | str` = `None`, Optional
        The emoji to set to.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    if emoji_value is None:
        emoji = None
    else:
        emoji = parse_emoji(emoji_value)
        if emoji is None:
            abort(f'Could not identify {emoji_value!s} as an emoji.')
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('community_message_moderation_up_vote_emoji_id', 0 if emoji is None else emoji.id)
    
    return f'Community message moderation up vote emoji set to: {get_emoji_representation(emoji)!s}.'


@COMMUNITY_MESSAGE_MODERATION_COMMANDS.interactions(name = 'vote-threshold')
async def community_message_moderation_set_vote_threshold(
    event,
    threshold : P(
        int,
        'Vote threshold to delete the message.',
        min_value = COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MIN,
        max_value = COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MAX,
    ) = 0,
):
    """
    Sets the vote threshold of community message moderation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    threshold : `int` = `0`, Optional
        Duration in hours.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    if threshold == 0:
        threshold = COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
        case = ' (default value)'
    elif threshold >= COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MAX:
        threshold = COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MAX
        case = ' (max value)'
    elif threshold <= COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MIN:
        threshold = COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_MIN
        case = ' (min value)'
    else:
        case = ''
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('community_message_moderation_vote_threshold', threshold)
    
    return f'Community message moderation vote threshold has been set to: {threshold!s}{case}.'


@COMMUNITY_MESSAGE_MODERATION_COMMANDS.interactions(name = 'log-state')
async def community_message_moderation_set_log_state(
    event,
    state : (['enabled', 'disabled'], 'Enable or disable.'),
):
    """
    Enable or disable community message moderation logging.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    state : `str`
        Whether to enable to disable it.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('community_message_moderation_log_enabled', state == 'enabled')
    
    return f'Community message moderation logging has been {state!s}.'


@COMMUNITY_MESSAGE_MODERATION_COMMANDS.interactions(name = 'log-channel')
async def community_message_moderation_set_log_channel(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
        channel_types = [ChannelType.guild_text, ChannelType.guild_announcements],
    ) = None,
):
    """
    Sets community message moderation log channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    channel : ``None | Channel`` = `None`, Optional
        The channel to log into.
    
    Returns
    -------
    response : `str`
    """
    check_user_permissions(event)
    channel = default_channel_and_check_its_guild(event, channel)
    check_channel_and_client_permissions(client, channel)
    
    automation_configuration = get_automation_configuration_for(event.guild_id)
    automation_configuration.set('community_message_moderation_log_channel_id', channel.id)
    
    return f'Community message moderation log messages will be sent to {channel:m}.'
