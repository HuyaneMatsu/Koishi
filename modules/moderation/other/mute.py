__all__ = ()

from hata import Embed, User

from ..shared_constants import PERMISSIONS__MUTE, WORD_CONFIG__MUTE
from ..shared_helpers import add_reason_field, add_standalone_field, create_auto_reason, process_reason
from ..shared_helpers_mute import (
    PARAMETER_DAYS, PARAMETER_HOURS, PARAMETER_MINUTES, PARAMETER_SECONDS, build_duration_string, get_duration
)

from .helpers import build_action_completed_embed, check_required_permissions, confirm_action, notify_user_action


def build_mute_embed(user, title, description, reason, notify_user, duration_string):
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
    duration_string : `str`
        The duration in string.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_standalone_field(embed, 'Duration', duration_string)
    add_standalone_field(embed, 'Notify user', 'true' if notify_user else 'false')
    add_reason_field(embed, reason)
    return embed


def build_mute_notification_embed(guild, reason, duration_string):
    """
    Builds a being muted user notification embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild.
    reason : `None`, `str`
        Action reason.
    duration_string : `str`
        For how the long the user is being muted.
    
    Returns
    -------
    embed : ``Embed``
    components : `None`
    """
    embed = Embed('Muted', f'You were muted in **{guild.name}**.')
    add_standalone_field(embed, 'Duration', duration_string)
    add_reason_field(embed, reason)
    return embed, None


async def mute_command(
    client,
    event,
    user: (User, 'Select the user to mute!'),
    days: PARAMETER_DAYS = 0,
    hours: PARAMETER_HOURS = 0,
    minutes: PARAMETER_MINUTES = 0,
    seconds: PARAMETER_SECONDS = 0,
    reason: (str, 'Any reason why you would want to mute?') = None,
    notify_user: (bool, 'Whether the user should get DM about the mute.') = False,
):
    """Mutes someone. You must have moderate users permission."""
    # Check permissions
    guild = event.guild
    
    check_required_permissions(client, event, guild, user, PERMISSIONS__MUTE, WORD_CONFIG__MUTE)
    duration = get_duration(days, hours, minutes, seconds)
    reason = process_reason(reason)
    duration_string = build_duration_string(duration)
    
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    # Ask, whether the user should be muted.
    component_interaction = await confirm_action(
        client, event, guild, user, build_mute_embed, WORD_CONFIG__MUTE, reason, notify_user, duration_string
    )
    if (component_interaction is None):
        return
    
    await client.user_guild_profile_edit(
        guild,
        user,
        timeout_duration = duration,
        reason = create_auto_reason(event, reason),
    )
    
    if notify_user:
        notify_note = await notify_user_action(
            client, guild, user, build_mute_notification_embed, reason, duration_string
        )
    else:
        notify_note = None
    
    await client.interaction_response_message_edit(
        component_interaction,
        allowed_mentions = None,
        components = None,
        embed = build_action_completed_embed(
            user, build_mute_embed, WORD_CONFIG__MUTE, notify_note, reason, notify_user, duration_string
        )
    )
