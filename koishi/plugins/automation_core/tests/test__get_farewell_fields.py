import vampytest
from hata import Channel

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_farewell_fields
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202407140004
    
    yield (
        None,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202407140005
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.farewell_enabled = False
    automation_configuration.farewell_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )

    guild_id = 202407140006
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.farewell_enabled = True
    automation_configuration.farewell_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202407140007
    channel_id = 202407140008
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.farewell_enabled = False
    automation_configuration.farewell_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202407140009
    channel_id = 202407140010
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.farewell_enabled = True
    automation_configuration.farewell_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )

    guild_id = 202407140011
    channel_id = 202407140012
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.farewell_enabled = False
    automation_configuration.farewell_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202407140013
    channel_id = 202407140014
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.farewell_enabled = True
    automation_configuration.farewell_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            (channel, None),
            channel_id,
        ),
    )

    guild_id = 202407140015
    channel_id = 202407140016
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.farewell_enabled = True
    automation_configuration.farewell_channel_id = channel_id
    automation_configuration.farewell_style_name = 'koishi'
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            (channel, 'koishi'),
            channel_id,
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_farewell_fields(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_farewell_fields`` works as intended.
    
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
    output : `None | (Channel, None | str)`
    channel_id : `int`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_farewell_fields(guild_id)
        vampytest.assert_instance(output, tuple, nullable = True)
        
        if (output is not None):
            vampytest.assert_eq(len(output), 2)
            vampytest.assert_instance(output[0], Channel, nullable = True)
            vampytest.assert_instance(output[1], str, nullable = True)
        
        return(
            output,
            (0 if automation_configuration is None else automation_configuration.farewell_channel_id),
        )
    
    finally:
        if (automation_configuration is not None):
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
