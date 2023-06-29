__all__ = ()

from hata import CHANNELS, Channel, ChannelType, Client, Permission
from hata.ext.slash import P, abort

from bot_utils.constants import GUILD__ORIN_PARTY_HOUSE, GUILD__SUPPORT
from bots import SLASH_CLIENT

from .configuration.operations import (
    delete_automation_configuration_of, get_automation_configuration_for, get_log_satori_channel,
    set_automation_configuration
)
from .configuration.satori import clear_satori_channel, discover_satori_channel



def check_user_permissions(event):
    """
    Checks whether the user has permission to use this command.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    """
    if not event.user_permissions.can_administrator:
        abort('You must have administrator permission to use this command.')


def default_channel_and_check_its_guild(event, channel):
    """
    Defaults the selected channel
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    channel : `None`, ``Channel``
        The selected channel
    
    Returns
    -------
    channel : ``Channel``
    """
    if channel is None:
        channel = event.channel
    
    if channel.guild_id != event.guild_id:
        abort('The selected channel\'s guild is from an other guild.')
    
    return channel


def check_channel_and_client_permissions(client, channel):
    """
    Checks the channel and the client's permissions in it.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel : ``Channel``
        The channel to log into.
    """
    if not channel.is_in_group_guild_system():
        abort('Please select a guild system channel.')
    
    if not channel.cached_permissions_for(client).can_send_messages:
        abort('I cannot send messages into the selected channel.')


def get_channel_mention(channel_id):
    """
    Gets channel mention for the given identifier.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    
    Returns
    -------
    mention : `str`
    """
    if channel_id:
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            pass
        else:
            return channel.mention
    
    return 'unset'


def get_bool(value):
    """
    Gets the boolean's representation.
    
    Parameters
    ----------
    value : `bool`
        The value to get its representation of.
    
    Returns
    -------
    representation : `str`
    """
    return 'true' if value else 'false'


AUTOMATION_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'automation',
    description = 'Automate logging with koishi ',
    guild = [GUILD__ORIN_PARTY_HOUSE, GUILD__SUPPORT, 866746184990720020],
    required_permissions = Permission().update_by_keys(administrator = True),
)

# Read

