import vampytest
from hata import Client, ClientWrapper, Guild, GuildProfile, Sticker, StickerType

from ..events import sticker_delete


async def test__sticker_delete():
    """
    Tests whether ``sticker_delete`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202503170082
    sticker_id_0 = 202503170083
    guild_id = 202503170088
    
    sticker_0 = Sticker.precreate(sticker_id_0, name = 'KoishiSmile', sticker_type = StickerType.guild)
    
    execute_sticker_delete_called = False
    
    async def mocked_execute_sticker_delete(input_sticker):
        nonlocal sticker_0
        nonlocal execute_sticker_delete_called
        
        vampytest.assert_is(sticker_0, input_sticker)
        execute_sticker_delete_called = True
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    guild = None
    try:
        client.guild_profiles[guild_id] = GuildProfile()
        
        guild = Guild.precreate(
            guild_id,
        )
        
        guild.clients.append(client)
        
        client_wrapper = ClientWrapper(client)
        
        mocked = vampytest.mock_globals(
            sticker_delete,
            execute_sticker_delete = mocked_execute_sticker_delete,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, sticker_0)
        
        vampytest.assert_true(execute_sticker_delete_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
