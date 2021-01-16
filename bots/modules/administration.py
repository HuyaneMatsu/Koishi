# -*- coding: utf-8 -*-
from hata import Color, Embed, DiscordException, sleep, Emoji, BUILTIN_EMOJIS, ERROR_CODES, ChannelBase, User, \
    AuditLogEvent, KOKORO, Client
from hata.ext.commands import Converter, Pagination, wait_for_reaction
from hata.ext.prettyprint import pchunkify

from bot_utils.command_utils import CHECK_MANAGE_MESSAGES, CHECK_OWNER_OR_CAN_INVITE, CHECK_BAN_USERS, \
    CHECK_OWNER_OR_GUILD_OWNER, CHECK_MANAGE_CHANNEL_AND_INVITES, CHECK_OWNER_ONLY, CHECK_VIEW_LOGS, \
    USER_CONVERTER_EVERYWHERE_NONE_DEFAULT, USER_CONVERTER_ALL_NONE_DEFAULT, CHECK_YEET_USERS, CHECK_ADMINISTRATION


ADMINISTRATION_COLOR = Color.from_rgb(148, 0, 211)

Koishi: Client

@Koishi.commands.from_class
class clear:
    async def command(client, message, limit : Converter('int', default=1,), reason):
        if not reason:
            reason = f'{message.author.full_name} asked for it'
        if limit > 0:
            await client.message_delete_sequence(channel=message.channel,limit=limit,reason=reason)
    
    category = 'ADMINISTRATION'
    checks = CHECK_MANAGE_MESSAGES
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('clear', (
            'I ll clear up the leftover after your lewd messages O-NEE-CHA-N.'
            f'Usage : `{prefix}clear <amount> <reason>`\n'
            '`amount` is optional, by default it is just 1.\n'
            'The `reason` will show up at the audit logs of the guild.'
            ), color=ADMINISTRATION_COLOR).add_footer(
                'This command can be executed only at a guild, and you must have '
                '`manage messages` permission as well.')


@Koishi.commands.from_class
class invite_create:
    async def command(client, message, content):
        user = message.author
        
        invite_ = None
        if content == 'perma':
            if client.is_owner(user) or user is message.guild.owner:
                invite_ = await client.vanity_invite_get(message.guild)
                if invite_ is None:
                    max_age = 0
                    max_use = 0
            else:
                await client.message_create(message.channel,
                    'You must be the owner of the guild, to create a permanent invite.')
                return
        else:
            max_age = 21600
            max_use = 1
        
        try:
            if invite_ is None:
                invite_ = await client.invite_create_preferred(message.guild, max_age, max_use)
        except DiscordException as err:
            content = repr(err)
        except ValueError as err:
            content = err.args[0]
        else:
            if invite_ is None:
                content = 'I do not have enough permission to create invite from the guild\'s preferred channel.'
            else:
                content = f'Here is your invite, dear:\n\n{invite_.url}'
            
        channel = await client.channel_private_create(user)
        try:
            await client.message_create(channel, content)
        except DiscordException as err:
            if err.code == ERROR_CODES.invalid_message_send_user: # User has dm-s disallowed
                await client.message_create(message.channel, 'You have DM disabled, could not send the invite.')
    
    category = 'ADMINISTRATION'
    checks = CHECK_OWNER_OR_CAN_INVITE
    
    async def description(client, message):
        guild = message.channel.guild
        user = message.author
        if guild is None:
            full = False
        else:
            if user == guild.owner:
                full = True
            else:
                full = False
        
        if not full:
            full = client.is_owner(user)
        
        prefix = client.command_processer.get_prefix_for(message)
        if full:
            content = (
                'I create an invite for you, to this guild.\n'
                f'Usage: `{prefix}invite-create (perma)`\n'
                'By passing `perma` after the command, I ll create for you, my dear A permanent invite to the guild.'
                    )
        else:
            content = (
                'I create an invite for you, to this guild.\n'
                f'Usage: `{prefix}invite-create`'
                    )
        
        return Embed('create-invite', content, color=ADMINISTRATION_COLOR).add_footer(
            'Guild only. You must have `create instant invite` permission to invoke this command.')


