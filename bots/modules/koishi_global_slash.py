# -*- coding: utf-8 -*-
from time import perf_counter
from random import random

from hata import Client, Embed, parse_emoji, DATETIME_FORMAT_CODE, id_to_time, elapsed_time, parse_emoji, \
    DiscordException, BUILTIN_EMOJIS, ERROR_CODES
from hata.ext.commands import wait_for_reaction

Koishi : Client

COMMAND_LIMIT = 50
SWITCHABLE_COMMANDS = {}

def switchable(command):
    SWITCHABLE_COMMANDS[command.name] = command
    return command

def prettify_command_name(command_name):
    return command_name.lower().replace('_', '-').replace(' ', '-')

COMMANDS_CATEGORY = Koishi.interactions(None, name='commands', is_global=True,
    description='Command to manage Koishi\'s slash commands inside of the guild.')

@COMMANDS_CATEGORY.interactions(name='list')
async def list_(client, event,
        current: ('bool', 'Whether the current commands should be listed.') = True,
            ):
    """Lists every available switchable commands or the switchable commands."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if current:
        yield
        
        commands = await client.application_command_guild_get_all(guild)
        command_names = [command.name for command in commands]
        command_names.sort()
        
        title = f'{guild.name}\' current commands'
    else:
        command_names = sorted(SWITCHABLE_COMMANDS)
        title = 'All switchable command'
    
    description_parts = []
    
    for index, command_name in enumerate(command_names, 1):
        description_parts.append(str(index))
        description_parts.append('.: `')
        description_parts.append(command_name)
        description_parts.append('`\n')
    
    description_parts[-1] = '`'
    
    description = ''.join(description_parts)
    
    yield Embed(title, description)
    return


@COMMANDS_CATEGORY.interactions
async def enable(client, event,
        command_name: ('str', 'The command\'s name to enable or disable.'),
        allow: ('bool', 'Enable?') = True,
            ):
    """Enables or disables a switchable command."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if not event.user_permissions.can_administrator:
        yield Embed('Permission denied', 'You must have administrator permission to use this command.')
        return
    
    command_name = prettify_command_name(command_name)
    if command_name not in SWITCHABLE_COMMANDS:
        yield Embed('Error', 'Unknown command-name.')
        return
    
    yield
    
    application_commands = await client.application_command_guild_get_all(guild)
    for application_command in application_commands:
        # If you are not working with overlapping names, a name check should be enough.
        if application_command.name == command_name:
            command_present = True
            break
    else:
        command_present = False
    
    if allow:
        if command_present:
            content = 'is already present'
        else:
            if len(application_commands) == COMMAND_LIMIT:
                content = f'could not be added; command limit ({COMMAND_LIMIT}) is reached'
            else:
                command = SWITCHABLE_COMMANDS[command_name]
                await client.application_command_guild_create(guild, command.get_schema())
                content = 'has been added'
    else:
        if command_present:
            await client.application_command_guild_delete(guild, application_command)
            content = 'has been disabled'
        else:
            content = 'is not present'
    
    yield Embed('Success', f'Command `{command_name}` {content}.')
    return

@COMMANDS_CATEGORY.interactions
async def describe(client, event,
        command_name: ('str', 'The command\'s name to enable or disable.'),
            ):
    """Shows the given switchable command's description."""
    command_name = prettify_command_name(command_name)
    
    try:
        command = SWITCHABLE_COMMANDS[command_name]
    except KeyError:
        return Embed('Error', f'No command found with name:\n{command_name})')
    
    return Embed(command_name, command.description)

@switchable
@Koishi.interactions
async def ping(client, event):
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@switchable
@Koishi.interactions
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


@switchable
@Koishi.interactions
async def showemoji(client, event,
        emoji : ('str', 'Yes?'),
            ):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji)
    if emoji is None:
        return 'That\'s not an emoji.'
    
    if emoji.is_unicode_emoji():
        return 'That\' an unicode emoji, cannot link it.'
    
    return f'**Name:** {emoji:e} **Link:** {emoji.url}'

@switchable
@Koishi.interactions(name='id-to-time')
async def idtotime(client, event,
        snowflake : ('int', 'Id please!'),
            ):
    """Converts the given Discord snowflake id to time."""
    time = id_to_time(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'


@switchable
@Koishi.interactions
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

@switchable
@Koishi.interactions
async def roll(client, event,
        dice_count: ([(str(v), v) for v in range(1, 7)], 'With how much dice do you wanna roll?') = 1,
            ):
    """Rolls with dices."""
    amount = 0
    for _ in range(dice_count):
        amount += round(1.+(random()*5.))
    
    return str(amount)

@switchable
@Koishi.interactions
async def yeet(client, event,
        user :('user', 'Select the user to yeet!'),
        reason : ('str', 'Any reason why you would want to yeet?') = None,
        delete_message_days : ([(str(v), v) for v in range(8)], 'Delete previous messages?') = 0,
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
    
    if (reason is None) or (not reason):
        caller = event.author
        reason = f'Requested by: {caller.full_name} [{caller.id}]'
    
    yield
    await banner.guild_ban_add(guild, user, reason=reason)
    yield Embed('Hecatia yeah!', f'{user.full_name} has been yeeted.')


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

@switchable
@Koishi.interactions
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

