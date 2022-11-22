__all__ = ()

from hata import Client, Embed

from ..shared_constants import PERMISSIONS__BAN, WORD_CONFIG__BAN
from ..shared_helpers import add_reason_field, create_auto_reason, process_reason

from .helpers import build_action_completed_embed, check_required_permissions, create_response_form


SLASH_CLIENT: Client
CUSTOM_ID_SELF_BAN = 'mod.self.form.ban'


def build_ban_embed(user, title, description, reason):
    """
    Build a self-ban embed.
    
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


async def ban_command(client, event):
    """Wanna ban yourself?"""
    guild = event.guild
    check_required_permissions(client, event, guild, PERMISSIONS__BAN, WORD_CONFIG__BAN)
    return create_response_form('Self ban confirmation', 'Ban', CUSTOM_ID_SELF_BAN)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SELF_BAN, target = 'form')
async def self_ban(client, event, *, reason = None):
    """Self-bans the user."""
    guild = event.guild
    if guild is None:
        # Guild out of cache? The client is probably removed.
        return
    
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event)
    
    await client.guild_ban_add(guild, event.user, reason = create_auto_reason(event, reason))
    
    await client.interaction_response_message_edit(
        event,
        allowed_mentions = None,
        embed = build_action_completed_embed(event.user, build_ban_embed, WORD_CONFIG__BAN, reason)
    )
