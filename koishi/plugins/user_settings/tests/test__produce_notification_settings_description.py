import vampytest

from ..builders import produce_notification_settings_description
from ..user_settings import UserSettings


def _iter_options():
    user_id = 202510080000
    
    user_settings = UserSettings(
        user_id,
        notification_daily_by_waifu = True,
        notification_daily_reminder = False,
        notification_gift = False,
        notification_proposal = False,
        notification_vote = False,
    )
    
    yield (
        user_settings,
        (
            '- Daily-by-waifu: true\n'
            '- Daily-reminder: false\n'
            '- Gift: false\n'
            '- Proposal: false\n'
            '- Vote: false'
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_notification_settings_description(user_settings):
    """
    Tests whether ``produce_notification_settings_description`` works as intended.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_notification_settings_description(user_settings)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
