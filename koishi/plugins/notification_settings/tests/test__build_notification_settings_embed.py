import vampytest
from hata import Embed, User

from ..builders import build_notification_settings_embed
from ..constants import NOTIFIER_NAME_DEFAULT
from ..notification_settings import NotificationSettings


def test__build_notification_settings_embed():
    """
    Tests whether ``build_notification_settings_embed`` works as intended.
    """
    user_id = 202309270000
    
    notification_settings = NotificationSettings(
        user_id,
        daily_by_waifu = True,
        daily_reminder = False,
        proposal = False,
        notifier_client_id = 202402250013,
    )
    
    user = User.precreate(user_id)
    
    expected_output = Embed(
        'Notification settings',
    ).add_thumbnail(
        user.avatar_url,
    ).add_field(
        'Notifier',
        (
            f'```\n'
            f'{NOTIFIER_NAME_DEFAULT!s}\n'
            f'```'
        ),
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
    )
        
    
    output = build_notification_settings_embed(user, notification_settings)
    vampytest.assert_instance(output, Embed)
    vampytest.assert_eq(output, expected_output)


def test__build_notification_settings_embed__field_notifier_set():
    """
    Tests whether ``build_notification_settings_embed`` works as intended.
    
    Case: Notifier set.
    """
    user_id = 202402250012
    notifier_client_id = 202402250014
    notifier_client_name = 'pudding'
    
    notification_settings = NotificationSettings(
        user_id,
        notifier_client_id = notifier_client_id,
    )
    
    user = User.precreate(user_id)
    notifier_client = User.precreate(notifier_client_id, name = notifier_client_name)
    
    expected_embed_field_value = (
        f'```\n'
        f'{notifier_client_name!s}\n'
        f'```'        
    )
    
    mocked = vampytest.mock_globals(build_notification_settings_embed, CLIENTS = {notifier_client_id: notifier_client})
    
    output = mocked(user, notification_settings)
    vampytest.assert_instance(output, Embed)
    
    for field in output.iter_fields():
        if field.name.casefold() == 'notifier':
            break
    else:
        field = None
    
    vampytest.assert_is_not(field, None)
    vampytest.assert_eq(field.value, expected_embed_field_value)
