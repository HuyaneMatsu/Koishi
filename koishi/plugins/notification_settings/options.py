__all__ = ('NOTIFICATION_SETTINGS_CHOICES', 'NOTIFICATION_SETTING_RESOLUTION')

from .notification_settings import NotificationSettings
from .option import NotificationSettingsOption


OPTION_DAILY = NotificationSettingsOption(NotificationSettings.daily, 'daily', 'daily-by-waifu')
OPTION_PROPOSAL = NotificationSettingsOption(NotificationSettings.proposal, 'proposal', 'proposal')


NOTIFICATION_SETTING_RESOLUTION = {
    OPTION_DAILY.system_name: OPTION_DAILY,
    OPTION_PROPOSAL.system_name: OPTION_PROPOSAL,
}

NOTIFICATION_SETTINGS_CHOICES = sorted(NOTIFICATION_SETTING_RESOLUTION.keys())
NOTIFICATION_SETTINGS_SORTED = (*(NOTIFICATION_SETTING_RESOLUTION[name] for name in NOTIFICATION_SETTINGS_CHOICES),)
