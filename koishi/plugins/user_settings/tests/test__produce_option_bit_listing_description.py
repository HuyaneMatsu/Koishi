import vampytest

from ..content_building import produce_option_bit_listing_description
from ..options import NOTIFICATION_SETTINGS_SORTED
from ..user_settings import UserSettings


def _iter_options():
    user_id = 202510080000
    
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
        NOTIFICATION_SETTINGS_SORTED,
        (
            '- Adventure-recovery-over: true\n'
            '- Daily-by-waifu: true\n'
            '- Daily-reminder: false\n'
            '- Gift: false\n'
            '- Market-place-item-finalisation: true\n'
            '- Proposal: false\n'
            '- Vote: false'
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_option_bit_listing_description(user_settings, option_bit_listing):
    """
    Tests whether ``produce_option_bit_listing_description`` works as intended.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    option_bit_listing : ``tuple<UserSettingsOptionBit>``
        Options to produce.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_option_bit_listing_description(user_settings, option_bit_listing)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
