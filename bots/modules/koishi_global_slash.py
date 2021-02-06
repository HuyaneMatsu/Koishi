# -*- coding: utf-8 -*-
from time import perf_counter
from random import random
from math import ceil
from html import unescape as html_unescape

from hata import Client, Embed, parse_emoji, DATETIME_FORMAT_CODE, id_to_time, elapsed_time, parse_emoji, Status, \
    DiscordException, BUILTIN_EMOJIS, ERROR_CODES, ICON_TYPE_NONE, RoleManagerType, ChannelCategory, ChannelVoice, \
    ChannelText, ChannelStore, ChannelThread, Lock, KOKORO
from hata.ext.commands import wait_for_reaction, Pagination

from bot_utils.tools import Cell

Koishi : Client

COMMAND_LIMIT = 50
SWITCHABLE_COMMANDS = {}


@Koishi.interactions(is_global=True)
async def ping(client, event):
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@Koishi.interactions(is_global=True)
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


@Koishi.interactions(is_global=True)
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


@Koishi.interactions(name='id-to-time', is_global=True)
async def id_to_time_(client, event,
        snowflake : ('int', 'Id please!'),
            ):
    """Converts the given Discord snowflake id to time."""
    time = id_to_time(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'


@Koishi.interactions(is_global=True)
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
    if (guild is None) or guild.partial:
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


@Koishi.interactions(is_global=True)
async def roll(client, event,
        dice_count: ([(str(v), v) for v in range(1, 7)], 'With how much dice do you wanna roll?') = 1,
            ):
    """Rolls with dices."""
    amount = 0
    for _ in range(dice_count):
        amount += round(1.+(random()*5.))
    
    return str(amount)


@Koishi.interactions(is_global=True)
async def yeet(client, event,
        user :('user', 'Select the user to yeet!'),
        reason : ('str', 'Any reason why you would want to yeet?') = None,
        delete_message_days : ([(str(v), v) for v in range(8)], 'Delete previous messages?') = 0,
        notify_user : ('bool', 'Whether the user should get DM about the ban.') = True,
            ):
    """Yeets someone out of the guild. You must have ban users permission."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
    
    if not event.user_permissions.can_ban_users:
        yield Embed('Permission denied', 'You must have ban users permission to use this command.')
        return
    
    for maybe_banner in guild.clients:
        if guild.cached_permissions_for(maybe_banner).can_ban_users:
            banner = maybe_banner
            break
    else:
        yield Embed('Permission denied', f'{client.name_at(guild)} cannot yeet in the guild.')
        return
    
    if (reason is not None) and (not reason):
        reason = None
    
    yield
    
    if notify_user:
        if user.is_bot:
            notify_note = None
        else:
            try:
                channel = await client.channel_private_create(user)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return # We cannot help no internet
                
                raise
            
            embed = Embed('Yeeted', f'You were yeeted from {guild.name}.'). \
                add_field('Reason', '*No reason provided.*' if reason is None else reason)
            
            try:
                await client.message_create(channel, embed=embed)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return # We cannot help no internet
                
                elif isinstance(err, DiscordException) and (err.code == ERROR_CODES.cannot_message_user):
                    notify_note = 'Notification cannot be delivered: user has DM disabled.'
                else:
                    raise
            else:
                notify_note = None
    else:
        notify_note = None
    
    if reason is None:
        caller = event.user
        reason = f'Requested by: {caller.full_name} [{caller.id}]'
        
    await banner.guild_ban_add(guild, user, delete_message_days=delete_message_days, reason=reason)
    
    embed = Embed('Hecatia yeah!', f'{user.full_name} has been yeeted.')
    if (notify_note is not None):
        embed.add_footer(notify_note)
    
    yield embed


ROLE_EMOJI_OK     = BUILTIN_EMOJIS['ok_hand']
ROLE_EMOJI_CANCEL = BUILTIN_EMOJIS['x']
ROLE_EMOJI_EMOJIS = (ROLE_EMOJI_OK, ROLE_EMOJI_CANCEL)

class _role_emoji_emoji_checker(object):
    __slots__ = ('guild',)
    
    def __init__(self, guild):
        self.guild = guild
    
    def __call__(self, event):
        if event.emoji not in ROLE_EMOJI_EMOJIS:
            return False
        
        user = event.user
        if user.is_bot:
            return False
        
        if not self.guild.permissions_for(user).can_administrator:
            return False
        
        return True

@Koishi.interactions(is_global=True)
async def emoji_role(client, event,
        emoji : ('str', 'Select the emoji to bind to roles.'),
        role_1 : ('role', 'Select a role.') = None,
        role_2 : ('role', 'Double role!') = None,
        role_3 : ('role', 'Triple role!') = None,
        role_4 : ('role', 'Quadra role!') = None,
        role_5 : ('role', 'Penta role!') = None,
        role_6 : ('role', 'Epic!') = None,
        role_7 : ('role', 'Legendary!') = None,
        role_8 : ('role', 'Mythical!') = None,
        role_9 : ('role', 'Lunatic!') = None,
            ):
    """Binds the given emoji to the selected roles. You must have administrator permission."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
        return
    
    if not event.user_permissions.can_ban_users:
        yield Embed('Permission denied', 'You must have ban users permission to use this command.')
        return
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_manage_emojis) or (not permissions.can_add_reactions):
        yield Embed('Permission denied',
            f'{client.name_at(guild)} requires manage emojis and add reactions permissions for this command.')
        return
    
    emoji = parse_emoji(emoji)
    if emoji is None:
        yield Embed('Error', 'That\'s not an emoji.')
        return
    
    if emoji.is_unicode_emoji():
        yield Embed('Error', 'Cannot edit unicode emojis.')
        return
    
    emoji_guild = emoji.guild
    if (emoji_guild is None) or (emoji_guild is not guild):
        yield Embed('Error', 'Wont edit emojis from an other guild.')
        return
    
    roles = set()
    for role in role_1, role_2, role_3, role_4, role_5, role_6, role_7, role_8, role_9:
        if role is None:
            continue
        
        if role.guild is guild:
            roles.add(role)
            continue
        
        yield Embed('Error', f'Role {role.name}, [{role.id}] is bound to an other guild.')
        return
    
    roles = sorted(roles)
    roles_ = emoji.roles
    
    embed = Embed().add_author(emoji.url, emoji.name)
    
    if (roles_ is None) or (not roles_):
        role_text = '*none*'
    else:
        role_text = ', '.join([role.mention for role in roles_])
    
    embed.add_field('Roles before:', role_text)
    
    if (not roles):
        role_text = '*none*'
    else:
        role_text = ', '.join([role.mention for role in roles])
    
    embed.add_field('Roles after:', role_text)
    
    yield
    message = yield embed
    for emoji_ in ROLE_EMOJI_EMOJIS:
        await client.reaction_add(message, emoji_)
    
    try:
        event = await wait_for_reaction(client, message, _role_emoji_emoji_checker(message.guild), 300.)
    except TimeoutError:
        emoji_ = ROLE_EMOJI_CANCEL
    else:
        emoji_ = event.emoji
    
    if message.channel.cached_permissions_for(client).can_manage_messages:
        try:
            await client.reaction_clear(message)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return
            
            raise
    
    if emoji_ is ROLE_EMOJI_OK:
        try:
            await client.emoji_edit(emoji, roles=roles)
        except DiscordException as err:
            footer = repr(err)
        else:
            footer = 'Emoji edited successfully.'
    
    elif emoji_ is ROLE_EMOJI_CANCEL:
        footer = 'Emoji edit cancelled'
    
    else: # should not happen
        return
    
    embed.add_footer(footer)
    
    await client.interaction_followup_message_edit(event, message, embed=embed)


