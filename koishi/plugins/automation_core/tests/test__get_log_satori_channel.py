import vampytest
from hata import Channel

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_log_satori_channel
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202405300000
    
    yield (
        None,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202405300001
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = False
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

    guild_id = 202405300002
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
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
    
    guild_id = 202405300003
    channel_id = 202405300004
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = False
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

    guild_id = 202405300005
    channel_id = 202405300006
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
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

    guild_id = 202405300007
    channel_id = 202405300008
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = False
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

    guild_id = 202405300009
    channel_id = 202405300010
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.log_satori_enabled = True
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
def test__get_log_satori_channel(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_log_satori_channel`` works as intended.
    
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
        
        output = get_log_satori_channel(guild_id)
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
