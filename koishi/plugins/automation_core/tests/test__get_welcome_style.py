import vampytest

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_welcome_style_name
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202405300093
    
    yield (
        None,
        guild_id,
        [],
        None,
    )
    
    guild_id = 202405300094
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_style_name = None
    
    yield (
        automation_configuration,
        guild_id,
        [],
        None,
    )

    guild_id = 202405300095
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.welcome_style_name = 'koishi'
    
    yield (
        automation_configuration,
        guild_id,
        [],
        'koishi',
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_welcome_style_name(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_welcome_style_name`` works as intended.
    
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
    output : `None | str`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_welcome_style_name(guild_id)
        vampytest.assert_instance(output, str, nullable = True)
        
        return output
    
    finally:
        if (automation_configuration is not None):
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
