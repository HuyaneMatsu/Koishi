__all__ = ()

from ...bots import FEATURE_CLIENTS

from .constants import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_ENABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_ENABLE, USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_ENABLE, USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_ENABLE, USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_ENABLE
)
from .options import (
    OPTION_NOTIFICATION_DAILY_BY_WAIFU, OPTION_NOTIFICATION_DAILY_REMINDER, OPTION_NOTIFICATION_GIFT,
    OPTION_NOTIFICATION_PROPOSAL, OPTION_NOTIFICATION_VOTE
)
from .utils import handle_user_settings_change


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_ENABLE)
async def handle_user_settings_notification_daily_by_waifu_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_BY_WAIFU, True)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE)
async def handle_user_settings_notification_daily_by_waifu_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_BY_WAIFU, False)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_ENABLE)
async def handle_user_settings_notification_daily_reminder_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_REMINDER, True)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE)
async def handle_user_settings_notification_daily_reminder_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_REMINDER, False)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_ENABLE)
async def handle_user_settings_notification_gift_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_GIFT, True)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_DISABLE)
async def handle_user_settings_notification_gift_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_GIFT, False)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_ENABLE)
async def handle_user_settings_notification_proposal_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_PROPOSAL, True)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE)
async def handle_user_settings_notification_proposal_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_PROPOSAL, False)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_ENABLE)
async def handle_user_settings_notification_vote_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_VOTE, True)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE)
async def handle_user_settings_notification_vote_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_VOTE, False)
