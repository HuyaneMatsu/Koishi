import re, sys, json

from hata import Color, Embed, eventlist, WaitTillExc, ReuBytesIO, Client, sleep, DiscordException, Emoji, \
    elapsed_time, ActivityUnknown, Status, ActivitySpotify, BUILTIN_EMOJIS, ChannelText, ChannelCategory, \
    cchunkify, Permission
from hata.ext.commands import Command, Cooldown, Converter, ConverterFlag, checks, Pagination
from hata.ext.prettyprint import pchunkify

from PIL import Image as PIL

from tools import CooldownHandler, PAGINATION_5PN

UTILITY_COLOR = Color(0x5dc66f)
UTILITY_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(UTILITY_COMMANDS)

def teardown(lib):
    Koishi.commands.unextend(UTILITY_COMMANDS)


@UTILITY_COMMANDS.from_class
class ping:
    async def command(client,message):
        await client.message_create(message.channel,
            embed=Embed(f'{client.gateway.latency*1000.:.0f} ms',color=UTILITY_COLOR))
    
    aliases = ['pong']
    category = 'UTILITY'
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('ping',(
            'Do you wanna know how bad my connection is to Discord?\n'
            f'Usage: `{prefix}ping`'
            ),color=UTILITY_COLOR)
        await client.message_create(message.channel,embed=embed)

@UTILITY_COMMANDS.from_class
class rawr:
    @Cooldown('channel', 60.0, handler = CooldownHandler())
    async def command(client, message):
        channel=message.channel
        loop=client.loop
        tasks=[]
        
        for client_ in channel.clients:
            if client_ is not client:
                if not channel.cached_permissions_for(client_).can_send_messages:
                    continue
            task=loop.create_task(client_.message_create(channel,'Rawrr !'))
            tasks.append(task)
        
        try:
            await WaitTillExc(tasks,loop)
        except:
            for task in tasks:
                task.cancel()
            raise

    category = 'UTILITY'

    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('rawr',(
            'Sends a message with every client, who can send a message to the channel.\n'
            f'Usage: `{prefix}rawr`'
            ),color=UTILITY_COLOR,).add_footer('With cooldown of 60 seconds.')
        await client.message_create(message.channel,embed=embed)

COLOR_HTML_RP=re.compile('#?([0-9a-f]{6})',re.I)
COLOR_REGULAR_RP=re.compile('([0-9]{1,3})\,? *([0-9]{1,3})\,? *([0-9]{1,3})')

@UTILITY_COMMANDS.from_class
class color:
    async def command(client,message,content):
        while True:
            parsed=COLOR_HTML_RP.fullmatch(content)
            if parsed is not None:
                full_color=int(parsed.group(1),base=16)
                color_r=(full_color&0xff0000)>>16
                color_g=(full_color&0x00ff00)>>8
                color_b=(full_color&0x00ff)
                break
            
            parsed=COLOR_REGULAR_RP.fullmatch(content)
            if parsed is not None:
                color_r,color_g,color_b=parsed.groups()
                color_r=int(color_r)
                if color_r>255:
                    return
                color_g=int(color_g)
                if color_g>255:
                    return
                color_b=int(color_b)
                if color_b>255:
                    return
                full_color=(color_r<<16)|(color_g<<8)|color_b
                break
            
            return
        
        color=(color_r,color_g,color_b)
        
        embed=Embed(content,color=full_color)
        embed.add_image('attachment://color.png')
        
        with ReuBytesIO() as buffer:
            image=PIL.new('RGB',(120,30),color)
            image.save(buffer,'png')
            buffer.seek(0)
            
            await client.message_create(message.channel,embed=embed,file=('color.png',buffer))
    
    category = 'UTILITY'
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('color',(
            'Do you wanna see a color?\n'
            f'Usage: `{prefix}color *color*`\n'
            'I accept regular RGB or HTML color format.'
                ),color=UTILITY_COLOR)
        await client.message_create(message.channel,embed=embed)