@Koishi.commands.from_class
class bans:
    async def command(client, message):
        guild = message.channel.guild
        if (guild is None):
            return
        
        if not guild.cached_permissions_for(client).can_ban_users:
            await client.message_create(message.channel, embed = Embed(
                description = 'I have no permissions at the guild.',
                color=ADMINISTRATION_COLOR))
            return
        
        ban_data = await client.message_id(guild)
        
        if not ban_data:
            await client.message_create(message.channel, 'None')
            return
        
        embeds = []
        main_text = f'Guild bans for {guild.name} {guild.id}:'
        limit = len(ban_data)
        index = 0
    
        while True:
            field_count = 0
            embed_length = len(main_text)
            embed = Embed(title=main_text)
            embeds.append(embed)
            while True:
                user, reason = ban_data[index]
                if reason is None:
                    reason = 'Not defined.'
                name = f'{user:f} {user.id}'
                embed_length += len(reason)+len(name)
                if embed_length > 5900:
                    break
                embed.add_field(name,reason)
                field_count += 1
                if field_count == 25:
                    break
                index +=1
                if index == limit:
                    break
            if index == limit:
                break
        
        index = 0
        field_count = 0
        embed_ln = len(embeds)
        result = []
        while True:
            embed = embeds[index]
            index +=1
            embed.add_footer(f'Page: {index}/{embed_ln}. Bans {field_count+1}-{field_count+len(embed.fields)}/{limit}')
            field_count += len(embed.fields)
            
            result.append(embed)
            
            if index == embed_ln:
                break
        
        await Pagination(client, message.channel, result)
    
    category = 'ADMINISTRATION'
    checks = CHECK_BAN_USERS
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('bans', (
            'I ll show you the banned users at the guild.\n'
            f'Usage: `{prefix}bans`'
            ), color=ADMINISTRATION_COLOR).add_footer(
                'Guild only. You must have `ban user` permission to '
                'invoke this command.')


@Koishi.commands.from_class
class leave_guild:
    async def command(client, message):
        await client.guild_leave(message.guild)
    
    category = 'ADMINISTRATION'
    checks = CHECK_OWNER_OR_GUILD_OWNER
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('leave-guild', (
            'You really want me to leave? :c\n'
            f'Usage: `{prefix}leave_guild`'
            ), color=ADMINISTRATION_COLOR).add_footer(
                'Guild only. You must be the owner of the guild to use this command.')


@Koishi.commands.from_class
class reaction_clear:
    async def command(client, message, message_id:int):
        while True:
            if not message.channel.cached_permissions_for(client).can_manage_messages:
                content='I have no permissions to execute this command at the channel.'
                break
            
            try:
                target_message = await client.message_get(message.channel, message_id)
            except DiscordException:
                content = 'Could not find that message.'
                break
            
            await client.reaction_clear(target_message)
            content = 'Done, pat me now!'
            break
        
        message = await client.message_create(message.channel, content)
        await sleep(30., KOKORO)
        await client.message_delete(message)
    
    category = 'ADMINISTRATION'
    checks = CHECK_MANAGE_MESSAGES
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('reaction_clear', (
            'Do you want me to remove all the reactions from a message?\n'
            f'Usage: `{prefix}reaction_clear *message_id*`'
                ), color=ADMINISTRATION_COLOR).add_footer(
                'Guild only! You must have manage messages permission to invoke this command.!')

@Koishi.commands.from_class
class show_help_for:
    async def command(client, message, user: USER_CONVERTER_ALL_NONE_DEFAULT, rest):
        if user is None:
            await client.message_create(message.channel,
                'Please define a user as well.')
            return
        
        message = message.custom(author=user)
        
        await client.command_processer.commands['help'](client, message, rest)
    
    category = 'ADMINISTRATION'
    checks = CHECK_OWNER_ONLY
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('show_help_for', (
            'Calls `help` command, as the given user would do it.\n'
            f'Usage: `{prefix}show_help_for *user*`\n'
                ), color=ADMINISTRATION_COLOR).add_footer(
                'Owner only!')

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

@Koishi.commands.from_class
class emoji_role:
    async def command(client, message, emoji:Emoji, *roles:'role'):
        permissions = message.channel.cached_permissions_for(client)
        if (not permissions.can_manage_emojis) or (not permissions.can_add_reactions):
            await client.message_create(message.channel,
                embed = Embed(description='I have no permissions to edit emojis, or to add reactions.'))
            return
        
        if emoji.is_unicode_emoji():
            await client.message_create(message.channel, embed=Embed('Ayaya', 'Unicode emoji cannot be edited.'))
            return
        
        emoji_guild = emoji.guild
        if (emoji_guild is None) or (emoji_guild is not message.guild):
            await client.message_create(message.channel, embed=Embed('Ayaya', 'The emoji is from a different guild.'))
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
        
        message = await client.message_create(message.channel, embed=embed)
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
        
        else: #should not happen
            return
        
        embed.add_footer(footer)
        
        await client.message_edit(message, embed=embed)
    
    name = 'emoji-role'
    category = 'ADMINISTRATION'
    checks = CHECK_ADMINISTRATION
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('emoji-role', (
            'Edits the emoji for which roles is available for.\n'
            f'Usage: `{prefix}emoji-role *emoji* <role_1> <role_2> ...`\n'
                ), color=ADMINISTRATION_COLOR).add_footer(
                'Guild only. You must have administration permission to execute this command')


