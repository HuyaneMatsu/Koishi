import json
from math import ceil
from functools import partial as partial_func
from colorsys import rgb_to_hsv, rgb_to_yiq
from datetime import datetime, timedelta
from random import choice

from hata import Color, Embed, Client, DiscordException, now_as_id, parse_emoji, CHANNEL_TYPES, \
    elapsed_time, Status, BUILTIN_EMOJIS, ChannelText, ChannelCategory, id_to_datetime, RoleManagerType, ERROR_CODES, \
    cchunkify, ICON_TYPE_NONE, KOKORO, ChannelVoice, ChannelStore, ChannelThread, DATETIME_FORMAT_CODE, parse_color, \
    StickerFormat, ZEROUSER, ChannelDirectory, Permission, escape_markdown
from hata.discord.invite.invite import EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID
from scarletio import WaitTillExc, ReuBytesIO
from hata.ext.slash.menus import Pagination
from hata.ext.slash import abort, InteractionResponse, set_permission, Button, Row

from PIL import Image as PIL
from dateutil.relativedelta import relativedelta

from bot_utils.tools import Pagination10step
from bot_utils.constants import ROLE__SUPPORT__TESTER, GUILD__SUPPORT, ROLE__SUPPORT__MODERATOR

UTILITY_COLOR = Color(0x5dc66f)

SLASH_CLIENT: Client

PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)

STATUS_ONLINE = Status.online
STATUS_IDLE = Status.idle
STATUS_DND = Status.dnd
STATUS_OFFLINE = Status.offline

STATUS_VALUE_OFFLINE = STATUS_OFFLINE.value

EMOJI_HEART_GREEN = BUILTIN_EMOJIS['green_heart']
EMOJI_HEART_YELLOW = BUILTIN_EMOJIS['yellow_heart']
EMOJI_HEART_RED = BUILTIN_EMOJIS['heart']
EMOJI_HEART_BLACK = BUILTIN_EMOJIS['black_heart']
EMOJI_HEART_GIFT = BUILTIN_EMOJIS['gift_heart']

STATUS_VALUE_TO_HEART_EMOJI = {
    STATUS_ONLINE.value: EMOJI_HEART_GREEN,
    STATUS_IDLE.value: EMOJI_HEART_YELLOW,
    STATUS_DND.value: EMOJI_HEART_RED,
    STATUS_OFFLINE.value: EMOJI_HEART_BLACK,
}

PLATFORMS = ('desktop', 'mobile', 'web')

@SLASH_CLIENT.interactions(is_global=True)
async def rawr(client, event):
    """Sends a message with everyone from my universe."""
    yield
    
    channel = event.channel
    tasks = []
    
    for client_ in channel.clients:
        if client_ is client:
            coroutine = client.interaction_response_message_create(event, 'Rawrr !')
        else:
            if not channel.cached_permissions_for(client_) & PERMISSION_MASK_MESSAGING:
                continue
            
            coroutine = client_.message_create(channel, 'Rawrr !')
        tasks.append(KOKORO.create_task(coroutine))
    
    try:
        await WaitTillExc(tasks, KOKORO)
    except:
        for task in tasks:
            task.cancel()
        raise


@SLASH_CLIENT.interactions(is_global=True)
async def color_(client, event,
    color: ('str', 'Beauty!')
):
    """Shows the given color"""
    
    color = parse_color(color)
    if color is None:
        yield 'Could not recognize the color.'
        return
    
    yield
    
    embed = Embed(color=color)
    embed.add_field('hex', f'#{color:06X}', inline=True)
    embed.add_field('rgb', f'{color >> 16} r\n{(color >> 8) & 255} g\n{color & 255} b', inline=True)
    r, g, b = color.as_rgb_float_tuple
    embed.add_field('rgb%', f'{r * 100.0:0.2f}% r\n{g * 100.0:0.2f}% g\n{b * 100.0:0.2f}% b', inline=True)
    h, s, v = rgb_to_hsv(r, g, b)
    embed.add_field('hsv%', f'{h * 100.0:0.2f}% h\n{s * 100.0:0.2f}% s\n{v * 100.0:0.2f}% v', inline=True)
    y, i, q = rgb_to_yiq(r, g, b)
    embed.add_field('yiq%', f'{y * 100.0:0.2f}% y\n{i * 100.0:0.2f}% i\n{q * 100.0:0.2f}% q', inline=True)
    
    embed.add_image('attachment://color.png')
    
    with ReuBytesIO() as buffer:
        image = PIL.new('RGB', (240, 30), color.as_rgb)
        image.save(buffer,'png')
        buffer.seek(0)
        
        await client.interaction_followup_message_create(event, embed=embed, file=('color.png', buffer))


@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, allow_by_default=False, target='message')
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def raw(client, event):
    """Shows up the message's payload."""
    if not event.user.has_role(ROLE__SUPPORT__TESTER):
        abort(f'You must have {ROLE__SUPPORT__TESTER.mention} to invoke this command.')
    
    data = await client.http.message_get(event.channel_id, event.interaction.target_id)
    chunks = cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
    
    pages = [Embed(description=chunk) for chunk in chunks]
    await Pagination(client, event, pages)


