import vampytest
from hata import Message

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..events import exclude_roles_from_automation_reaction_role_entry


def _iter_options():
    # Delete modifies, removes role from multiple additions
    guild_id = 202510010240
    channel_id = 202510010241
    message_id = 202510010242
    entry_id = 777
    
    role_id_0 = 202510010243
    role_id_1 = 202510010244
    role_id_2 = 202510010245
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        AutomationReactionRoleItem(
            200,
            (role_id_0, role_id_1,),
            None,
        ),
        AutomationReactionRoleItem(
            201,
            (role_id_0, role_id_2,),
            None,
        ),
        AutomationReactionRoleItem(
            202,
            (role_id_0,),
            None,
        ),
    ]
    
    yield (
        automation_reaction_role_entry,
        {
            role_id_0,
        },
        (
            True,
            [
                AutomationReactionRoleItem(
                    200,
                    (role_id_1,),
                    None,
                ),
                AutomationReactionRoleItem(
                    201,
                    (role_id_2,),
                    None,
                ),
                AutomationReactionRoleItem(
                    202,
                    None,
                    None,
                ),
            ]
        ),
    )
    # Delete modifies, removes role from multiple removal
    guild_id = 202510020000
    channel_id = 202510020001
    message_id = 202510020002
    entry_id = 777
    
    role_id_0 = 202510020003
    role_id_1 = 202510020004
    role_id_2 = 202510020005
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        AutomationReactionRoleItem(
            200,
            None,
            (role_id_0, role_id_1,),
        ),
        AutomationReactionRoleItem(
            201,
            None,
            (role_id_0, role_id_2,),
        ),
        AutomationReactionRoleItem(
            202,
            None,
            (role_id_0,),
        ),
    ]
    
    yield (
        automation_reaction_role_entry,
        {
            role_id_0,
        },
        (
            True,
            [
                AutomationReactionRoleItem(
                    200,
                    None,
                    (role_id_1,),
                ),
                AutomationReactionRoleItem(
                    201,
                    None,
                    (role_id_2,),
                ),
                AutomationReactionRoleItem(
                    202,
                    None,
                    None,
                ),
            ]
        ),
    )
    
    # Do not remove anything.
    guild_id = 202510020010
    channel_id = 202510020011
    message_id = 202510020012
    entry_id = 777
    
    role_id_0 = 202510020013
    role_id_1 = 202510020014
    role_id_2 = 202510020015
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        AutomationReactionRoleItem(
            200,
            (role_id_0,),
            (role_id_1,),
        ),
    ]
    
    yield (
        automation_reaction_role_entry,
        {
            role_id_2,
        },
        (
            False,
            [
                AutomationReactionRoleItem(
                    200,
                    (role_id_0,),
                    (role_id_1,),
                ),
            ]
        ),
    )
    
    # Nothing to remove from.
    guild_id = 202510020020
    channel_id = 202510020021
    message_id = 202510020022
    entry_id = 777
    
    role_id_0 = 202510020023
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    
    yield (
        automation_reaction_role_entry,
        {
            role_id_0,
        },
        (
            False,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__exclude_roles_from_automation_reaction_role_entry(automation_reaction_role_entry, role_ids_to_exclude):
    """
    Tests whether ``exclude_roles_from_automation_reaction_role_entry`` works as intended.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The auto react orle entry to update.
    
    role_ids_to_exclude : `set<int>`
        The roles' identifier to exclude.
    
    Returns
    -------
    output : ``(bool, None | list<AutomationReactionRoleItem>)``
    """
    automation_reaction_role_entry = automation_reaction_role_entry.copy()
    output = exclude_roles_from_automation_reaction_role_entry(automation_reaction_role_entry, role_ids_to_exclude)
    vampytest.assert_instance(output, bool)
    return output, automation_reaction_role_entry.items
