__all__ = ()

from hata import Embed, User, DiscordException, ERROR_CODES

from ..shared_constants import PERMISSIONS__BAN, WORD_CONFIG__UN_BAN
from ..shared_helpers import add_reason_field, add_standalone_field, create_auto_reason, process_reason

from .helpers import build_action_completed_embed, check_required_permissions_only, confirm_action, notify_user_action


def build_un_ban_embed(user, title, description, reason, notify_user):
    """
    Build a un-ban embed.
    
    Parameters
    ----------
    title : `str`
        Embed title.
    description : `str`
        Embed description.
    reason : `None`, `str`
        Action reason.
    notify_user : `bool`
        Whether the user should be notified.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_standalone_field(embed, 'Notify user', 'true' if notify_user else 'false')
    add_reason_field(embed, reason)
    return embed


def build_un_ban_notification_embed(guild, reason):
    """
    Builds an un-banned user notification embed.
    
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
    embed = Embed('Un-banned', f'You were un-banned from **{guild.name}**.')
    add_reason_field(embed, reason)
    return embed, None


def build_un_ban_failed_successfully_embed(user, embed_builder, *position_parameters):
    """
    Creates a successfully failed un-ban embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who would been banned.
    embed_builder : `FunctionType`
        The embed builder to call.
    *position_parameters : Positional Parameters
        Additional positional parameters to pass to the embed builder.
    
    Returns
    -------
    embed : ``Embed``
    """
    return embed_builder(
        user, 'Task failed successfully', f'**{user.full_name}** was not banned all along!', *position_parameters
    )


async def un_ban_user(client, event, guild, user, reason):
    """
    Unbans the user. Returns whether the user was unbanned. Returns `-1` on error.
    
    This function is a coroutine
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild : ``Guild``
        The guild to check the action at.
    event : `AuditLogEntryType``
        The audit log event ot search for.
    user : ``ClientUserBase``
        The user to check for.
    reason : `None`, `str`
        Action reason.
    
    Returns
    -------
    was_un_banned : `bool`
    """
    try:
        await client.guild_ban_delete(guild, user, reason = create_auto_reason(event, reason))
    except ConnectionError:
        return -1
    
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_ban:
            return 0
        
        raise
    
    return 1


async def un_ban_command(
    client,
    event,
    user: (User, 'Select the user to un.ban.'),
    reason: (str, 'Un-ban reason?') = None,
    notify_user: (bool, 'Whether the user should get DM about the un-ban.') = False,
):
    """Un-bans the user. You must have ban users permission."""
    guild = event.guild
    check_required_permissions_only(client, event, guild, PERMISSIONS__BAN, WORD_CONFIG__UN_BAN)
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    # Ask, whether the user should be banned.
    component_interaction = await confirm_action(
        client, event, guild, user, build_un_ban_embed, WORD_CONFIG__UN_BAN, reason, notify_user
    )
    if (component_interaction is None):
        return
    
    was_un_banned = await un_ban_user(client, event, guild, user, reason)
    if was_un_banned == 2:
        return
    
    if was_un_banned:
        if notify_user:
            notify_note = await notify_user_action(client, guild, user, build_un_ban_notification_embed, reason)
        else:
            notify_note = None
        
        embed = build_action_completed_embed(
            user, guild.id, build_un_ban_embed, WORD_CONFIG__UN_BAN, notify_note, reason, notify_user
        )
    
    else:
        embed = build_un_ban_failed_successfully_embed(user, build_un_ban_embed, reason, notify_user)
    
    await client.interaction_response_message_edit(
        component_interaction,
        allowed_mentions = None,
        components = None,
        embed = embed,
    )
