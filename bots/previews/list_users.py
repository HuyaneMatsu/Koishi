__all__ = ()

from scarletio import to_json
from hata import Client, Permission, Embed, datetime_to_timestamp
from hata.ext.slash import P, abort, InteractionResponse
from bot_utils.constants import GUILD__SUPPORT


SLASH_CLIENT: Client


def iterate_user_datas(guild, offset, limit):
    user_iterator = iter(guild.users.values())
    
    while offset > 0:
        next(user_iterator)
        offset -= 1
    
    for user in user_iterator:
        yield create_user_object(user, guild)
        
        limit -= 1
        if limit > 0:
            continue
        
        break


def create_user_object(user, guild):
    user_data = {}
    
    avatar_type = user.avatar_type
    if avatar_type:
        user_data['avatar_hash'] = user.avatar_hash
        user_data['avatar_type'] = avatar_type.value
    
    user_data['discriminator'] = user.discriminator
    
    flags = user.flags
    if flags:
        user_data['flags'] = flags
   
    user_data['id'] = user.id
    
    user_data['name'] = user.name
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is not None):
        guild_profile_data = {}
        user_data['guild_profile'] = guild_profile_data
            
        avatar_type = guild_profile.avatar_type
        if avatar_type:
            guild_profile_data['avatar_hash'] = guild_profile.avatar_hash
            guild_profile_data['avatar_type'] = avatar_type.value
        
        boosts_since = guild_profile.boosts_since
        if (boosts_since is not None):
            guild_profile_data['boosts_since'] = datetime_to_timestamp(boosts_since)
        
        joined_at = guild_profile.joined_at
        if (joined_at is not None):
            guild_profile_data['joined_at'] = datetime_to_timestamp(joined_at)
        
        nick = guild_profile.nick
        if (nick is not None):
            guild_profile_data['nick'] = nick
        
        pending = guild_profile.pending
        if pending:
            guild_profile_data['pending'] = pending
        
        role_ids = guild_profile.role_ids
        if (role_ids is not None):
            guild_profile_data['role_ids'] = [*role_ids]
        
        timed_out_until = guild_profile.timed_out_until
        if (timed_out_until is not None):
            guild_profile_data['timed_out_until'] = datetime_to_timestamp(timed_out_until)
    
    return user_data


@SLASH_CLIENT.interactions(
    guild = GUILD__SUPPORT,
    allow_in_dm = False,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def list_users(
    client,
    event,
    offset : P('int', 'User listing offset.', min_value=0) = 0,
    limit: P('int', 'The maximal amount of users to list.', min_value=1, max_value=1000) = 1000,
):
    guild = event.guild
    if guild is None:
        guild = await client.guild_get(event.guild_id)
    
    if offset < 0:
        offset = 0
    
    if limit < 0:
        limit = 0
    elif limit > 1000:
        limit = 1000
    
    if offset >= guild.user_count or limit <= 0:
        abort('Would have return 0 users.')
    
    if guild.user_count > len(guild.users):
        yield
        await client.request_members(guild)
    
    json = to_json([*iterate_user_datas(guild, offset, limit)])
    
    yield InteractionResponse(
        embed = Embed(
            f'Users of {guild.name}'
        ).add_thumbnail(
            guild.icon_url
        ).add_field(
            'Offset',
            (
                f'```\n'
                f'{offset}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Limit',
            (
                f'```\n'
                f'{limit}\n'
                f'```'
            ),
            inline = True,
        ),
        file = ('users.json', json),
    )
