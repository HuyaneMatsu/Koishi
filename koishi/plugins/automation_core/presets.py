__all__ = ()

from .automation_configuration import AutomationConfiguration
from .constants import AUTOMATION_CONFIGURATIONS

from ...bot_utils.constants import (
    CHANNEL__SUPPORT__LOG_EMOJI, CHANNEL__SUPPORT__LOG_MENTION, CHANNEL__SUPPORT__LOG_SATORI,
    CHANNEL__SUPPORT__LOG_STICKER, CHANNEL__SUPPORT__LOG_USER, CHANNEL__SUPPORT__WELCOME, GUILD__SUPPORT
)


def apply_presets():
    """
    Applies presets.
    
    Called when db is not available,
    """
    support_guild_configuration = AutomationConfiguration(GUILD__SUPPORT.id)
    
    # Logging
    support_guild_configuration.log_emoji_channel_id = CHANNEL__SUPPORT__LOG_EMOJI.id
    support_guild_configuration.log_emoji_enabled = True
    support_guild_configuration.log_mention_channel_id = CHANNEL__SUPPORT__LOG_MENTION.id
    support_guild_configuration.log_mention_enabled = True
    support_guild_configuration.log_sticker_channel_id = CHANNEL__SUPPORT__LOG_STICKER.id
    support_guild_configuration.log_sticker_enabled = True
    support_guild_configuration.log_user_channel_id = CHANNEL__SUPPORT__LOG_USER.id
    support_guild_configuration.log_user_enabled = True
    
    # Satori
    support_guild_configuration.log_satori_auto_start = True
    support_guild_configuration.log_satori_channel_id = CHANNEL__SUPPORT__LOG_SATORI.id
    support_guild_configuration.log_satori_enabled = True
    
    # Reaction copy
    support_guild_configuration.reaction_copy_enabled = True
    support_guild_configuration.reaction_copy_flags = 3
    support_guild_configuration.reaction_copy_role_id = 0
    
    # Touhou feed
    support_guild_configuration.touhou_feed_enabled = True
    
    # Welcome
    support_guild_configuration.welcome_channel_id = CHANNEL__SUPPORT__WELCOME.id
    support_guild_configuration.welcome_enabled = True
    support_guild_configuration.welcome_reply_buttons_enabled = True
    support_guild_configuration.welcome_style_name = None
    
    # Community message moderation
    support_guild_configuration.community_message_moderation_availability_duration = 0
    support_guild_configuration.community_message_moderation_down_vote_emoji_id = 0
    support_guild_configuration.community_message_moderation_enabled = False
    support_guild_configuration.community_message_moderation_up_vote_emoji_id = 0
    support_guild_configuration.community_message_moderation_vote_threshold = 0
    support_guild_configuration.community_message_moderation_log_enabled = False
    support_guild_configuration.community_message_moderation_log_channel_id = 0
    
    # Farewell
    support_guild_configuration.farewell_channel_id = 0
    support_guild_configuration.farewell_enabled = False
    support_guild_configuration.farewell_style_name = None
    
    AUTOMATION_CONFIGURATIONS[support_guild_configuration.guild_id] = support_guild_configuration
