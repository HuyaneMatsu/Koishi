__all__ = ()

from ...bots import SLASH_CLIENT

from .notification import DAILY_NOTIFICATION_OPTION, PROPOSAL_NOTIFICATION_OPTION, change_notification_button_click


@SLASH_CLIENT.interactions(custom_id = 'accessibility.change_notification_settings.proposal.enable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, PROPOSAL_NOTIFICATION_OPTION, True)


@SLASH_CLIENT.interactions(custom_id = 'accessibility.change_notification_settings.proposal.disable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, PROPOSAL_NOTIFICATION_OPTION, False)


@SLASH_CLIENT.interactions(custom_id = 'accessibility.change_notification_settings.daily.enable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, DAILY_NOTIFICATION_OPTION, True)


@SLASH_CLIENT.interactions(custom_id = 'accessibility.change_notification_settings.daily.disable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, DAILY_NOTIFICATION_OPTION, False)
