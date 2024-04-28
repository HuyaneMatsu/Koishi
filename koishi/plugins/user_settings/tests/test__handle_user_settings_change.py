import vampytest
from hata import Embed, InteractionEvent, User
from hata.ext.slash import InteractionResponse

from ..user_settings import UserSettings
from ..options import OPTION_NOTIFICATION_DAILY_BY_WAIFU, OPTION_NOTIFICATION_PROPOSAL
from ..utils import handle_user_settings_change


def _iter_options():
    user = User.precreate(
        202309270061,
        name = 'Koishi',
    )
    
    yield (
        InteractionEvent.precreate(
            202309270062,
            user = user,
        ),
        OPTION_NOTIFICATION_DAILY_BY_WAIFU,
        True,
        UserSettings(user.id, notification_daily_by_waifu = False),
        None,
        InteractionResponse(
            embed = Embed(
                'Great success!',
                'From now on, you will receive daily-by-waifu notifications.'
            ).add_thumbnail(
                user.avatar_url,
            ),
            show_for_invoking_user_only = True,
        ),
    )

    yield (
        InteractionEvent.precreate(
            202309270063,
            user = user,
        ),
        OPTION_NOTIFICATION_PROPOSAL,
        False,
        UserSettings(user.id, notification_proposal = True),
        UserSettings(user.id, notification_proposal = False),
        InteractionResponse(
            embed = Embed(
                'Great success!',
                'From now, you will **not** receive proposal notifications.'
            ).add_thumbnail(
                user.avatar_url,
            ),
            show_for_invoking_user_only = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__handle_user_settings_change(
    event,
    option,
    value,
    user_settings,
    expected_saved_user_settings,
):
    """
    Tests whether ``handle_user_settings_change`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    option : ``NotificationOption``
        Option representing the changed notification setting.
    value : `bool`
        The new value to set.
    user_settings : ``UserSettings``
        The notification settings to return from get query.
    expected_saved_user_settings : `None | UserSettings`
        Whether we expected anything to be saved and what exactly.
    
    Returns
    -------
    output : ``InteractionResponse``
    """
    get_query_called = False
    called_with_user_id = 0
    
    async def get_query(user_id):
        nonlocal get_query_called
        nonlocal called_with_user_id
        nonlocal user_settings
        
        get_query_called = True
        called_with_user_id = user_id
        return user_settings
    
    
    save_query_called = False
    called_with_user_settings = None
    
    
    async def save_query(user_settings):
        nonlocal save_query_called
        nonlocal called_with_user_settings
        
        save_query_called = True
        called_with_user_settings = user_settings.copy()
    
    
    mocked = vampytest.mock_globals(
        handle_user_settings_change,
        2,
        get_one_user_settings = get_query,
        save_one_user_settings = save_query,
    )
    
    output = await mocked(event, option, value)
    vampytest.assert_instance(output, InteractionResponse)
    vampytest.assert_true(get_query_called)
    vampytest.assert_eq(called_with_user_id, event.user.id)
    if expected_saved_user_settings is not None:
        vampytest.assert_true(save_query_called)
        vampytest.assert_eq(called_with_user_settings, expected_saved_user_settings)
    return output
