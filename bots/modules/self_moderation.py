from hata import Client, Embed, Emoji
from datetime import datetime, timedelta
from random import random, randint
from hata.ext.slash import abort, P

SLASH_CLIENT: Client


EMOJI_KOKORO_THINK = Emoji.precreate(852857888892649492)
EMOJI_KOKORO = Emoji.precreate(927881929401974834)
EMOJI_KOKORO_STARE = Emoji.precreate(754796863370166445)
EMOJI_KOKORO_SHOCKED = Emoji.precreate(860898436752080916)


def create_random_durations():
    if random() <= 0.5:
        days = randint(1, 28)
    else:
        days = 0
    
    if days == 28:
        hours = 0
        minutes = 0
        seconds = 0
    
    else:
        if random() <= 0.25:
            hours = randint(1, 24)
        else:
            hours = 0
        
        if random() <= 0.125:
            minutes = randint(1, 60)
        else:
            minutes = 0
        
        if random() <= 0.0675:
            seconds = randint(1, 60)
        else:
            seconds = 0
        
        if not days and not hours and not minutes and not seconds:
            days = 1
    
    return (days, hours, minutes, seconds)


@SLASH_CLIENT.interactions(is_global=True, allow_in_dm=False)
async def self_mute(
    client,
    event,
    days: P('int', 'days', min_value=0, max_value=28) = 0,
    hours: P('int', 'hours', min_value=0, max_value=24) = 0,
    minutes: P('int', 'minutes', min_value=0, max_value=60) = 0,
    seconds: P('int', 'seconds', min_value=0, max_value=60) = 0,
):
    """Get a rest."""
    if days == 28:
        difference = timedelta(days=28)
    elif days or hours or minutes or seconds:
        difference = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    else:
        difference = None
    
    
    if (difference is not None):
        guild = event.guild
        if (guild is None) or (not guild.cached_permissions_for(client).can_moderate_users):
            abort('I require moderate users permission to execute this command.')
        
        if not client.has_higher_role_than_at(event.user, guild):
            abort('Oke boss.')
        
        yield
        await client.user_guild_profile_edit(guild, event.user, timed_out_until=datetime.utcnow()+difference)
    
    
    description_parts = ['Duration: ']
    if days == 28:
        description_parts.append('28 days')
    
    else:
        if difference is None:
            unit_values = create_random_durations()
            unit_names = (
                EMOJI_KOKORO_THINK.as_emoji,
                EMOJI_KOKORO.as_emoji,
                EMOJI_KOKORO_STARE.as_emoji,
                EMOJI_KOKORO_SHOCKED.as_emoji,
            )
        
        else:
            unit_values = (days, hours, minutes, seconds)
            unit_names = ('days', 'hours', 'minutes', 'seconds')
        
        field_added = False
        for unit_value, unit_name in zip(unit_values, unit_names):
            if unit_value:
                if field_added:
                    description_parts.append(', ')
                else:
                    field_added = True
                
                description_parts.append(str(unit_value))
                description_parts.append(' ')
                description_parts.append(unit_name)
    
    description = ''.join(description_parts)
    description_parts = None
    
    yield Embed('Mute', description).add_author('Self moderation')
