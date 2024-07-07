from itertools import chain

import vampytest
from hata import Client, Guild, User

from ..orin import should_show_orin


async def test__should_show_orin():
    """
    Tests whether ``should_show_orin`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407050332
    user_id = 202407050333
    guild_id = 202407050334
    count = 0
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    user = User.precreate(user_id)
    guild = Guild.precreate(guild_id)
    
    async def count_entries_mock(client, guild, user, audit_log_interval, entry_types):
        nonlocal count
        return count
    
    mocked = vampytest.mock_globals(
        should_show_orin,
        count_entries = count_entries_mock,
    )
    
    try:
        count = 5
        output = await mocked(client, guild, user)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        
        
        for count in chain(range(0, 5), range(6, 10)):
            output = await mocked(client, guild, user)
            vampytest.assert_instance(output, bool)
            vampytest.assert_eq(output, False)
        
    finally:
        client._delete()
        client = None