@Koishi.interactions(name='user', is_global=True)
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
        profile = user.guild_profiles.get(guild)
    
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

@Koishi.interactions(name='role', is_global=True)
async def role_(client, event,
        role: ('role', 'Select the role to show information of.'),
            ):
    """Shows the information about a role."""
    if role.partial:
        return Embed('Error', 'I must be in the guild, where the role is.')
    
    embed = Embed(f'Role information for: {role.name}', color=role.color)
    embed.add_field('Position', str(role.position), inline=True)
    embed.add_field('Id', str(role.id), inline=True)
    
    embed.add_field('Separated', 'true' if role.separated else 'false', inline=True)
    embed.add_field('Mentionable', 'true' if role.mentionable else 'false', inline=True)
    
    manager_type = role.manager_type
    if manager_type is RoleManagerType.NONE:
        managed_description = 'false'
    else:
        if manager_type is RoleManagerType.UNSET:
            await client.sync_roles(role.guild)
            manager_type = role.manager_type
        
        if manager_type is RoleManagerType.BOT:
            managed_description = f'Special role for bot: {role.manager:f}'
        elif manager_type is RoleManagerType.BOOSTER:
            managed_description = 'Role for the boosters of the guild.'
        elif manager_type is RoleManagerType.INTEGRATION:
            managed_description = f'Special role for integration: {role.manager.name}'
        elif manager_type is RoleManagerType.UNKNOWN:
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

