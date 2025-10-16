__all__ = ()

from hata import Embed
from hata.ext.slash import InteractionResponse

from config import MARISA_MODE

from ..automation_core import (
    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT, COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)


try:
    from ..automation_reaction_copy import get_reaction_copy_flag_parse_names

except ImportError:
    if not MARISA_MODE:
        raise
    
    get_reaction_copy_flag_parse_names = lambda flags : '*none*'


from .constants import LOG_SATORI_ALLOWED_IDS
from .representation_getters import (
    get_bool_representation, get_channel_id_representation, get_choice_representation, get_duration_representation,
    get_emoji_id_representation, get_role_id_representation
)


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
    description_parts.append(str(community_message_moderation_vote_threshold))
    
    
    description_parts.append(
        '\n'
        'Logging state: '
    )
    description_parts.append(get_bool_representation(automation_configuration.community_message_moderation_log_enabled))
    description_parts.append(
        '\n'
        'Log channel: '
    )
    description_parts.append(get_channel_id_representation(
        automation_configuration.community_message_moderation_log_channel_id
    ))
    
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
        f'{guild.name!s}\'s automations',
    ).add_thumbnail(
        guild.icon_url,
    ).add_field(
        'Log-emoji',
        (
            f'State: {get_bool_representation(automation_configuration.log_emoji_enabled)!s}\n'
            f'Channel: {get_channel_id_representation(automation_configuration.log_emoji_channel_id)!s}'
        ),
    ).add_field(
        'Log-mention',
        (
            f'State: {get_bool_representation(automation_configuration.log_mention_enabled)!s}\n'
            f'Channel: {get_channel_id_representation(automation_configuration.log_mention_channel_id)!s}'
        ),
    )
    
    # Render satori only if allowed in the guild
    if guild.id in LOG_SATORI_ALLOWED_IDS:
        embed.add_field(
            'Log-satori',
            (
                f'State: {get_bool_representation(automation_configuration.log_satori_enabled)!s}\n'
                f'Channel: {get_channel_id_representation(automation_configuration.log_satori_channel_id)!s}\n'
                f'Auto start: {get_bool_representation(automation_configuration.log_satori_auto_start)!s}'
            )
        )
    
    embed.add_field(
        'Log-sticker',
        (
            f'State: {get_bool_representation(automation_configuration.log_sticker_enabled)!s}\n'
            f'Channel: {get_channel_id_representation(automation_configuration.log_sticker_channel_id)!s}'
        ),
    ).add_field(
        'Log-user',
        (
            f'State: {get_bool_representation(automation_configuration.log_user_enabled)!s}\n'
            f'Channel: {get_channel_id_representation(automation_configuration.log_user_channel_id)!s}'
        ),
    ).add_field(
        'Reaction-copy',
        (
            f'State: {get_bool_representation(automation_configuration.reaction_copy_enabled)!s}\n'
            f'Parse: {get_reaction_copy_flag_parse_names(automation_configuration.reaction_copy_flags)!s}\n'
            f'Role: {get_role_id_representation(automation_configuration.reaction_copy_role_id)!s}'
        ),
    ).add_field(
        'Touhou-feed',
        f'State: {get_bool_representation(automation_configuration.touhou_feed_enabled)!s}',
    ).add_field(
        'Welcome',
        (
            f'State: {get_bool_representation(automation_configuration.welcome_enabled)!s}\n'
            f'Channel: {get_channel_id_representation(automation_configuration.welcome_channel_id)!s}\n'
            f'Reply buttons: {get_bool_representation(automation_configuration.welcome_reply_buttons_enabled)!s}\n'
            f'Style: {get_choice_representation(automation_configuration.welcome_style_name)!s}'
        )
    ).add_field(
        'Farewell',
        (
            f'State: {get_bool_representation(automation_configuration.farewell_enabled)!s}\n'
            f'Channel: {get_channel_id_representation(automation_configuration.farewell_channel_id)!s}\n'
            f'Style: {get_choice_representation(automation_configuration.farewell_style_name)!s}'
        )
    ).add_field(
        'Community-message-moderation',
        render_community_message_moderation_description(automation_configuration),
    )
    
    
    return InteractionResponse(
        allowed_mentions = None,
        embed = embed,
    )
