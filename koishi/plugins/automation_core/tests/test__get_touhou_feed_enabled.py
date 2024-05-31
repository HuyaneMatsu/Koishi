import vampytest

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_touhou_feed_enabled
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202405300077
    
    yield (
        None,
        guild_id,
        [],
        False,
    )
    
    guild_id = 202405300078
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.touhou_feed_enabled = False
    
    yield (
        automation_configuration,
        guild_id,
        [],
        False,
    )

    guild_id = 202405300079
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.touhou_feed_enabled = True
    
    yield (
        automation_configuration,
        guild_id,
        [],
        True,
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_touhou_feed_enabled(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_touhou_feed_enabled`` works as intended.
    
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
    output : `bool`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_touhou_feed_enabled(guild_id)
        vampytest.assert_instance(output, bool)
        
        return output
    
    finally:
        if (automation_configuration is not None):
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
