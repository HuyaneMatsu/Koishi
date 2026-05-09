__all__ = ()

from ...bots import FEATURE_CLIENTS

from .constants import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_ENABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_ENABLE, USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_ENABLE, USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_ENABLE, USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_ENABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_RECOVERY_OVER_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_RECOVERY_OVER_ENABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION_DISABLE,
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION_ENABLE,
)
from .options import (
    OPTION_NOTIFICATION_DAILY_BY_WAIFU, OPTION_NOTIFICATION_DAILY_REMINDER, OPTION_NOTIFICATION_GIFT,
    OPTION_NOTIFICATION_PROPOSAL, OPTION_NOTIFICATION_VOTE, OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER,
    OPTION_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION
)
from .utils import handle_user_settings_change


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_RECOVERY_OVER_ENABLE)
async def handle_user_settings_notification_adventure_recovery_over_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER, 1)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_RECOVERY_OVER_DISABLE)
async def handle_user_settings_notification_adventure_recovery_over_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_ADVENTURE_RECOVERY_OVER, 0)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_ENABLE)
async def handle_user_settings_notification_daily_by_waifu_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_BY_WAIFU, 1)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE)
async def handle_user_settings_notification_daily_by_waifu_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_BY_WAIFU, 0)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_ENABLE)
async def handle_user_settings_notification_daily_reminder_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_REMINDER, 1)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE)
async def handle_user_settings_notification_daily_reminder_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_DAILY_REMINDER, 0)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_ENABLE)
async def handle_user_settings_notification_gift_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_GIFT, 1)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_DISABLE)
async def handle_user_settings_notification_gift_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_GIFT, 0)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION_ENABLE)
async def handle_user_settings_notification_market_place_item_finalisation_enable(client, interaction_event):
    await handle_user_settings_change(
        client, interaction_event, OPTION_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION, 1
    )


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION_DISABLE)
async def handle_user_settings_notification_market_place_item_finalisation_disable(client, interaction_event):
    await handle_user_settings_change(
        client, interaction_event, OPTION_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION, 0
    )


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_ENABLE)
async def handle_user_settings_notification_proposal_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_PROPOSAL, 1)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE)
async def handle_user_settings_notification_proposal_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_PROPOSAL, 0)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_ENABLE)
async def handle_user_settings_notification_vote_enable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_VOTE, 1)


@FEATURE_CLIENTS.interactions(custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE)
async def handle_user_settings_notification_vote_disable(client, interaction_event):
    await handle_user_settings_change(client, interaction_event, OPTION_NOTIFICATION_VOTE, 0)
