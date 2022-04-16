from hata import Client, Embed
from sqlalchemy.sql import select

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression

SLASH_CLIENT: Client

ACCESSIBILITY_INTERACTIONS = SLASH_CLIENT.interactions(
    None,
    name = 'accessibility',
    description = 'Customize your Koishi experience (actually just a few things).',
    is_global = True,
)


def field_value_to_code_block(field_value):
    if field_value:
        code_block = (
            '```\n'
            'true\n'
            '```'
        )
    else:
        code_block = (
            '```\n'
            'false\n'
            '```'
        )
    
    return code_block


@ACCESSIBILITY_INTERACTIONS.interactions
async def notification_settings(event):
    """Shows your notification settings."""
    user = event.user
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.notify_proposal,
                    user_common_model.notify_daily,
                    
                ],
            ).where(
                user_common_model.user_id == user.id,
            )
        )
    
    results = await response.fetchall()
    if results:
        notify_proposal, notify_daily = results[0]
    else:
        notify_proposal = True
        notify_daily = True
    
    return Embed(
        'Notification settings',
    ).add_field(
        'Proposal',
        field_value_to_code_block(notify_proposal),
        inline = True,
    ).add_field(
        'Daily claimed by waifu',
        field_value_to_code_block(notify_daily),
        inline = True,
    ).add_thumbnail(
        user.avatar_url,
    )


NOTIFICATION_TYPE_TO_OPTION = {}
NOTIFICATION_CHOICES = []

class NotificationOption:
    __slots__ = ('id', 'name', 'name_in_line', 'system_name', 'field')
    
    _id_counter = 1
    
    def __new__(cls, name, system_name, name_in_line):
        id_ = cls._id_counter
        cls._id_counter = id_ + 1
        
        field = getattr(user_common_model, system_name)
        
        self = object.__new__(cls)
        self.id = id_
        self.name = name
        self.name_in_line = name_in_line
        self.system_name = system_name
        self.field = field
        
        NOTIFICATION_TYPE_TO_OPTION[id_] = self
        NOTIFICATION_CHOICES.append((name, id_))
        
        return self

PROPOSAL_NOTIFICATION_OPTION = NotificationOption(
    'Proposal',
    'notify_proposal',
    'proposal',
)


DAILY_NOTIFICATION_OPTION = NotificationOption(
    'Daily',
    'notify_daily',
    'daily-by-waifu',
)


async def switch_notification(user_id, enable, notification_option):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    notification_option.field,
                ],
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        if response.rowcount:
            entry_id, notification_value = await response.fetchone()
        else:
            entry_id = -1
            notification_value = True
        
        if notification_value != enable:
            update_to = {notification_option.system_name: enable}
            
            if entry_id == -1:
                to_execute = get_create_common_user_expression(user_id, **update_to)
            else:
                to_execute = USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    **update_to,
                )
            
            await connector.execute(to_execute)


def get_notification_change_description(notification_option, enable):
    name_in_line = notification_option.name_in_line
    
    if enable:
        description = f'From now on, you will receive {name_in_line} notifications.'
    else:
        description = f'From now, you will **not** receive {name_in_line} notifications.'
    
    return description


@ACCESSIBILITY_INTERACTIONS.interactions
async def change_notification_setting(event,
    notification_type: (NOTIFICATION_CHOICES, 'Select the notification to change.'),
    enabled: ('bool', 'Whether the notification should be enabled.'),
):
    """Set your notification."""
    user = event.user
    
    notification_option = NOTIFICATION_TYPE_TO_OPTION[notification_type]
    
    await switch_notification(
        user.id,
        enabled,
        notification_option,
    )
    
    description = get_notification_change_description(notification_option, enabled)
    
    return Embed(
        'Great success!',
        description,
    ).add_thumbnail(
        user.avatar_url,
    )

    

async def change_notification_button_click(client, event, notification_option, enable):
    await switch_notification(event.user.id, enable, notification_option)
    await client.interaction_response_message_create(
        event,
        get_notification_change_description(notification_option, enable),
        show_for_invoking_user_only = True,
    )


@SLASH_CLIENT.interactions(custom_id='accessibility.change_notification_settings.proposal.enable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, PROPOSAL_NOTIFICATION_OPTION, True)

@SLASH_CLIENT.interactions(custom_id='accessibility.change_notification_settings.proposal.disable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, PROPOSAL_NOTIFICATION_OPTION, False)

@SLASH_CLIENT.interactions(custom_id='accessibility.change_notification_settings.daily.enable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, DAILY_NOTIFICATION_OPTION, True)

@SLASH_CLIENT.interactions(custom_id='accessibility.change_notification_settings.daily.disable')
async def enable_proposal_notification(client, event):
    await change_notification_button_click(client, event, DAILY_NOTIFICATION_OPTION, False)
