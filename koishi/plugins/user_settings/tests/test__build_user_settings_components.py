import vampytest
from hata import Component, create_text_display

from ..component_building import build_user_settings_components
from ..constants import (
    PREFERRED_CLIENT_NAME_DEFAULT, PREFERRED_IMAGE_SOURCE_TOUHOU, PREFERRED_IMAGE_SOURCE_NAME_TOUHOU
)
from ..user_settings import UserSettings


def _iter_options():
    user_id = 202605040000
    
    user_settings = UserSettings.create_with_specification(
        user_id,
        feature_market_place_inbox = 0,
        notification_adventure_recovery_over = 0,
        notification_daily_by_waifu = 0,
        notification_daily_reminder = 0,
        notification_gift = 0,
        notification_market_place_item_finalisation = 0,
        notification_proposal = 0,
        notification_vote = 0,
        preferred_client_id = 202605040001,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU,
    )
    
    yield (
        'default',
        user_settings,
        0,
        [
            create_text_display(
                '- Market-place-inbox: false'
            ),
            create_text_display(
                '- Adventure-recovery-over: false\n'
                '- Daily-by-waifu: false\n'
                '- Daily-reminder: false\n'
                '- Gift: false\n'
                '- Market-place-item-finalisation: false\n'
                '- Proposal: false\n'
                '- Vote: false'
            ),
            create_text_display(
                f'- Preferred client: {PREFERRED_CLIENT_NAME_DEFAULT!s}\n'
                f'- Preferred image source: {PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__build_user_settings_components(user_settings, guild_id):
    """
    Tests whether ``build_user_settings_components`` works as intended.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    guild_id : `int`
        The local guild's identifier.
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_user_settings_components(user_settings, guild_id)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