class RoleCache:
    __slots__ = ('cache', 'guild', 'roles',)
    def __new__(cls, guild):
        self = object.__new__(cls)
        self.guild = guild
        roles = guild.role_list
        roles.reverse()
        self.roles = roles
        self.cache = {}
        
        self.create_page_0(guild)
        return self
    
    def create_page_0(self, guild):
        embed = Embed(
            f'Roles of **{guild.name}**:',
            '\n'.join([role.mention for role in self.roles]),
            color = (guild.icon_hash & 0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id >> 22) & 0xFFFFFF),
        )
        
        embed.add_footer(f'Page 1 / {len(self.roles) + 1}')
        self.cache[0] = embed
    
    def __getitem__(self,index):
        page = self.cache.get(index, None)
        if page is None:
            page = self.create_page(index)
        
        return page

    def create_page(self,index):
        role = self.roles[index - 1]
        embed = Embed(role.name,
            '\n'.join([
                f'id : {role.id!r}',
                f'color : {role.color.as_html}',
                f'permission number : {role.permissions:d}',
                f'managed : {role.managed}',
                f'separated : {role.separated}',
                f'mentionable : {role.mentionable}',
                '\nPermissions:\n```diff',
                *(f'{"+" if value else "-"}{key.replace("_", "-")}' for key, value in role.permissions.items()),
                '```',
            ]),
            color = role.color,
        )
        embed.add_footer(f'Page {index + 1} /  {len(self.roles) + 1}')
        
        self.cache[index] = embed
        return embed
    
    def __len__(self):
        return len(self.roles) + 1

PERMISSION_MASK_REACT = Permission().update_by_keys(
    add_reactions = True,
)

@SLASH_CLIENT.interactions(is_global=True)
async def roles_(client, event):
    """Lists the roles of the guild for my cutie!"""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute this command')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions & PERMISSION_MASK_MESSAGING) or ( not permissions & PERMISSION_MASK_REACT):
        abort('I require `send messages` and `add reactions` permissions to execute this command.')
    
    await Pagination10step(client, event, RoleCache(guild))


@SLASH_CLIENT.interactions(is_global=True)
async def welcome_screen_(client, event):
    """Shows the guild's welcome screen."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute this command')
    
    yield
    
    welcome_screen = await client.welcome_screen_get(guild)
    if welcome_screen is None:
        yield Embed(description=f'**{guild.name}** *has no welcome screen enabled*.')
        return
    
    description = welcome_screen.description
    if (description is None):
        description = '*TOP THINGS TO DO HERE*'
    else:
        description = f'{welcome_screen.description}\n\n*TOP THINGS TO DO HERE*'
    
    embed = Embed(f'Welcome to **{guild.name}**', description)
    
    icon_url = guild.icon_url
    if (icon_url is not None):
        embed.add_thumbnail(icon_url)
    
    welcome_channels = welcome_screen.welcome_channels
    if (welcome_channels is not None):
        for welcome_channel in welcome_channels:
            embed.add_field(
                f'{welcome_channel.emoji:e} {welcome_channel.description}',
                f'#{welcome_channel.channel:d}',
            )
    
    yield embed

ID = SLASH_CLIENT.interactions(
    None,
    name = 'id',
    description = 'Shows the id of the selected entity',
    is_global = True,
)

@ID.interactions
async def user_(client, event,
    user: ('user', 'Who\'s id do you want to see?') = None,
):
    """Returns your or the selected user's identifier."""
    if user is None:
        user = event.user
    
    return str(user.id)


@ID.interactions
async def channel_(client, event,
    channel: ('channel', 'Which channel\'s id do you want to see?') = None,
):
    """Returns this or the selected channel's identifier."""
    if channel is None:
        channel = event.channel
    
    return str(channel.id)


@ID.interactions
async def guild_(client, event):
    """Returns the guild's identifier."""
    guild = event.guild
    if guild is None:
        return Embed('Error', 'Guild only command.', color=UTILITY_COLOR)
    
    return str(guild.id)

@ID.interactions
async def role_(client, event,
    role: ('role', 'Which role\'s id do you want to see?') = None,
):
    """Returns this or the guild\'s default role's identifier."""
    guild = event.guild
    if guild is None:
        return Embed('Error', 'Guild only command.', color=UTILITY_COLOR)
    
    if role is None:
        # Hax
        role_id = guild.id
    else:
        role_id = role.id
    
    return str(role_id)


@SLASH_CLIENT.interactions(is_global=True)
async def now_as_id_(client, event):
    """Returns the current time as discord snowflake."""
    return str(now_as_id())


