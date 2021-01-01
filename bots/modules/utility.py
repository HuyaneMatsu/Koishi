# -*- coding: utf-8 -*-
import json

from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import perf_counter

from hata import Color, Embed, Client, WaitTillExc, ReuBytesIO, sleep, DiscordException, Emoji, now_as_id, WebhookType,\
    elapsed_time, ActivityUnknown, Status, ActivityTypes, BUILTIN_EMOJIS, ChannelText, ChannelCategory, id_to_time, \
    cchunkify, ICON_TYPE_NONE, KOKORO, ChannelVoice, ChannelStore, ChannelThread, DATETIME_FORMAT_CODE

from hata.discord.utils import DISCORD_EPOCH_START
from hata.ext.commands import Cooldown, Converter, ConverterFlag, checks, Pagination, Closer
from hata.ext.prettyprint import pchunkify

from PIL import Image as PIL

from bot_utils.tools import CooldownHandler, PAGINATION_5PN
from bot_utils.shared import TESTER_ROLE
from bot_utils.command_utils import CHECK_ADMINISTRATIOR, CHANNEL_TEXT_CONVERTER_MESSAGE_CHANNEL_DEFAULT, \
    CLIENT_CONVERTER_ALL_CLIENT_DEFAULT, USER_CONVERTER_ALL_AUTHOR_DEFAULT, USER_CONVERTER_EVERYWHERE_AUTHOR_DEFAULT, \
    MESSAGE_CONVERTER_ALL

UTILITY_COLOR = Color(0x5dc66f)

Koishi: Client
@Koishi.commands.from_class
class ping:
    async def command(client, message):
        await client.message_create(message.channel,
            embed=Embed(f'{client.gateway.latency*1000.:.0f} ms',color=UTILITY_COLOR))
    
    aliases = 'pong'
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('ping',(
            'Do you wanna know how bad my connection is to Discord?\n'
            f'Usage: `{prefix}ping`'
            ), color=UTILITY_COLOR)

@Koishi.commands.from_class
class ping_http:
    async def command(client, message):
        start = perf_counter()
        message = await client.message_create(message.channel, 'ping-pong')
        delay = (perf_counter()-start)*1000.0
        
        await client.message_edit(message, '', embed=Embed(f'{delay:.0f} ms', color=UTILITY_COLOR))
    
    aliases = 'pong-http'
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('ping', (
            'Do you wanna see how bad is my http connection to Discord?\n'
            f'Usage: `{prefix}ping-http`'
            ), color=UTILITY_COLOR)

@Koishi.commands.from_class
class rawr:
    @Cooldown('guild', 60.0, handler=CooldownHandler())
    async def command(client, message):
        channel = message.channel
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

    category = 'UTILITY'

    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('rawr', (
            'Sends a message with every client, who can send a message to the channel.\n'
            f'Usage: `{prefix}rawr`'
            ), color=UTILITY_COLOR,).add_footer(
                'With cooldown of 60 seconds.')

@Koishi.commands.from_class
class color:
    async def command(client, message, color: 'color'):
        embed = Embed(f'#{color:06X}', color=color)
        embed.add_image('attachment://color.png')
        
        with ReuBytesIO() as buffer:
            image = PIL.new('RGB', (120, 30), color.as_rgb)
            image.save(buffer,'png')
            buffer.seek(0)
            
            await client.message_create(message.channel, embed=embed, file=('color.png', buffer))
    
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('color',(
            'Do you wanna see a color?\n'
            f'Usage: `{prefix}color *color*`\n'
                ), color=UTILITY_COLOR)

@Koishi.commands.from_class
class update_application_info:
    async def update_application_info(client, message, user: CLIENT_CONVERTER_ALL_CLIENT_DEFAULT):
        await user.update_application_info()
        content = f'Application info of `{user:f}` is updated succesfully!'
        await client.message_create(message.channel, content)
    
    category = 'UTILITY'
    checks = [checks.owner_only()]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('update_application_info',(
            'I can update applicaction info of any of the active clients '
            'at my mansion.\n'
            f'Usage: `{prefix}update_application_info <user>`\n'
            '`user` is otional and can be only an another client.'
                ), color=UTILITY_COLOR).add_footer(
                'Owner only!')

