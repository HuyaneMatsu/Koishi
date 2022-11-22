__all__ = ()

from hata import AuditLogEvent, Embed, User
from hata.ext.slash import Button

from ..shared_constants import PERMISSIONS__KICK, WORD_CONFIG__REGRET_UN_KICK
from ..shared_helpers import add_reason_field, process_reason

from .helpers import (
    build_action_completed_embed, build_cannot_regret_embed, check_required_permissions_only, confirm_action,
    notify_user_action
)
from .regret_helpers import can_regret, check_regret_cooldown, check_regret_permissions, get_regret_invite_url


def build_regret_kick_embed(user, title, description, reason):
    """
    Build a kick embed.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_reason_field(embed, reason)
    return embed


def build_regret_kick_notification_embed(guild, reason, user, invite_url):
    """
    Builds a regret-kick user notification embed.
    
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
        'Regret', f'You were un-kicked from **{guild.name}**.'
    ).add_author(
        user.full_name, user.avatar_url
    )
    add_reason_field(embed, reason)
    return embed, Button('Join back here', url = invite_url)


async def regret_un_kick_command(
    client,
    event,
    user: (User, 'Select the user who you regret kicking!'),
    reason: (str, 'Any regrets?') = None,
):
    """Un-kicks the user and sends a regret message & invite."""
    guild = event.guild
    check_required_permissions_only(client, event, guild, PERMISSIONS__KICK, WORD_CONFIG__REGRET_UN_KICK)
    check_regret_permissions(client, guild)
    check_regret_cooldown(event.user)
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event)
    
    regret_mode = await can_regret(client, guild, user, AuditLogEvent.member_kick)
    if regret_mode == -1:
        return
    
    if not regret_mode:
        await client.interaction_response_message_edit(
            event, embed = build_cannot_regret_embed(user, reason, 'kicking'),
        )
        return
    
    component_interaction = await confirm_action(
        client, event, guild, user, build_regret_kick_embed, WORD_CONFIG__REGRET_UN_KICK, reason
    )
    if (component_interaction is None):
        return
    
    invite_url = await get_regret_invite_url(client, guild)
    if invite_url is None:
        return
    
    notify_note = await notify_user_action(
        client, guild, user, build_regret_kick_notification_embed, reason, event.user, invite_url
    )
    
    await client.interaction_response_message_edit(
        component_interaction,
        allowed_mentions = None,
        components = None,
        embed = build_action_completed_embed(
            user, build_regret_kick_embed, WORD_CONFIG__REGRET_UN_KICK, notify_note, reason
        ),
    )