# Koishi user caching will be disabled, so this command would not work.
'''
def shared_guilds_pagination_check(user, event):
    event_user = event.user
    if user is event.user:
        return True
    
    if event.channel.permissions_for(event_user).can_manage_messages:
        return True
    
    return False


@SLASH_CLIENT.interactions(is_global=True)
async def shared_guilds(client, event):
    """Returns the shared guilds between you and me."""
    pages = []
    lines = []
    lines_count = 0
    
    user = event.user
    for guild_id, guild_profile in user.guild_profiles.items():
        guild = GUILDS[guild_id]
        nick = guild_profile.nick
        guild_name = guild.name
        if nick is None:
            line = guild_name
        else:
            line = f'{guild_name} [{nick}]'
        
        lines.append(line)
        lines_count += 1
        
        if lines_count == 10:
            pages.append('\n'.join(lines))
            lines.clear()
            lines_count = 0
    
    if lines_count:
        pages.append('\n'.join(lines))
    
    if not pages:
        pages.append('*none*')
    
    embeds = []
    embed_title = f'Shared guilds with {user.full_name}:'
    
    for page in pages:
        embed = Embed(embed_title, page, color=UTILITY_COLOR)
        embeds.append(embed)
    
    await Pagination(client, event, embeds, check=partial_func(shared_guilds_pagination_check, user))
'''

@SLASH_CLIENT.interactions(name='user', is_global=True)
async def user_(client, event,
    user: ('user', 'Check out someone other user?') = None,
):
    """Shows some information about your or about the selected user."""
    if user is None:
        user = event.user
    
    guild = event.guild
    
    embed = Embed(
        user.full_name,
    ).add_thumbnail(
        user.avatar_url,
    )
    
    created_at = user.created_at
    embed.add_field(
        'User Information',
        (
            f'Created: {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
            f'Profile: {user:m}\n'
            f'ID: {user.id}'
        ),
    )
    
    guild_profile = user.get_guild_profile_for(guild)
    
    if guild_profile is None:
        if user.avatar_type is ICON_TYPE_NONE:
            color = user.default_avatar.color
        else:
            color = user.avatar_hash & 0xFFFFFF
        embed.color = color
    
    else:
        embed.color = user.color_at(guild)
        roles = guild_profile.roles
        if roles is None:
            roles = '*none*'
        else:
            roles = ', '.join(role.mention for role in reversed(roles))
        
        text = []
        if guild_profile.nick is not None:
            text.append(f'Nick: {guild_profile.nick}')
        
        # Joined at can be `None` if the user is in lurking mode.
        joined_at = guild_profile.joined_at
        if joined_at is not None:
            text.append(f'Joined: {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]')
        
        boosts_since = guild_profile.boosts_since
        if (boosts_since is not None):
            text.append(f'Booster since: {boosts_since:{DATETIME_FORMAT_CODE}} [*{elapsed_time(boosts_since)}*]')
        
        text.append(f'Roles: {roles}')
        embed.add_field('In guild profile', '\n'.join(text))
    
    return embed


@SLASH_CLIENT.interactions(name='role', is_global=True)
async def role_(client, event,
    role: ('role', 'Select the role to show information of.'),
):
    """Shows the information about a role."""
    if role.partial:
        abort('I must be in the guild, where the role is.')
    
    embed = Embed(f'Role information for: {role.name}', color=role.color)
    embed.add_field('Position', str(role.position), inline=True)
    embed.add_field('Id', str(role.id), inline=True)
    
    embed.add_field('Separated', 'true' if role.separated else 'false', inline=True)
    embed.add_field('Mentionable', 'true' if role.mentionable else 'false', inline=True)
    
    manager_type = role.manager_type
    if manager_type is RoleManagerType.none:
        managed_description = 'false'
    else:
        if manager_type is RoleManagerType.unset:
            await client.sync_roles(role.guild)
            manager_type = role.manager_type
        
        if manager_type is RoleManagerType.bot:
            managed_description = f'Special role for bot: {role.manager:f}'
        elif manager_type is RoleManagerType.booster:
            managed_description = 'Role for the boosters of the guild.'
        elif manager_type is RoleManagerType.integration:
            managed_description = f'Special role for integration: {role.manager.name}'
        elif manager_type is RoleManagerType.unknown:
            managed_description = 'Some new things.. Never heard of them.'
        else:
            managed_description = 'I have no clue.'
    
    embed.add_field('Managed', managed_description, inline=True)
    
    color = role.color
    embed.add_field('color',
        (
            f'html: {color.as_html}\n'
            f'rgb: {color.as_rgb}\n'
            f'int: {color:d}'
        ),
        inline = True,
    )
    
    created_at = role.created_at
    embed.add_field(
        'Created at',
        (
            f'{created_at:{DATETIME_FORMAT_CODE}}\n'
            f'{elapsed_time(created_at)} ago'
        ),
        inline = True,
    )
    
    return embed


async def add_guild_generic_field(client, guild, embed, even_if_empty):
    await add_guild_info_field(client, guild, embed, False)
    await add_guild_counts_field(client, guild, embed, False)
    await add_guild_emojis_field(client, guild, embed, False)
    await add_guild_stickers_field(client, guild, embed, False)

async def add_guild_info_field(client, guild, embed, even_if_empty):
    created_at = guild.created_at
    sections_parts = [
        '**Created**: ', created_at.__format__(DATETIME_FORMAT_CODE), ' [*', elapsed_time(created_at), ' ago*]\n'
        '**Voice region**: ', guild.region.name,
    ]
    
    features = guild.features
    if features:
        sections_parts.append('\n**Features**: ')
        for feature in features:
            sections_parts.append(feature.name)
            sections_parts.append(', ')
        
        del sections_parts[-1]
    
    embed.add_field('Guild information', ''.join(sections_parts))

