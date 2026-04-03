import vampytest
from hata import Channel

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_log_satori_channel_if_auto_start
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202405300011
    
    yield (
        None,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202405300012
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = False
    automation_configuration.log_satori_auto_start = False
    automation_configuration.log_satori_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )

    guild_id = 202405300013
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
    automation_configuration.log_satori_auto_start = False
    automation_configuration.log_satori_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202405300014
    channel_id = 202405300015
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = False
    automation_configuration.log_satori_auto_start = False
    automation_configuration.log_satori_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300016
    channel_id = 202405300017
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
    automation_configuration.log_satori_auto_start = False
    automation_configuration.log_satori_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300018
    channel_id = 202405300019
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = False
    automation_configuration.log_satori_auto_start = False
    automation_configuration.log_satori_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300020
    channel_id = 202405300021
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
    automation_configuration.log_satori_auto_start = False
    automation_configuration.log_satori_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300022
    channel_id = 202405300023
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
    automation_configuration.log_satori_auto_start = True
    automation_configuration.log_satori_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )

    guild_id = 202405300024
    channel_id = 202405300025
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
    automation_configuration.log_satori_auto_start = True
    automation_configuration.log_satori_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            channel,
            channel_id,
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_log_satori_channel_if_auto_start(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_log_satori_channel_if_auto_start`` works as intended.
    
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
    output : `None | Channel`
    channel_id : `int`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_log_satori_channel_if_auto_start(guild_id)
        vampytest.assert_instance(output, Channel, nullable = True)
        
        return(
            output,
            (0 if automation_configuration is None else automation_configuration.log_satori_channel_id),
        )
    
    finally:
        if (automation_configuration is not None):
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
