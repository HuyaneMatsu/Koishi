import vampytest

from ..automation_configuration import AutomationConfiguration
from ..operations import get_automation_configuration_for
from ..constants import AUTOMATION_CONFIGURATIONS


def test__get_automation_configuration_for__hit():
    """
    Tests whether ``get_automation_configuration_for`` works as intended.
    
    Case: hit.
    """
    guild_id = 202405290012
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        AUTOMATION_CONFIGURATIONS[guild_id] = automation_configuration
        
        output = get_automation_configuration_for(guild_id)
        vampytest.assert_instance(output, AutomationConfiguration)
        vampytest.assert_is(output, automation_configuration)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__get_automation_configuration_for__miss():
    """
    Tests whether ``get_automation_configuration_for`` works as intended.
    
    Case: miss.
    """
    guild_id = 202405290013
    
    try:
        output = get_automation_configuration_for(guild_id)
        vampytest.assert_instance(output, AutomationConfiguration)
        vampytest.assert_eq(output.guild_id, guild_id)
        
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass
