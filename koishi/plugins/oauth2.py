__all__ = ()

from scarletio import sleep
from hata import Color, Embed, parse_oauth2_redirect_url, DiscordException, ERROR_CODES, Channel, ChannelType
from hata.ext.commands_v2 import checks
from hata.ext.slash.menus import Pagination

from ..bots import COMMAND_CLIENT

OAUTH2_COLOR = Color.from_rgb(148, 0, 211)

COMMAND_CLIENT.command_processor.create_category('OAUTH2', checks = checks.owner_only())

VALUABLE_SCOPES = [
    'identify',
    'connections',
    'guilds',
    'guilds.join',
    'email',
    'applications.commands.permissions.update',
    'applications.builds.read',
    'applications.builds.upload',
    'applications.entitlements',
    'applications.store.update',
]

OA2_accesses = {}

def _oauth2_query(message, content):
    author_id = message.author.id
    if not (16<len(content)<33):
        return OA2_accesses.get(author_id, None)
    try:
        user_id = int(content)
    except ValueError:
        return OA2_accesses.get(author_id, None)
    
    user = OA2_accesses.get(user_id, None)
    if user is None:
        user = OA2_accesses.get(author_id, None)
    return user


async def oauth2_link_description(command_context):
    prefix = command_context.prefix
    return Embed(
        'oauth2_link',
        (
            'I ll give you a nice authorization link for some oauth 2 scopes.\n'
            f'Usage: `{prefix}oauth2_link`\n'
            'After you authorized yourself, you should call the `oauth2_feed` '
            'command, to feed the authorized link to me.\n'
            f'Example: `{prefix}oauth2_feed *link*`\n'
            'By doing this you will unlock other oauth 2 commands, like:\n'
            f'- `{prefix}oauth2_user <user_id>`\n'
            f'- `{prefix}oauth2_connections <user_id>`\n'
            f'- `{prefix}oauth2_guilds <user_id>`\n'
            f'- `{prefix}oauth2_my_guild <user_id>`\n'
            f'- `{prefix}oauth2_renew <user_id>`'
        ),
        color = OAUTH2_COLOR,
    ).add_footer(
        'Owner only!',
    )


@COMMAND_CLIENT.commands(
    category = 'OAUTH2',
    description = oauth2_link_description,
)
async def oauth2_link(client, message,): #just a test link
    await client.message_create(
        message.channel,
        (
            'https://discordapp.com/oauth2/authorize?client_id=486565096164687885'
            '&redirect_uri=https%3A%2F%2Fgithub.com%2FHuyaneMatsu'
            '&response_type=code&scope=identify%20connections%20guilds%20guilds.join'
            '%20email%20applications.entitlements'
        ),
    )


async def oauth2_feed_description(command_context):
    prefix = command_context.prefix
    return Embed(
        'oauth2_feed',
        (
            'Feeds your oauth 2 authorized redirect url.\n'
            f'Usage: `{prefix}oauth2_feed *link*`\n'
            f'How to get an oauth 2 authorization url?, use: `{prefix}oauth2_link`\n'
            'By doing this you will unlock other oauth 2 commands, like:\n'
            f'- `{prefix}oauth2_user <user_id>`\n'
            f'- `{prefix}oauth2_connections <user_id>`\n'
            f'- `{prefix}oauth2_guilds <user_id>`\n'
            f'- `{prefix}oauth2_my_guild <user_id>`\n'
            f'- `{prefix}oauth2_renew <user_id>`'
        ),
        color = OAUTH2_COLOR,
    ).add_footer(
        'Owner only!',
    )


@COMMAND_CLIENT.commands(
    category = 'OAUTH2',
    description = oauth2_feed_description,
)
async def oauth2_feed(client, message, content):
    try:
        await client.message_delete(message)
    except BaseException as err:
        if isinstance(err,ConnectionError):
            # no internet
            return
        
        elif isinstance(err, DiscordException):
            if err.code == ERROR_CODES.missing_access: # client removed
                return
        
        raise
    
    result = parse_oauth2_redirect_url(content)
    if result is None:
        await client.message_create(message.channel,'Bad link')
        return

    access = await client.activate_authorization_code(*result, VALUABLE_SCOPES)

    if access is None:
        await client.message_create(message.channel,'Too old link')
        return
    
    user = await client.user_info_get(access)
    OA2_accesses[user.id] = user
    await client.message_create(message.channel,'Thanks')


async def oauth2_user_description(command_context):
    return Embed(
        'oauth2_user',
        (
            'After you authorized yourself, I will know your deepest secrets :3\n'
            'Using this command, I ll show the extra user information , I '
            'received.\n'
            f'Usage: `{command_context.prefix}oauth2_user <user_id>`\n'
            'Well, every other owner will know it too, by passing your id, '
            'so take care, you can not trust them! *Only me!*\n'
            'If you don\'t know how to authorize yourself; use : '
            f'`{command_context.prefix}help oauth2_link`'
        ),
        color = OAUTH2_COLOR
    ).add_footer(
        'Owner only!'
    )