async def add_guild_counts_field(client, guild, embed, even_if_empty):
    approximate_user_count = guild.approximate_user_count
    if approximate_user_count == 0:
        await client.guild_get(guild)
        approximate_user_count = guild.approximate_user_count
    
    channel_text = 0
    channel_announcements = 0
    channel_category = 0
    channel_voice = 0
    channel_thread = 0
    channel_store = 0
    channel_directory = 0
    
    for channel in guild.channels.values():
        channel_type = channel.__class__
        if channel_type is ChannelText:
            channel_text +=1
            if channel.type == 5:
                channel_announcements += 1
            continue
        
        if channel_type is ChannelCategory:
            channel_category += 1
            continue
        
        if channel_type is ChannelVoice:
            channel_voice += 1
            continue
        
        if channel_type is ChannelThread:
            channel_thread += 1
            continue
        
        if channel_type is ChannelStore:
            channel_store += 1
            continue
        
        if channel_type is ChannelDirectory:
            channel_directory += 1
            continue
    
    sections_parts = [
        '**Users: ', str(approximate_user_count), '**\n'
        '**Roles: ', str(len(guild.roles)), '**'
    ]
    
    if channel_text:
        sections_parts.append('\n**Text channels: ')
        sections_parts.append(str(channel_text))
        sections_parts.append('**')
        
        if channel_announcements:
            sections_parts.append(' [')
            sections_parts.append(str(channel_announcements))
            sections_parts.append(' Announcements]')
    
    if channel_voice:
        sections_parts.append('\n**Voice channels: ')
        sections_parts.append(str(channel_voice))
        sections_parts.append('**')
    
    if channel_category:
        sections_parts.append('\n**Category channels: ')
        sections_parts.append(str(channel_category))
        sections_parts.append('**')
    
    if channel_thread:
        sections_parts.append('\n**Thread channels: ')
        sections_parts.append(str(channel_thread))
        sections_parts.append('**')
    
    if channel_store:
        sections_parts.append('\n**Store channels: ')
        sections_parts.append(str(channel_store))
        sections_parts.append('**')
    
    if channel_directory:
        sections_parts.append('\n**Directory channels: ')
        sections_parts.append(str(channel_directory))
        sections_parts.append('**')
    
    embed.add_field('Counts', ''.join(sections_parts))


async def add_guild_emojis_field(client, guild, embed, even_if_empty):
    emoji_count = len(guild.emojis)
    if emoji_count:
        sections_parts = [
            '**Total: ', str(emoji_count), '**\n'
            '**Static emojis: '
        ]
        
        normal_static, normal_animated, managed_static, managed_animated = guild.emoji_counts
        emoji_limit = guild.emoji_limit
        sections_parts.append(str(normal_static))
        sections_parts.append('** [')
        sections_parts.append(str(emoji_limit - normal_static))
        sections_parts.append(
            ' free]\n'
            '**Animated emojis: '
        )
        sections_parts.append(str(normal_animated))
        sections_parts.append('** [')
        sections_parts.append(str(emoji_limit - normal_animated))
        sections_parts.append(' free]')
        
        managed_total = managed_static + managed_animated
        if managed_total:
            sections_parts.append('\n**Managed: ')
            sections_parts.append(str(managed_total))
            sections_parts.append('** [')
            sections_parts.append(str(managed_static))
            sections_parts.append(' static, ')
            sections_parts.append(str(managed_animated))
            sections_parts.append(' animated]')
        
        embed.add_field('Emojis', ''.join(sections_parts))
    
    elif even_if_empty:
        embed.add_field('Emojis', '*The guild has no emojis*')

async def add_guild_stickers_field(client, guild, embed, even_if_empty):
    sticker_count = len(guild.stickers)
    if sticker_count:
        sections_parts = [
            '**Total: ', str(sticker_count), '** [', str(guild.sticker_limit - sticker_count), ' free]\n'
            '**Static stickers: '
        ]
        
        static_count, animated_count, lottie_count = guild.sticker_count
        
        sections_parts.append(str(static_count))
        sections_parts.append(
            '**\n'
            '**Animated stickers: '
        )
        sections_parts.append(str(animated_count))
        sections_parts.append('**')
        
        if lottie_count:
            sections_parts.append('\n**Lottie stickers:')
            sections_parts.append(str(lottie_count))
            sections_parts.append('**')

        embed.add_field('Stickers', ''.join(sections_parts))
    
    elif even_if_empty:
        embed.add_field('Stickers', '*The guild has no stickers*')


async def add_guild_boosters_field(client, guild, embed, even_if_empty):
    boosters = guild.boosters
    if boosters:
        count = len(boosters)
        to_render = count if count < 21 else 21
        
        embed.add_field(f'Most awesome people of the guild',
            f'{to_render} {EMOJI_HEART_GIFT:e} out of {count} {EMOJI_HEART_GIFT:e}')
        
        for user in boosters[:21]:
            embed.add_field(user.full_name,
                f'since: {elapsed_time(user.get_guild_profile_for(guild).boosts_since)}')
    
    elif even_if_empty:
        embed.add_field(f'Most awesome people of the guild', '*The guild has no chicken nuggets.*')

