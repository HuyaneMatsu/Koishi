__all__ = ()

from datetime import datetime

from dateutil.relativedelta import relativedelta
from hata import DATETIME_FORMAT_CODE, Embed, elapsed_time


def build_user_embed(guild, user, guild_profile, join):
    """
    Builds a user join or leave embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    user : ``ClientUserBase``
        The user who joined or left.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile in the guild.
    join : `bool`
        Whether the user joined or left.
    
    Returns
    -------
    embed : ``Embed``
    """
    created_at = user.created_at
    description_parts = [
        'Created: ',
        format(created_at, DATETIME_FORMAT_CODE),
        '\nProfile: ',
        user.mention,
        '\nID: ',
        str(user.id),
        '\n'
    ]
    
    if guild_profile is None:
        joined_at = None
    else:
        joined_at = guild_profile.joined_at
    
    if joined_at is None:
        joined_text = 'Lurking'
        if join:
            joined_at = datetime.utcnow()
    else:
        joined_text = 'Joined'
    
    description_parts.append(joined_text)
    description_parts.append(': ')
    
    if (joined_at is None):
        joined_at_string = 'N/A'
    else:
        joined_at_string = format(joined_at, DATETIME_FORMAT_CODE)
    
    description_parts.append(joined_at_string)
    
    if join:
        description_parts.append('\nDifference: ')
        
        if joined_at is None:
            difference_string = 'N/A'
        else:
            difference_string = elapsed_time(relativedelta(created_at, joined_at))
        
        description_parts.append(difference_string)
    
    else:
        description_parts.append('\nCreated-joined difference: ')
        
        if joined_at is None:
            difference_string = 'N/A'
        else:
            difference_string = elapsed_time(relativedelta(created_at, joined_at))
        
        description_parts.append(difference_string)
    
        description_parts.append('\nJoined-left difference: ')
        
        if joined_at is None:
            difference_string = 'N/A'
        else:
            difference_string = elapsed_time(joined_at)
        
        description_parts.append(difference_string)
    
    
    description = ''.join(description_parts)
    description_parts = None
    
    embed = Embed(
        user.full_name,
        description,
    ).add_thumbnail(
        user.avatar_url,
    )
    
    if join:
        state = 'joined to'
    else:
        state = 'left from'
    
    embed.add_author(
        f'User {state} {guild.name}'
    )
    
    return embed