@Koishi.interactions(name='guild', is_global=True)
async def guild_(client, event,
        field: ([(name, name) for name in GUILD_FIELDS], 'Which field of the info should I show?') = 'all',
            ):
    """Shows some information about the guild."""
    guild = event.guild
    if guild.partial:
        return Embed('Error', 'I must be in the guild to execute this command.')
    
    embed = Embed(guild.name, color=(
        guild.icon_hash&0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id>>22)&0xFFFFFF)
            ).add_thumbnail(guild.icon_url_as(size=128))
    
    GUILD_FIELDS[field](guild, embed, True)
    
    return embed


USER_PER_PAGE = 16
class InRolePageGetter(object):
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

class PaginationCheckUserOrPermission(object):
    __slots__ = ('user', 'channel')
    def __init__(self, user, channel):
        self.user = user
        self.channel = channel
    
    def __call__(self, event):
        user = event.user
        if user is self.user:
            return True
        
        if self.channel.permissions_for(user).can_manage_messages:
            return True
        
        return False

@Koishi.interactions(is_global=True)
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
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
        return
    
    roles = set()
    for role in role_1, role_2, role_3, role_4, role_5, role_6, role_7, role_8, role_9:
        if role is None:
            continue
        
        if role.guild is guild:
            roles.add(role)
            continue
        
        yield Embed('Error', f'Role {role.name}, [{role.id}] is bound to an other guild.')
        return
    
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
    
    yield
    
    channel = event.channel
    await Pagination(client, channel, pages, check=PaginationCheckUserOrPermission(event.user, channel))



LAST_MEME_AFTER = Cell()
MEME_QUEUE = []
MEME_URL = 'https://www.reddit.com/r/goodanimemes.json'
MEME_REQUEST_LOCK = Lock(KOKORO)

async def get_memes():
    if MEME_REQUEST_LOCK.locked():
        await MEME_REQUEST_LOCK
        return
    
    async with MEME_REQUEST_LOCK:
        after = LAST_MEME_AFTER.value
        if after is None:
            after = ''
        
        async with Koishi.http.get(MEME_URL, params={'limit': 100, 'after': after}) as response:
            json = await response.json()
        
        for meme_children in json['data']['children']:
            meme_children_data = meme_children['data']
            if meme_children_data.get('is_self', False) or \
                    meme_children_data.get('is_video', False) or \
                    meme_children_data.get('over_18', False):
                continue
            
            url = meme_children_data['url']
            if url.startswith('https://www.reddit.com/gallery/'):
                continue
            
            MEME_QUEUE.append((meme_children_data['title'], url))
        
        LAST_MEME_AFTER.value = json['data'].get(after)

async def get_meme():
    if MEME_QUEUE:
        return MEME_QUEUE.pop()
    
    await get_memes()
    
    if MEME_QUEUE:
        return MEME_QUEUE.pop()
    
    return None

