__all__ = ()

from ...bots import FEATURE_CLIENTS

from .constants import (
    NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_BY_WAIFU_DISABLE, NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_BY_WAIFU_ENABLE,
    NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_REMINDER_DISABLE, NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_REMINDER_ENABLE,
    NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_DISABLE, NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_ENABLE,
)
from .options import OPTION_DAILY_BY_WAIFU, OPTION_DAILY_REMINDER, OPTION_PROPOSAL
from .utils import handle_notification_settings_change


@FEATURE_CLIENTS.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_BY_WAIFU_ENABLE)
async def handle_notification_settings_daily_by_waifu_enable(event):
    return await handle_notification_settings_change(event, OPTION_DAILY_BY_WAIFU, True)


@FEATURE_CLIENTS.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_BY_WAIFU_DISABLE)
async def handle_notification_settings_daily_by_waifu_disable(event):
    return await handle_notification_settings_change(event, OPTION_DAILY_BY_WAIFU, False)


@FEATURE_CLIENTS.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_REMINDER_ENABLE)
async def handle_notification_settings_daily_reminder_enable(event):
    return await handle_notification_settings_change(event, OPTION_DAILY_REMINDER, True)


@FEATURE_CLIENTS.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_REMINDER_DISABLE)
async def handle_notification_settings_daily_reminder_disable(event):
    return await handle_notification_settings_change(event, OPTION_DAILY_REMINDER, False)


@FEATURE_CLIENTS.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_ENABLE)
async def handle_notification_settings_proposal_enable(event):
    return await handle_notification_settings_change(event, OPTION_PROPOSAL, True)


@FEATURE_CLIENTS.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_DISABLE)
async def handle_notification_settings_proposal_disable(event):
    return await handle_notification_settings_change(event, OPTION_PROPOSAL, False)
