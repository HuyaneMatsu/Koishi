__all__ = ()

from hata import DiscordException, ERROR_CODES, Permission
from hata.ext.slash import Form, InteractionResponse, TextInput, TextInputStyle, abort
from scarletio import CancelledError

from ...bot_utils.user_getter import get_user
from ...bots import SLASH_CLIENT

from .components_satori_auto_start import (
    COMPONENT_DELETE_CHANNEL, SATORI_CUSTOM_ID_CHANNEL_DELETE, SATORI_CUSTOM_ID_USER_BAN_RP,
    SATORI_CUSTOM_ID_USER_KICK_RP, create_satori_custom_id_user_ban, create_satori_custom_id_user_kick
)
from .embed_builder_satori_start import build_satori_user_actioned_embed


PERMISSION_BAN = Permission().update_by_keys(ban_users = True)
PERMISSION_KICK = Permission().update_by_keys(kick_users = True)

REASON_LENGTH_MAX = 400


def create_response_form(title, reason_name, custom_id):
    """
    Creates a confirmation form for either kicking or banning the user.
    
    Parameters
    ----------
    title : `str`
        The form's title.
    reason_name : `str`
        The reason name. Should be already capitalised.
    custom_id : `str`
        The form's custom id.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    return  Form(
        title,
        [
            TextInput(
                'Reason',
                max_length = REASON_LENGTH_MAX,
                custom_id = 'reason',
                placeholder = f'{reason_name} reason',
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = custom_id,
    )


def check_action_user_required_permissions(client, event, guild, user, required_permission, action_name):
    """
    Checks whether the permissions requirements are met.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    guild : ``Guild``
        The guild where the action would be executed.
    user : ``ClientUserBase``
        The user to be actioned.
    required_permission : ``Permission``
        The required permissions to execute the action.
    action_name : `str`
        The action's name we are checking for.
    """
    if guild is None:
        abort('Guild not in cache.')
    
    if not (event.user_permissions & required_permission):
        abort(f'You have no permissions to {action_name}.')
    
    if not (guild.cached_permissions_for(client) & required_permission):
        abort(f'{client.name_at(guild)} has no permissions to {action_name}.')
    
    if not client.has_higher_role_than_at(user, guild):
        abort(f'I must have higher role than the user to be actioned.')


def process_reason(event, reason):
    """
    Processes the given raw reason.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interactions event.
    reason : `None`, `str`
        Reason given.
    
    Returns
    -------
    reason : `str`
    """
    reason_parts = []
    
    if (reason is not None) and reason:
        reason_parts.append(reason)
        reason_parts.append('\n')
    
    caller = event.user
    reason_parts.append('Requested by: ')
    reason_parts.append(caller.full_name)
    reason_parts.append(' [')
    reason_parts.append(str(caller.id))
    reason_parts.append(']')
    
    return ''.join(reason_parts)


@SLASH_CLIENT.interactions(custom_id = SATORI_CUSTOM_ID_CHANNEL_DELETE)
async def channel_delete(client, event):
    """
    Deletes the channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    channel = event.channel
    if not channel.cached_permissions_for(client).can_manage_channels:
        abort('Cannot delete channel: missing permissions')
        return
    
    try:
        await client.channel_delete(channel)
    except (GeneratorExit, CancelledError):
        raise
    
    except ConnectionError:
        return
    
    except BaseException as err:
        if isinstance(err, DiscordException) and err.code in (
            ERROR_CODES.unknown_channel, # channel deleted
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed
        ):
            return
        
        await client.events.error(client, 'log.satori.channel.delete', err)
        return


@SLASH_CLIENT.interactions(custom_id = SATORI_CUSTOM_ID_USER_KICK_RP)
async def user_kick_confirmation(client, event, user_id):
    """
    Returns a form to confirm the kick.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user_id : `str`
        The user's identifier to kick in hexadecimal format. Later converted to `int`.
    
    Returns
    -------
    response : ``InteractionForm``
    """
    user = await get_user(int(user_id, base = 16))
    check_action_user_required_permissions(client, event, event.guild, user, PERMISSION_KICK, 'kick')
    return create_response_form(f'Kicking {user.full_name}', 'Kick', create_satori_custom_id_user_kick(user))


@SLASH_CLIENT.interactions(custom_id = SATORI_CUSTOM_ID_USER_KICK_RP, target = 'form')
async def user_kick_execute(client, event, user_id, *, reason = None):
    """
    Executes kicking the user.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user_id : `str`
        The user's identifier to kick in hexadecimal format.
    reason : `None`, `str` = `None`, Optional (Keyword only)
        Confirmation reason if any.
    
    Yields
    ------
    acknowledgement / response : `None` / ``InteractionResponse``
    """
    user = await get_user(int(user_id, base = 16))
    guild = event.guild
    check_action_user_required_permissions(client, event, guild, user, PERMISSION_KICK, 'kick')
    
    if (reason is not None) and (not reason):
        reason = None
    
    yield
    
    try:
        await client.guild_user_delete(guild, user, reason = process_reason(event, reason))
    except (GeneratorExit, CancelledError):
        raise
    
    except ConnectionError:
        return
    
    except BaseException as err:
        if isinstance(err, DiscordException) and err.code in (
            ERROR_CODES.unknown_user, # user deleted
            ERROR_CODES.unknown_member, # user left
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed
        ):
            return
        
        await client.events.error(client, 'log.satori.user.kick', err)
        return
    
    yield InteractionResponse(
        allowed_mentions = None,
        components = COMPONENT_DELETE_CHANNEL,
        embed = build_satori_user_actioned_embed(user, reason, 'Kicked'),
    )


@SLASH_CLIENT.interactions(custom_id = SATORI_CUSTOM_ID_USER_BAN_RP)
async def user_ban_confirmation(client, event, user_id):
    """
    Returns a form to confirm the ban.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user_id : `str`
        The user's identifier to ban in hexadecimal format. Later converted to `int`.
    
    Returns
    -------
    response : ``InteractionForm``
    """
    user = await get_user(int(user_id, base = 16))
    check_action_user_required_permissions(client, event, event.guild, user, PERMISSION_BAN, 'ban')
    return create_response_form(f'Banning {user.full_name}', 'Ban', create_satori_custom_id_user_ban(user))


@SLASH_CLIENT.interactions(custom_id = SATORI_CUSTOM_ID_USER_BAN_RP, target = 'form')
async def user_ban_execute(client, event, user_id, *, reason = None):
    """
    Executes banning the user.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user_id : `str`
        The user's identifier to ban in hexadecimal format. Later converted to `int`.
    reason : `None`, `str` = `None`, Optional (Keyword only)
        Confirmation reason if any.
    
    Yields
    ------
    acknowledgement / response : `None` / ``InteractionResponse``
    """
    user = await get_user(int(user_id, base = 16))
    guild = event.guild
    check_action_user_required_permissions(client, event, guild, user, PERMISSION_BAN, 'ban')
    
    if (reason is not None) and (not reason):
        reason = None
    
    yield
    
    try:
        await client.guild_ban_add(guild, user, reason = process_reason(event, reason))
    except (GeneratorExit, CancelledError):
        raise
    
    except ConnectionError:
        return
    
    except BaseException as err:
        if isinstance(err, DiscordException) and err.code in (
            ERROR_CODES.unknown_user, # user deleted
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed
        ):
            return
        
        await client.events.error(client, 'log.satori.user.ban', err)
        return
    
    
    yield InteractionResponse(
        allowed_mentions = None,
        components = COMPONENT_DELETE_CHANNEL,
        embed = build_satori_user_actioned_embed(user, reason, 'Banned'),
    )
