__all__ = ()

import re
from datetime import timedelta as TimeDelta

from hata import Embed

from ....bots import FEATURE_CLIENTS

from ..shared_constants import PERMISSIONS__MUTE, WORD_CONFIG__MUTE
from ..shared_helpers import (
    add_reason_field, add_standalone_field, check_user_cannot_be_admin, create_auto_reason, process_reason
)
from ..shared_helpers_mute import (
    PARAMETER_DAYS, PARAMETER_HOURS, PARAMETER_MINUTES, PARAMETER_SECONDS, build_duration_string, get_duration
)

from .helpers import build_action_completed_embed, check_required_permissions, create_response_form


CUSTOM_ID_SELF_MUTE = 'mod.self.form.mute'


def build_mute_embed(user, title, description, reason, duration_string):
    """
    Builds a self-mute embed.
    
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
    duration_string : `str`
        The duration in string.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(title, description).add_thumbnail(user.avatar_url)
    add_standalone_field(embed, 'Duration', duration_string)
    add_reason_field(embed, reason)
    return embed


async def mute_command(
    client,
    event,
    days: PARAMETER_DAYS = 0,
    hours: PARAMETER_HOURS = 0,
    minutes: PARAMETER_MINUTES = 0,
    seconds: PARAMETER_SECONDS = 0,
):
    """Wanna mute yourself?"""
    guild = event.guild
    check_required_permissions(client, event, guild, PERMISSIONS__MUTE, WORD_CONFIG__MUTE)
    check_user_cannot_be_admin(guild, event.user, WORD_CONFIG__MUTE)
    
    duration = get_duration(days, hours, minutes, seconds)
    duration_string = build_duration_string(duration)
    if len(duration_string) > 20:
        duration_string = f'{duration_string[:20]} ...'
    
    return create_response_form(
        f'Self mute for {duration_string}', 'Mute', f'{CUSTOM_ID_SELF_MUTE}.{duration.total_seconds():.0f}'
    )


@FEATURE_CLIENTS.interactions(custom_id = re.compile(f'{re.escape(CUSTOM_ID_SELF_MUTE)}\\.(\\d+)'), target = 'form')
async def self_mute(client, event, duration_seconds, *, reason = None):
    """Self-mutes the user."""
    guild = event.guild
    if guild is None:
        # Guild out of cache? The client is probably removed.
        return
    
    duration = TimeDelta(seconds = int(duration_seconds))
    reason = process_reason(reason)
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    await client.user_guild_profile_edit(
        guild,
        event.user,
        timeout_duration = duration,
        reason = create_auto_reason(event, reason),
    )
    
    await client.interaction_response_message_edit(
        event,
        allowed_mentions = None,
        embed = build_action_completed_embed(
            event.user, guild.id, build_mute_embed, WORD_CONFIG__MUTE, reason, build_duration_string(duration)
        )
    )
