# -*- coding: utf-8 -*-
import json
from math import ceil
from time import perf_counter
from functools import partial as partial_func
from colorsys import rgb_to_hsv, rgb_to_yiq
from datetime import datetime, timedelta


from hata import Color, Embed, Client, WaitTillExc, ReuBytesIO, DiscordException, now_as_id, parse_emoji, \
    elapsed_time, Status, BUILTIN_EMOJIS, ChannelText, ChannelCategory, id_to_time, RoleManagerType, ERROR_CODES, \
    cchunkify, ICON_TYPE_NONE, KOKORO, ChannelVoice, ChannelStore, ChannelThread, DATETIME_FORMAT_CODE, parse_color, \
    parse_message_reference, MESSAGES, CHANNELS

from hata.ext.command_utils import Pagination
from hata.ext.prettyprint import pchunkify
from hata.ext.slash import abort, SlashResponse, set_permission

from PIL import Image as PIL
from dateutil.relativedelta import relativedelta

from bot_utils.tools import PAGINATION_5PN
from bot_utils.shared import ROLE__NEKO_DUNGEON__TESTER, GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__MODERATOR

UTILITY_COLOR = Color(0x5dc66f)

SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(is_global=True)
async def rawr(client, event):
    """Sends a message with everyone from my universe."""
    yield
    
    channel = event.channel
    tasks = []
    
    for client_ in channel.clients:
        if client_ is not client:
            if not channel.cached_permissions_for(client_).can_send_messages:
                continue
        task = KOKORO.create_task(client_.message_create(channel, 'Rawrr !'))
        tasks.append(task)
    
    try:
        await WaitTillExc(tasks, KOKORO)
    except:
        for task in tasks:
            task.cancel()
        raise


@SLASH_CLIENT.interactions(is_global=True)
async def color_(client, event,
        color: ('str', 'Beauty!')):
    """Shows the given color"""
    
    color = parse_color(color)
    if color is None:
        yield 'Could not recognize the color.'
        return
    
    yield
    
    embed = Embed(color=color)
    embed.add_field('hex', f'#{color:06X}', inline=True)
    embed.add_field('rgb', f'{color>>16} r\n{(color>>8)&255} g\n{color&255} b', inline=True)
    r, g, b = color.as_rgb_float_tuple
    embed.add_field('rgb%', f'{r*100.0:0.2f}% r\n{g*100.0:0.2f}% g\n{b*100.0:0.2f}% b', inline=True)
    h, s, v = rgb_to_hsv(r, g, b)
    embed.add_field('hsv%', f'{h*100.0:0.2f}% h\n{s*100.0:0.2f}% s\n{v*100.0:0.2f}% v', inline=True)
    y, i, q = rgb_to_yiq(r, g, b)
    embed.add_field('yiq%', f'{y*100.0:0.2f}% y\n{i*100.0:0.2f}% i\n{q*100.0:0.2f}% q', inline=True)
    
    embed.add_image('attachment://color.png')
    
    with ReuBytesIO() as buffer:
        image = PIL.new('RGB', (240, 30), color.as_rgb)
        image.save(buffer,'png')
        buffer.seek(0)
        
        await client.interaction_followup_message_create(event, embed=embed, file=('color.png', buffer))


