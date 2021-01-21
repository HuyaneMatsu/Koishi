# -*- coding: utf-8 -*-
from time import perf_counter
from random import random

from hata import Client, Embed, parse_emoji, DATETIME_FORMAT_CODE, id_to_time, elapsed_time, parse_emoji, \
    DiscordException, BUILTIN_EMOJIS, ERROR_CODES, ICON_TYPE_NONE
from hata.ext.commands import wait_for_reaction

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
