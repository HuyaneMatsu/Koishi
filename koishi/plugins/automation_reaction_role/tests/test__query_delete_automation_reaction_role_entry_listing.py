import vampytest
from hata import Message

from ....bot_utils.models import DB_ENGINE

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..queries import query_delete_automation_reaction_role_entry_listing


@vampytest.skip_if(DB_ENGINE is not None)
async def test__query_delete_automation_reaction_role_entry_listing():
    """
    Tests whether ``query_delete_automation_reaction_role_entry_listing`` works as intended.
    
    This function is a coroutine.
    """
    message_id_0 = 202510030030
    message_id_1 = 202510030033
    message_id_2 = 202510030034
    channel_id_0 = 202510030031
    channel_id_1 = 202510030034
    channel_id_2 = 202510030036
    guild_id_0 = 202510030032
    guild_id_1 = 202510030035
    entry_id_0 = 777
    entry_id_1 = 778
    entry_id_2 = 779
    query_called = False
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id_0,
        guild_id = guild_id_0,
    )
    
    message_1 = Message.precreate(
        message_id_1,
        channel_id = channel_id_1,
        guild_id = guild_id_0,
    )
    
    message_2 = Message.precreate(
        message_id_2,
        channel_id = channel_id_2,
        guild_id = guild_id_1,
    )
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message_0,
    )
    automation_reaction_role_entry_0.entry_id = entry_id_0
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(
        message_1,
    )
    automation_reaction_role_entry_1.entry_id = entry_id_1
    
    automation_reaction_role_entry_2 = AutomationReactionRoleEntry(
        message_2,
    )
    automation_reaction_role_entry_2.entry_id = entry_id_2
    
    
    
    automation_reaction_role_by_message_id = {
        message_id_0 : automation_reaction_role_entry_0,
        message_id_1 : automation_reaction_role_entry_1,
        message_id_2 : automation_reaction_role_entry_2,
    }
    automation_reaction_role_by_guild_id = {
        guild_id_0 : [
            automation_reaction_role_entry_0,
            automation_reaction_role_entry_1,
        ],
        guild_id_1 : [
            automation_reaction_role_entry_2,
        ],
    }
    
    async def query(input_automation_reaction_role_entries):
        nonlocal automation_reaction_role_entry_0
        nonlocal automation_reaction_role_entry_1
        nonlocal query_called
        vampytest.assert_eq([automation_reaction_role_entry_0, automation_reaction_role_entry_1], input_automation_reaction_role_entries)
        query_called = True
    
    mocked = vampytest.mock_globals(
        query_delete_automation_reaction_role_entry_listing,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID = automation_reaction_role_by_guild_id,
        _query_delete_automation_reaction_role_entry_listing = query,
        recursion = 2,
    )
    
    await mocked([automation_reaction_role_entry_0, automation_reaction_role_entry_1])
    
    vampytest.assert_true(query_called)
    
    vampytest.assert_eq(
        automation_reaction_role_by_message_id,
        {
            message_id_2: automation_reaction_role_entry_2,
        },
    )
    
    vampytest.assert_eq(
        automation_reaction_role_by_guild_id,
        {
            guild_id_1: [
                automation_reaction_role_entry_2,
            ],
        },
    )
