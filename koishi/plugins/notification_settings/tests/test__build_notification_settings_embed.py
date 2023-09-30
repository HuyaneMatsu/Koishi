import vampytest
from hata import Embed, User

from ..builders import build_notification_settings_embed
from ..notification_settings import NotificationSettings


def test__build_notification_settings_embed():
    """
    Tests whether ``build_notification_settings_embed`` works as intended.
    """
    user = User.precreate(
        202309270000,
    )
    
    notification_settings = NotificationSettings(user.id, daily = True, proposal = False)
    
    expected_output = Embed(
        'Notification settings',
    ).add_thumbnail(
        user.avatar_url,
    ).add_field(
        'Daily-by-waifu',
        (
            '```\n'
            'true\n'
            '```'
        ),
    ).add_field(
        'Proposal',
        (
            '```\n'
            'false\n'
            '```'
        ),
    )
    
    output = build_notification_settings_embed(user, notification_settings)
    vampytest.assert_instance(output, Embed)
    vampytest.assert_eq(output, expected_output)
