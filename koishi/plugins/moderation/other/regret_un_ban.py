__all__ = ()

from hata import AuditLogEntryType, Embed, User, create_button

from ..shared_constants import PERMISSIONS__BAN, WORD_CONFIG__REGRET_UN_BAN
from ..shared_helpers import add_reason_field, process_reason

from .helpers import (
    build_action_completed_embed, build_cannot_regret_embed, check_required_permissions_only, confirm_action,
    notify_user_action
)
from .regret_helpers import can_regret, check_regret_cooldown, check_regret_permissions, get_regret_invite_url
from .un_ban import build_un_ban_failed_successfully_embed, un_ban_user


def build_regret_ban_embed(user, title, description, reason):
    """
    Build a ban embed.
    
    Parameters
    ----------
    title : `str`
        Embed title.
    description : `str`
        Embed description.
    reason : `None`, `str`
        Action reason.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_reason_field(embed, reason)
    return embed


def build_regret_ban_notification_embed(guild, reason, user, invite_url):
    """
    Builds a regret-ban user notification embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild.
    reason : `None`, `str`
        Action reason.
    user : ``ClientUserBase``
        The user who regretted the action.
    invite_url : `str`
        Invite url back to the guild.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Regret', f'You were un-banned from **{guild.name}**.'
    ).add_author(
        user.full_name, user.avatar_url
    )
    add_reason_field(embed, reason)
    return embed, create_button('Join back here', url = invite_url)


async def regret_un_ban_command(
    client,
    event,
    user: (User, 'Select the user who you regret banning!'),
    reason: (str, 'Any regrets?') = None,
):
    """Un-bans the user and sends a regret message & invite."""
    guild = event.guild
    check_required_permissions_only(client, event, guild, PERMISSIONS__BAN, WORD_CONFIG__REGRET_UN_BAN)
    check_regret_permissions(client, guild)
    check_regret_cooldown(event.user)
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    regret_mode = await can_regret(client, guild, user, AuditLogEntryType.user_ban_add)
    if regret_mode == -1:
        return
    
    if not regret_mode:
        await client.interaction_response_message_edit(
            event, embed = build_cannot_regret_embed(user, reason, 'banning'),
        )
        return
    
    component_interaction = await confirm_action(
        client, event, guild, user, build_regret_ban_embed, WORD_CONFIG__REGRET_UN_BAN, reason
    )
    if (component_interaction is None):
        return
    
    was_un_banned = await un_ban_user(client, event, guild, user, reason)
    if was_un_banned == 2:
        return
    
    if was_un_banned:
        invite_url = await get_regret_invite_url(client, guild)
        if invite_url is None:
            return
        
        notify_note = await notify_user_action(
            client, guild, user, build_regret_ban_notification_embed, reason, event.user, invite_url
        )
        
        embed = build_action_completed_embed(
            user, build_regret_ban_embed, WORD_CONFIG__REGRET_UN_BAN, notify_note, reason
        )
        
    else:
        embed = build_un_ban_failed_successfully_embed(user, build_regret_ban_embed, reason)
    
    await client.interaction_response_message_edit(
        component_interaction,
        allowed_mentions = None,
        components = None,
        embed = embed,
    )