@COMMAND_CLIENT.commands(
    category = 'OAUTH2',
    description = oauth2_user_description,
    
)
async def oauth2_user(client, message, content):
    user = _oauth2_query(message, content)
    if user is None:
        await client.message_create(message.channel, 'Could not find that user')
        return
    
    await Pagination(client, message.channel, [Embed(description = repr(user))])



async def oauth2_connections_description(command_context):
    return Embed(
        'oauth2_connections',
        (
            'After you authorized yourself, I will know your deepest secrets :3\n'
            'You might ask what are your connections. '
            'Those are your connected apps and sites.\n'
            f'Usage: `{command_context.prefix}oauth2_connections <user_id>`\n'
            'Well, every other owner will know it too, by passing your id, '
            'so take care, you can not trust them! *Only me!*\n'
            'If you don\'t know how to authorize yourself; use : '
            f'`{command_context.prefix}help oauth2_link`'
        ),
        color = OAUTH2_COLOR,
    ).add_footer(
        'Owner only!'
    )


@COMMAND_CLIENT.commands(
    category = 'OAUTH2',
    description = oauth2_connections_description,
)
async def oauth2_connections(client, message, content):
    user = _oauth2_query(message,content)
    if user is None:
        await client.message_create(message.channel, 'Could not find that user')
        return
    
    connections = await client.user_connection_get_all(user.access)
    
    await Pagination(client, message.channel, [Embed(description = repr(connections))])


async def oauth2_guilds_description(command_context):
    return Embed(
        'oauth2_guilds',
        (
            'After you authorized yourself, I will know your deepest secrets :3\n'
            'By using this command, I ll show your guilds. '
            '*And everything, what I know about them.*\n'
            f'Usage: `{command_context.prefix}oauth2_guilds <user_id>`\n'
            'Well, every other owner will know it too, by passing your id, '
            'so take care, you can not trust them! *Only me!*\n'
            'If you don\'t know how to authorize yourself; use : '
            f'`{command_context.prefix}help oauth2_link`'
        ),
        color = OAUTH2_COLOR,
    ).add_footer(
        'Owner only!',
    )


@COMMAND_CLIENT.commands(
    category = 'OAUTH2',
    description = oauth2_guilds_description,
)
async def oauth2_guilds(client,message,content):
    user = _oauth2_query(message,content)
    if user is None:
        await client.message_create(message.channel, 'Could not find that user')
        return
    
    guilds = await client.user_guild_get_all(user.access)
    
    await Pagination(client, message.channel, [Embed(description = repr(guilds))])


async def oauth2_my_guild_description(command_context):
    return Embed(
        'oauth2_my_guild',
        (
            'After you authorized yourself, I can create a guild for you, '
            'so just sit back!\n'
            f'Usage: `{command_context.prefix}oauth2_my_guild <user_id>`\n'
            'Other owners can create a guild for you, after you authorized, '
            'take care!\n'
            'If you don\'t know how to authorize yourself, use : '
            f'`{command_context.prefix}help oauth2_link`'
        ),
        color = OAUTH2_COLOR,
    ).add_footer(
        'Owner only!',
    )

    
@COMMAND_CLIENT.commands(
    category = 'OAUTH2',
    description = oauth2_my_guild_description,
)
async def oauth2_my_guild(client,message,content):
    user = _oauth2_query(message,content)
    if user is None:
        await client.message_create(message.channel, 'Could not find that user')
        return
    
    guild = None
    try:
        guild = await client.guild_create(
            'Luv ya',
            channels = [
                Channel(name = f'Love u {message.author.name}', channel_type = ChannelType.guild_text).to_data(),
            ],
        )
        
        await sleep(1.0, client.loop)
        await client.guild_user_add(guild, user)
        await sleep(1.0, client.loop)
        await client.guild_edit(guild, owner = user.id)
    finally:
        if guild is None:
            return
        
        await sleep(1.0, client.loop)
        if client is guild.owner:
            await client.guild_delete(guild)
        else:
            await client.guild_leave(guild)


async def oauth2_renew_description(command_context):
    return Embed(
        'oauth2_renew',
        (
            'Your oauth2 authorization might expire; with this command you can '
            'renew it.\n'
            f'Usage: `{command_context.prefix}oauth2_renew <user_id>`\n'
            'Other owners can renew it for you as well!\n'
            'If you don\'t know how to authorize yourself;\n'
            f'Use : `{command_context.prefix}help oauth2_link`'
        ),
        color = OAUTH2_COLOR,
    ).add_footer(
        'Owner only!',
    )


@COMMAND_CLIENT.commands(
    category = 'OAUTH2',
    description = oauth2_renew_description,
)
async def oauth2_renew(client,message,content):
    user = _oauth2_query(message,content)
    if user is None:
        await client.message_create(message.channel, 'Could not find that user')
        return
    
    access = user.access
    last = access.created_at
    await client.renew_access_token(access)
    new = access.created_at
    await client.message_create(
        message.channel,
        (
            f'{user:f}\' access token is renewed.\n'
            f'From creation time at: {last:%Y.%m.%d-%H:%M:%S}\n'
            f'To creation time at: {new:%Y.%m.%d-%H:%M:%S}'
        ),
    )
