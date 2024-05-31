import vampytest
from hata import BUILTIN_EMOJIS, Channel, ChannelType, EMOJIS, Embed, Guild, Role
from hata.ext.slash import InteractionResponse

from ....bot_utils.constants import GUILD__SUPPORT

from ...automation_core import (
    AutomationConfiguration, COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)

from ..constants import CHOICE_DEFAULT, ENTITY_REPRESENTATION_DEFAULT
from ..list_all import build_response_list_all
from ..representation_getters import get_duration_representation


def _iter_options():
    automation_configuration = AutomationConfiguration(0)
    
    guild_id = 202405310003
    guild_name = 'Orin\s dance house'
    guild = Guild.precreate(guild_id, name = guild_name)
    
    yield (
        automation_configuration,
        guild,
        [],
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed(
                f'{guild_name!s}\'s automations',
            ).add_thumbnail(
                guild.icon_url,
            ).add_field(
                'Log-emoji',
                (
                    f'State: disabled\n'
                    f'Channel: {ENTITY_REPRESENTATION_DEFAULT!s}'
                ),
            ).add_field(
                'Log-mention',
                (
                    f'State: disabled\n'
                    f'Channel: {ENTITY_REPRESENTATION_DEFAULT!s}'
                ),
            ).add_field(
                'Log-sticker',
                (
                    f'State: disabled\n'
                    f'Channel: {ENTITY_REPRESENTATION_DEFAULT!s}'
                ),
            ).add_field(
                'Log-user',
                (
                    f'State: disabled\n'
                    f'Channel: {ENTITY_REPRESENTATION_DEFAULT!s}'
                ),
            ).add_field(
                'Reaction-copy',
                (
                    f'State: disabled\n'
                    f'Role: {ENTITY_REPRESENTATION_DEFAULT!s}'
                ),
            ).add_field(
                'Touhou-feed',
                (
                    f'State: disabled'
                ),
            ).add_field(
                'Welcome',
                (
                    f'State: disabled\n'
                    f'Channel: {ENTITY_REPRESENTATION_DEFAULT!s}\n'
                    f'Reply buttons: disabled\n'
                    f'Style: {CHOICE_DEFAULT!s}'
                )
            ).add_field(
                'Community-message-moderation',
                (
                    f'State: disabled\n'
                    f'Down vote emoji: {EMOJIS[COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT].as_emoji!s}\n'
                    f'Up vote emoji: {ENTITY_REPRESENTATION_DEFAULT!s}\n'
                    f'Availability duration: {get_duration_representation(COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT)!s}\n'
                    f'Vote threshold: {COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT!s}\n'
                    f'Logging state: disabled\n'
                    f'Log channel: {ENTITY_REPRESENTATION_DEFAULT!s}'
                ),
            ),
        )
    )
    
    guild_name = 'Koishi Wonderland'
    guild = GUILD__SUPPORT
    guild.name = guild_name
    
    log_emoji_channel_id = 202405310003
    log_emoji_channel = Channel.precreate(
        log_emoji_channel_id, channel_type = ChannelType.guild_text, name = 'pocky'
    )
    log_mention_channel_id = 202405310004
    log_mention_channel = Channel.precreate(
        log_mention_channel_id, channel_type = ChannelType.guild_text, name = 'kiss'
    )
    log_satori_channel_id = 202405310005
    log_satori_channel = Channel.precreate(
        log_satori_channel_id, channel_type = ChannelType.guild_category, name = 'pocky-kiss'
    )
    log_sticker_channel_id = 202405310006
    log_sticker_channel = Channel.precreate(
        log_sticker_channel_id, channel_type = ChannelType.guild_text, name = 'lap'
    )
    log_user_channel_id = 202405310007
    log_user_channel = Channel.precreate(
        log_user_channel_id, channel_type = ChannelType.guild_text, name = 'sleep'
    )
    reaction_copy_role_id = 202405310008
    reaction_copy_role = Role.precreate(reaction_copy_role_id, name = 'lap-sleep')
    
    welcome_channel_id = 202405310009
    welcome_channel = Channel.precreate(
        welcome_channel_id, channel_type = ChannelType.guild_text, name = 'hug'
    )
    welcome_style_name = 'flandre'
    
    automation_configuration = AutomationConfiguration(0)
    automation_configuration.log_emoji_enabled = True
    automation_configuration.log_emoji_channel_id = log_emoji_channel_id
    automation_configuration.log_mention_enabled = True
    automation_configuration.log_mention_channel_id = log_mention_channel_id
    automation_configuration.log_satori_enabled = True
    automation_configuration.log_satori_channel_id = log_satori_channel_id
    automation_configuration.log_satori_auto_start = True
    automation_configuration.log_sticker_enabled = True
    automation_configuration.log_sticker_channel_id = log_sticker_channel_id
    automation_configuration.log_user_enabled = True
    automation_configuration.log_user_channel_id = log_user_channel_id
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = reaction_copy_role_id
    automation_configuration.touhou_feed_enabled = True
    automation_configuration.welcome_enabled = True
    automation_configuration.welcome_channel_id = welcome_channel_id
    automation_configuration.welcome_reply_buttons_enabled = True
    automation_configuration.welcome_style_name = welcome_style_name
    automation_configuration.community_message_moderation_enabled = True
    
    yield (
        automation_configuration,
        GUILD__SUPPORT,
        [
            log_emoji_channel,
            log_mention_channel,
            log_satori_channel,
            log_sticker_channel,
            log_user_channel,
            reaction_copy_role,
            welcome_channel,
        ],
        InteractionResponse(
            allowed_mentions = None,
            embed = Embed(
                f'{guild_name!s}\'s automations',
            ).add_thumbnail(
                guild.icon_url,
            ).add_field(
                'Log-emoji',
                (
                    f'State: enabled\n'
                    f'Channel: {log_emoji_channel.mention!s}'
                ),
            ).add_field(
                'Log-mention',
                (
                    f'State: enabled\n'
                    f'Channel: {log_mention_channel.mention!s}'
                ),
            ).add_field(
                'Log-satori',
                (
                    f'State: enabled\n'
                    f'Channel: {log_satori_channel.mention!s}\n'
                    f'Auto start: enabled'
                ),
            ).add_field(
                'Log-sticker',
                (
                    f'State: enabled\n'
                    f'Channel: {log_sticker_channel.mention!s}'
                ),
            ).add_field(
                'Log-user',
                (
                    f'State: enabled\n'
                    f'Channel: {log_user_channel.mention!s}'
                ),
            ).add_field(
                'Reaction-copy',
                (
                    f'State: enabled\n'
                    f'Role: {reaction_copy_role.mention!s}'
                ),
            ).add_field(
                'Touhou-feed',
                (
                    f'State: enabled'
                ),
            ).add_field(
                'Welcome',
                (
                    f'State: enabled\n'
                    f'Channel: {welcome_channel.mention!s}\n'
                    f'Reply buttons: enabled\n'
                    f'Style: {welcome_style_name!s}'
                )
            ).add_field(
                'Community-message-moderation',
                (
                    f'State: enabled\n'
                    f'Down vote emoji: {EMOJIS[COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT].as_emoji!s}\n'
                    f'Up vote emoji: {ENTITY_REPRESENTATION_DEFAULT!s}\n'
                    f'Availability duration: {get_duration_representation(COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT)!s}\n'
                    f'Vote threshold: {COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT!s}\n'
                    f'Logging state: disabled\n'
                    f'Log channel: {ENTITY_REPRESENTATION_DEFAULT!s}'
                ),
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_response_list_all(automation_configuration, guild, extras):
    """
    Tests whether ``build_response_list_all`` works as intended.
    
    Parameters
    ----------
    automation_configuration : ``AutomationConfiguration``
        The configuration to show.
    guild : ``Guild``
        The guild the automation configuration is bound to.
    extras : `list<str>`
        Extra entities to keep in cache.
    
    Returns
    -------
    output : ``InteractionResponse``
    """
    output = build_response_list_all(automation_configuration, guild)
    vampytest.assert_instance(output, InteractionResponse)
    return output
