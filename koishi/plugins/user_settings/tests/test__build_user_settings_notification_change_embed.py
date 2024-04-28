import vampytest
from hata import Embed, User

from ..builders import build_user_settings_notification_change_embed
from ..options import OPTION_NOTIFICATION_DAILY_BY_WAIFU, OPTION_NOTIFICATION_PROPOSAL


def _iter_options():
    user = User.precreate(202309270060)
    
    expected_output = Embed(
        'Great success!',
        'From now on, you will receive daily-by-waifu notifications.'
    ).add_thumbnail(
        user.avatar_url,
    )
    yield user, OPTION_NOTIFICATION_DAILY_BY_WAIFU, True, True, expected_output


    expected_output = Embed(
        'Uoh',
        'You were already **not** receiving proposal notifications.'
    ).add_thumbnail(
        user.avatar_url,
    )
    yield user, OPTION_NOTIFICATION_PROPOSAL, False, False, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_notification_change_embed(user, option, value, changed):
    """
    Tests whether ``build_user_settings_notification_change_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's notification settings are changed.
    option : ``NotificationOption``
        Option representing the changed notification setting.
    value : `bool`
        The new value to set.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    embed : ``Embed``
    """
    output = build_user_settings_notification_change_embed(user, option, value, changed)
    vampytest.assert_instance(output, Embed)
    return output
