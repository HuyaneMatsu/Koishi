__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from scarletio import LOOP_TIME

from hata import DiscordException, ERROR_CODES
from hata.ext.slash import abort

from .constants import EMOJI__KOKORO, REGRET_COOLDOWN, REGRET_INTERVAL, REGRET_INVITE_MAX_AGE, REGRETS


def check_regret_permissions(client, guild):
    """
    Checks whether the client meets the pre-required regret permissions.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild where the action would be executed.
    """
    permissions = guild.cached_permissions_for(client)
    if not permissions.can_create_instant_invite:
        abort(f'{client.name_at(guild)} requires create instant invites permission for this action.')
    
    if not permissions.can_view_audit_logs:
        abort(f'{client.name_at(guild)} requires view audit logs permission for this action.')


async def can_regret(client, guild, user, entry_type):
    """
    Checks whether the given action can be regret. Returns `-1` on error.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild : ``Guild``
        The guild to check the action at.
    user : ``ClientUserBase``
        The user to check for.
    entry_type : `AuditLogEntryType``
        The audit log event ot search for.
    
    Returns
    -------
    regret_mode : `int`
    """
    try:
        audit_log = await client.audit_log_get_chunk(
            guild, after = DateTime.now(TimeZone.utc) - REGRET_INTERVAL, entry_type = entry_type
        )
    except ConnectionError:
        return -1
    
    except DiscordException as err:
        if err.code in (
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
        ):
            return -1
        
        raise
    
    for entry in audit_log:
        if entry.target is user:
            return 1
    
    return 0


async def get_regret_invite_url(client, guild):
    """
    Gets a regret invite-url for the given guild. Returns `None` on error.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild : ``Guild``
        The guild to check the action at.
    
    Returns
    -------
    invite_url : `None`, `str`
    """
    invite_url = guild.vanity_url
    if (invite_url is not None):
        return invite_url
    
    try:
        invite = await client.invite_create_preferred(guild, max_age = REGRET_INVITE_MAX_AGE, max_uses = 1)
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code in (
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
        ):
            return
        
        raise
    
    return invite.url


def check_regret_cooldown(user):
    """
    Checks whether the user is on cooldown.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who is regretting.
    """
    user_id = user.id
    now = LOOP_TIME()
    
    try:
        expires = REGRETS[user_id]
    except KeyError:
        pass
    else:
        if expires > now:
            abort(f'{EMOJI__KOKORO} You are on cooldown btw')
    
    REGRETS[user_id] = now + REGRET_COOLDOWN
