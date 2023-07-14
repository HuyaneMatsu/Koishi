__all__ = ()

from io import StringIO
from csv import writer as CsvWriter
from scarletio import to_json
from hata import Permission, Embed, datetime_to_timestamp
from hata.ext.slash import P, abort, InteractionResponse

from ..bot_utils.constants import GUILD__SUPPORT
from ..bots import SLASH_CLIENT


def iter_users(guild, offset, limit):
    user_iterator = iter(guild.users.values())
    
    while offset > 0:
        next(user_iterator)
        offset -= 1
    
    for user in user_iterator:
        yield user
        
        limit -= 1
        if limit > 0:
            continue
        
        break


def koishi_json_user_create(user, guild):
    user_data = {}
    
    avatar_type = user.avatar_type
    if avatar_type:
        user_data['avatar_hash'] = user.avatar_hash
        user_data['avatar_type'] = avatar_type.value
    
    banner_color = user.banner_color
    if (banner_color is not None):
        user_data['banner_color'] = banner_color
    
    if user.bot:
        user_data['bot'] = True
    
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


def discord_json_user_create(user, guild):
    member_data = {}
    
    user_data = {}
    member_data['user'] = user_data
    
    avatar = user.avatar
    if avatar:
        base16_avatar_hash = avatar.as_base_16_hash
    else:
        base16_avatar_hash = None
    user_data['avatar'] = base16_avatar_hash
    
    user_data['accent_color'] = user.banner_color
    user_data['discriminator'] = format(user.discriminator, '0>4')
    user_data['bot'] = user.bot
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
            base16_avatar_hash = avatar.as_base_16_hash
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


def create_json_data(guild, offset, limit, serialisation):
    if serialisation.startswith('koishi.s'):
        object_creator = koishi_json_user_create
    else:
        object_creator = discord_json_user_create
    
    return to_json([object_creator(user, guild) for user in iter_users(guild, offset, limit)])


def koishi_csv_header_create():
    return (
        'avatar_hash',
        'avatar_type',
        'banner_color',
        'discriminator',
        'flags',
        'id',
        'bot'
        'name',
        'guild_profile_avatar_hash',
        'guild_profile_avatar_type',
        'guild_profile_boosts_since',
        'guild_profile_joined_at',
        'guild_profile_nick',
        'guild_profile_pending',
        'guild_profile_role_ids',
        'guild_profile_timed_out_until',
    )


def discord_csv_header_create():
    return (
        'user_avatar',
        'user_accent_color',
        'user_bot',
        'user_discriminator',
        'user_public_flags',
        'user_id',
        'user_username',
        'avatar',
        'premium_since',
        'joined_at',
        'nick',
        'pending',
        'roles',
        'communication_disabled_until',
    )


def koishi_csv_user_create(user, guild):
    avatar_hash = user.avatar_hash
    avatar_type = user.avatar_type.value
    banner_color = user.banner_color
    discriminator = user.discriminator
    flags = format(user.flags, 'd')
    id_ = user.id
    name = user.name
    bot = 'true' if user.bot else 'false'
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is None):
        guild_profile_avatar_hash = 0
        guild_profile_avatar_type = 0
        guild_profile_boosts_since = None
        guild_profile_joined_at = None
        guild_profile_nick = None
        guild_profile_pending = 'false'
        guild_profile_role_ids = None
        guild_profile_timed_out_until = None
    
    else:
        guild_profile_avatar_hash = guild_profile.avatar_hash
        guild_profile_avatar_type = guild_profile.avatar_type.value
        
        boosts_since = guild_profile.boosts_since
        if (boosts_since is None):
            guild_profile_boosts_since = None
        else:
            guild_profile_boosts_since = datetime_to_timestamp(boosts_since)
        
        joined_at = guild_profile.joined_at
        if (joined_at is None):
            guild_profile_joined_at = None
        else:
            guild_profile_joined_at = datetime_to_timestamp(joined_at)
        
        guild_profile_nick = guild_profile.nick
        
        guild_profile_pending = 'true' if guild_profile.pending else 'false'
        
        role_ids = guild_profile.role_ids
        if (role_ids is None):
            guild_profile_role_ids = None
        else:
            guild_profile_role_ids = ' '.join([str(role_id) for role_id in role_ids])
        
        timed_out_until = guild_profile.timed_out_until
        if (timed_out_until is None):
            guild_profile_timed_out_until = None
        else:
            guild_profile_timed_out_until = datetime_to_timestamp(timed_out_until)
    
    return (
        avatar_hash,
        avatar_type,
        banner_color,
        discriminator,
        flags,
        id_,
        bot,
        name,
        guild_profile_avatar_hash,
        guild_profile_avatar_type,
        guild_profile_boosts_since,
        guild_profile_joined_at,
        guild_profile_nick,
        guild_profile_pending,
        guild_profile_role_ids,
        guild_profile_timed_out_until,
    )


