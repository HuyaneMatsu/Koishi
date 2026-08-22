__all__ = (
    'FEATURE_SETTINGS_CHOICES', 'FEATURE_SETTING_RESOLUTION', 'NOTIFICATION_SETTINGS_CHOICES',
    'NOTIFICATION_SETTING_RESOLUTION', 'OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER', 'OPTION_PREFERRED_CLIENT_ID',
    'OPTION_PREFERRED_IMAGE_SOURCE'
)

from .constants import (
    USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_ACTION,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE
)
from .option import (
    user_settings_option_create_bit, user_settings_option_create_bit_with_hook, user_settings_option_create_regular
)
from .user_settings import UserSettings


# Features

OPTION_FEATURE_MARKET_PLACE_INBOX = user_settings_option_create_bit(
    UserSettings.feature_flags,
    'feature_market_place_inbox',
    'market-place-inbox',
    USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX,
)

FEATURE_SETTING_RESOLUTION = {
    OPTION_FEATURE_MARKET_PLACE_INBOX.name : OPTION_FEATURE_MARKET_PLACE_INBOX,
}

FEATURE_SETTINGS_CHOICES = sorted(
    (option.display_name, option.name) for option in FEATURE_SETTING_RESOLUTION.values()
)
FEATURE_SETTINGS_SORTED = (*(FEATURE_SETTING_RESOLUTION[item[1]] for item in FEATURE_SETTINGS_CHOICES),)


# Notifications

OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER = user_settings_option_create_bit_with_hook(
    UserSettings.notification_flags,
    'notification_adventure_recovery_over',
    'adventure-recovery-over',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER,
)

OPTION_NOTIFICATION_DAILY_BY_WAIFU = user_settings_option_create_bit(
    UserSettings.notification_flags,
    'notification_daily_by_waifu',
    'daily-by-waifu',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU,
)

OPTION_NOTIFICATION_DAILY_REMINDER = user_settings_option_create_bit(
    UserSettings.notification_flags,
    'notification_daily_reminder',
    'daily-reminder',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER,
)

OPTION_NOTIFICATION_GIFT = user_settings_option_create_bit(
    UserSettings.notification_flags,
    'notification_gift',
    'gift',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT,
)

OPTION_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION = user_settings_option_create_bit(
    UserSettings.notification_flags,
    'notification_market_place_item_finalisation',
    'market-place-item-finalisation',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION,
)

OPTION_NOTIFICATION_PROPOSAL = user_settings_option_create_bit(
    UserSettings.notification_flags,
    'notification_proposal',
    'proposal',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL,
)

OPTION_NOTIFICATION_VOTE = user_settings_option_create_bit(
    UserSettings.notification_flags,
    'notification_vote',
    'vote',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE,
)

OPTION_NOTIFICATION_ADVENTURE_ACTION = user_settings_option_create_bit_with_hook(
    UserSettings.notification_flags,
    'notification_adventure_action',
    'adventure-action',
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_ACTION,
)


NOTIFICATION_SETTING_RESOLUTION = {
    OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER.name : OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER,
    OPTION_NOTIFICATION_DAILY_BY_WAIFU.name: OPTION_NOTIFICATION_DAILY_BY_WAIFU,
    OPTION_NOTIFICATION_DAILY_REMINDER.name: OPTION_NOTIFICATION_DAILY_REMINDER,
    OPTION_NOTIFICATION_GIFT.name: OPTION_NOTIFICATION_GIFT,
    OPTION_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION.name : OPTION_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION,
    OPTION_NOTIFICATION_PROPOSAL.name: OPTION_NOTIFICATION_PROPOSAL,
    OPTION_NOTIFICATION_VOTE.name: OPTION_NOTIFICATION_VOTE,
    OPTION_NOTIFICATION_ADVENTURE_ACTION.name : OPTION_NOTIFICATION_ADVENTURE_ACTION,
}

NOTIFICATION_SETTINGS_CHOICES = sorted(
    (option.display_name, option.name) for option in NOTIFICATION_SETTING_RESOLUTION.values()
)
NOTIFICATION_SETTINGS_SORTED = (*(NOTIFICATION_SETTING_RESOLUTION[item[1]] for item in NOTIFICATION_SETTINGS_CHOICES),)

# Preference

OPTION_PREFERRED_CLIENT_ID = user_settings_option_create_regular(
    UserSettings.preferred_client_id,
    'preferred_client_id',
    'preferred-client',
)

OPTION_PREFERRED_IMAGE_SOURCE = user_settings_option_create_regular(
    UserSettings.preferred_image_source,
    'preferred_image_source',
    'preferred-image-source',
)
