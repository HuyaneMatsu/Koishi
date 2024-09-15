__all__ = ()

from hata import DiscordException, ERROR_CODES, Embed, User

from ..shared_constants import PERMISSIONS__BAN, WORD_CONFIG__BAN
from ..shared_helpers import add_reason_field

from .helpers import check_required_permissions_only


def build_is_banned_embed(user, ban_entry):
    """
    Build an is-banned embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    ban_entry : `None`, ``BanEntry``
        The user's ban entry.
    
    Returns
    -------
    embed : ``Embed``
    """
    if ban_entry is None:
        description = f'**{user.full_name}** is **NOT YET** banned.'
    else:
        description = f'**{user.full_name}** is banned.'
        
    embed = Embed(f'Ban entry', description).add_thumbnail(user.avatar_url)
    
    if (ban_entry is not None):
        add_reason_field(embed, ban_entry.reason)
    
    return embed


async def is_banned_command(
    client,
    event,
    user: (User, 'Who should I check?'),
):
    """Checks whether the user is banned."""
    guild = event.guild
    check_required_permissions_only(client, event, guild, PERMISSIONS__BAN, WORD_CONFIG__BAN)
    
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    try:
        ban_entry = await client.guild_ban_get(event.guild, user)
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_ban:
            ban_entry = None
        else:
            raise
    
    await client.interaction_response_message_edit(
        event,
        embed = build_is_banned_embed(user, ban_entry),
    )
