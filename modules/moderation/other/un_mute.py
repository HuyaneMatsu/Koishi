__all__ = ()

from datetime import datetime as DateTime

from hata import Embed, User
from hata.ext.slash import abort

from ..shared_constants import PERMISSIONS__MUTE, WORD_CONFIG__UN_MUTE
from ..shared_helpers import add_reason_field, add_standalone_field, create_auto_reason, process_reason

from .helpers import build_action_completed_embed, check_required_permissions, confirm_action, notify_user_action


def check_can_un_mute(user, guild):
    """
    Returns whether the user can be un-muted.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to check.
    guild : ``Guild``
        The respective guild.
    """
    guild_profile = user.get_guild_profile_for(guild)
    if guild_profile is None:
        abort('The user must be in the guild to be un-muted.')
    
    timed_out_until = guild_profile.timed_out_until
    if (timed_out_until is None) or timed_out_until < DateTime.utcnow():
        abort('The user is not muted.')


def build_un_mute_embed(user, title, description, reason, notify_user):
    """
    Builds a mute embed.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_standalone_field(embed, 'Notify user', 'true' if notify_user else 'false')
    add_reason_field(embed, reason)
    return embed


def build_un_mute_notification_embed(guild, reason):
    """
    Builds a being un-muted user notification embed.
    
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
    embed = Embed('Un-muted', f'You were un-muted in **{guild.name}**.')
    add_reason_field(embed, reason)
    return embed, None


async def un_mute_command(
    client,
    event,
    user: (User, 'Select the user to mute!'),
    reason: (str, 'Any reason why you would want to mute?') = None,
    notify_user: (bool, 'Whether the user should get DM about the mute.') = True,
):
    """Un-mutes someone. You must have moderate users permission."""
    guild = event.guild
    check_required_permissions(client, event, guild, user, PERMISSIONS__MUTE, WORD_CONFIG__UN_MUTE)
    check_can_un_mute(user, guild)
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    # Ask, whether the user should be un-muted.
    component_interaction = await confirm_action(
        client, event, guild, user, build_un_mute_embed, WORD_CONFIG__UN_MUTE, reason, notify_user
    )
    if (component_interaction is None):
        return
    
    await client.user_guild_profile_edit(
        guild,
        user,
        timeout_duration = None,
        reason = create_auto_reason(event, reason),
    )
    
    if notify_user:
        notify_note = await notify_user_action(client, guild, user, build_un_mute_notification_embed, reason)
    else:
        notify_note = None
    
    await client.interaction_response_message_edit(
        component_interaction,
        allowed_mentions = None,
        components = None,
        embed = build_action_completed_embed(
            user, build_un_mute_embed, WORD_CONFIG__UN_MUTE, notify_note, reason, notify_user
        )
    )