# We don't need it rn.
"""
def add_activity(text, activity):
    
    text.append(activity.name)
    text.append('\n')
    
    activity_type = activity.type
    text.append(f'**>>** type : {("game", "stream", "spotify", "watching", "custom", "competing")[activity_type]} ({activity_type})\n')
    if activity_type == ActivityTypes.custom:
        return
    
    timestamps = activity.timestamps
    if (timestamps is not None):
        start = activity.start
        if (start is not None):
            text.append(f'**>>** started : {elapsed_time(start)} ago\n')
        
        end = activity.end
        if (end is not None):
            text.append(f'**>>** ends after : {elapsed_time(end)}\n')
    
    details = activity.details
    if (details is not None):
        text.append(f'**>>** details : {details}\n')
    
    state = activity.state
    if (state is not None):
        text.append(f'**>>** state : {state}\n')
    
    party = activity.party
    if (party is not None):
        id_ = activity.id
        if (id_ is not None):
            text.append(f'**>>** party id : {id_}\n')
        
        size = party.size
        max_ = party.max
        if size or max_:
            if size:
                text.append(f'**>>** party size : {size}\n')
            
            if max_:
                text.append(f'**>>** party max : {max_}\n')
    
    assets = activity.assets
    if (assets is not None):
        image_large_url = activity.image_large_url
        if (image_large_url is not None):
            text.append(f'**>>** asset image large url : {image_large_url}\n')
        
        text_large = assets.text_large
        if (text_large is not None):
            text.append(f'**>>** asset text large : {text_large}\n')
        
        image_small_url = activity.image_small_url
        if (image_small_url is not None):
            text.append(f'**>>** asset image small url : {image_small_url}\n')
        
        text_small = assets.text_small
        if text_small:
            text.append(f'**>>** asset text small : {text_small}\n')
    
    album_cover_url = activity.album_cover_url
    if album_cover_url is not None:
        text.append(f'**>>** album cover : {album_cover_url}\n')
    
    secrets = activity.secrets
    if (secrets is not None):
        join = secrets.secret
        if (join is not None):
            text.append(f'**>>** secret join : {join}\n')
        
        spectate = secrets.spectate
        if (spectate is not None):
            text.append(f'**>>** secret spectate : {spectate}\n')
        
        match = secrets.match
        if (match is not None):
            text.append(f'**>>** secret match : {match}\n')
    
    url = activity.url
    if (url is not None):
        text.append(f'**>>** url : {url}\n')
    
    sync_id = activity.sync_id
    if (sync_id is not None):
        text.append(f'**>>** sync id : {sync_id}\n')
    
    session_id = activity.session_id
    if (session_id is not None):
        text.append(f'**>>** session id : {session_id}\n')
    
    flags = activity.flags
    if flags:
        text.append(f'**>>** flags : {activity.flags} ({", ".join(list(flags))})\n')
    
    application_id = activity.application_id
    if activity.application_id:
        text.append(f'**>>** application id : {application_id}\n')
    
    created_at = activity.created_at
    if created_at > DISCORD_EPOCH_START:
        text.append(f'**>>** created at : {elapsed_time(created_at)} ago\n')
    
    id_ = activity.id
    if id_:
        text.append(f'**>>** id : {id_}\n')
"""

def message_pagination_check(user, event):
    event_user = event.user
    if user is event.user:
        return True
    
    if event.message.channel.permissions_for(event_user).can_manage_messages:
        return True
    
    return False

@SLASH_CLIENT.interactions(is_global=True)
async def message_(client, event,
        message : ('str', 'Link to the message'),
        raw : ('bool', 'Should display json?') = True,
            ):
    """Shows up the message's payload. (You must have Tester role in ND)"""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__TESTER):
        yield Embed('Ohoho', f'You must have {ROLE__NEKO_DUNGEON__TESTER.mention} to invoke this command.',
            color=UTILITY_COLOR)
        return
    
    if not event.channel.cached_permissions_for(client).can_send_messages:
        yield Embed('Permission denied', 'I need `send messages` permission to execute this command.',
            color=UTILITY_COLOR)
        return
    
    message_reference = parse_message_reference(message)
    if message_reference is None:
        yield Embed('Error', 'Could not identify the message.', color=UTILITY_COLOR)
        return
    
    guild_id, channel_id, message_id = message_reference
    try:
        message = MESSAGES[message_id]
    except KeyError:
        if channel_id:
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                yield Embed('Ohoho', 'I have no access to the channel.', color=UTILITY_COLOR)
                return
        else:
            channel = event.channel
        
        if not channel.cached_permissions_for(client).can_read_message_history:
            yield Embed('Ohoho', 'I have no permission to get that message.', color=UTILITY_COLOR)
            return
        
        # We only really need `channel_id` and `guild_id`, so we can ignore `guild_id`.
        
        if raw:
            getter_coroutine = client.http.message_get(channel.id, message_id)
        else:
            getter_coroutine = client.message_get(channel, message_id)
    else:
        if raw:
            getter_coroutine = client.http.message_get(message.channel.id, message_id)
        else:
            getter_coroutine = None
    
    if (getter_coroutine is not None):
        yield
        
        try:
            response = await getter_coroutine
            if raw:
                data = response
            else:
                message = response
        except ConnectionError:
            # No internet
            return
        except DiscordException as err:
            if err.code in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.unknown_message, # channel deleted
                        ):
                # The message is already deleted.
                yield Embed('OOf', 'The referenced message is already yeeted.', color=UTILITY_COLOR)
                return
            
            if err.code == ERROR_CODES.missing_access: # client removed
                # This is not nice.
                return
            
            if err.code == ERROR_CODES.missing_permissions: # permissions changed meanwhile
                yield Embed('Ohoho', 'I have no permission to get that message.', color=UTILITY_COLOR)
                return
            
            raise
    
    if raw:
        chunks = cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
    else:
        chunks = pchunkify(message)
    
    pages = [Embed(description=chunk) for chunk in chunks]
    await Pagination(client, event, pages, check=partial_func(message_pagination_check, event.user))


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
        embed = Embed(f'Roles of **{guild.name}**:',
            '\n'.join([role.mention for role in self.roles]),
            color=(guild.icon_hash&0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id>>22)&0xFFFFFF))
        
        embed.add_footer(f'Page 1 / {len(self.roles)+1}')
        self.cache[0] = embed
    
    def __getitem__(self,index):
        page = self.cache.get(index, None)
        if page is None:
            page = self.create_page(index)
        
        return page

    def create_page(self,index):
        role = self.roles[index-1]
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
            color=role.color)
        embed.add_footer(f'Page {index+1} /  {len(self.roles)+1}')
        
        self.cache[index] = embed
        return embed
    
    def __len__(self):
        return len(self.roles)+1

@SLASH_CLIENT.interactions(is_global=True)
async def roles_(client, event):
    """Lists the roles of the guild for my cutie!"""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if guild not in client.guild_profiles:
        abort('I must be in the guild to execute this command')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_send_messages) or (not permissions.can_add_reactions):
        abort('I require `send messages` and `add reactions` permissions to execute this command.')
    
    await PAGINATION_5PN(client, event, RoleCache(guild))

@SLASH_CLIENT.interactions(is_global=True)
async def welcome_screen_(client, event):
    """Shows the guild's welcome screen."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if guild not in client.guild_profiles:
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
                f'#{welcome_channel.channel:d}'
                    )
    
    yield embed

ID = SLASH_CLIENT.interactions(None,
    name = 'id',
    description = 'Shows the id of the selected entity',
    is_global = True,
        )

@ID.interactions
async def user_(client, event,
        user : ('user', 'Who\'s id do you want to see?') = None,
           ):
    """Returns your or the selected user's identifier."""
    if user is None:
        user = event.user
    
    return str(user.id)


@ID.interactions
async def channel_(client, event,
        channel : ('channel', 'Which channel\'s id do you want to see?') = None,
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
        role : ('role', 'Which role\'s id do you want to see?') = None,
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
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_send_messages) or (not permissions.can_add_reactions):
        yield Embed('Permission denied',
            'I require `send messages` and `add reactions` permissions to execute this command.',
            color=UTILITY_COLOR,
                )
        return
    
    # Ack the event, hell yeah!
    yield
    
    pages = []
    lines = []
    lines_count = 0
    
    user = event.user
    for guild, guild_profile in user.guild_profiles.items():
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