@Koishi.interactions(is_global=True, name='meme')
async def meme_(client, event):
    """Shows a meme."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
        return
    
    yield
    
    meme = await get_meme()
    if meme is None:
        embed = Embed('Oof', 'No memes for now.')
    else:
        title, url = meme
        embed = Embed(title, url=url).add_image(url)
    
    yield embed
    return

TRIVIA_QUEUE = []
TRIVIA_URL = 'https://opentdb.com/api.php'
TRIVIA_REQUEST_LOCK = Lock(KOKORO)
TRIVIA_USER_LOCK = set()

async def get_trivias():
    if TRIVIA_REQUEST_LOCK.locked():
        await TRIVIA_REQUEST_LOCK
        return
    
    async with TRIVIA_REQUEST_LOCK:
        async with Koishi.http.get(TRIVIA_URL, params={'amount': 100, 'category': 31}) as response:
            json = await response.json()
        
        for trivia_data in json['results']:
            trivia = (
                html_unescape(trivia_data['question']),
                html_unescape(trivia_data['correct_answer']),
                [html_unescape(element) for element in trivia_data['incorrect_answers']],
                    )
            
            TRIVIA_QUEUE.append(trivia)
    
    
async def get_trivia():
    if TRIVIA_QUEUE:
        return TRIVIA_QUEUE.pop()
    
    await get_trivias()
    
    if TRIVIA_QUEUE:
        return TRIVIA_QUEUE.pop()
    
    return None

TRIVIA_OPTIONS = (
    BUILTIN_EMOJIS['regional_indicator_a'],
    BUILTIN_EMOJIS['regional_indicator_b'],
    BUILTIN_EMOJIS['regional_indicator_c'],
    BUILTIN_EMOJIS['regional_indicator_d'],
        )

class check_for_trivia_emoji(object):
    __slots__ = ('user',)
    
    def __init__(self, user):
        self.user = user
    
    def __call__(self, event):
        if event.user is not self.user:
            return False
        
        if event.emoji not in TRIVIA_OPTIONS:
            return False
        
        return True


@Koishi.interactions(is_global=True, name='trivia')
async def trivia_(client, event):
    """Asks a trivia."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
        return
    
    if not event.channel.cached_permissions_for(client).can_add_reactions:
        yield Embed('Permission error', 'I need add reactions permission to execute this command.')
        return
    
    user = event.user
    if user.id in TRIVIA_USER_LOCK:
        yield Embed('Ohoho', 'You are already in a trivia game.')
        return
    
    TRIVIA_USER_LOCK.add(user.id)
    try:
        yield
        
        trivia = await get_trivia()
        if trivia is None:
            yield Embed('Oof', 'No memes for now.')
            return
        
        question, correct, wrong = trivia
        possibilities = [correct, *wrong]
        correct_emoji = TRIVIA_OPTIONS[possibilities.index(correct)]
        
        description_parts = []
        for emoji, possibility in zip(TRIVIA_OPTIONS, possibilities):
            description_parts.append(emoji.as_emoji)
            description_parts.append(' ')
            description_parts.append(possibility)
            description_parts.append('\n')
        
        del description_parts[-1]
        
        description = ''.join(description_parts)
        
       
        message = yield Embed(question, description).add_author(user.avatar_url, user.full_name)
        
        for emoji in TRIVIA_OPTIONS:
            await client.reaction_add(message, emoji)
        
        try:
           reaction_add_event = await wait_for_reaction(client, message, check_for_trivia_emoji(user), 300.)
        except TimeoutError:
            title = 'Oof'
            description = 'Timeout occurred.'
        else:
            if reaction_add_event.emoji is correct_emoji:
                title = 'Noice'
                description = f'I raised that neko.\n\n{correct_emoji.as_emoji} {correct}'
            else:
                title = 'Oof'
                description = f'The correct answer is:\n\n{correct_emoji.as_emoji} {correct}'
        
        yield Embed(title, description).add_author(user.avatar_url, user.full_name)
        
        if message.channel.cached_permissions_for(client).can_manage_messages:
            await client.reaction_clear(message)
    
    finally:
        TRIVIA_USER_LOCK.discard(user.id)