def discord_csv_user_create(user, guild):
    avatar = user.avatar
    if avatar:
        user_avatar = avatar.as_base_16_hash
    else:
        user_avatar = None
    
    user_accent_color = user.banner_color
    user_discriminator = format(user.discriminator, '0>4')
    user_public_flags = format(user.flags, 'd')
    user_id = user.id
    user_username = user.name
    user_bot = 'true' if user.bot else 'false'
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is None):
        avatar = None
        premium_since = None
        joined_at = None
        nick = None
        pending = 'false'
        roles = None
        communication_disabled_until = None
    
    else:
        avatar = guild_profile.avatar
        if avatar:
            avatar = avatar.as_base_16_hash
        else:
            avatar = None
        
        boosts_since = guild_profile.boosts_since
        if boosts_since is None:
            premium_since = None
        else:
            premium_since = datetime_to_timestamp(boosts_since)
    
        joined_at = guild_profile.joined_at
        if (joined_at is None):
            joined_at = None
        else:
            joined_at = datetime_to_timestamp(joined_at)
        
        nick = guild_profile.nick
        pending = 'true' if guild_profile.pending else 'false'
        
        role_ids = guild_profile.role_ids
        if (role_ids is None):
            roles = None
        else:
            roles = ' '.join([str(role_id) for role_id in role_ids])
        
        timed_out_until = guild_profile.timed_out_until
        if (timed_out_until is None):
            communication_disabled_until = None
        else:
            communication_disabled_until = datetime_to_timestamp(timed_out_until)
    
    
    return (
        user_avatar,
        user_accent_color,
        user_bot,
        user_discriminator,
        user_public_flags,
        user_id,
        user_username,
        avatar,
        premium_since,
        joined_at,
        nick,
        pending,
        roles,
        communication_disabled_until,
    )


def create_csv_data(guild, offset, limit, serialisation):

    if serialisation.startswith('koishi.'):
        header_creator = koishi_csv_header_create
        row_creator = koishi_csv_user_create
    else:
        header_creator = discord_csv_header_create
        row_creator = discord_csv_user_create
    
    file = StringIO()
    
    writer = CsvWriter(file)
    writer.writerow(header_creator())
    
    for user in iter_users(guild, offset, limit):
         writer.writerow(row_creator(user, guild))
    
    return file.getvalue()


SERIALIZATION_MODES = ['koishi.json', 'discord.json', 'koishi.csv', 'discord.csv']


@SLASH_CLIENT.interactions(
    guild = GUILD__SUPPORT,
    allow_in_dm = False,
    required_permissions = Permission().update_by_keys(manage_messages = True),
)
async def list_users(
    client,
    event,
    serialisation: (SERIALIZATION_MODES, 'Select on which mode I should serialize the data.'),
    offset : P('int', 'User listing offset.', min_value = 0) = 0,
    limit: P('int', 'The maximal amount of users to list.', min_value = 1, max_value = 1000) = 1000,
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
        await client.request_all_users_of(guild)
    
    if serialisation.endswith('.json'):
        data = create_json_data(guild, offset, limit, serialisation)
        postfix = 'json'
    else:
        data = create_csv_data(guild, offset, limit, serialisation)
        postfix = 'csv'
    
    
    yield InteractionResponse(
        embed = Embed(
            f'Users of {guild.name}'
        ).add_thumbnail(
            guild.icon_url
        ).add_field(
            'Serialisation',
            (
                f'```\n'
                f'{serialisation}\n'
                f'```'
            ),
            inline = True,
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
        file = (f'users.{postfix}', data),
    )