@UTILITY_COMMANDS.from_class
class update_application_info:
    async def update_application_info(client, message, user:Converter('user', flags=ConverterFlag.user_default.update_by_keys(everywhere=True), default_code='client')):
        if type(user) is Client:
            await user.update_application_info()
            content = f'Application info of `{user:f}` is updated succesfully!'
        else:
             content = 'I can update application info only of a client.'
        
        await client.message_create(message.channel, content)
    
    category = 'UTILITY'
    checks = [checks.owner_only()]
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('update_application_info',(
            'I can update applicaction info of any of the active clients '
            'at my mansion.\n'
            f'Usage: `{prefix}update_application_info <user>`\n'
            '`user` is otional and can be only an another client.'
                ),color=UTILITY_COLOR).add_footer(
                'Owner only!')
        await client.message_create(message.channel,embed=embed)


@UTILITY_COMMANDS.from_class
class resend_webhook:
    async def command(client,message,message_id:int,channel : Converter('channel', default_code='message.channel')):
        permissions=message.channel.cached_permissions_for(client)
        can_delete=permissions.can_manage_messages
        
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
        if webhooks:
            webhook=webhooks[0]
        else:
            webhook = await client.webhook_create(channel,'Love You')
    
        await client.webhook_send(webhook,
            embed=target_message.embeds,
            name=target_message.author.name,
            avatar_url=target_message.author.avatar_url)
    
    category = 'UTILITY'
    checks = [checks.guild_only(), checks.owner_only()]
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('resend_webhook',(
            'I can resend a webhook, if chu really want.\n'
            f'Usage: `{prefix}resend_webhook *message_id* <channel>`\n'
            'The `message_id` must be the `id` of the message sent by the '
            'webhook.\n'
            'The `channel` by default is zhis channel, but if the message '
            'is at a different channel, you should tell me > <.'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only. Owner only!')
        await client.message_create(message.channel,embed=embed)


@UTILITY_COMMANDS.from_class
class se:
    async def command(client,message,emoji : Emoji):
        if emoji.is_custom_emoji():
            await client.message_create(message.channel,f'**Name:** {emoji:e} **Link:** {emoji.url}')
    
    category = 'UTILITY'
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('se',(
            '`se` stands for `show emoji`.\n'
            f'Usage: `{prefix}se *emoji*`\n'
            'I can show only custom emojis.'
                ),color=UTILITY_COLOR)
        await client.message_create(message.channel,embed=embed)


def add_activity(text,activity):
    ACTIVITY_FLAG=activity.ACTIVITY_FLAG
    
    text.append(activity.name)
    text.append('\n')
    text.append(f'**>>** type : {("game","stream","spotify","watching","custom")[activity.type]} ({activity.type})\n')

    if ACTIVITY_FLAG&0b0000000000000001:
        if activity.timestamp_start:
            text.append(f'**>>** started : {elapsed_time(activity.start)} ago\n')
        if activity.timestamp_end:
            text.append(f'**>>** ends after : {elapsed_time(activity.end)}\n')

    if ACTIVITY_FLAG&0b0000000000000010:
        if activity.details:
            text.append(f'**>>** details : {activity.details}\n')

    if ACTIVITY_FLAG&0b0000000000000100:
        if activity.state is not None:
            text.append(f'**>>** state : {activity.state}\n')
            
    if ACTIVITY_FLAG&0b0000000000001000:
        if activity.party_id:
            text.append(f'**>>** party id : {activity.party_id}\n')
        if activity.party_size:
            text.append(f'**>>** party size : {activity.party_size}\n')
        if activity.party_max:
            text.append(f'**>>** party limit : {activity.party_max}\n')

    if ACTIVITY_FLAG&0b0000000000010000:
        if ACTIVITY_FLAG&0b0000010000000000:
            if activity.asset_image_large:
                text.append(f'**>>** asset image large url : {activity.image_large_url}\n')
            if activity.asset_text_large:
                text.append(f'**>>** asset text large : {activity.asset_text_large}\n')
            if activity.asset_image_small:
                text.append(f'**>>** asset image small url : {activity.image_small_url}\n')
            if activity.asset_text_small:
                text.append(f'**>>** asset text small : {activity.asset_text_small}\n')
            
        elif activity.type==ActivitySpotify.type:
            album_cover_url=activity.album_cover_url
            if album_cover_url is not None:
                text.append(f'**>>** album cover : {album_cover_url}\n')
        
    if ACTIVITY_FLAG&0b0000000000100000:
        if activity.secret_join:
            text.append(f'**>>** secret join : {activity.secret_join}\n')
        if activity.secret_spectate:
            text.append(f'**>>** secret spectate : {activity.secret_spectate}\n')
        if activity.secret_match:
            text.append(f'**>>** secret match : {activity.secret_match}\n')
            
    if ACTIVITY_FLAG&0b0000000001000000:
        if activity.url:
            text.append(f'**>>** url : {activity.url}\n')

    if ACTIVITY_FLAG&0b0000000010000000:
        if activity.sync_id:
            text.append(f'**>>** sync id : {activity.sync_id}\n')

    if ACTIVITY_FLAG&0b0000000100000000:
        if activity.session_id:
            text.append(f'**>>** session id : {activity.session_id}\n')

    if ACTIVITY_FLAG&0b0000001000000000:
        if activity.flags:
            text.append(f'**>>** flags : {activity.flags} ({", ".join(list(activity.flags))})\n')

    if ACTIVITY_FLAG&0b0000010000000000:
        if activity.application_id:
            text.append(f'**>>** application id : {activity.application_id}\n')

    if ACTIVITY_FLAG&0b0000100000000000:
        if activity.emoji is not None:
            text.append(f'**>>** emoji : {activity.emoji.as_emoji}\n')

    created_at=activity.created_at
    if created_at is not None:
        text.append(f'**>>** created at : {elapsed_time(created_at)} ago\n')

    if ACTIVITY_FLAG&0b0001000000000000:
        text.append(f'**>>** id : {activity.id}\n')

@UTILITY_COMMANDS.from_class
class user_info:
    async def command(client, message, user : Converter('user', ConverterFlag.user_default.update_by_keys(everywhere = True, profile = True), default_code='message.author')):
        guild=message.guild
        
        embed=Embed(user.full_name)
        embed.add_field('User Information',
            f'Created: {elapsed_time(user.created_at)} ago\n'
            f'Profile: {user:m}\n'
            f'ID: {user.id}')
        
        try:
            profile=user.guild_profiles[guild]
        except KeyError:
            if user.avatar:
                embed.color=user.avatar&0xFFFFFF
            else:
                embed.color=user.default_avatar.color
        else:
            embed.color=user.color(guild)
            roles = profile.roles
            if roles:
                roles.sort()
                roles=', '.join(role.mention for role in reversed(roles))
            else:
                roles='none'
            text=[]
            if profile.nick is not None:
                text.append(f'Nick: {profile.nick}')
            if profile.joined_at is None:
                await client.guild_user_get(user.id)
            text.append(f'Joined: {elapsed_time(profile.joined_at)} ago')
            boosts_since=profile.boosts_since
            if boosts_since is not None:
                text.append(f'Booster since: {elapsed_time(boosts_since)}')
            text.append(f'Roles: {roles}')
            embed.add_field('In guild profile','\n'.join(text))
        
        embed.add_thumbnail(user.avatar_url_as(size=128))
    
        if user.activity is not ActivityUnknown or user.status is not Status.offline:
            text=[]
            
            if user.status is Status.offline:
                text.append('Status : offline\n')
            elif len(user.statuses)==1:
                for platform,status in user.statuses.items():
                    text.append(f'Status : {status} ({platform})\n')
            else:
                text.append('Statuses :\n')
                for platform,status in user.statuses.items():
                    text.append(f'**>>** {status} ({platform})\n')
            
            if user.activity is ActivityUnknown:
                text.append('Activity : *unknown*\n')
            elif len(user.activities)==1:
                text.append('Activity : ')
                add_activity(text,user.activities[0])
            else:
                text.append('Activities : \n')
                for index,activity in enumerate(user.activities,1):
                    text.append(f'{index}.: ')
                    add_activity(text,activity)
                    
            embed.add_field('Status and Activity',''.join(text))
        await client.message_create(message.channel,embed=embed)
        
    name='user'
    category = 'UTILITY'
    aliases = ['profile']
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('user',(
            'I show you some information about the given user.\n'
            'If you use it inside of a guild and the user is inside as well, '
            'will show information, about their guild profile too.\n'
            f'Usage: `{prefix}user <user>`\n'
            'If no user is passed, I will tell your secrets :3'
            ),color=UTILITY_COLOR)
        await client.message_create(message.channel,embed=embed)


GREEN_HEART = BUILTIN_EMOJIS['green_heart']
YELLOW_HEART = BUILTIN_EMOJIS['yellow_heart']
RED_HEART = BUILTIN_EMOJIS['heart']
BLACK_HEART = BUILTIN_EMOJIS['black_heart']

@UTILITY_COMMANDS.from_class
class guild_info:
    async def command(client,message):
        guild=message.guild
        if guild is None:
            return
    
        #most usual first
        s_grey  = Status.offline
        s_green = Status.online
        s_yellow= Status.idle
        s_red   = Status.dnd
        
        v_grey  = 0
        v_green = 0
        v_yellow= 0
        v_red   = 0
    
        for user in guild.users.values():
            status=user.status
            if   status is s_grey:
                v_grey+=1
            elif status is s_green:
                v_green+=1
            elif status is s_yellow:
                v_yellow+=1
            elif status is s_red:
                v_red+=1
            else: #if we change our satus to invisible, it will be invisible till we get the dispatch event, then it turns offline.
                v_grey+=1
        
        del s_grey
        del s_green
        del s_yellow
        del s_red
        
        channel_text    = 0
        channel_category= 0
        channel_voice   = 0
        
        for channel in guild.all_channel.values():
            if type(channel) is ChannelText:
                channel_text+=1
            elif type(channel) is ChannelCategory:
                channel_category+=1
            else:
                channel_voice+=1
        
        if guild.features:
            features=', '.join(feature.name for feature in guild.features)
        else:
            features='none'
        
        embed=Embed(guild.name,color=guild.icon&0xFFFFFF if guild.icon else (guild.id>>22)&0xFFFFFF)
        embed.add_field('Guild information',
            f'Created: {elapsed_time(guild.created_at)} ago\n'
            f'Voice region: {guild.region}\n'
            f'Features: {features}\n')
        embed.add_field('Counts',
            f'Users: {guild.user_count}\n'
            f'Roles: {len(guild.roles)}\n'
            f'Text channels: {channel_text}\n'
            f'Voice channels: {channel_voice}\n'
            f'Category channels: {channel_category}\n')
        embed.add_field('Users',
            f'{GREEN_HEART:e} {v_green}\n'
            f'{YELLOW_HEART:e} {v_yellow}\n'
            f'{RED_HEART:e} {v_red}\n'
            f'{BLACK_HEART:e} {v_grey}\n')
    
        boosters=guild.boosters
        if boosters:
            emoji=BUILTIN_EMOJIS['gift_heart']
            count=len(boosters)
            to_render=count if count<21 else 21
            
            embed.add_field('Most awesome people of the guild',
                            f'{to_render} {emoji:e} out of {count} {emoji:e}')
    
            for user in boosters[:21]:
                embed.add_field(user.full_name,
                    f'since: {elapsed_time(user.guild_profiles[guild].boosts_since)}')
        
        embed.add_thumbnail(guild.icon_url_as(size=128))
    
        await client.message_create(message.channel,embed=embed)
    
    name = 'guild'
    category = 'UTILITY'
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('user',(
            'Do you want me to list, some information about this guild?\n'
            f'Usage: `{prefix}guild`\n'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only!')
        await client.message_create(message.channel,embed=embed)

@UTILITY_COMMANDS.from_class
class message:
    async def command(client,message,message_id:int,channel:Converter('channel', default_code='message.channel')):
        if not channel.cached_permissions_for(client).can_read_message_history:
            await client.message_create(message.channel,
                'I am unable to read the messages at the specified channel.')
            return
        
        try:
            target_message = await client.message_get(channel,message_id)
        except DiscordException as err:
            await client.message_create(message.channel,err.__repr__())
            return
        await Pagination(client,message.channel,[Embed(description=chunk) for chunk in pchunkify(target_message)])
    
    category = 'UTILITY'
    checks=[checks.has_permissions(Permission().update_by_keys(administrator=True))]
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('message',(
            'If you want, I show the representation of a message.\n'
            f'Usage: `{prefix}message *message_id* <channel>`\n'
            'By default `channel` is the channel, where you used the command.'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only! Administrator only!')
        await client.message_create(message.channel,embed=embed)


@UTILITY_COMMANDS.from_class
class message_pure:
    async def command(client,message,message_id:int,channel:Converter('channel',default_code='message.channel')):
        if not channel.cached_permissions_for(client).can_read_message_history:
            await client.message_create(message.channel,
                'I am unable to read the messages at the specified channel.')
            return
        
        try:
            data = await client.http.message_get(channel.id,message_id)
        except DiscordException as err:
            await client.message_create(message.channel,repr(err))
            return
        
        await Pagination(client,message.channel,[Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())])
    
    category = 'UTILITY'
    checks=[checks.has_permissions(Permission().update_by_keys(administrator=True))]
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('message_pure',(
            'If you want, I show the pure json representing a message.\n'
            f'Usage: `{prefix}message_pure *message_id* <channel>`\n'
            'By default `channel` is the channel, where you used the command.'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only! Administrator only!')
        await client.message_create(message.channel,embed=embed)

@UTILITY_COMMANDS.from_class
class roles:
    class command(object):
        __slots__=('cache','guild','roles',)
        async def __new__(cls,client,message):
            channel=message.channel
            self=object.__new__(cls)
            self.roles=list(reversed(channel.guild.roles))
            self.cache=[None for _ in range(len(self.roles)+1)]
            self.createpage0(channel.guild)
            #we return awaitable, so it is OK
            return await PAGINATION_5PN(client,channel,self)
            
        def __len__(self):
            return self.cache.__len__()
        
        def createpage0(self,guild):
            embed=Embed(f'Roles of **{guild.name}**:',
                '\n'.join([role.mention for role in self.roles]),
                color=guild.icon&0xFFFFFF if guild.icon else (guild.id>>22)&0xFFFFFF)
            embed.add_footer(f'Page 1 /  {len(self.cache)}')
            self.cache[0]=embed
        
        def __getitem__(self,index):
            page=self.cache[index]
            if page is None:
                return self.create_page(index)
            return page
        
        def create_page(self,index):
            role=self.roles[index-1]
            embed=Embed(role.name,
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
            
            self.cache[index]=embed
            return embed
    
    category = 'UTILITY'
    checks = [checks.guild_only()]
    
    async def description(client,message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('roles',(
            'Cutie, do you want me, to list the roles of the guild and their '
            'permissions?\n'
            f'Usage: `{prefix}roles`'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only!')
        await client.message_create(message.channel,embed=embed)

@UTILITY_COMMANDS.from_class
class avatar:
    async def command(client, message, user : Converter('user',flags=ConverterFlag.user_default.update_by_keys(everywhere=True),default_code='message.author')):
        color = user.avatar&0xffffff
        if color==0:
            color = user.default_avatar.color
        
        url=user.avatar_url_as(size=4096)
        embed=Embed(f'{user:f}\'s avatar', color=color, url=url)
        embed.add_image(url)
        
        await client.message_create(message.channel, embed=embed)
    
    category = 'UTILITY'
    
    async def description(client,message):
        prefix=client.events.message_create.prefix(message)
        embed=Embed('avatar',(
            'Pure 4K user avatar showcase!\n'
            f'Usage: `{prefix}avatar <user>`\n'
            'If no `user` is passed, I will showcase your avatar.'
                ),color=UTILITY_COLOR)
        await client.message_create(message.channel,embed=embed)

@UTILITY_COMMANDS.from_class
class guild_icon:
    async def command(client, message):
        guild = message.guild
        if guild is None:
            return
        
        icon_url = guild.icon_url_as(size=4096)
        if icon_url is None:
            embed=Embed(description=f'`{guild.name}` has no icon.')
        else:
            color=guild.icon&0xffffff
            embed=Embed(f'{guild.name}\' icon', color=color, url=icon_url)
            embed.add_image(icon_url)
        
        await client.message_create(message.channel,embed=embed)
    
    name='guild-icon'
    category = 'UTILITY'
    
    async def description(client,message):
        prefix=client.events.message_create.prefix(message)
        embed=Embed('guild-icon',(
            'Do you wanna see the guild\'s icon in 4K?!\n'
            f'Usage: `{prefix}guild-icon`\n'
                ),color=UTILITY_COLOR).add_footer(
                'Guild only!')
        await client.message_create(message.channel,embed=embed)


