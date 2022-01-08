from datetime import datetime
from hata import Client, Embed, DATETIME_FORMAT_CODE, elapsed_time
from dateutil.relativedelta import relativedelta
from bot_utils.constants import CHANNEL__SUPPORT__LOG_USER, GUILD__SUPPORT
from hata.ext.extension_loader import require

require(Satori=Client)

Satori: Client

def create_user_embed(user, guild_profile, join):
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
        description_parts.append(elapsed_time(relativedelta(created_at, joined_at)))
    
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
        f'User {state} {GUILD__SUPPORT.name}'
    )
    
    return embed


@Satori.events
async def guild_user_add(client, guild, user):
    if guild is not GUILD__SUPPORT:
        return
    
    embed = create_user_embed(user, user.get_guild_profile_for(guild), True)
    
    await client.message_create(CHANNEL__SUPPORT__LOG_USER, embed=embed)


@Satori.events
async def guild_user_delete(client, guild, user, guild_profile):
    if guild is not GUILD__SUPPORT:
        return
    
    embed = create_user_embed(user, guild_profile, False)
    
    await client.message_create(CHANNEL__SUPPORT__LOG_USER, embed=embed)
