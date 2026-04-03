import vampytest

from hata import Message

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..helpers import iter_automation_reaction_role_entry_role_ids


def _iter_options():
    message_id = 202510050050
    channel_id = 202510050051
    guild_id = 202510050052
    
    role_id_0 = 202510050053
    role_id_1 = 202510050054
    role_id_2 = 202510050055
    role_id_3 = 202510050056
    role_id_4 = 202510050057
    role_id_5 = 202510050058
    
    emoji_id_0 = 666
    emoji_id_1 = 669
    emoji_id_2 = 670
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_item_0 = AutomationReactionRoleItem(
        emoji_id_0,
        None,
        (role_id_5,),
    )
    automation_reaction_role_item_1 = AutomationReactionRoleItem(
        emoji_id_1,
        None,
        (role_id_4,)
    )
    automation_reaction_role_item_2 = AutomationReactionRoleItem(
        emoji_id_2,
        (role_id_0, role_id_1),
        (role_id_2, role_id_3),
    )
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry_0.entry_id = 888
    
    yield (
        automation_reaction_role_entry_0,
        AutomationReactionRoleItem.add_role_ids,
        set(),
    )
    
    yield (
        automation_reaction_role_entry_0,
        AutomationReactionRoleItem.remove_role_ids,
        set(),
    )
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry_1.entry_id = 889
    automation_reaction_role_entry_1.items = [
        automation_reaction_role_item_0,
        automation_reaction_role_item_1,
        automation_reaction_role_item_2,
    ]
    
    yield (
        automation_reaction_role_entry_1,
        AutomationReactionRoleItem.add_role_ids,
        {
            role_id_0,
            role_id_1,
        },
    )
    
    yield (
        automation_reaction_role_entry_1,
        AutomationReactionRoleItem.remove_role_ids,
        {
            role_id_5,
            role_id_4,
            role_id_2,
            role_id_3,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_automation_reaction_role_entry_role_ids(automation_reaction_role_entry, role_ids_slot):
    """
    Tests whether ``iter_automation_reaction_role_entry_role_ids`` works as intended.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role entry to query from.
    
    role_ids_slot : `GetSetDescriptorType | MemberDescriptorType`
        The slot of the entry to get the role identifies for.
    
    Returns
    -------
    output : `set<int>`
    """
    output = {*iter_automation_reaction_role_entry_role_ids(automation_reaction_role_entry, role_ids_slot)}
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