@SLASH_CLIENT.interactions(name='user', is_global=True)
async def user_(client, event,
        user :('user', '*spy?*') = None,
            ):
    """Shows some information about your or about the selected user."""
    
    if user is None:
        user = event.user
    
    guild = event.guild
    
    embed = Embed(user.full_name)
    created_at = user.created_at
    embed.add_field('User Information',
        f'Created: {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
        f'Profile: {user:m}\n'
        f'ID: {user.id}')
    
    if guild is None:
        profile = None
    else:
        profile = user.guild_profiles.get(guild, None)
    
    if profile is None:
        if user.avatar_type is ICON_TYPE_NONE:
            color = user.default_avatar.color
        else:
            color = user.avatar_hash&0xFFFFFF
        embed.color = color
    
    else:
        embed.color = user.color_at(guild)
        roles = profile.roles
        if roles is None:
            roles = '*none*'
        else:
            roles.sort()
            roles = ', '.join(role.mention for role in reversed(roles))
        
        text = []
        if profile.nick is not None:
            text.append(f'Nick: {profile.nick}')
        
        if profile.joined_at is None:
            await client.guild_user_get(user.id)
        
        # Joined at can be `None` if the user is in lurking mode.
        joined_at = profile.joined_at
        if joined_at is not None:
            text.append(f'Joined: {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]')
        
        boosts_since = profile.boosts_since
        if (boosts_since is not None):
            text.append(f'Booster since: {boosts_since:{DATETIME_FORMAT_CODE}} [*{elapsed_time(boosts_since)}*]')
        
        text.append(f'Roles: {roles}')
        embed.add_field('In guild profile','\n'.join(text))
    
    embed.add_thumbnail(user.avatar_url_as(size=128))
    
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
        f'html: {color.as_html}\n'
        f'rgb: {color.as_rgb}\n'
        f'int: {color:d}',
            inline = True)
    
    created_at = role.created_at
    embed.add_field('Created at',
        f'{created_at:{DATETIME_FORMAT_CODE}}\n'
        f'{elapsed_time(created_at)} ago',
            inline=True)
    
    return embed


GREEN_HEART = BUILTIN_EMOJIS['green_heart']
YELLOW_HEART = BUILTIN_EMOJIS['yellow_heart']
RED_HEART = BUILTIN_EMOJIS['heart']
BLACK_HEART = BUILTIN_EMOJIS['black_heart']
GIFT_HEART = BUILTIN_EMOJIS['gift_heart']

def add_guild_all_field(guild, embed, even_if_empty):
    add_guild_info_field(guild, embed, False)
    add_guild_counts_field(guild, embed, False)
    add_guild_emojis_field(guild ,embed, False)
    add_guild_users_field(guild, embed, False)
    add_guild_boosters_field(guild, embed, False)


def add_guild_info_field(guild, embed, even_if_empty):
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

