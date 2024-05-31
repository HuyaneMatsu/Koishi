import vampytest
from hata import Role

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..operations import get_reaction_copy_enabled_and_role
from ..constants import AUTOMATION_CONFIGURATIONS


def _iter_options():
    guild_id = 202405300066
    
    yield (
        None,
        guild_id,
        [],
        (
            (False, None),
            0,
        ),
    )
    
    guild_id = 202405300067
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = False
    automation_configuration.reaction_copy_role_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (False, None),
            0,
        ),
    )

    guild_id = 202405300068
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = 0
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (True, None),
            0,
        ),
    )
    
    guild_id = 202405300069
    role_id = 202405300070
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = False
    automation_configuration.reaction_copy_role_id = role_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (False, None),
            role_id,
        ),
    )

    guild_id = 202405300071
    role_id = 202405300072
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = role_id
    
    yield (
        automation_configuration,
        guild_id,
        [],
        (
            (True, None),
            0,
        ),
    )

    guild_id = 202405300073
    role_id = 202405300074
    role = Role.precreate(role_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = False
    automation_configuration.reaction_copy_role_id = role_id
    
    yield (
        automation_configuration,
        guild_id,
        [role],
        (
            (False, None),
            role_id,
        ),
    )

    guild_id = 202405300075
    role_id = 202405300076
    role = Role.precreate(role_id)
    automation_configuration = AutomationConfiguration(guild_id)
    automation_configuration.reaction_copy_enabled = True
    automation_configuration.reaction_copy_role_id = role_id
    
    yield (
        automation_configuration,
        guild_id,
        [role],
        (
            (True, role),
            role_id,
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_reaction_copy_enabled_and_role(automation_configuration, guild_id, extras):
    """
    Tests whether ``get_reaction_copy_enabled_and_role`` works as intended.
    
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
    output : `(bool, None | Role)`
    role_id : `int`
    """
    try:
        if (automation_configuration is not None):
            AUTOMATION_CONFIGURATIONS[automation_configuration.guild_id] = automation_configuration
        
        output = get_reaction_copy_enabled_and_role(guild_id)
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        vampytest.assert_instance(output[0], bool)
        vampytest.assert_instance(output[1], Role, nullable = True)
        
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
