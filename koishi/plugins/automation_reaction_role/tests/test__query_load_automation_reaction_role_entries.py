import vampytest

from ....bot_utils.models import DB_ENGINE

from ..constants import ENTRY_DATA_VERSION
from ..queries import query_load_automation_reaction_role_entries


@vampytest.skip_if(DB_ENGINE is not None)
async def test__query_load_automation_reaction_role_entries():
    """
    Tests whether ``query_load_automation_reaction_role_entries`` works as intended.
    
    This function is a coroutine.
    """
    message_id_0 = 202510050070
    message_id_1 = 202510050071
    message_id_2 = 202510050072
    channel_id_0 = 202510050073
    channel_id_1 = 202510050074
    channel_id_2 = 202510050075
    guild_id_0 = 202510050076
    guild_id_1 = 202510050077
    entry_id_0 = 777
    entry_id_1 = 778
    entry_id_2 = 779
    query_called = False
    
    response_data = [
        {
            'id': entry_id_0,
            'flags': 0,
            'data': None,
            'data_version':ENTRY_DATA_VERSION,
            'message_id': message_id_0,
            'channel_id': channel_id_0,
            'guild_id': guild_id_0,
        },
        {
            'id': entry_id_1,
            'flags': 0,
            'data': None,
            'data_version':ENTRY_DATA_VERSION,
            'message_id': message_id_1,
            'channel_id': channel_id_1,
            'guild_id': guild_id_1,
        },
        {
            'id': entry_id_2,
            'flags': 0,
            'data': None,
            'data_version':ENTRY_DATA_VERSION,
            'message_id': message_id_2,
            'channel_id': channel_id_2,
            'guild_id': guild_id_1,
        },
    ]
    
    
    automation_reaction_role_by_message_id = {}
    automation_reaction_role_by_guild_id = {}
    
    async def query():
        nonlocal response_data
        nonlocal query_called
        query_called = True
        return response_data
    
    mocked = vampytest.mock_globals(
        query_load_automation_reaction_role_entries,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID = automation_reaction_role_by_guild_id,
        _query_get_automation_reaction_role_entries = query,
        recursion = 2,
    )
    
    await mocked()
    
    vampytest.assert_true(query_called)
    
    vampytest.assert_eq(
        {*automation_reaction_role_by_message_id.keys()},
        {message_id_0, message_id_1, message_id_2},
    )
    
    vampytest.assert_eq(
        {*automation_reaction_role_by_guild_id.keys()},
        {guild_id_0, guild_id_1},
    )
