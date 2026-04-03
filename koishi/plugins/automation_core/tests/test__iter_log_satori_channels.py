import vampytest
from hata import Channel

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import iter_log_satori_channels
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id_0 = 202405300026
    
    yield (
        [],
        [],
        (
            set(),
            [],
        ),
    )
    
    guild_id_0 = 202405300027
    automation_configuration_0 = AutomationConfiguration(guild_id_0)
    automation_configuration_0.log_satori_enabled = False
    automation_configuration_0.log_satori_channel_id = 0
    
    yield (
        [
            automation_configuration_0,
        ],
        [],
        (
            set(),
            [0],
        ),
    )

    guild_id_0 = 202405300028
    automation_configuration_0 = AutomationConfiguration(guild_id_0)
    automation_configuration_0.log_satori_enabled = True
    automation_configuration_0.log_satori_channel_id = 0
    
    yield (
        [
            automation_configuration_0
        ],
        [],
        (
            set(),
            [0],
        ),
    )
    
    guild_id_0 = 202405300029
    channel_id_0 = 202405300030
    automation_configuration_0 = AutomationConfiguration(guild_id_0)
    automation_configuration_0.log_satori_enabled = False
    automation_configuration_0.log_satori_channel_id = channel_id_0
    
    yield (
        [
            automation_configuration_0
        ],
        [],
        (
            set(),
            [channel_id_0],
        ),
    )

    guild_id_0 = 202405300031
    channel_id_0 = 202405300032
    automation_configuration_0 = AutomationConfiguration(guild_id_0)
    automation_configuration_0.log_satori_enabled = True
    automation_configuration_0.log_satori_channel_id = channel_id_0
    
    yield (
        [
            automation_configuration_0
        ],
        [],
        (
            set(),
            [channel_id_0],
        ),
    )

    guild_id_0 = 202405300033
    channel_id_0 = 202405300034
    channel_0 = Channel.precreate(channel_id_0)
    automation_configuration_0 = AutomationConfiguration(guild_id_0)
    automation_configuration_0.log_satori_enabled = False
    automation_configuration_0.log_satori_channel_id = channel_id_0
    
    yield (
        [
            automation_configuration_0
        ],
        [channel_0],
        (
            set(),
            [channel_id_0],
        ),
    )
    
    guild_id_0 = 202405300035
    channel_id_0 = 202405300036
    channel_0 = Channel.precreate(channel_id_0)
    automation_configuration_0 = AutomationConfiguration(guild_id_0)
    automation_configuration_0.log_satori_enabled = True
    automation_configuration_0.log_satori_channel_id = channel_id_0
    
    yield (
        [
            automation_configuration_0
        ],
        [channel_0],
        (
            {channel_0},
            [channel_id_0],
        ),
    )
    
    guild_id_0 = 202405300037
    channel_id_0 = 202405300038
    channel_0 = Channel.precreate(channel_id_0)
    automation_configuration_0 = AutomationConfiguration(guild_id_0)
    automation_configuration_0.log_satori_enabled = True
    automation_configuration_0.log_satori_channel_id = channel_id_0
    
    guild_id_1 = 202405300039
    channel_id_1 = 202405300040
    channel_1 = Channel.precreate(channel_id_1)
    automation_configuration_1 = AutomationConfiguration(guild_id_1)
    automation_configuration_1.log_satori_enabled = True
    automation_configuration_1.log_satori_channel_id = channel_id_1
    
    yield (
        [
            automation_configuration_0,
            automation_configuration_1,
        ],
        [channel_0, channel_1],
        (
            {channel_0, channel_1},
            [channel_id_0, channel_id_1],
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_log_satori_channels(automation_configurations, extras):
    """
    Tests whether ``iter_log_satori_channels`` works as intended.
    
    Parameters
    ----------
    automation_configurations : `list<AutomationConfiguration>`
        Cache entries to add / clear.
    extras : `list<object>`
        Objects to keep reference for.
    
    Returns
    -------
    output : `set<Channel>`
    channel_ids : `list<int>`
    """
    try:
        for automation_configuration in automation_configurations:
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = {*iter_log_satori_channels()}
        
        for element in output:
            vampytest.assert_instance(element, Channel, nullable = True)
        
        return(
            output,
            [automation_configuration.log_satori_channel_id for automation_configuration in automation_configurations]
        )
    
    finally:
        for automation_configuration in automation_configurations:
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
