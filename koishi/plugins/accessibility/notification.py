__all__ = ()

from hata import Embed
from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression



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


async def get_notification_settings(user_id):
    """
    Gets the notification settings for the given `user_id`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        the user's identifier.
    
    Returns
    -------
    notify_proposal : `bool`
    notify_daily : `bool`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.notify_proposal,
                    user_common_model.notify_daily,
                ],
            ).where(
                user_common_model.user_id == user_id,
            )
        )
    
    results = await response.fetchall()
    if results:
        notify_proposal, notify_daily = results[0]
    else:
        notify_proposal = True
        notify_daily = True
    
    return notify_proposal, notify_daily


def build_notification_settings_embed(user, notification_settings):
    """
    Builds notification settings embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    notification_settings : `tuple<bool>`
        The user's notification settings.
    
    Returns
    -------
    embed : ``Embed``
    """
    notify_proposal, notify_daily = notification_settings
    
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


def build_notification_settings_change_description(notification_option, enable):
    name_in_line = notification_option.name_in_line
    
    if enable:
        description = f'From now on, you will receive {name_in_line} notifications.'
    else:
        description = f'From now, you will **not** receive {name_in_line} notifications.'
    
    return description


def build_notification_settings_change_embed(user, notification_option, enabled):
    """
    Builds notification change embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's notification settings are changed.
    notification_option : ``NotificationOption``
        Option representing the changed notification setting.
    enabled : `bool`
        Whether we enabled / disabled the setting.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Great success!',
        build_notification_settings_change_description(notification_option, enabled),
    ).add_thumbnail(
        user.avatar_url,
    )


async def change_notification_button_click(client, event, notification_option, enable):
    await switch_notification(event.user.id, enable, notification_option)
    await client.interaction_response_message_create(
        event,
        build_notification_settings_change_embed(event.user, notification_option, enable),
        show_for_invoking_user_only = True,
    )
