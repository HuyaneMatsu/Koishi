import vampytest
from hata import Client, Embed, InteractionEvent, User
from hata.ext.slash import InteractionResponse

from ..notification_settings import NotificationSettings
from ..utils import handle_notification_settings_set_notifier


async def test__handle_notification_settings_set_notifier():
    """
    Tests whether ``build_notification_settings_notifier_change_embed`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202402260013
    client_id = 202402260014
    client_name = 'komeiji'
    
    notification_settings = NotificationSettings(
        user_id,
    )
    expected_saved_notification_settings = NotificationSettings(
        user_id,
        notifier_client_id = client_id,
    )
    
    user = User.precreate(user_id)
    
    event = InteractionEvent(
        user = user,
    )
    value = 'koishi'
    
    get_notification_settings_notifier_called = False
    get_query_called = False
    save_query_called = False
    
    
    def get_notification_settings_notifier(input_event, input_value):
        nonlocal event
        nonlocal value
        nonlocal client
        nonlocal get_notification_settings_notifier_called
        
        vampytest.assert_is(event, input_event)
        vampytest.assert_is(value, input_value)
        get_notification_settings_notifier_called = True
        return True, client
    
    
    async def get_query(input_user_id):
        nonlocal get_query_called
        nonlocal user_id
        nonlocal notification_settings
        
        get_query_called = True
        
        vampytest.assert_eq(input_user_id, user_id)
        
        return notification_settings
    
    
    async def save_query(input_notification_settings):
        nonlocal save_query_called
        nonlocal expected_saved_notification_settings
        
        vampytest.assert_eq(input_notification_settings, expected_saved_notification_settings)
        
        save_query_called = True
    
    
    mocked = vampytest.mock_globals(
        handle_notification_settings_set_notifier,
        2,
        get_one_notification_settings = get_query,
        save_one_notification_settings = save_query,
        get_notification_settings_notifier = get_notification_settings_notifier,
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
        vampytest.assert_true(get_notification_settings_notifier_called)
        
        vampytest.assert_eq(
            output,
            InteractionResponse(
                embed = Embed(
                    'Great success!',
                    f'Notifier set to `{client_name!s}`.',
                ).add_thumbnail(
                    user.avatar_url,
                ),
                show_for_invoking_user_only = True,
            ),
        )
    finally:
        client._delete()
        client = None