DEFAULT_GUILD_FILED = 'generic'

GUILD_FIELDS = {
    DEFAULT_GUILD_FILED : add_guild_generic_field  ,
    'info'              : add_guild_info_field     ,
    'counts'            : add_guild_counts_field   ,
    'emojis'            : add_guild_emojis_field   ,
    'stickers'          : add_guild_stickers_field ,
    'boosters'          : add_guild_boosters_field ,
}

@SLASH_CLIENT.interactions(name='guild', is_global=True)
async def guild_(client, event,
    field: (list(GUILD_FIELDS.keys()), 'Which fields should I show?') = DEFAULT_GUILD_FILED,
):
    """Shows some information about the guild."""
    guild = event.guild
    if guild.partial:
        abort('I must be in the guild to execute this command.')
    
    embed = Embed(
        guild.name,
        color = (guild.icon_hash & 0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id >> 22) & 0xFFFFFF),
    ).add_thumbnail(
        guild.icon_url_as(size=128),
    )
    
    await GUILD_FIELDS[field](client, guild, embed, True)
    
    return embed


USER_PER_PAGE = 16
class InRolePageGetter:
    __slots__ = ('users', 'guild', 'title')
    def __init__(self, users, guild, roles):
        title_parts = ['Users with roles: ']
        
        roles = sorted(roles)
        index = 0
        limit = len(roles)
        
        while True:
            role = roles[index]
            index += 1
            role_name = role.name
            
            # Handle special case, when the role is an application's role, what means it's length can be over 32-
            if len(role_name) > 32:
                role_name = role_name[:32]+'...'
            
            title_parts.append(role_name)
            
            if index == limit:
                break
            
            title_parts.append(', ')
            
        self.title = ''.join(title_parts)
        self.users = users
        self.guild = guild
    
    def __len__(self):
        length = len(self.users)
        if length:
            length = ceil(length / USER_PER_PAGE)
        else:
            length = 1
        
        return length
    
    def __getitem__(self, index):
        users = self.users
        length = len(users)
        guild = self.guild
        if length:
            user_index = index * USER_PER_PAGE
            user_limit = user_index + USER_PER_PAGE
            
            if user_limit > length:
                user_limit = length
            
            description_parts = []
            while True:
                user = users[user_index]
                user_index += 1
                description_parts.append(user.full_name)
                guild_profile = user.get_guild_profile_for(guild)
                if (guild_profile is not None):
                    nick = guild_profile.nick
                    if nick is not None:
                        description_parts.append(' *[')
                        description_parts.append(nick)
                        description_parts.append(']*')
                
                if user_index == user_limit:
                    break
                
                description_parts.append('\n')
                continue
            
            description = ''.join(description_parts)
        
        else:
            description = '*none*'
        
        return Embed(
            self.title,
            description,
        ).add_author(
            guild.icon_url,
            guild.name,
        ).add_footer(
            f'Page {index + 1}/{ceil(len(self.users) / USER_PER_PAGE)}',
        )


def in_role_pagination_check(user, event):
    event_user = event.user
    if user is event.user:
        return True
    
    if event.message.channel.permissions_for(event_user).can_manage_messages:
        return True
    
    return False

@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT)
async def in_role(client, event,
    role_1: ('role', 'Select a role.'),
    role_2: ('role', 'Double role!') = None,
    role_3: ('role', 'Triple role!') = None,
    role_4: ('role', 'Quadra role!') = None,
    role_5: ('role', 'Penta role!') = None,
    role_6: ('role', 'Epic!') = None,
    role_7: ('role', 'Legendary!') = None,
    role_8: ('role', 'Mythical!') = None,
    role_9: ('role', 'Lunatic!') = None,
):
    """Shows the users with the given roles."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    roles = set()
    for role in role_1, role_2, role_3, role_4, role_5, role_6, role_7, role_8, role_9:
        if role is None:
            continue
        
        if role.guild is guild:
            roles.add(role)
            continue
        
        abort(f'Role {role.name}, [{role.id}] is bound to an other guild.')
    
    users = []
    for user in guild.users.values():
        guild_profile = user.get_guild_profile_for(guild)
        if guild_profile is None:
            continue
        
        guild_profile_roles = guild_profile.roles
        if guild_profile_roles is None:
            continue
        
        if not roles.issubset(guild_profile_roles):
            continue
        
        users.append(user)
    
    pages = InRolePageGetter(users, guild, roles)
    
    await Pagination(client, event, pages, check=partial_func(in_role_pagination_check, event.user))


@SLASH_CLIENT.interactions(is_global=True)
async def avatar(client, event,
    user : ('user', 'Choose a user!') = None,
):
    """Shows your or the chosen user's avatar."""
    if user is None:
        user = event.user
    
    if user.avatar:
        color = user.avatar_hash & 0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    return Embed(f'{user:f}\'s avatar', color=color, url=url).add_image(url)