@Koishi.commands.from_class
class resend_webhook:
    async def command(client,message, message_id:int, channel: CHANNEL_TEXT_CONVERTER_MESSAGE_CHANNEL_DEFAULT):
        permissions = message.channel.cached_permissions_for(client)
        can_delete = permissions.can_manage_messages
        
        if not permissions.can_manage_webhooks:
            message = await client.message_create(message.channel,
                'I have no permissions to get webhooks from this channel.')
            if can_delete:
                await sleep(30.0,client.loop)
                await client.message_delete(message)
            return
        
        try:
            target_message = await client.message_get(channel,message_id)
        except DiscordException as err:
            message = await client.message_create(message.channel,repr(err))
            if can_delete:
                await sleep(30.0,client.loop)
                await client.message_delete(message)
            return
    
        webhooks = await client.webhook_get_channel(channel)
        for webhook in webhooks:
            if webhook.type is WebhookType.bot:
                break
        else:
            webhook = await client.webhook_create(channel, 'Love You')
    
        await client.webhook_message_create(webhook,
            embed=target_message.embeds,
            name=target_message.author.name,
            avatar_url=target_message.author.avatar_url)
    
    category = 'UTILITY'
    checks = [checks.guild_only(), checks.owner_only()]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('resend_webhook', (
            'I can resend a webhook, if chu really want.\n'
            f'Usage: `{prefix}resend_webhook *message_id* <channel>`\n'
            'The `message_id` must be the `id` of the message sent by the '
            'webhook.\n'
            'The `channel` by default is zhis channel, but if the message '
            'is at a different channel, you should tell me > <.'
                ), color=UTILITY_COLOR).add_footer(
                'Guild only. Owner only!')


@Koishi.commands.from_class
class show_emoji:
    async def command(client, message, emoji : Emoji):
        if emoji.is_custom_emoji():
            await client.message_create(message.channel, f'**Name:** {emoji:e} **Link:** {emoji.url}')
    
    name = 'showemoji'
    category = 'UTILITY'
    aliases = ['show-emoji', 'se']
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('se',(
            'I show the given emoji, tho I can only the custom ones.\n'
            f'Usage: `{prefix}showemoji *emoji*`\n'
                ), color=UTILITY_COLOR)


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
    
    state = activity
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

@Koishi.commands.from_class
class user_info:
    async def command(client, message, user: USER_CONVERTER_ALL_AUTHOR_DEFAULT):
        guild = message.guild
        
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
        
        if user.activity is not ActivityUnknown or user.status is not Status.offline:
            text = []
            
            if user.status is Status.offline:
                text.append('Status : offline\n')
            elif len(user.statuses) == 1:
                for platform,status in user.statuses.items():
                    text.append(f'Status : {status} ({platform})\n')
            else:
                text.append('Statuses :\n')
                for platform,status in user.statuses.items():
                    text.append(f'**>>** {status} ({platform})\n')
            
            if user.activity is ActivityUnknown:
                text.append('Activity : *unknown*\n')
            elif len(user.activities) == 1:
                text.append('Activity : ')
                add_activity(text, user.activities[0])
            else:
                text.append('Activities : \n')
                for index,activity in enumerate(user.activities, 1):
                    text.append(f'{index}.: ')
                    add_activity(text, activity)
            
            embed.add_field('Status and Activity',''.join(text))
        await client.message_create(message.channel, embed=embed)
    
    name = 'user'
    category = 'UTILITY'
    aliases = 'profile'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('user', (
            'I show you some information about the given user.\n'
            'If you use it inside of a guild and the user is inside as well, '
            'will show information, about their guild profile too.\n'
            f'Usage: `{prefix}user <user>`\n'
            'If no user is passed, I will tell your secrets :3'
                ), color=UTILITY_COLOR)


GREEN_HEART = BUILTIN_EMOJIS['green_heart']
YELLOW_HEART = BUILTIN_EMOJIS['yellow_heart']
RED_HEART = BUILTIN_EMOJIS['heart']
BLACK_HEART = BUILTIN_EMOJIS['black_heart']

