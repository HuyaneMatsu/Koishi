import vampytest
from hata import Message

from ....bot_utils.models import DB_ENGINE

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..queries import query_save_automation_reaction_role_entry


@vampytest.skip_if(DB_ENGINE is not None)
async def test__query_save_automation_reaction_role_entry():
    """
    Tests whether ``query_save_automation_reaction_role_entry`` works as intended.
    
    This function is a coroutine.
    """
    message_id = 202510030000
    channel_id = 202510030001
    guild_id = 202510030002
    entry_id = 777
    query_called = False
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    
    automation_reaction_role_by_message_id = {}
    automation_reaction_role_by_guild_id = {}
    
    async def query(input_automation_reaction_role_entry):
        nonlocal automation_reaction_role_entry
        nonlocal entry_id
        nonlocal query_called
        vampytest.assert_eq(automation_reaction_role_entry, input_automation_reaction_role_entry)
        query_called = True
        return entry_id
    
    mocked = vampytest.mock_globals(
        query_save_automation_reaction_role_entry,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID = automation_reaction_role_by_guild_id,
        _query_save_automation_reaction_role_entry_entry = query,
    )
    
    await mocked(automation_reaction_role_entry)
    
    vampytest.assert_true(query_called)
    
    vampytest.assert_eq(
        automation_reaction_role_by_message_id,
        {
            message_id: automation_reaction_role_entry,
        },
    )
    
    vampytest.assert_eq(
        automation_reaction_role_by_guild_id,
        {
            guild_id: [
                automation_reaction_role_entry,
            ],
        },
    )
    
    vampytest.assert_eq(
        automation_reaction_role_entry.entry_id,
        entry_id,
    )
