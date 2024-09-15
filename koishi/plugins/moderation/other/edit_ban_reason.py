__all__ = ()

from hata import DiscordException, ERROR_CODES, Embed, User

from ..shared_constants import PERMISSIONS__BAN, WORD_CONFIG__BAN
from ..shared_helpers import add_reason_field, create_auto_reason, process_reason

from .helpers import check_required_permissions_only


def build_edit_ban_reason_embed(user, reason, success):
    """
    Builds an edit ban reason embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    reason : `None | str`
        Action reason.
    success : `bool`
        Whether the operation went through successfully.
    
    Returns
    -------
    embed : ``Embed``
    """
    if success:
        description = f'**{user.full_name}**\'s ban reason has been edited.'
    else:
        description = f'**{user.full_name}** is **NOT YET** banned.'
    
    embed = Embed(
        f'Edit ban reason', description,
    ).add_thumbnail(
        user.avatar_url
    )
    add_reason_field(embed, reason)
    
    return embed


async def edit_ban_reason_command(
    client,
    event,
    user: (User, 'Who\'s ban reason to edit?'),
    reason: (str, 'New ban reason') = None,
):
    """
    Edits the user's ban reason.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    user : ``ClientUserBase``
        The user who's ban to edit.
    reason : `None | str` = `None`, Optional
        The user who's abn reason to edit.
    """
    guild = event.guild
    check_required_permissions_only(client, event, guild, PERMISSIONS__BAN, WORD_CONFIG__BAN)
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    try:
        await client.guild_ban_delete(event.guild, user)
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_ban:
            success = False
        
        else:
            raise
    
    else:
        try:
            await client.guild_ban_add(event.guild, user, reason = create_auto_reason(event, reason))
        except ConnectionError:
            return
        
        success = True
    
    await client.interaction_response_message_edit(
        event,
        embed = build_edit_ban_reason_embed(user, reason, success),
    )
