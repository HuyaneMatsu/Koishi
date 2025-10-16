import vampytest
from hata import Message

from ....bot_utils.models import DB_ENGINE

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..queries import query_update_automation_reaction_role_entry


@vampytest.skip_if(DB_ENGINE is not None)
async def test__query_update_automation_reaction_role_entry():
    """
    Tests whether ``query_update_automation_reaction_role_entry`` works as intended.
    
    This function is a coroutine.
    """
    message_id = 202510030010
    channel_id = 202510030011
    guild_id = 202510030012
    query_called = False
    entry_id = 777
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    
    async def query(input_automation_reaction_role_entry):
        nonlocal automation_reaction_role_entry
        nonlocal query_called
        vampytest.assert_eq(automation_reaction_role_entry, input_automation_reaction_role_entry)
        query_called = True
    
    mocked = vampytest.mock_globals(
        query_update_automation_reaction_role_entry,
        _query_update_automation_reaction_role_entry = query,
    )
    
    await mocked(automation_reaction_role_entry)
    
    vampytest.assert_true(query_called)