@Koishi.commands.from_class
class invites:
    async def command(client, message, channel:ChannelBase=None):
        guild = message.channel.guild
        if channel is None:
            if not guild.cached_permissions_for(client).can_manage_guild:
                await client.message_create(message.channel,
                    'I don\'t have enough permission, to request the invites.')
                return
            invites = await client.invite_get_all_guild(guild)
        else:
            if not channel.cached_permissions_for(client).can_manage_channel:
                await client.message_create(message.channel,
                    'I don\'t have enough permission, to request the invites.')
                return
            invites = await client.invite_get_channel(channel)
        
        pages = [Embed(description=chunk) for chunk in pchunkify(invites,write_parents=False)]
        await Pagination(client, message.channel,pages,120.)
    
    category = 'ADMINISTRATION'
    checks = CHECK_MANAGE_CHANNEL_AND_INVITES
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('invites', (
            'I can list you the invites of the guild.\n'
            f'Usage: `{prefix}invites <channel>`\n'
            'If `channel` is passed, I ll check the invites only at that channel.'
                ), color=ADMINISTRATION_COLOR).add_footer(
                'Guild only! You must have manage channel & create instant invite permission to use this command.')


@Koishi.commands.from_class
class logs:
    async def command(client, message, guild:'guild'=None, user:User=None, event_name: str=''):
        if guild is None:
            guild = message.guild
            if guild is None:
                await client.message_create(message.channel,
                    'Cannot default to current guild. The command was not called from a guild.')
                return
        
        if not guild.cached_permissions_for(client).can_view_audit_logs:
            await client.message_create(message.channel,
                'I have no permissions at the guild, to request audit logs.')
            return
        
        while True:
            if not event_name:
                event=None
                break
            
            try:
                event = AuditLogEvent.INSTANCES[int(event_name)]
                break
            except (KeyError, ValueError):
                pass
            
            try:
                event = getattr(AuditLogEvent, event_name.upper())
                break
            except AttributeError:
                pass
            
            event = None
            break
    
        with client.keep_typing(message.channel):
            iterator = await client.audit_log_iterator(guild,user,event)
            await iterator.load_all()
            logs = iterator.transform()
        
        await Pagination(client, message.channel, [Embed(description=chunk) for chunk in pchunkify(logs)])
    
    category = 'ADMINISTRATION'
    checks = CHECK_VIEW_LOGS
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('logs', (
            'I can list you the audit logs of the guild.\n'
            f'Usage: `{prefix}logs <guild> <user> <event>`\n'
            'Both `user` and `event` is optional.\n'
            '`user` is the user, who executed the logged operations.\n'
            'The `event` is the internal value or name of the type of the '
            'operation.'
                ), color=ADMINISTRATION_COLOR).add_footer(
                'Guild only!')

@Koishi.commands.from_class
class telekinesisban:
    async def command(client, message, guild: 'guild', user:USER_CONVERTER_EVERYWHERE_NONE_DEFAULT, reason):
        
        # Should not happen normally
        if guild is None:
            return
        
        if user is None:
            await client.message_create(message.channel, 'Please define the user to ban.')
            return
        
        if not reason:
            author = message.author
            reason = f'For the request of {author.full_name} ({author.id})'
        
        for maybe_banner in guild.clients:
            if guild.cached_permissions_for(client).can_ban_users:
                banner = maybe_banner
                break
        else:
            await client.message_create(message.channel, 'No permission to ban user in the guild.')
            return
        
        await banner.guild_ban_add(guild, user, reason=reason)
        await client.message_create(message.channel,
            f'{user.full_name} banned at guild {guild.name} by {banner.full_name}.')
    
    category = 'ADMINISTRATION'
    checks = CHECK_OWNER_ONLY
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('telekinesisban', (
            'Bans the given user at the specified guild.\n'
            f'Usage: `{prefix}telekinesisban *guild* *user* <reason>`\n'
                ), color=ADMINISTRATION_COLOR).add_footer(
                'Owner only!')

@Koishi.commands.from_class
class yeet:
    async def command(client, message, user: USER_CONVERTER_EVERYWHERE_NONE_DEFAULT, reason):
        
        guild = message.guild
        if guild is None:
            return
        
        if user is None:
            await client.message_create(message.channel, 'Please define the user to yeet.')
            return
        
        if not reason:
            author = message.author
            reason = f'For the request of {author.full_name} ({author.id})'
        
        for maybe_banner in guild.clients:
            if guild.cached_permissions_for(maybe_banner).can_ban_users:
                banner = maybe_banner
                break
        else:
            await client.message_create(message.channel, 'No permission to yeet user in the guild.')
            return
        
        await banner.guild_ban_add(guild, user, reason=reason)
        await client.message_create(message.channel, f'{user.full_name} yeeted Hecatia yeah!')
    
    category = 'ADMINISTRATION'
    checks = CHECK_YEET_USERS
    aliases = 'ban'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('yeet', (
            'Bans the given user.\n'
            f'Usage: `{prefix}yeet *user* <reason>`\n'
                ), color=ADMINISTRATION_COLOR).add_footer(
                'You must have yeet users permission to use this command!')
        