async def guild_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('user', (
        'Do you want me to list some information about this guild?\n'
        f'Usage: `{prefix}guild <section>`\n'
        '\n'
        'You can also specify which field you wanna display from the following ones:\n'
        '- *info*\n'
        '- *counts*\n'
        '- *emojis*\n'
        '- *users*\n'
        '- *boosters*'
            ), color=UTILITY_COLOR).add_footer(
            'Guild only!')

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
            sections_parts.append(' anmiated]')
        
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
        emoji = BUILTIN_EMOJIS['gift_heart']
        count = len(boosters)
        to_render = count if count < 21 else 21
        
        embed.add_field(f'Most awesome people of the guild', f'{to_render} {emoji:e} out of {count} {emoji:e}')
        
        for user in boosters[:21]:
            embed.add_field(user.full_name,
                f'since: {elapsed_time(user.guild_profiles[guild].boosts_since)}')
    
    elif even_if_empty:
        embed.add_field(f'Most awesome people of the guild', '*The guild has no chicken duggets.*')

GUILD_FIELDS = {
    'info': add_guild_info_field,
    'counts': add_guild_counts_field,
    'emojis': add_guild_emojis_field,
    'users': add_guild_users_field,
    'boosters': add_guild_boosters_field
        }

@Koishi.commands(name='guild', category='UTILITY', description=guild_description, checks=checks.guild_only())
async def guild_info(client, message, field: str=None):
    guild = message.guild
    if guild is None:
        return
    
    if (field is not None):
        try:
            func = GUILD_FIELDS[field.lower()]
        except KeyError:
            embed = await guild_description(client, message)
            await Closer(client, message.channel, embed)
            return
    
    embed = Embed(guild.name, color=(
        guild.icon_hash&0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id>>22)&0xFFFFFF)
            ).add_thumbnail(guild.icon_url_as(size=128))
    
    if field is None:
        add_guild_info_field(guild, embed, False)
        add_guild_counts_field(guild, embed, False)
        add_guild_emojis_field(guild ,embed, False)
        add_guild_users_field(guild, embed, False)
        add_guild_boosters_field(guild, embed, False)
    else:
        func(guild, embed, True)
    
    await client.message_create(message.channel, embed=embed)


@Koishi.commands.from_class
class message:
    async def command(client, message, target_message: MESSAGE_CONVERTER_ALL):
        await Pagination(client,message.channel, [Embed(description=chunk) for chunk in pchunkify(target_message)])
    
    category = 'UTILITY'
    checks = [checks.guild_only(), CHECK_ADMINISTRATIOR | checks.has_role(TESTER_ROLE)]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('message',(
            'If you want, I show the representation of a message.\n'
            f'Usage: `{prefix}message *message_id* <channel>`\n'
            'By default `channel` is the channel, where you used the command.'
                ), color=UTILITY_COLOR).add_footer(
                f'Guild only! You must have dministrator permission or {TESTER_ROLE.name}!')


@Koishi.commands.from_class
class message_pure:
    async def command(client, message, target_message: MESSAGE_CONVERTER_ALL):
        try:
            data = await client.http.message_get(target_message.channel.id, target_message.id)
        except DiscordException as err:
            await client.message_create(message.channel,repr(err))
            return
        
        await Pagination(client, message.channel, [
            Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
                ])
    
    category = 'UTILITY'
    checks = [checks.guild_only(), checks.has_role(TESTER_ROLE)]
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('message-pure', (
            'If you want, I show the pure json representing a message.\n'
            f'Usage: `{prefix}message-pure *message_id* <channel>`\n'
            'By default `channel` is the channel, where you used the command.'
                ), color=UTILITY_COLOR).add_footer(
                f'Guild only! You must {TESTER_ROLE.name} to use it!')

