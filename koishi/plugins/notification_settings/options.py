__all__ = ('NOTIFICATION_SETTINGS_CHOICES', 'NOTIFICATION_SETTING_RESOLUTION')

from .notification_settings import NotificationSettings
from .option import NotificationSettingsOption


OPTION_DAILY_BY_WAIFU = NotificationSettingsOption(
    NotificationSettings.daily_by_waifu,
    'daily_by_waifu',
    'daily-by-waifu',
)

OPTION_DAILY_REMINDER = NotificationSettingsOption(
    NotificationSettings.daily_reminder,
    'daily_reminder',
    'daily-reminder',
)

OPTION_NOTIFIER_CLIENT_ID = NotificationSettingsOption(
    NotificationSettings.notifier_client_id,
    'notifier_client_id',
    'notifier-client',
)

OPTION_PROPOSAL = NotificationSettingsOption(
    NotificationSettings.proposal,
    'proposal',
    'proposal',
)


NOTIFICATION_SETTING_RESOLUTION = {
    OPTION_DAILY_BY_WAIFU.system_name: OPTION_DAILY_BY_WAIFU,
    OPTION_DAILY_REMINDER.system_name: OPTION_DAILY_REMINDER,
    OPTION_PROPOSAL.system_name: OPTION_PROPOSAL,
}

NOTIFICATION_SETTINGS_CHOICES = sorted(NOTIFICATION_SETTING_RESOLUTION.keys())
NOTIFICATION_SETTINGS_SORTED = (*(NOTIFICATION_SETTING_RESOLUTION[name] for name in NOTIFICATION_SETTINGS_CHOICES),)
