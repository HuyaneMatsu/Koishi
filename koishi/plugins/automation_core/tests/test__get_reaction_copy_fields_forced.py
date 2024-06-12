import vampytest
from hata import Role

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_reaction_copy_fields_forced
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202406100015
    
    yield (
        None,
        guild_id,
        [],
        (
            (False, None, 0),
            0,
        ),
    )
    
    guild_id = 202406100016
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = False
    automation_configuration.reaction_copy_role_id = 0
    automation_configuration.reaction_copy_flags = 12
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (False, None, 12),
            0,
        ),
    )

    guild_id = 202406100017
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = 0
    automation_configuration.reaction_copy_flags = 12
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (True, None, 12),
            0,
        ),
    )
    
    guild_id = 202406100018
    role_id = 202406100019
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = False
    automation_configuration.reaction_copy_role_id = role_id
    automation_configuration.reaction_copy_flags = 12
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (False, None, 12),
            0,
        ),
    )

    guild_id = 202406100020
    role_id = 202406100021
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = role_id
    automation_configuration.reaction_copy_flags = 12
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (True, None, 12),
            0,
        ),
    )

    guild_id = 202406100022
    role_id = 202406100023
    role = Role.precreate(role_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = False
    automation_configuration.reaction_copy_role_id = role_id
    automation_configuration.reaction_copy_flags = 12
    
    yield (
        automation_configuration,
        guild_id,
        [role],
        (
            (False, role, 12),
            role_id,
        ),
    )

    guild_id = 202406100024
    role_id = 202406100025
    role = Role.precreate(role_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = role_id
    automation_configuration.reaction_copy_flags = 12
    
    yield (
        automation_configuration,
        guild_id,
        [role],
        (
            (True, role, 12),
            role_id,
        ),
    )

    guild_id = 202406100026
    role_id = 202406100027
    role = Role.precreate(role_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = role_id
    automation_configuration.reaction_copy_flags = 0
    
    yield (
        automation_configuration,
        guild_id,
        [role],
        (
            (True, role, 0),
            role_id,
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_reaction_copy_fields_forced(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_reaction_copy_fields_forced`` works as intended.
    
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
    output : `None | (None | Role, int)`
    role_id : `int`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_reaction_copy_fields_forced(guild_id)
        vampytest.assert_instance(output, tuple)
        vampytest.assert_instance(output[0], int)
        vampytest.assert_instance(output[1], Role, nullable = True)
        vampytest.assert_instance(output[2], int)
        
        return(
            output,
            (0 if automation_configuration is None else automation_configuration.reaction_copy_role_id),
        )
    
    finally:
        if (automation_configuration is not None):
            try:
                del AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id]
            except KeyError:
                pass
