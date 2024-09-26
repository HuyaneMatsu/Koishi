import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..automation_configuration_saver import AutomationConfigurationSaver
from ..constants import AUTOMATION_CONFIGURATIONS


def _assert_fields_set(automation_configuration_saver):
    """
    Tests whether every fields are set of the given automation configuration saver.
    
    Parameters
    ----------
    automation_configuration_saver : ``AutomationConfigurationSaver``
        The instance to check.
    """
    vampytest.assert_instance(automation_configuration_saver, AutomationConfigurationSaver)
    vampytest.assert_instance(automation_configuration_saver.entry_proxy, AutomationConfiguration)
    vampytest.assert_instance(automation_configuration_saver.ensured_for_deletion, bool)
    vampytest.assert_instance(automation_configuration_saver.modified_fields, dict, nullable = True)
    vampytest.assert_instance(automation_configuration_saver.run_task, Task, nullable = True)


def test__AutomationConfigurationSaver__new():
    """
    Tests whether ``AutomationConfigurationSaver.__new__`` works as intended.
    """
    guild_id = 202405280020
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        _assert_fields_set(automation_configuration_saver)
        
        vampytest.assert_is(automation_configuration_saver.entry_proxy, automation_configuration)

    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


@vampytest.skip_if(DB_ENGINE is not None)
async def test__AutomationConfigurationSaver__repr():
    """
    Tests whether ``AutomationConfigurationSaver.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    guild_id = 202405280021
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        ensured_for_deletion = True
        modified_fields = {'satori_log_enabled': True}
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        automation_configuration_saver.ensured_for_deletion = ensured_for_deletion
        automation_configuration_saver.modified_fields = modified_fields
        automation_configuration_saver.run_task = Task(get_event_loop(), automation_configuration_saver.run())
        
        output = repr(automation_configuration_saver)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(AutomationConfigurationSaver.__name__, output)
        vampytest.assert_in(f'entry_proxy = {automation_configuration!r}', output)
        vampytest.assert_in(f'ensured_for_deletion = {ensured_for_deletion!r}', output)
        vampytest.assert_in(f'modified_fields = {modified_fields!r}', output)
        vampytest.assert_in(f'running = {True!r}', output)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfigurationSaver__add_modification():
    """
    Tests whether ``AutomationConfigurationSaver.add_modification`` works as intended.
    """
    guild_id = 202405280022
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        
        vampytest.assert_eq(
            automation_configuration_saver.modified_fields,
            None,
        )
        
        automation_configuration_saver.add_modification('log_satori_auto_start', True)
        
        vampytest.assert_eq(
            automation_configuration_saver.modified_fields,
            {
                'log_satori_auto_start': True,
            }
        )
        
        automation_configuration_saver.add_modification('log_satori_enabled', True)
        
        vampytest.assert_eq(
            automation_configuration_saver.modified_fields,
            {
                'log_satori_enabled': True,
                'log_satori_auto_start': True,
            }
        )
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfigurationSaver__ensure_deletion():
    """
    Tests whether ``AutomationConfigurationSaver.ensure_deletion`` works as intended.
    """
    guild_id = 202405280023
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        
        vampytest.assert_eq(automation_configuration_saver.ensured_for_deletion, False)
        
        automation_configuration_saver.ensure_deletion()
        
        vampytest.assert_eq(automation_configuration_saver.ensured_for_deletion, True)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfigurationSaver__is_modified__not():
    """
    Tests whether ``AutomationConfigurationSaver.is_modified`` works as intended.
    
    Case: not modified.
    """
    guild_id = 202405280025
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        
        output = automation_configuration_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfigurationSaver__is_modified__delete():
    """
    Tests whether ``AutomationConfigurationSaver.is_modified`` works as intended.
    
    Case: ensured for deletion.
    """
    guild_id = 202405280026
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        automation_configuration_saver.ensure_deletion()
        
        output = automation_configuration_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfigurationSaver__is_modified__field():
    """
    Tests whether ``AutomationConfigurationSaver.is_modified`` works as intended.
    
    Case: field modified.
    """
    guild_id = 202405280027
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        automation_configuration_saver.add_modification('satori_log_enabled', True)
        
        output = automation_configuration_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


@vampytest.skip_if(DB_ENGINE is not None)
async def test__AutomationConfigurationSaver__begin():
    """
    Tests whether ``AutomationConfigurationSaver.begin`` works as intended.
    
    This function is a coroutine.
    """
    guild_id = 202405280024
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        automation_configuration.saver = automation_configuration_saver
        
        output = automation_configuration_saver.begin()
        
        vampytest.assert_instance(output, Task)
        vampytest.assert_is(automation_configuration_saver.run_task, output)
        vampytest.assert_is(automation_configuration.saver, automation_configuration_saver)
        
        # do save
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        # after save nothing should be set.
        vampytest.assert_is(automation_configuration_saver.run_task, None)
        vampytest.assert_is(automation_configuration.saver, None)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass



@vampytest.skip_if(DB_ENGINE is not None)
async def AutomationConfigurationSaver__running():
    """
    Tests whether ``AutomationConfigurationSaver.running`` works as intended.
    """
    guild_id = 202409190000
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        automation_configuration_saver = AutomationConfigurationSaver(automation_configuration)
        automation_configuration.saver = automation_configuration_saver
        
        output = automation_configuration_saver.running
        vampytest.assert_eq(output, False)
        
        automation_configuration_saver.begin()
        
        output = automation_configuration_saver.running
        vampytest.assert_eq(output, True)
        
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass
