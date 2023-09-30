__all__ = ()

from ...bots import SLASH_CLIENT

from .constants import (
    NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_DISABLE, NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_ENABLE,
    NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_DISABLE, NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_ENABLE,
)
from .options import OPTION_DAILY, OPTION_PROPOSAL
from .utils import handle_notification_settings_change


@SLASH_CLIENT.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_ENABLE)
async def handle_notification_settings_daily_enable(event):
    return await handle_notification_settings_change(event, OPTION_DAILY, True)


@SLASH_CLIENT.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_DAILY_DISABLE)
async def handle_notification_settings_daily_disable(event):
    return await handle_notification_settings_change(event, OPTION_DAILY, False)


@SLASH_CLIENT.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_ENABLE)
async def handle_notification_settings_proposal_enable(event):
    return await handle_notification_settings_change(event, OPTION_PROPOSAL, True)


@SLASH_CLIENT.interactions(custom_id = NOTIFICATION_SETTINGS_CUSTOM_ID_PROPOSAL_DISABLE)
async def handle_notification_settings_proposal_disable(event):
    return await handle_notification_settings_change(event, OPTION_PROPOSAL, False)
