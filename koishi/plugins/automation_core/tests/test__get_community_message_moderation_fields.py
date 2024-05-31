import vampytest
from hata import BUILTIN_EMOJIS, Channel

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_community_message_moderation_fields
from ..constants import (
    AUTOMATION_CONFIGURATIONS, COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)


def _iter_options():
    guild_id = 202405300096
    
    yield (
        None,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202405300097
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = False
    automation_configuration.community_message_moderation_log_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )

    guild_id = 202405300098
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = True
    automation_configuration.community_message_moderation_log_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (
                COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
                0,
                COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
                COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT,
                None,
            ),
            0,
        ),
    )
    
    guild_id = 202405300099
    channel_id = 202405300100
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = False
    automation_configuration.community_message_moderation_log_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300101
    channel_id = 202405300102
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = True
    automation_configuration.community_message_moderation_log_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (
                COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
                0,
                COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
                COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT,
                None,
            ),
            channel_id,
        ),
    )

    guild_id = 202405300103
    channel_id = 202405300104
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = False
    automation_configuration.community_message_moderation_log_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300105
    channel_id = 202405300106
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = True
    automation_configuration.community_message_moderation_log_enabled = True
    automation_configuration.community_message_moderation_log_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            (
                COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
                0,
                COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
                COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT,
                channel,
            ),
            channel_id,
        ),
    )

    guild_id = 202405300107
    channel_id = 202405300108
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = True
    automation_configuration.community_message_moderation_log_enabled = True
    automation_configuration.community_message_moderation_log_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (
                COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
                0,
                COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
                COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT,
                None,
            ),
            0,
        ),
    )

    guild_id = 202405300109
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.community_message_moderation_enabled = True
    automation_configuration.community_message_moderation_log_enabled = False
    automation_configuration.community_message_moderation_log_channel_id = 0
    automation_configuration.community_message_moderation_down_vote_emoji_id = BUILTIN_EMOJIS['black_heart'].id
    automation_configuration.community_message_moderation_up_vote_emoji_id = BUILTIN_EMOJIS['red_heart'].id
    automation_configuration.community_message_moderation_availability_duration = 1801
    automation_configuration.community_message_moderation_vote_threshold = 6
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (
                BUILTIN_EMOJIS['black_heart'].id,
                BUILTIN_EMOJIS['red_heart'].id,
                1801,
                6,
                None,
            ),
            0,
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_community_message_moderation_fields(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_community_message_moderation_fields`` works as intended.
    
    Parameters
    ----------
    automation_configuration : `None | AutomationConfiguration`
        Cache entry to add / clear.
    guild_id : `int`
        Guild identifiers to test with.
    extras : `list<object>`
        Objects to keep reference for.
    
    Returns
    -------
    output : `None | (int, int, int, int, None | Channel)`
    channel_id : `int`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_community_message_moderation_fields(guild_id)
        vampytest.assert_instance(output, tuple, nullable = True)
        
        if (output is not None):
            vampytest.assert_eq(len(output), 5)
            vampytest.assert_instance(output[0], int)
            vampytest.assert_instance(output[1], int)
            vampytest.assert_instance(output[2], int)
            vampytest.assert_instance(output[3], int)
            vampytest.assert_instance(output[4], Channel, nullable = True)
        
        return(
            output,
            (0 if automation_configuration is None else automation_configuration.community_message_moderation_log_channel_id),
        )
    
    finally:
        if (automation_configuration is not None):
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