def add_guild_counts_field(guild, embed, even_if_empty):
    channel_text = 0
    channel_announcements = 0
    channel_category = 0
    channel_voice = 0
    channel_thread = 0
    channel_store = 0
    
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
    
    sections_parts = [
        '**Users: ', str(guild.user_count), '**\n'
        '**Roles: ', str(len(guild.role_list)), '**'
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
    
    embed.add_field('Counts', ''.join(sections_parts))

def add_guild_emojis_field(guild, embed, even_if_empty):
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
        sections_parts.append(str(emoji_limit-normal_static))
        sections_parts.append(' free]\n')
        sections_parts.append('**Animated emojis: ')
        sections_parts.append(str(normal_animated))
        sections_parts.append('** [')
        sections_parts.append(str(emoji_limit-normal_animated))
        sections_parts.append(' free]')
        
        managed_total = managed_static+managed_animated
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

def add_guild_users_field(guild, embed, even_if_empty):
    # most usual first
    s_grey = Status.offline
    s_green = Status.online
    s_yellow = Status.idle
    s_red = Status.dnd
    
    v_grey = 0
    v_green = 0
    v_yellow = 0
    v_red = 0

    for user in guild.users.values():
        status = user.status
        if   status is s_grey:
            v_grey += 1
        elif status is s_green:
            v_green += 1
        elif status is s_yellow:
            v_yellow += 1
        elif status is s_red:
            v_red += 1
        else:
            v_grey += 1
    
    del s_grey
    del s_green
    del s_yellow
    del s_red
    
    embed.add_field('Users',
        f'{GREEN_HEART:e} **{v_green}**\n'
        f'{YELLOW_HEART:e} **{v_yellow}**\n'
        f'{RED_HEART:e} **{v_red}**\n'
        f'{BLACK_HEART:e} **{v_grey}**')

def add_guild_boosters_field(guild, embed, even_if_empty):
    boosters = guild.boosters
    if boosters:
        count = len(boosters)
        to_render = count if count < 21 else 21
        
        embed.add_field(f'Most awesome people of the guild',
            f'{to_render} {GIFT_HEART:e} out of {count} {GIFT_HEART:e}')
        
        for user in boosters[:21]:
            embed.add_field(user.full_name,
                f'since: {elapsed_time(user.guild_profiles[guild].boosts_since)}')
    
    elif even_if_empty:
        embed.add_field(f'Most awesome people of the guild', '*The guild has no chicken nuggets.*')

GUILD_FIELDS = {
    'all'      : add_guild_all_field      ,
    'info'     : add_guild_info_field     ,
    'counts'   : add_guild_counts_field   ,
    'emojis'   : add_guild_emojis_field   ,
    'users'    : add_guild_users_field    ,
    'boosters' : add_guild_boosters_field ,
        }

@SLASH_CLIENT.interactions(name='guild', is_global=True)
async def guild_(client, event,
        field: ([(name, name) for name in GUILD_FIELDS], 'Which field of the info should I show?') = 'all',
            ):
    """Shows some information about the guild."""
    guild = event.guild
    if guild.partial:
        abort('I must be in the guild to execute this command.')
    
    embed = Embed(guild.name, color=(
        guild.icon_hash&0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id>>22)&0xFFFFFF)
            ).add_thumbnail(guild.icon_url_as(size=128))
    
    GUILD_FIELDS[field](guild, embed, True)
    
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
            length = ceil(length/USER_PER_PAGE)
        else:
            length = 1
        
        return length
    
    def __getitem__(self, index):
        users = self.users
        length = len(users)
        if length:
            user_index = index*USER_PER_PAGE
            user_limit = user_index+USER_PER_PAGE
            
            if user_limit > length:
                user_limit = length
            
            description_parts = []
            guild = self.guild
            while True:
                user = users[user_index]
                user_index += 1
                description_parts.append(user.full_name)
                try:
                    guild_profile = user.guild_profiles[guild]
                except KeyError:
                    pass
                else:
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
        
        return Embed(self.title, description). \
            add_author(guild.icon_url, guild.name). \
            add_footer(f'Page {index+1}/{ceil(len(self.users)/USER_PER_PAGE)}')


def in_role_pagination_check(user, event):
    event_user = event.user
    if user is event.user:
        return True
    
    if event.message.channel.permissions_for(event_user).can_manage_messages:
        return True
    
    return False

@SLASH_CLIENT.interactions(is_global=True)
async def in_role(client, event,
        role_1 : ('role', 'Select a role.'),
        role_2 : ('role', 'Double role!') = None,
        role_3 : ('role', 'Triple role!') = None,
        role_4 : ('role', 'Quadra role!') = None,
        role_5 : ('role', 'Penta role!') = None,
        role_6 : ('role', 'Epic!') = None,
        role_7 : ('role', 'Legendary!') = None,
        role_8 : ('role', 'Mythical!') = None,
        role_9 : ('role', 'Lunatic!') = None,
            ):
    """Shows the users with the given roles."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if guild not in client.guild_profiles:
        abort('I must be in the guild to do this.')
    
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
        try:
            guild_profile = user.guild_profiles[guild]
        except KeyError:
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
async def ping(client, event):
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@SLASH_CLIENT.interactions(is_global=True)
async def avatar(client, event,
        user : ('user', 'Choose a user!') = None,
            ):
    """Shows your or the chosen user's avatar."""
    if user is None:
        user = event.user
    
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    return Embed(f'{user:f}\'s avatar', color=color, url=url).add_image(url)