@SLASH_CLIENT.interactions(is_global=True, target='user')
async def status_(user):
    status = user.status
    emoji = STATUS_VALUE_TO_HEART_EMOJI.get(status.value, EMOJI_HEART_BLACK)
    
    embed = Embed(f'{user.full_name}\'s status', f'{emoji:e} {status.name}').add_thumbnail(user.avatar_url)
    
    statuses = user.statuses
    if (statuses is not None) and statuses:
        field_value_parts = []
        
        for platform in PLATFORMS:
            status_value = statuses.get(platform, STATUS_VALUE_OFFLINE)
            emoji = STATUS_VALUE_TO_HEART_EMOJI.get(status_value, EMOJI_HEART_BLACK)
            
            if field_value_parts:
                field_value_parts.append('\n')
            
            field_value_parts.append(platform)
            field_value_parts.append(': ')
            field_value_parts.append(emoji.as_emoji)
            field_value_parts.append(' ')
            field_value_parts.append(status_value)
        
        field_value = ''.join(field_value_parts)
        
        embed.add_field('Per platform', field_value)
    
    
    return embed


@SLASH_CLIENT.interactions(is_global=True)
async def show_emoji(client, event,
    emoji: ('str', 'Yes?'),
):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji)
    if emoji is None:
        return 'That\'s not an emoji.'
    
    if emoji.is_unicode_emoji():
        return 'That\' an unicode emoji, cannot link it.'
    
    return f'**Name:** {emoji:e} **Link:** {emoji.url}'


@SLASH_CLIENT.interactions(name='id-to-time', is_global=True)
async def id_to_datetime_(client, event,
    snowflake: ('int', 'Id please!'),
):
    """Converts the given Discord snowflake to time."""
    time = id_to_datetime(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'



GUILD_ICON_CUSTOM_ID_ICON = 'guild_icon.icon'
GUILD_ICON_CUSTOM_ID_BANNER = 'guild_icon.banner'
GUILD_ICON_CUSTOM_ID_DISCOVERY_SPLASH = 'guild_icon.discovery_splash'
GUILD_ICON_CUSTOM_ID_INVITE_SPLASH = 'guild_icon.invite_splash'


BUTTON_ICON = Button('Icon', custom_id=GUILD_ICON_CUSTOM_ID_ICON)
BUTTON_BANNER = Button('Banner', custom_id=GUILD_ICON_CUSTOM_ID_BANNER)
BUTTON_DISCOVERY_SPLASH = Button('Discovery splash', custom_id=GUILD_ICON_CUSTOM_ID_DISCOVERY_SPLASH)
BUTTON_INVITE_SPLASH = Button('Invite splash', custom_id=GUILD_ICON_CUSTOM_ID_INVITE_SPLASH)


GUILD_ICON_ICON_COMPONENTS = Row(
    BUTTON_ICON.copy_with(enabled=False),
    BUTTON_BANNER,
    BUTTON_DISCOVERY_SPLASH,
    BUTTON_INVITE_SPLASH,
)

GUILD_ICON_BANNER_COMPONENTS = Row(
    BUTTON_ICON,
    BUTTON_BANNER.copy_with(enabled=False),
    BUTTON_DISCOVERY_SPLASH,
    BUTTON_INVITE_SPLASH,
)

GUILD_ICON_DISCOVERY_SPLASH_COMPONENTS = Row(
    BUTTON_ICON,
    BUTTON_BANNER,
    BUTTON_DISCOVERY_SPLASH.copy_with(enabled=False),
    BUTTON_INVITE_SPLASH,
)

GUILD_ICON_INVITE_SPLASH_COMPONENTS = Row(
    BUTTON_ICON,
    BUTTON_BANNER,
    BUTTON_DISCOVERY_SPLASH,
    BUTTON_INVITE_SPLASH.copy_with(enabled=False),
)


def create_embed(guild, name, url, hash_value):
    if url is None:
        color = (guild.id >> 22) & 0xFFFFFF
        embed = Embed(f'{guild.name} has no {name}', color=color)
    else:
        color = hash_value & 0xFFFFFF
        embed = Embed(f'{guild.name}\'s {name}', color=color, url=url).add_image(url)
    
    return embed


GUILD_ICON_CHOICES = [
    ('Icon'             , 'icon'             ),
    ('Banner'           , 'banner'           ),
    ('Discovery-splash' , 'discovery_splash' ),
    ('Invite-splash'    , 'invite_splash'    ),
]

@SLASH_CLIENT.interactions(is_global=True)
async def guild_icon(event,
        choice: (GUILD_ICON_CHOICES, 'Which icon of the guild?' ) = 'icon',
            ):
    """Shows the guild's icon."""
    guild = event.guild
    if (guild is None) or guild.partial:
        abort('The command unavailable in guilds, where the application\'s bot is not in.')
    
    if choice == 'icon':
        name = 'icon'
        url = guild.icon_url_as(size=4096)
        hash_value = guild.icon_hash
        components = GUILD_ICON_ICON_COMPONENTS
    
    elif choice == 'banner':
        name = 'banner'
        url = guild.banner_url_as(size=4096)
        hash_value = guild.banner_hash
        components = GUILD_ICON_BANNER_COMPONENTS
    
    elif choice == 'discovery_splash':
        name = 'discovery splash'
        url = guild.discovery_splash_url_as(size=4096)
        hash_value = guild.discovery_splash_hash
        components = GUILD_ICON_ICON_COMPONENTS
    
    else:
        name = 'invite splash'
        url = guild.invite_splash_url_as(size=4096)
        hash_value = guild.invite_splash_hash
        components = GUILD_ICON_DISCOVERY_SPLASH_COMPONENTS
    
    embed = create_embed(guild, name, url, hash_value)
    return InteractionResponse(embed=embed, components=components)


@SLASH_CLIENT.interactions(custom_id=GUILD_ICON_CUSTOM_ID_ICON)
async def handle_guild_icon(event):
    guild = event.guild
    if (guild is not None):
        embed = create_embed(guild, 'icon', guild.icon_url_as(size=4096), guild.icon_hash)
        return InteractionResponse(embed=embed, components=GUILD_ICON_ICON_COMPONENTS)


@SLASH_CLIENT.interactions(custom_id=GUILD_ICON_CUSTOM_ID_BANNER)
async def handle_guild_banner(event):
    guild = event.guild
    if (guild is not None):
        embed = create_embed(guild, 'banner', guild.banner_url_as(size=4096), guild.banner_hash)
        return InteractionResponse(embed=embed, components=GUILD_ICON_BANNER_COMPONENTS)


@SLASH_CLIENT.interactions(custom_id=GUILD_ICON_CUSTOM_ID_DISCOVERY_SPLASH)
async def handle_guild_discovery_splash(event):
    guild = event.guild
    if (guild is not None):
        embed = create_embed(guild, 'discovery splash', guild.discovery_splash_url_as(size=4096),
            guild.discovery_splash_hash)
        return InteractionResponse(embed=embed, components=GUILD_ICON_DISCOVERY_SPLASH_COMPONENTS)
    

@SLASH_CLIENT.interactions(custom_id=GUILD_ICON_CUSTOM_ID_INVITE_SPLASH)
async def handle_guild_invite_splash(event):
    guild = event.guild
    if (guild is not None):
        embed = create_embed(guild, 'invite splash', guild.invite_splash_url_as(size=4096), guild.invite_splash_hash)
        return InteractionResponse(embed=embed, components=GUILD_ICON_INVITE_SPLASH_COMPONENTS)


def add_user_field(embed, index, joined_at, user):
    created_at = user.created_at
    embed.add_field(
        f'{index}. {user.full_name}',
        (
            f'Id: {user.id}\n'
            f'Mention: {user.mention}\n'
            '\n'
            f'Joined : {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]\n'
            f'Created : {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
            f'Difference : {elapsed_time(relativedelta(created_at, joined_at))}'
        ),
    )

@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__MODERATOR, True)
async def latest_users(client, event):
    """Shows the new users of the guild."""
    if not event.user.has_role(ROLE__SUPPORT__MODERATOR):
        abort('Hacker trying to hack Discord.')
    
    date_limit = datetime.now() - timedelta(days=7)
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        # Use created at and not `joined_at`, we can ignore lurkers.
        created_at = user.get_guild_profile_for(guild).created_at
        if created_at > date_limit:
            users.append((created_at, user))
    
    users.sort(reverse=True)
    del users[10:]
    
    embed = Embed('Recently joined users')
    if users:
        for index, (joined_at, user) in enumerate(users, 1):
            add_user_field(embed, index, joined_at, user)
    
    else:
        embed.description = '*none*'
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__MODERATOR, True)
async def all_users(client, event,):
    """Shows the new users of the guild."""
    if not event.user.has_role(ROLE__SUPPORT__MODERATOR):
        abort('Hacker trying to hack Discord.')
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        joined_at = user.get_guild_profile_for(guild).joined_at
        if (joined_at is not None):
            users.append((joined_at, user))
    
    users.sort(reverse=True)
    
    embeds = []
    
    for index, (joined_at, user) in enumerate(users, 1):
        if index % 10 == 1:
            embed = Embed('Joined users')
            embeds.append(embed)
        
        add_user_field(embed, index, joined_at, user)
    
    
    await Pagination(client, event, embeds)


