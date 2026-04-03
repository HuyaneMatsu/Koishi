import vampytest
from hata import Message

from ....bot_utils.models import DB_ENGINE

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..helpers import get_or_create_automation_reaction_role_entry


@vampytest.skip_if(DB_ENGINE is not None)
async def test__get_or_create_automation_reaction_role_entry__new():
    """
    Tests whether ``get_or_create_automation_reaction_role_entry`` works as intended.
    
    This function is a coroutine.
    
    Case: new.
    """
    message_id = 202510040000
    channel_id = 202510040001
    guild_id = 202510040002
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_by_guild_id = {}
    automation_reaction_role_by_message_id = {}
    
    mocked = vampytest.mock_globals(
        get_or_create_automation_reaction_role_entry,
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID = automation_reaction_role_by_guild_id,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
        recursion = 3,
    )
    
    output = await mocked(message)
    
    # Assert output
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], AutomationReactionRoleEntry)
    vampytest.assert_instance(output[1], int)
    
    automation_reaction_role_entry, page_index = output
    
    vampytest.assert_is_not(automation_reaction_role_entry, None)
    vampytest.assert_is(automation_reaction_role_entry.message, message)
    vampytest.assert_true(automation_reaction_role_entry.message_cached)
    vampytest.assert_true(automation_reaction_role_entry.entry_id)
    
    vampytest.assert_eq(page_index, 0)
    
    # Assert cache
    vampytest.assert_eq(
        automation_reaction_role_by_guild_id,
        {
            guild_id : [
                automation_reaction_role_entry,
            ],
        },
    )
    
    vampytest.assert_eq(
        automation_reaction_role_by_message_id,
        {
            message_id : automation_reaction_role_entry,
        },
    )


@vampytest.skip_if(DB_ENGINE is not None)
async def test__get_or_create_automation_reaction_role_entry__existing():
    """
    Tests whether ``get_or_create_automation_reaction_role_entry`` works as intended.
    
    This function is a coroutine.
    
    Case: existing.
    """
    message_id = 202510040010
    channel_id = 202510040011
    guild_id = 202510040012
    entry_id = 888
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    
    automation_reaction_role_by_guild_id = {
        guild_id : [
            automation_reaction_role_entry,
        ],
    }
    automation_reaction_role_by_message_id = {
        message_id : automation_reaction_role_entry,
    }
    
    
    mocked = vampytest.mock_globals(
        get_or_create_automation_reaction_role_entry,
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID = automation_reaction_role_by_guild_id,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
        recursion = 3,
    )
    
    output = await mocked(message)
    
    # Assert output
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], AutomationReactionRoleEntry)
    vampytest.assert_instance(output[1], int)
    
    returned_automation_reaction_role_entry, page_index = output
    
    vampytest.assert_is_not(returned_automation_reaction_role_entry, None)
    vampytest.assert_is(returned_automation_reaction_role_entry, automation_reaction_role_entry)
    vampytest.assert_true(automation_reaction_role_entry.message_cached)
    
    vampytest.assert_eq(page_index, 0)
    
    # Assert cache
    vampytest.assert_eq(
        automation_reaction_role_by_guild_id,
        {
            guild_id : [
                automation_reaction_role_entry,
            ],
        },
    )
    
    vampytest.assert_eq(
        automation_reaction_role_by_message_id,
        {
            message_id : automation_reaction_role_entry,
        },
    )
