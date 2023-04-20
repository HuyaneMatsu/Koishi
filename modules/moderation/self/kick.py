__all__ = ()

from hata import Client, Embed

from ..shared_constants import PERMISSIONS__KICK, WORD_CONFIG__KICK
from ..shared_helpers import add_reason_field, create_auto_reason, process_reason

from .helpers import (
    build_action_completed_embed, check_required_permissions, check_user_remove_safety, create_response_form
)


SLASH_CLIENT: Client
CUSTOM_ID_SELF_KICK = 'mod.self.form.kick'


def build_kick_embed(user, title, description, reason):
    """
    Build a self-kick embed
    
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


async def kick_command(client, event):
    """Wanna kick yourself?"""
    guild = event.guild
    check_required_permissions(client, event, guild, PERMISSIONS__KICK, WORD_CONFIG__KICK)
    check_user_remove_safety(event)
    return create_response_form('Self kick confirmation', 'Kick', CUSTOM_ID_SELF_KICK)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SELF_KICK, target = 'form')
async def self_kick(client, event, *, reason = None):
    """Self-kicks the user."""
    guild = event.guild
    if guild is None:
        # Guild out of cache? The client is probably removed.
        return
    
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    await client.guild_user_delete(guild, event.user, reason = create_auto_reason(event, reason))
    
    await client.interaction_response_message_edit(
        event,
        allowed_mentions = None,
        embed = build_action_completed_embed(event.user, build_kick_embed, WORD_CONFIG__KICK, reason)
    )