@AUTOMATION_COMMANDS.interactions.interactions(show_for_invoking_user_only = True)
async def show_all(
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
    response : `str`
    """
    check_user_permissions(event)
    automation_configuration = get_automation_configuration_for(event.guild_id)
    
    return (
        f'**Logging**\n'
        f'- Emoji: {get_channel_mention(automation_configuration.log_emoji_channel_id)}\n'
        f'- Mention: {get_channel_mention(automation_configuration.log_mention_channel_id)}\n'
        f'- Satori: {get_channel_mention(automation_configuration.log_satori_channel_id)}\n'
        f'  - Auto start: {get_bool(automation_configuration.log_satori_auto_start)}\n'
        f'- Sticker: {get_channel_mention(automation_configuration.log_sticker_channel_id)}\n'
        f'- User: {get_channel_mention(automation_configuration.log_user_channel_id)}\n'
        f'\n'
        f'**Welcome**\n'
        f'{get_channel_mention(automation_configuration.welcome_channel_id)}\n'
    )


@AUTOMATION_COMMANDS.interactions.interactions(show_for_invoking_user_only = True)
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
    
    satori_channel = get_log_satori_channel(event.guild_id)
    if (satori_channel is not None):
        clear_satori_channel(satori_channel)
    
    delete_automation_configuration_of(event.guild_id)
    return 'All automation has been disabled.'


# Emoji Logging

LOG_EMOJI_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-emoji',
    description = 'Enable or disable emoji logging.',
)


@LOG_EMOJI_COMMANDS.interactions(show_for_invoking_user_only = True)
async def enable(
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
    automation_configuration.log_emoji_channel_id = channel.id
    set_automation_configuration(automation_configuration)
    
    return f'Emoji log messages will be sent to {channel:m}.'


@LOG_EMOJI_COMMANDS.interactions(show_for_invoking_user_only = True)
async def disable(
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
    automation_configuration.log_emoji_channel_id = 0
    set_automation_configuration(automation_configuration)
    
    return f'Emoji log messages will not be sent anymore.'


# Mention Logging

LOG_MENTION_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-mention',
    description = 'Enable or disable mention logging.',
)


@LOG_MENTION_COMMANDS.interactions(show_for_invoking_user_only = True)
async def enable(
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
    automation_configuration.log_mention_channel_id = channel.id
    set_automation_configuration(automation_configuration)
    
    return f'Mention log messages will be sent to {channel:m}.'


@LOG_MENTION_COMMANDS.interactions(show_for_invoking_user_only = True)
async def disable(
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
    automation_configuration.log_mention_channel_id = 0
    set_automation_configuration(automation_configuration)
    
    return f'Mention log messages will not be sent anymore.'

# Satori Logging

LOG_SATORI_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-satori',
    description = 'Enable or disable satori logging.',
)


@LOG_SATORI_COMMANDS.interactions(show_for_invoking_user_only = True)
async def enable(
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
        automation_configuration.log_satori_channel_id = channel.id
        set_automation_configuration(automation_configuration)
    
    return f'Satori (presence) log messages will be sent to {channel:m}.'


@LOG_SATORI_COMMANDS.interactions(show_for_invoking_user_only = True)
async def disable(
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
        automation_configuration.log_satori_channel_id = 0
        set_automation_configuration(automation_configuration)
    
    return f'Satori (presence) log messages will not be sent anymore.'


@LOG_SATORI_COMMANDS.interactions(show_for_invoking_user_only = True)
async def auto_start(
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
    automation_configuration.log_satori_auto_start = value
    set_automation_configuration(automation_configuration)
    
    return f'Satori channels {"will" if value else "wont"} be auto started when a user joins.'


# Sticker Logging

LOG_STICKER_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-sticker',
    description = 'Enable or disable sticker logging.',
)


@LOG_STICKER_COMMANDS.interactions(show_for_invoking_user_only = True)
async def enable(
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
    automation_configuration.log_sticker_channel_id = channel.id
    set_automation_configuration(automation_configuration)
    
    return f'Sticker log messages will be sent to {channel:m}.'


@LOG_STICKER_COMMANDS.interactions(show_for_invoking_user_only = True)
async def disable(
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
    automation_configuration.log_sticker_channel_id = 0
    set_automation_configuration(automation_configuration)
    
    return f'Sticker log messages will not be sent anymore.'


# User Logging

LOG_USER_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'log-user',
    description = 'Enable or disable user logging.',
)


@LOG_USER_COMMANDS.interactions(show_for_invoking_user_only = True)
async def enable(
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
    automation_configuration.log_user_channel_id = channel.id
    set_automation_configuration(automation_configuration)
    
    return f'User log messages will be sent to {channel:m}.'


@LOG_USER_COMMANDS.interactions(show_for_invoking_user_only = True)
async def disable(
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
    automation_configuration.log_user_channel_id = 0
    set_automation_configuration(automation_configuration)
    
    return f'User log messages will not be sent anymore.'



# Welcome messages

WELCOME_COMMANDS = AUTOMATION_COMMANDS.interactions(
    None,
    name = 'welcome',
    description = 'Enable or disable welcome messages.',
)


@WELCOME_COMMANDS.interactions(show_for_invoking_user_only = True)
async def enable(
    client,
    event,
    channel: P(
        Channel,
        'Select the channel to log to.',
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
    automation_configuration.welcome_channel_id = channel.id
    set_automation_configuration(automation_configuration)
    
    return f'Welcome messages will be sent to {channel:m}.'


@WELCOME_COMMANDS.interactions(show_for_invoking_user_only = True)
async def disable(
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
    automation_configuration.welcome_channel_id = 0
    set_automation_configuration(automation_configuration)
    
    return f'Welcome messages will not be sent anymore.'
