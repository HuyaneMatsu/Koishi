__all__ = ()

from scarletio import to_json
from hata import Client, Permission, Embed, datetime_to_timestamp
from hata.ext.slash import P, abort, InteractionResponse
from bot_utils.constants import GUILD__SUPPORT


SLASH_CLIENT: Client


def iterate_user_datas(guild, offset, limit, user_object_creator):
    user_iterator = iter(guild.users.values())
    
    while offset > 0:
        next(user_iterator)
        offset -= 1
    
    for user in user_iterator:
        yield user_object_creator(user, guild)
        
        limit -= 1
        if limit > 0:
            continue
        
        break


def create_user_object_koishi(user, guild):
    user_data = {}
    
    avatar_type = user.avatar_type
    if avatar_type:
        user_data['avatar_hash'] = user.avatar_hash
        user_data['avatar_type'] = avatar_type.value
    
    banner_color = user.banner_color
    if (banner_color is not None):
        user_data['banner_color'] = banner_color
    
    user_data['discriminator'] = user.discriminator
    
    flags = user.flags
    if flags:
        user_data['flags'] = flags
   
    user_data['id'] = user.id
    
    user_data['name'] = user.name
    
    
    guild_profile_data = {}
    user_data['guild_profile'] = guild_profile_data
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is not None):
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


def create_user_object_discord(user, guild):
    member_data = {}
    
    user_data = {}
    member_data['user'] = user_data
    
    avatar = user.avatar
    if avatar:
        base16_avatar_hash = avatar.as_base16_hash
    else:
        base16_avatar_hash = None
    user_data['avatar'] = base16_avatar_hash
    
    user_data['accent_color'] = user.banner_color
    user_data['discriminator'] = str(user.discriminator)
    user_data['public_flags'] = user.flags
    user_data['id'] = str(user.id)
    user_data['username'] = user.name
    
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is None):
        base16_avatar_hash = None
        boosts_since_timestamp = None
        joined_at_timestamp = None
        nick = None
        pending = False
        role_id_array = []
        timed_out_until_timestamp = None
    
    else:
        avatar = guild_profile.avatar
        if avatar:
            base16_avatar_hash = avatar.as_base16_hash
        else:
            base16_avatar_hash = None
        
        boosts_since = guild_profile.boosts_since
        if boosts_since is None:
            boosts_since_timestamp = None
        else:
            boosts_since_timestamp = datetime_to_timestamp(boosts_since)
    
        joined_at = guild_profile.joined_at
        if (joined_at is None):
            joined_at_timestamp = None
        else:
            joined_at_timestamp = datetime_to_timestamp(joined_at)
        
        nick = guild_profile.nick
        pending = guild_profile.pending
        
        role_ids = guild_profile.role_ids
        if (role_ids is None):
            role_id_array = []
        else:
            role_id_array = [str(role_id) for role_id in role_ids]
        
        timed_out_until = guild_profile.timed_out_until
        if (timed_out_until is None):
            timed_out_until_timestamp = None
        else:
            timed_out_until_timestamp = datetime_to_timestamp(timed_out_until)
    
    
    member_data['avatar'] = base16_avatar_hash
    member_data['premium_since'] = boosts_since_timestamp
    member_data['joined_at'] = joined_at_timestamp
    member_data['nick'] = nick
    member_data['pending'] = pending
    member_data['roles'] = role_id_array
    member_data['communication_disabled_until'] = timed_out_until_timestamp
    
    return member_data


@SLASH_CLIENT.interactions(
    guild = GUILD__SUPPORT,
    allow_in_dm = False,
    required_permissions = Permission().update_by_keys(manage_messages = True),
)
async def list_users(
    client,
    event,
    serialisation: (['koishi', 'discord'], 'Select on which mode I should serialise the data.'),
    offset : P('int', 'User listing offset.', min_value=0) = 0,
    limit: P('int', 'The maximal amount of users to list.', min_value=1, max_value=1000) = 1000,
):
    """Lists a chunk of the guild's users."""
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
    
    if serialisation == 'koishi':
        user_object_creator = create_user_object_koishi
    else:
        user_object_creator = create_user_object_discord
    
    json = to_json([*iterate_user_datas(guild, offset, limit, user_object_creator)])
    
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