def build_sticker_embed(sticker):

    sticker_url = sticker.url_as(size=4096)
    
    description_parts = []
    
    sticker_description = sticker.description
    if (sticker_description is not None):
        description_parts.append(sticker_description)
        description_parts.append('\n\n')
    
    
    tags = sticker.tags
    if (tags is not None):
        description_parts.append('**Tags:**: ')
        description_parts.append(', '.join(sorted(tags)))
        description_parts.append('\n')
    
    
    description_parts.append('**Id**: ')
    description_parts.append(str(sticker.id))
    description_parts.append('\n')
    
    created_at = sticker.created_at
    description_parts.append('**Created at:** ')
    description_parts.append(created_at.__format__(DATETIME_FORMAT_CODE))
    description_parts.append(' *[')
    description_parts.append(elapsed_time(created_at))
    description_parts.append(']*\n')
    
    
    sticker_type = sticker.type
    description_parts.append('**Type:** ')
    description_parts.append(sticker_type.name)
    description_parts.append(' (')
    description_parts.append(str(sticker_type.value))
    description_parts.append(')\n')
    
    
    sticker_format = sticker.format
    description_parts.append('**Format:** ')
    description_parts.append(sticker_format.name)
    description_parts.append(' (')
    description_parts.append(str(sticker_format.value))
    description_parts.append(')')
    
    
    sort_value = sticker.sort_value
    if sort_value:
        description_parts.append('\n**Sort value:** ')
        description_parts.append(str(sort_value))
    
    
    user = sticker.user
    if (user is not ZEROUSER):
        description_parts.append('\n**Creator:** ')
        description_parts.append(user.full_name)
        description_parts.append(' (')
        description_parts.append(str(user.id))
        description_parts.append(')')
    
    
    guild_id = sticker.guild_id
    if guild_id:
        description_parts.append('\n**Guild id:** ')
        description_parts.append(str(guild_id))
    
    
    pack_id = sticker.pack_id
    if pack_id:
        description_parts.append('\n**pack id:** ')
        description_parts.append(str(pack_id))
    
    
    description = ''.join(description_parts)
    
    embed = Embed(sticker.name, description, url=sticker_url)
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker_url)
    
    return embed


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def sticker_(client, message):
    """Shows up the message's sticker."""
    sticker = message.sticker
    if sticker is None:
        abort('The message has no sticker.')
    
    try:
        await client.sticker_get(sticker)
    except BaseException as err:
        if isinstance(err, ConnectionError):
            return
        
        if isinstance(err, DiscordException):
            if err.code == ERROR_CODES.unknown_sticker:
                abort(f'Sticker: {sticker.id} is already deleted.')
        
        raise
    
    return build_sticker_embed(sticker)


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def escape(message):
    content = message.content
    if content is None:
        abort('The message has no content to escape')
    
    content = escape_markdown(content)
    if len(content) > 2000:
        content = content[:1997]+'...'
    
    return InteractionResponse(content, allowed_mentions=None)