@SLASH_CLIENT.interactions(is_global=True)
async def show_emoji(client, event,
        emoji : ('str', 'Yes?'),
            ):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji)
    if emoji is None:
        return 'That\'s not an emoji.'
    
    if emoji.is_unicode_emoji():
        return 'That\' an unicode emoji, cannot link it.'
    
    return f'**Name:** {emoji:e} **Link:** {emoji.url}'


@SLASH_CLIENT.interactions(name='id-to-time', is_global=True)
async def id_to_time_(client, event,
        snowflake : ('int', 'Id please!'),
            ):
    """Converts the given Discord snowflake id to time."""
    time = id_to_time(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'


@SLASH_CLIENT.interactions(is_global=True)
async def guild_icon(client, event,
        choice: ({
            'Icon'             : 'icon'             ,
            'Banner'           : 'banner'           ,
            'Discovery-splash' : 'discovery_splash' ,
            'Invite-splash'    : 'invite_splash'    ,
                }, 'Which icon of the guild?' ) = 'icon',
            ):
    """Shows the guild's icon or it's selected splash."""
    guild = event.guild
    if (guild is None) or (guild not in client.guild_profiles):
        return Embed('Error', 'The command unavailable in guilds, where the application\'s bot is not in.')
    
    if choice == 'icon':
        name = 'icon'
        url = guild.icon_url_as(size=4096)
        hash_value = guild.icon_hash
    elif choice == 'banner':
        name = 'banner'
        url = guild.banner_url_as(size=4096)
        hash_value = guild.banner_hash
    elif choice == 'discovery_splash':
        name = 'discovery splash'
        url = guild.discovery_splash_url_as(size=4096)
        hash_value = guild.discovery_splash_hash
    else:
        name = 'invite splash'
        url = guild.invite_splash_url_as(size=4096)
        hash_value = guild.invite_splash_hash
    
    if url is None:
        color = (event.id>>22)&0xFFFFFF
        return Embed(f'{guild.name} has no {name}', color=color)
    
    color = hash_value&0xFFFFFF
    return Embed(f'{guild.name}\'s {name}', color=color, url=url).add_image(url)


def add_user_field(embed, index, joined_at, user):
    created_at = user.created_at
    embed.add_field(
        f'{index}. {user.full_name}',
        f'Id: {user.id}\n'
        f'Mention: {user.mention}\n'
        '\n'
        f'Joined : {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]\n'
        f'Created : {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
        f'Difference : {elapsed_time(relativedelta(created_at, joined_at))}',
            )

@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__MODERATOR, True)
async def latest_users(client, event,):
    """Shows the new users of the guild."""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__MODERATOR):
        abort('Hacker trying to hack Discord.')
    
    date_limit = datetime.now() - timedelta(days=7)
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        # Use created at and not `joined_at`, we can ignore lurkers.
        created_at = user.guild_profiles[guild].created_at
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
    
    return SlashResponse(embed=embed, allowed_mentions=None)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__MODERATOR, True)
async def all_users(client, event,):
    """Shows the new users of the guild."""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__MODERATOR):
        abort('Hacker trying to hack Discord.')
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        joined_at = user.guild_profiles[guild].joined_at
        if (joined_at is not None):
            users.append((joined_at, user))
    
    users.sort(reverse=True)
    
    embeds = []
    
    for index, (joined_at, user) in enumerate(users, 1):
        if index%10==1:
            embed = Embed('Joined users')
            embeds.append(embed)
        
        add_user_field(embed, index, joined_at, user)
    
    
    await Pagination(client, event, embeds)
