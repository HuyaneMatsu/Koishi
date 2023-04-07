__all__ = ()

from hata import Embed, User

from ..shared_constants import PERMISSIONS__KICK, WORD_CONFIG__KICK
from ..shared_helpers import add_reason_field, add_standalone_field, create_auto_reason, process_reason

from .helpers import build_action_completed_embed, check_required_permissions, confirm_action, notify_user_action
from .orin import apply_orin_mode, should_show_orin


def build_kick_embed(user, title, description, reason, notify_user, orin_mode):
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
    notify_user : `bool`
        Whether the user should be notified.
    orin_mode : `bool`
        Whether orin mode should be applied.
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_standalone_field(embed, 'Notify user', 'true' if notify_user else 'false')
    add_reason_field(embed, reason)
    if orin_mode:
        apply_orin_mode(embed)
    return embed


def build_kick_notification_embed(guild, reason):
    """
    Builds a being kicked user notification embed.
    
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
    embed = Embed('Kicked', f'You were kicked from **{guild.name}**.')
    add_reason_field(embed, reason)
    return embed, None


async def kick_command(
    client,
    event,
    user: (User, 'Select the user to kick!'),
    reason: (str, 'Any reason why you would want to kick?') = None,
    notify_user: (bool, 'Whether the user should get DM about the kick.') = True,
):
    """Kicks someone out of the guild. You must have kick users permission."""
    guild = event.guild
    check_required_permissions(client, event, guild, user, PERMISSIONS__KICK, WORD_CONFIG__KICK)
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    orin_mode = await should_show_orin(client, guild, event.user)
    
    # Ask, whether the user should be kicked.
    component_interaction = await confirm_action(
        client, event, guild, user, build_kick_embed, WORD_CONFIG__KICK, reason, notify_user, False
    )
    if (component_interaction is None):
        return
    
    if notify_user:
        notify_note = await notify_user_action(client, guild, user, build_kick_notification_embed, reason)
    else:
        notify_note = None
    
    await client.guild_user_delete(guild, user, reason = create_auto_reason(event, reason))
    
    await client.interaction_response_message_edit(
        component_interaction,
        allowed_mentions = None,
        components = None,
        embed = build_action_completed_embed(
            user, build_kick_embed, WORD_CONFIG__KICK, notify_note, reason, notify_user, orin_mode
        )
    )
