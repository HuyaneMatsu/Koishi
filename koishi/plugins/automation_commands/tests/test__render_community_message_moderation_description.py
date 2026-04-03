import vampytest
from hata import BUILTIN_EMOJIS, Channel, ChannelType, EMOJIS

from ...automation_core import (
    AutomationConfiguration, COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)

from ..constants import ENTITY_REPRESENTATION_DEFAULT
from ..list_all import render_community_message_moderation_description
from ..representation_getters import get_duration_representation


def _iter_options():
    automation_configuration = AutomationConfiguration(0)
    
    yield (
        automation_configuration,
        [],
        (
            f'State: disabled\n'
            f'Down vote emoji: {EMOJIS[COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT].as_emoji!s}\n'
            f'Up vote emoji: {ENTITY_REPRESENTATION_DEFAULT!s}\n'
            f'Availability duration: {get_duration_representation(COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT)!s}\n'
            f'Vote threshold: {COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT!s}\n'
            f'Logging state: disabled\n'
            f'Log channel: {ENTITY_REPRESENTATION_DEFAULT!s}'
        ),
    )
    
    down_vote_emoji_id = BUILTIN_EMOJIS['black_heart'].id
    up_vote_emoji_id = BUILTIN_EMOJIS['red_heart'].id
    availability_duration = 1602
    vote_threshold = 5
    log_channel_id = 202405310002
    log_channel = Channel.precreate(log_channel_id, channel_type = ChannelType.guild_text, name = 'pudding')
    
    automation_configuration = AutomationConfiguration(0)
    automation_configuration.community_message_moderation_enabled = True
    automation_configuration.community_message_moderation_down_vote_emoji_id = down_vote_emoji_id
    automation_configuration.community_message_moderation_up_vote_emoji_id = up_vote_emoji_id
    automation_configuration.community_message_moderation_availability_duration = availability_duration
    automation_configuration.community_message_moderation_vote_threshold = vote_threshold
    automation_configuration.community_message_moderation_log_enabled = True
    automation_configuration.community_message_moderation_log_channel_id = 202405310002
    
    yield (
        automation_configuration,
        [log_channel],
        (
            f'State: enabled\n'
            f'Down vote emoji: {EMOJIS[down_vote_emoji_id].as_emoji!s}\n'
            f'Up vote emoji: {EMOJIS[up_vote_emoji_id].as_emoji!s}\n'
            f'Availability duration: {get_duration_representation(availability_duration)!s}\n'
            f'Vote threshold: {vote_threshold!s}\n'
            f'Logging state: enabled\n'
            f'Log channel: {log_channel.mention!s}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_community_message_moderation_description(automation_configuration, extras):
    """
    Tests whether ``render_community_message_moderation_description`` works as intended.
    
    Parameters
    ----------
    automation_configuration : ``AutomationConfiguration``
        The automation configuration to render.
    extras : `list<str>`
        Extra entities to keep in cache.
    
    Returns
    -------
    output : `str`
    """
    output = render_community_message_moderation_description(automation_configuration)
    vampytest.assert_instance(output, str)
    return output
