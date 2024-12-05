import vampytest
from hata import Embed, User

from ..builders import build_notification_settings_embed
from ..user_settings import UserSettings


def test__build_notification_settings_embed():
    """
    Tests whether ``build_notification_settings_embed`` works as intended.
    """
    user_id = 202309270000
    
    user_settings = UserSettings(
        user_id,
        notification_daily_by_waifu = True,
        notification_daily_reminder = False,
        notification_proposal = False,
        notification_vote = False,
    )
    
    user = User.precreate(user_id)
    
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
        'Daily-reminder',
        (
            '```\n'
            'false\n'
            '```'
        ),
    ).add_field(
        'Proposal',
        (
            '```\n'
            'false\n'
            '```'
        ),
    ).add_field(
        'Vote',
        (
            '```\n'
            'false\n'
            '```'
        ),
    )
    
    
    output = build_notification_settings_embed(user, user_settings)
    vampytest.assert_instance(output, Embed)
    vampytest.assert_eq(output, expected_output)