@Koishi.commands.from_class
class roles:
    class command(object):
        __slots__ = ('cache','guild','roles',)
        async def __new__(cls,client,message):
            channel = message.channel
            self = object.__new__(cls)
            roles = channel.guild.role_list
            roles.reverse()
            self.roles = roles
            self.cache=[None for _ in range(len(self.roles)+1)]
            self.createpage0(channel.guild)
            #we return awaitable, so it is OK
            return await PAGINATION_5PN(client,channel,self)
            
        def __len__(self):
            return len(self.cache)
        
        def createpage0(self,guild):
            embed=Embed(f'Roles of **{guild.name}**:',
                '\n'.join([role.mention for role in self.roles]),
                color=(guild.icon_hash&0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id>>22)&0xFFFFFF))
            embed.add_footer(f'Page 1 /  {len(self.cache)}')
            self.cache[0]=embed
        
        def __getitem__(self,index):
            page=self.cache[index]
            if page is None:
                return self.create_page(index)
            return page
        
        def create_page(self,index):
            role = self.roles[index-1]
            embed = Embed(role.name,
                '\n'.join([
                    f'id : {role.id!r}',
                    f'color : {role.color.as_html}',
                    f'permission number : {role.permissions}',
                    f'managed : {role.managed}',
                    f'separated : {role.separated}',
                    f'mentionable : {role.mentionable}',
                    '\nPermissions:\n```diff',
                    *(f'{"+" if value else "-"}{key}' for key,value in role.permissions.items()),
                    '```',
                        ]),
                color=role.color)
            embed.add_footer(f'Page {index+1} /  {len(self.cache)}')
            
            self.cache[index] = embed
            return embed
    
    category = 'UTILITY'
    checks = checks.guild_only()
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('roles',(
            'Cutie, do you want me, to list the roles of the guild and their '
            'permissions?\n'
            f'Usage: `{prefix}roles`'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only!')

@Koishi.commands.from_class
class avatar:
    async def command(client, message, user: USER_CONVERTER_EVERYWHERE_AUTHOR_DEFAULT):
        color = user.avatar_hash
        if color:
            color &=0xffffff
        else:
            color = user.default_avatar.color
        
        url = user.avatar_url_as(size=4096)
        embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
        embed.add_image(url)
        
        await client.message_create(message.channel, embed=embed)
    
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('avatar',(
            'Pure 4K user avatar showcase!\n'
            f'Usage: `{prefix}avatar <user>`\n'
            'If no `user` is passed, I will showcase your avatar.'
                ), color=UTILITY_COLOR)

@Koishi.commands.from_class
class guild_icon:
    async def command(client, message):
        guild = message.guild
        if guild is None:
            return
        
        icon_url = guild.icon_url_as(size=4096)
        if icon_url is None:
            embed = Embed(description=f'`{guild.name}` has no icon.')
        else:
            color = guild.icon_hash&0xffffff
            embed = Embed(f'{guild.name}\' icon', color=color, url=icon_url)
            embed.add_image(icon_url)
        
        await client.message_create(message.channel, embed=embed)
    
    category = 'UTILITY'
    checks = checks.guild_only()
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('guild-icon',(
            'Do you wanna see the guild\'s icon in 4K?!\n'
            f'Usage: `{prefix}guild-icon`\n'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only!')


@Koishi.commands.from_class
class welcome_screen:
    async def command(client, message):
        guild = message.guild
        if guild is None:
            return
        
        welscome_screen = await client.welcome_screen_get(guild)
        if welscome_screen is None:
            embed = Embed(description=f'**{guild.name}** *has no welcome screen enabled*.')
        else:
            description = welcome_screen.description
            if (description is None):
                description = '*TOP THINGS TO DO HERE*'
            else:
                description = f'{welscome_screen.description}\n\n*TOP THINGS TO DO HERE*'
            
            embed = Embed(f'Welcome to **{guild.name}**', description)
            
            icon_url = guild.icon_url
            if (icon_url is not None):
                embed.add_thumbnail(icon_url)
            
            welcome_channels = welscome_screen.welcome_channels
            if (welcome_channels is not None):
                for welcome_channel in welcome_channels:
                    embed.add_field(f'{welcome_channel.emoji:e} {welcome_channel.description}',
                        f'#{welcome_channel.channel:d}')
        
        await client.message_create(message.channel, embed=embed)
    
    aliases = 'guild_welcome_screen'
    category = 'UTILITY'
    checks = checks.guild_only()
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('welcome-screen', (
            'Displays the guild\'s welcome screen\n'
            f'Usage: `{prefix}welcome-screen`'
                ), color=UTILITY_COLOR).add_footer(
                'Guild only!')


@Koishi.commands.from_class
class get_user_id:
    async def command(client, message, user: Converter('user',
            ConverterFlag().update_by_keys(mention=True, name=True), default_code='message.author')):
        await client.message_create(message.channel, str(user.id))
    
    name = 'userid'
    aliases = ['user-id', 'uid']
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('userid', (
            'Sends your or the given user\'s id.\n'
            f'Usage: `{prefix}userid <user name / mention>`'
                ), color=UTILITY_COLOR)


@Koishi.commands.from_class
class get_channel_id:
    async def command(client, message, channel: Converter('channel',
            ConverterFlag().update_by_keys(mention=True, name=True), default_code='message.channel')):
        await client.message_create(message.channel, str(channel.id))
    
    name = 'channelid'
    aliases = ['channel-id', 'cid']
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('channelid', (
            'Sends this or the given channel\'s id.\n'
            f'Usage: `{prefix}channelid <channel name / mention>`'
                ), color=UTILITY_COLOR)


@Koishi.commands.from_class
class get_guild_id:
    async def command(client, message):
        channel = message.channel
        guild = channel.guild
        if guild is None:
            return
        
        await client.message_create(channel, str(guild.id))
    
    name = 'guildid'
    aliases = ['guild-id', 'serverid', 'server-id', 'gid', 'sid']
    category = 'UTILITY'
    checks = checks.guild_only()
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('guildid', (
            'Sends the guild\'s id.\n'
            f'Usage: `{prefix}guildid`'
                ), color=UTILITY_COLOR).add_footer('Guild only.')


@Koishi.commands.from_class
class get_role_id:
    async def command(client, message, role: Converter('role',
            ConverterFlag().update_by_keys(mention=True, name=True), default_code='message.guild.default_role')):
        
        if role is None:
            role_id = 'N/A'
        else:
            role_id = str(role.id)
        
        await client.message_create(message.channel, role_id)
    
    name = 'roleid'
    aliases = ['role-id', 'rid']
    category = 'UTILITY'
    checks = [checks.guild_only()]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('roleid', (
            'Sends the guild\'s default role\'s or the given role\'s id.\n'
            f'Usage: `{prefix}roleid <role name / mention>`'
                ), color=UTILITY_COLOR).add_footer('Guild only.')


@Koishi.commands.from_class
class get_now_as_id:
    async def command(client, message):
        await client.message_create(message.channel, str(now_as_id()))
    
    name = 'now-as-id'
    aliases = ['nowasid']
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('now-as-id', (
            'Sends the current time as Discord snowflake id.\n'
            f'Usage: `{prefix}now-as-id`'
                ), color=UTILITY_COLOR)


@Koishi.commands.from_class
class get_id_as_time:
    async def command(client, message, snowflake:int):
        if snowflake < 0 or snowflake > ((1<<63)-1):
            return
        
        time = id_to_time(snowflake)
        await client.message_create(message.channel, f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago')
    
    name = 'id-as-time'
    aliases = ['idastime', 'idtotime', 'id-to-time']
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('id-as-time', (
            'Converts the given Discord snowflake id to time.\n'
            f'Usage: `{prefix}now-as-time *id*`'
                ), color=UTILITY_COLOR)


# COUNTDOWN DISABLED, SINCE IT IS OVER
EVENT_DEADLINE = datetime(2020, 11, 18, 0, 0, 0)

async def countdown_description(client, message):
    now = datetime.utcnow()
    if now >= EVENT_DEADLINE:
        result = 'the countdown is already over'
    else:
        result = elapsed_time(relativedelta(now, EVENT_DEADLINE))
        result = f'there is {result} left'
    
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('countdown', (
        'Returns when the hata codejam ends!\n'
        f'Usage: `{prefix}countdown`\n'
        '\n'
        f'Dont worry, we got you, {result}.'
            ), color=UTILITY_COLOR)

#@Koishi.commands(aliases=['deadline', 'event_deadline'], description=countdown_description, category='UTILITY')
async def countdown(client, message):
    now = datetime.utcnow()
    if now >= EVENT_DEADLINE:
        result = 'Countdown over!'
    else:
        result = elapsed_time(relativedelta(now, EVENT_DEADLINE))
    
    await client.message_create(message.channel, result)


async def shared_guilds_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('deadline', (
        'Returns the shared guilds between you and me.\n'
        f'Usage: `{prefix}shared-guilds`\n'
            ), color=UTILITY_COLOR)


@Koishi.commands(description=shared_guilds_description, category='UTILITY')
async def shared_guilds(client, message):
    pages = []
    lines = []
    lines_count = 0
    
    user = message.author
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
    
    await Pagination(client, message.channel, embeds)

