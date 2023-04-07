__all__ = ()

from hata import Embed, User

from ..shared_constants import PERMISSIONS__BAN, WORD_CONFIG__BAN
from ..shared_helpers import add_reason_field, add_standalone_field, create_auto_reason, process_reason

from .helpers import build_action_completed_embed, check_required_permissions, confirm_action, notify_user_action
from .orin import apply_orin_mode, should_show_orin


def build_ban_embed(user, title, description, reason, notify_user, delete_message_days, orin_mode):
    """
    Build a ban embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    title : `str`
        Embed title.
    description : `str`
        Embed description.
    reason : `None`, `str`
        Action reason.
    notify_user : `bool`
        Whether the user should be notified.
    delete_message_days : `int`
        How much message should be deleted (in days).
    orin_mode : `bool`
        Whether orin mode should be applied.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_standalone_field(embed, 'Delete message day', str(delete_message_days))
    add_standalone_field(embed, 'Notify user', 'true' if notify_user else 'false')
    add_reason_field(embed, reason)
    if orin_mode:
        apply_orin_mode(embed)
    return embed


def build_ban_notification_embed(guild, reason):
    """
    Builds a being banned user notification embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild.
    reason : `None`, `str`
        Action reason.
    
    Returns
    -------
    embed : ``Embed``
    components : `None`
    """
    embed = Embed('Banned', f'You were banned from **{guild.name}**.')
    add_reason_field(embed, reason)
    return embed, None


async def ban_command(
    client,
    event,
    user: (User, 'Select the user to ban!'),
    reason: (str, 'Any reason why you would want to ban?') = None,
    notify_user: (bool, 'Whether the user should get DM about the ban.') = True,
    delete_message_days: (range(8), 'Delete previous messages?') = 0,
):
    """
    Yeets someone out of the guild. You must have ban users permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user : ``ClientUserBase``
        The user to ban.
    reason : `None`, `str` = `None`, Optional
        Ban reason. Will show up in the guild's audit logs.
    notify_user : `bool` = `False`, Optional
        Whether the user should be notified.
    delete_message_days : `int` = `0`, Optional
        How hold old messages should be also deleted of the user.
    """
    guild = event.guild
    check_required_permissions(client, event, guild, user, PERMISSIONS__BAN, WORD_CONFIG__BAN)
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    orin_mode = await should_show_orin(client, guild, event.user)
    
    # Ask, whether the user should be banned.
    component_interaction = await confirm_action(
        client, event, guild, user, build_ban_embed, WORD_CONFIG__BAN, reason, notify_user, delete_message_days, False
    )
    if (component_interaction is None):
        return
    
    if notify_user:
        notify_note = await notify_user_action(client, guild, user, build_ban_notification_embed, reason)
    else:
        notify_note = None
    
    await client.guild_ban_add(
        guild,
        user,
        delete_message_duration = delete_message_days * 24 * 60 * 60,
        reason = create_auto_reason(event, reason),
    )
    
    await client.interaction_response_message_edit(
        component_interaction,
        allowed_mentions = None,
        components = None,
        embed = build_action_completed_embed(
            user, build_ban_embed, WORD_CONFIG__BAN, notify_note, reason, notify_user, delete_message_days, orin_mode
        )
    )
