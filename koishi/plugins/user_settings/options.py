__all__ = ('NOTIFICATION_SETTINGS_CHOICES', 'NOTIFICATION_SETTING_RESOLUTION', 'OPTION_PREFERRED_CLIENT_ID')

from .user_settings import UserSettings
from .option import UserSettingsOption


# Notifications

OPTION_NOTIFICATION_DAILY_BY_WAIFU = UserSettingsOption(
    UserSettings.notification_daily_by_waifu,
    'notification_daily_by_waifu',
    'daily-by-waifu',
)

OPTION_NOTIFICATION_DAILY_REMINDER = UserSettingsOption(
    UserSettings.notification_daily_reminder,
    'notification_daily_reminder',
    'daily-reminder',
)

OPTION_NOTIFICATION_GIFT = UserSettingsOption(
    UserSettings.notification_gift,
    'notification_gift',
    'gift',
)

OPTION_NOTIFICATION_PROPOSAL = UserSettingsOption(
    UserSettings.notification_proposal,
    'notification_proposal',
    'proposal',
)

OPTION_NOTIFICATION_VOTE = UserSettingsOption(
    UserSettings.notification_vote,
    'notification_vote',
    'vote',
)


NOTIFICATION_SETTING_RESOLUTION = {
    OPTION_NOTIFICATION_DAILY_BY_WAIFU.system_name: OPTION_NOTIFICATION_DAILY_BY_WAIFU,
    OPTION_NOTIFICATION_DAILY_REMINDER.system_name: OPTION_NOTIFICATION_DAILY_REMINDER,
    OPTION_NOTIFICATION_GIFT.system_name: OPTION_NOTIFICATION_GIFT,
    OPTION_NOTIFICATION_PROPOSAL.system_name: OPTION_NOTIFICATION_PROPOSAL,
    OPTION_NOTIFICATION_VOTE.system_name: OPTION_NOTIFICATION_VOTE,
}

NOTIFICATION_SETTINGS_CHOICES = sorted(
    (option.display_name, option.system_name) for option in NOTIFICATION_SETTING_RESOLUTION.values()
)
NOTIFICATION_SETTINGS_SORTED = (*(NOTIFICATION_SETTING_RESOLUTION[item[1]] for item in NOTIFICATION_SETTINGS_CHOICES),)

# Preference

OPTION_PREFERRED_CLIENT_ID = UserSettingsOption(
    UserSettings.preferred_client_id,
    'preferred_client_id',
    'preferred-client',
)

OPTION_PREFERRED_IMAGE_SOURCE = UserSettingsOption(
    UserSettings.preferred_image_source,
    'preferred_image_source',
    'preferred-image_source',
)
