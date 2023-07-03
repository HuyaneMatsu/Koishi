__all__ = ()

from hata import CHANNELS, Embed
from hata.ext.slash import InteractionResponse

from .constants import LOG_SATORI_ALLOWED_IDS


def get_channel_representation(channel_id):
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


def get_bool_representation(value):
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
    return 'enabled' if value else 'disabled'



def render_logging_description(automation_configuration):
    """
    Renders the logging field's description.
    
    Parameters
    ----------
    automation_configuration : ``AutomationConfiguration``
        The automation configuration to render.
    
    Returns
    -------
    description : `str`
    """
    description_parts = []
    
    description_parts.append(
        '- Emoji: '
    )
    description_parts.append(get_channel_representation(automation_configuration.log_emoji_channel_id))
    description_parts.append(
        '\n'
        '- Mention: ')
    description_parts.append(get_channel_representation(automation_configuration.log_mention_channel_id))
    
    # Render satori only if allowed in the guild
    if automation_configuration.guild_id in LOG_SATORI_ALLOWED_IDS:
        description_parts.append(
        '\n'
        '- Satori: '
        )
        description_parts.append(get_channel_representation(automation_configuration.log_satori_channel_id))
        description_parts.append(
            '\n'
            f'  - Auto start: '
        )
        description_parts.append(get_bool_representation(automation_configuration.log_satori_auto_start))
    
    description_parts.append(
        '\n'
        f'- Sticker: '
    )
    description_parts.append(get_channel_representation(automation_configuration.log_sticker_channel_id))
    description_parts.append(
        '\n'
        '- User: '
    )
    description_parts.append(get_channel_representation(automation_configuration.log_user_channel_id))
    
    return ''.join(description_parts)


def build_response_show_all(automation_configuration, guild):
    """
    Builds `show-all` command response.
    
    Parameters
    ----------
    automation_configuration : ``AutomationConfiguration``
        The configuration to show.
    guild : ``Guild``
        The guild the automation configuration is bound to.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    embed = Embed(
        f'{guild.name}\'s automations',
    ).add_thumbnail(
        guild.icon_url,
    ).add_field(
        'Logging',
        render_logging_description(automation_configuration),
    ).add_field(
        'Reaction-copy',
        get_bool_representation(automation_configuration.reaction_copy_enabled),
    ).add_field(
        'Touhou-feed',
        get_bool_representation(automation_configuration.touhou_feed_enabled),
    ).add_field(
        'Welcome',
        f'Channel: {get_channel_representation(automation_configuration.welcome_channel_id)}',
    )
    
    return InteractionResponse(
        embed = embed,
    )
