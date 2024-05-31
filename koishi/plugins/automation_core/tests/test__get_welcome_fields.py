import vampytest
from hata import Channel

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_welcome_fields
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202405300080
    
    yield (
        None,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202405300081
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_enabled = False
    automation_configuration.welcome_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )

    guild_id = 202405300082
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_enabled = True
    automation_configuration.welcome_channel_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )
    
    guild_id = 202405300083
    channel_id = 202405300084
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_enabled = False
    automation_configuration.welcome_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300085
    channel_id = 202405300086
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_enabled = True
    automation_configuration.welcome_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            None,
            0,
        ),
    )

    guild_id = 202405300087
    channel_id = 202405300088
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_enabled = False
    automation_configuration.welcome_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            None,
            channel_id,
        ),
    )

    guild_id = 202405300089
    channel_id = 202405300090
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_enabled = True
    automation_configuration.welcome_channel_id = channel_id
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            (channel, False, None),
            channel_id,
        ),
    )

    guild_id = 202405300091
    channel_id = 202405300092
    channel = Channel.precreate(channel_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_enabled = True
    automation_configuration.welcome_channel_id = channel_id
    automation_configuration.welcome_reply_buttons_enabled = True
    automation_configuration.welcome_style_name = 'koishi'
    
    yield (
        automation_configuration,
        guild_id,
        [channel],
        (
            (channel, True, 'koishi'),
            channel_id,
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_welcome_fields(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_welcome_fields`` works as intended.
    
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
    output : `None | (Channel, bool, None | str)`
    channel_id : `int`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_welcome_fields(guild_id)
        vampytest.assert_instance(output, tuple, nullable = True)
        
        if (output is not None):
            vampytest.assert_eq(len(output), 3)
            vampytest.assert_instance(output[0], Channel, nullable = True)
            vampytest.assert_instance(output[1], bool)
            vampytest.assert_instance(output[2], str, nullable = True)
        
        return(
            output,
            (0 if automation_configuration is None else automation_configuration.welcome_channel_id),
        )
    
    finally:
        if (automation_configuration is not None):
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
