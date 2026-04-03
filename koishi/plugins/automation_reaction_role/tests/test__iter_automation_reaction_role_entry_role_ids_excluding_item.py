import vampytest

from hata import Message

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..helpers import iter_automation_reaction_role_entry_role_ids_excluding_item


def _iter_options():
    message_id = 202510050060
    channel_id = 202510050061
    guild_id = 202510050062
    
    role_id_0 = 202510050063
    role_id_1 = 202510050064
    role_id_2 = 202510050065
    role_id_3 = 202510050066
    role_id_4 = 202510050067
    role_id_5 = 202510050068
    
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
    automation_reaction_role_entry_0.entry_id = 889
    automation_reaction_role_entry_0.items = [
        automation_reaction_role_item_0,
        automation_reaction_role_item_1,
        automation_reaction_role_item_2,
    ]
    
    yield (
        automation_reaction_role_entry_0,
        AutomationReactionRoleItem.add_role_ids,
        automation_reaction_role_item_0,
        {
            role_id_0,
            role_id_1,
        },
    )
    
    yield (
        automation_reaction_role_entry_0,
        AutomationReactionRoleItem.remove_role_ids,
        automation_reaction_role_item_0,
        {
            role_id_4,
            role_id_2,
            role_id_3,
        },
    )
    
    yield (
        automation_reaction_role_entry_0,
        AutomationReactionRoleItem.add_role_ids,
        automation_reaction_role_item_2,
        set()
    )
    
    yield (
        automation_reaction_role_entry_0,
        AutomationReactionRoleItem.remove_role_ids,
        automation_reaction_role_item_2,
        {
            role_id_5,
            role_id_4,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_automation_reaction_role_entry_role_ids_excluding_item(
    automation_reaction_role_entry, role_ids_slot, excluded_automation_reaction_role_item
):
    """
    Tests whether ``iter_automation_reaction_role_entry_role_ids_excluding_item`` works as intended.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role entry to query from.
    
    role_ids_slot : `GetSetDescriptorType | MemberDescriptorType`
        The slot of the entry to get the role identifies for.
    
    excluded_automation_reaction_role_item : ``AutomationReactionRoleItem``
        The item to exclude.
    
    Returns
    -------
    output : `set<int>`
    """
    output = {*iter_automation_reaction_role_entry_role_ids_excluding_item(
        automation_reaction_role_entry, role_ids_slot, excluded_automation_reaction_role_item
    )}
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
