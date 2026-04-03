import vampytest

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import delete_automation_configuration_of
from ..constants import AUTOMATION_CONFIGURATIONS


@vampytest.skip_if(DB_ENGINE is not None)
def test__delete_automation_configuration_of__hit():
    """
    Tests whether ``delete_automation_configuration_of`` works as intended.
    
    Case: hit.
    """
    guild_id = 202405290014
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        AUTOMATION_CONFIGURATIONS[guild_id] = automation_configuration
        
        delete_automation_configuration_of(guild_id)
        
        vampytest.assert_is_not(automation_configuration.saver, None)
        vampytest.assert_eq(automation_configuration.saver.ensured_for_deletion, True)
        
        
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


@vampytest.skip_if(DB_ENGINE is not None)
def test__delete_automation_configuration_of__miss():
    """
    Tests whether ``delete_automation_configuration_of`` works as intended.
    
    Case: miss.
    """
    guild_id = 202405290015
    
    try:
        delete_automation_configuration_of(guild_id)
        
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass
