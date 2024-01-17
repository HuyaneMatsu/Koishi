__all__ = ()

from hata import Embed
from hata.ext.slash import InteractionResponse

from ..automation_core import (
    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT, COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)

from .constants import LOG_SATORI_ALLOWED_IDS
from .representation_getters import (
    get_bool_representation, get_channel_representation, get_choice_representation, get_duration_representation,
    get_emoji_id_representation, get_role_representation
)


def render_logging_description(automation_configuration):
    """
    Renders the logging fields' description.
    
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
        '- Mention: '
    )
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


def render_community_message_moderation_description(automation_configuration):
    """
    Renders the community message moderation fields' description.
    
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
        'State: '
    )
    description_parts.append(get_bool_representation(automation_configuration.community_message_moderation_enabled))
    
    
    description_parts.append(
        '\n'
        'Down vote emoji: '
    )
    community_message_moderation_down_vote_emoji_id = (
        automation_configuration.community_message_moderation_down_vote_emoji_id
    )
    if not community_message_moderation_down_vote_emoji_id:
        community_message_moderation_down_vote_emoji_id = COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT
    description_parts.append(get_emoji_id_representation(community_message_moderation_down_vote_emoji_id))
    
    
    description_parts.append(
        '\n'
        'Up vote emoji: '
    )
    community_message_moderation_up_vote_emoji_id = (
        automation_configuration.community_message_moderation_up_vote_emoji_id
    )
    description_parts.append(get_emoji_id_representation(community_message_moderation_up_vote_emoji_id))
    
    
    description_parts.append(
        '\n'
        'Availability duration: '
    )
    community_message_moderation_availability_duration = (
        automation_configuration.community_message_moderation_availability_duration
    )
    if not community_message_moderation_availability_duration:
        community_message_moderation_availability_duration = COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT
    description_parts.append(get_duration_representation(community_message_moderation_availability_duration))
    
    
    description_parts.append(
        '\n'
        'Vote threshold: '
    )
    community_message_moderation_vote_threshold = (
        automation_configuration.community_message_moderation_vote_threshold
    )
    if not community_message_moderation_vote_threshold:
        community_message_moderation_vote_threshold = COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
    description_parts.append(repr(community_message_moderation_vote_threshold))
    
    
    return ''.join(description_parts)


def build_response_list_all(automation_configuration, guild):
    """
    Builds `list-all` command response.
    
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
        (
            f'State: {get_bool_representation(automation_configuration.reaction_copy_enabled)}\n'
            f'Role: {get_role_representation(automation_configuration.reaction_copy_role_id)}'
        ),
    ).add_field(
        'Touhou-feed',
        f'State: {get_bool_representation(automation_configuration.touhou_feed_enabled)}',
    ).add_field(
        'Welcome',
        (
            f'Channel: {get_channel_representation(automation_configuration.welcome_channel_id)}\n'
            f'Reply buttons: {get_bool_representation(automation_configuration.welcome_reply_buttons_enabled)}\n'
            f'Style: {get_choice_representation(automation_configuration.welcome_style_name)}'
        )
    ).add_field(
        'Community message moderation',
        render_community_message_moderation_description(automation_configuration),
    )
    
    return InteractionResponse(
        allowed_mentions = None,
        embed = embed,
    )