@SLASH_CLIENT.interactions(is_global=True)
async def calc(
    expression: ('expression', 'Mathematical expression to evaluate')
):
    return repr(expression)


@SLASH_CLIENT.interactions(is_global=True)
async def choose(
    choice_1: (str, 'choice'),
    choice_2: (str, 'another one') = None,
    choice_3: (str, 'another one') = None,
    choice_4: (str, 'another one') = None,
    choice_5: (str, 'another one') = None,
    choice_6: (str, 'another one') = None,
    choice_7: (str, 'another one') = None,
    choice_8: (str, 'another one') = None,
    choice_9: (str, 'another one') = None,
    choice_10: (str, 'another one') = None,
    choice_11: (str, 'another one') = None,
    choice_12: (str, 'another one') = None,
    choice_13: (str, 'another one') = None,
    choice_14: (str, 'another one') = None,
    choice_15: (str, 'another one') = None,
    choice_16: (str, 'another one') = None,
    choice_17: (str, 'another one') = None,
    choice_18: (str, 'another one') = None,
    choice_19: (str, 'another one') = None,
    choice_20: (str, 'another one') = None,
    choice_21: (str, 'another one') = None,
    choice_22: (str, 'another one') = None,
    choice_23: (str, 'another one') = None,
    choice_24: (str, 'another one') = None,
    choice_25: (str, 'another one') = None,
):
    return InteractionResponse(
        choice([
            choice_ for choice_ in (
                choice_1, choice_2, choice_3, choice_4, choice_5,
                choice_6, choice_7, choice_8, choice_9, choice_10,
                choice_11, choice_12, choice_13, choice_14, choice_15,
                choice_16, choice_17, choice_18, choice_19, choice_20,
                choice_21, choice_22, choice_23, choice_24, choice_25,
            ) if choice_ is not None
        ]),
        allowed_mentions = None,
    )


CREATE_EMBEDDED_ACTIVITY_PERMISSIONS = Permission().update_by_keys(
    start_embedded_activities = True,
    create_instant_invite = True,
)

@SLASH_CLIENT.interactions(is_global=True)
async def create_activity(
    client,
    event,
    activity: (EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID, 'Select an activity'),
    channel: ('channel_guild_voice', 'The channel to create the activity for.') = None,
):
    """Creates an embedded activity."""
    if event.user_permissions & CREATE_EMBEDDED_ACTIVITY_PERMISSIONS != CREATE_EMBEDDED_ACTIVITY_PERMISSIONS:
        abort(
            'You need to have `create instant invite` and `create embedded activities` permission to invoke this '
            'command'
        )
    
    # Use goto to detect channel.
    while True:
        if channel is not None:
            break
        
        guild = event.guild
        if (guild is not None):
            try:
                voice_state = guild.voice_states[event.user.id]
            except KeyError:
                pass
            else:
                channel = voice_state.channel
                if channel.type == CHANNEL_TYPES.guild_voice:
                    break
        
        abort('Please give a voice channel or be in one.')
    
    client_permissions = channel.cached_permissions_for(client)
    if client_permissions & CREATE_EMBEDDED_ACTIVITY_PERMISSIONS != CREATE_EMBEDDED_ACTIVITY_PERMISSIONS:
        abort(
            f'I need to have `create instant invite` and `create embedded activities` permission in '
            f'{channel.mention} to execute this command.'
        )
    
    invite = await client.application_invite_create(channel, activity, max_age=21600) # 6 hours
    return invite.url
