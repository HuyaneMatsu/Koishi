import vampytest
from hata import Component, create_text_display

from ..component_building import build_notification_settings_components
from ..user_settings import UserSettings


def _iter_options():
    user_id = 202309270000
    
    user_settings = UserSettings.create_with_specification(
        user_id,
        notification_adventure_recovery_over = 1,
        notification_daily_by_waifu = 1,
        notification_daily_reminder = 0,
        notification_gift = 0,
        notification_market_place_item_finalisation = 1,
        notification_proposal = 0,
        notification_vote = 0,
    )
    
    yield (
        user_settings,
        [
            create_text_display(
                '- Adventure-recovery-over: true\n'
                '- Daily-by-waifu: true\n'
                '- Daily-reminder: false\n'
                '- Gift: false\n'
                '- Market-place-item-finalisation: true\n'
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
