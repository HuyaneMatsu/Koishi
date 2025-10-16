import vampytest

from hata import Message

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..helpers import get_automation_reaction_role_item_with_emoji_id


def _iter_options():
    message_id = 202510050030
    channel_id = 202510050031
    guild_id = 202510050032
    
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
        None,
    )
    automation_reaction_role_item_1 = AutomationReactionRoleItem(
        emoji_id_1,
        None,
        None,
    )
    automation_reaction_role_item_2 = AutomationReactionRoleItem(
        emoji_id_2,
        None,
        None,
    )
    
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry_0.entry_id = 888
    
    yield (
        automation_reaction_role_entry_0,
        emoji_id_2,
        None,
    )
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry_1.entry_id = 889
    automation_reaction_role_entry_1.items = [
        automation_reaction_role_item_0,
        automation_reaction_role_item_1,
    ]
    
    yield (
        automation_reaction_role_entry_1,
        emoji_id_2,
        None,
    )
    
    
    automation_reaction_role_entry_2 = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry_2.entry_id = 890
    automation_reaction_role_entry_2.items = [
        automation_reaction_role_item_0,
        automation_reaction_role_item_1,
        automation_reaction_role_item_2,
    ]
    
    yield (
        automation_reaction_role_entry_2,
        emoji_id_2,
        automation_reaction_role_item_2,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_automation_reaction_role_item_with_emoji_id(automation_reaction_role_entry, emoji_id):
    """
    Tests whether ``get_automation_reaction_role_item_with_emoji_id`` works as intended.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role entry to query from.
    
    emoji_id : `int`
        The emoji's identifier.
    
    Returns
    -------
    automation_reaction_role_item : ``None | AutomationReactionRoleItem``
    """
    output = get_automation_reaction_role_item_with_emoji_id(automation_reaction_role_entry, emoji_id)
    vampytest.assert_instance(output, AutomationReactionRoleItem, nullable = True)
    return output
