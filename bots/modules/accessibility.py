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
        'Notification settings'
    ).add_field(
        NOTIFICATION_NAME_PROPOSAL,
        field_value_to_code_block(notify_proposal),
        inline = True,
    ).add_field(
        NOTIFICATION_NAME_DAILY,
        field_value_to_code_block(notify_daily),
        inline = True,
    ).add_thumbnail(
        user.avatar_url,
    )

NOTIFICATION_TYPE_PROPOSALS = 1
NOTIFICATION_TYPE_DAILY = 2

NOTIFICATION_NAME_PROPOSAL = 'Proposals'
NOTIFICATION_NAME_DAILY = 'Daily'

NOTIFICATION_NAME_IN_LINE_PROPOSAL = 'proposal'
NOTIFICATION_NAME_IN_LINE_DAILY = 'daily'

NOTIFICATION_CHOICES = [
    (NOTIFICATION_NAME_PROPOSAL, NOTIFICATION_TYPE_PROPOSALS),
    (NOTIFICATION_NAME_DAILY, NOTIFICATION_TYPE_DAILY),
]

NOTIFICATION_TYPE_TO_FIELD = {
    NOTIFICATION_TYPE_PROPOSALS: user_common_model.notify_proposal,
    NOTIFICATION_TYPE_DAILY: user_common_model.notify_daily,
}

NOTIFICATION_TYPE_TO_NAME = {
    NOTIFICATION_TYPE_PROPOSALS: NOTIFICATION_NAME_PROPOSAL,
    NOTIFICATION_TYPE_DAILY: NOTIFICATION_NAME_DAILY,
}

NOTIFICATION_TYPE_TO_SYSTEM_NAME = {
    NOTIFICATION_TYPE_PROPOSALS: 'notify_proposal',
    NOTIFICATION_TYPE_DAILY: 'notify_daily',
}


NOTIFICATION_TYPE_TO_NAME_INLINE = {
    NOTIFICATION_TYPE_PROPOSALS: NOTIFICATION_NAME_IN_LINE_PROPOSAL,
    NOTIFICATION_TYPE_DAILY: NOTIFICATION_NAME_IN_LINE_DAILY,
}

@ACCESSIBILITY_INTERACTIONS.interactions
async def change_notification_setting(event,
    notification_type: (NOTIFICATION_CHOICES, 'Select the notification to change.'),
    enabled: ('bool', 'Whether the notification should be enabled.'),
):
    """Set your notification."""
    user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    NOTIFICATION_TYPE_TO_FIELD[notification_type],
                ],
            ).where(
                user_common_model.user_id == user.id,
            )
        )
        
        if response.rowcount:
            entry_id, notification_value = await response.fetchone()
        else:
            entry_id = -1
            notification_value = True
        
        if notification_value != enabled:
            update_to = {NOTIFICATION_TYPE_TO_SYSTEM_NAME[notification_type]: enabled}
            
            if entry_id == -1:
                to_execute = get_create_common_user_expression(user.id, **notification_value)
            else:
                to_execute = USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    **update_to,
                )
            
            await connector.execute(to_execute)
    
    
    name_in_line = NOTIFICATION_TYPE_TO_NAME_INLINE[notification_type]
    
    if enabled:
        description = f'From now on you will receive {name_in_line} notifications.'
    else:
        description = f'From now, you will not receive {name_in_line} notifications.'
    
    return Embed(
        'Great success!',
        description,
    ).add_thumbnail(
        user.avatar_url,
    )
