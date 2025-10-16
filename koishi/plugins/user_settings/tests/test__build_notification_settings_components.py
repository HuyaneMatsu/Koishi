import vampytest
from hata import Component, create_text_display

from ..builders import build_notification_settings_components
from ..user_settings import UserSettings


def _iter_options():
    user_id = 202309270000
    
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
        [
            create_text_display(
                '- Daily-by-waifu: true\n'
                '- Daily-reminder: false\n'
                '- Gift: false\n'
                '- Proposal: false\n'
                '- Vote: false'
            ),
        ],
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_settings_components(user_settings):
    """
    Tests whether ``build_notification_settings_components`` works as intended.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_notification_settings_components(user_settings)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
