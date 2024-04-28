import vampytest
from hata import Client, Embed, InteractionEvent, User
from hata.ext.slash import InteractionResponse

from ..user_settings import UserSettings
from ..utils import handle_user_settings_set_preferred_client


async def test__handle_user_settings_set_preferred_client():
    """
    Tests whether ``build_user_settings_preferred_client_change_embed`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202402260013
    client_id = 202402260014
    client_name = 'komeiji'
    
    user_settings = UserSettings(
        user_id,
    )
    expected_saved_user_settings = UserSettings(
        user_id,
        preferred_client_id = client_id,
    )
    
    user = User.precreate(user_id)
    
    event = InteractionEvent(
        user = user,
    )
    value = 'koishi'
    
    get_user_settings_preferred_client_called = False
    get_query_called = False
    save_query_called = False
    
    
    def get_user_settings_preferred_client(input_event, input_value):
        nonlocal event
        nonlocal value
        nonlocal client
        nonlocal get_user_settings_preferred_client_called
        
        vampytest.assert_is(event, input_event)
        vampytest.assert_is(value, input_value)
        get_user_settings_preferred_client_called = True
        return True, client
    
    
    async def get_query(input_user_id):
        nonlocal get_query_called
        nonlocal user_id
        nonlocal user_settings
        
        get_query_called = True
        
        vampytest.assert_eq(input_user_id, user_id)
        
        return user_settings
    
    
    async def save_query(input_user_settings):
        nonlocal save_query_called
        nonlocal expected_saved_user_settings
        
        vampytest.assert_eq(input_user_settings, expected_saved_user_settings)
        
        save_query_called = True
    
    
    mocked = vampytest.mock_globals(
        handle_user_settings_set_preferred_client,
        2,
        get_one_user_settings = get_query,
        save_one_user_settings = save_query,
        get_user_settings_preferred_client = get_user_settings_preferred_client,
    )
    
    client = Client(
        'token' + str(client_id),
        client_id = client_id,
        name = client_name,
    )
    
    try:
        output = await mocked(event, value)
        vampytest.assert_instance(output, InteractionResponse)
        vampytest.assert_true(get_query_called)
        vampytest.assert_true(save_query_called)
        vampytest.assert_true(get_user_settings_preferred_client_called)
        
        vampytest.assert_eq(
            output,
            InteractionResponse(
                embed = Embed(
                    'Great success!',
                    f'Preferred client set to `{client_name!s}`.',
                ).add_thumbnail(
                    user.avatar_url,
                ),
                show_for_invoking_user_only = True,
            ),
        )
    finally:
        client._delete()
        client = None
