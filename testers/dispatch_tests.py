# -*- coding: utf-8 -*-
from hata import DiscordException,  cchunkify, Status, EXTRA_EMBED_TYPES, Embed, Task, Color, eventlist, Permission, \
    listdifference
from hata.discord.parsers import EVENTS, DEFAULT_EVENT
from hata.ext.prettyprint import pretty_print
from hata.ext.commands import Pagination, Command
from hata.backend.dereaddons_local import method

DISPATCH_TESTS = eventlist(type_=Command)
DISPTACH_COLOR = Color.from_rgb(120, 108, 128)

def setup(lib):
    Koishi.commands.extend(DISPATCH_TESTS)
    
def teardown(lib):
    Koishi.commands.unextend(DISPATCH_TESTS)

class dispatch_tester:
    channel=None
    old_events={}

    @classmethod
    async def here(self,client,message):
        if message.channel is self.channel:
            try:
                await client.message_create(message.channel,'Current channel removed')
            except DiscordException:
                return
            self.channel=None
        else:
            try:
                await client.message_create(message.channel,f'Channel set to {message.channel.name} {message.channel.id}')
            except DiscordException:
                return
            self.channel=message.channel
            
    @classmethod
    async def switch(self,client,message,content):
        if (not (5<len(content)<50)):
            return
        if content not in EVENTS.defaults:
            await client.message_create(message.channel,f'Invalid dispatcher: {content}')
            return
        event=getattr(self,content,None)
        if event is None:
            await client.message_create(message.channel,f'Unallowed/undefined dispatcher: {content}')
            return
        
        actual=getattr(client.events,content)
        if type(actual) is method and actual.__self__ is self:
            setattr(client.events,content,DEFAULT_EVENT)
            await client.message_create(message.channel,'Event removed')
        else:
            self.old_events[content]=actual
            setattr(client.events,content,event)
            await client.message_create(message.channel,'Event set')

    @classmethod
    async def client_edit(self,client,old):
        Task(self.old_events['client_edit'](client,old),client.loop)
        if self.channel is None:
            return
        
        result=[]
        result.append(f'Me, {client.full_name} was edited')
        for key,value in old.items():
            result.append(f'{key} changed: {value} -> {getattr(client,key)}')

        try:
            await client.message_create(self.channel,'\n'.join(result))
        except DiscordException:
            self.channel=None

    @classmethod
    async def message_delete(self,client,message):
        Task(self.old_events['message_delete'](client,message),client.loop)
        if self.channel is None:
            return
        
        text=pretty_print(message)
        text.insert(0,f'Message {message.id} got deleted')
        pages=[Embed(description=chunk) for chunk in cchunkify(text)]
        await Pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def message_edit(self,client,message,old):
        Task(self.old_events['message_edit'](client,message,old),client.loop)
        if self.channel is None:
            return
        
        result=[f'Message {message.id} was edited']

        channel=message.channel
        result.append(f'At channel : {channel:d} {channel.id}')
        guild=channel.guild
        if guild is not None:
            result.append(f'At guild : {guild.name} {guild.id}')

        for key,value in old.items():
            if key in ('pinned','activity_party_id','everyone_mention'): 
                result.append(f'{key} changed: {value!r} -> {getattr(message,key)!r}')
                continue
            if key in ('edited',):
                if value is None:
                    result.append(f'{key} changed: None -> {getattr(message,key):%Y.%m.%d-%H:%M:%S}')
                else:
                    result.append(f'{key} changed: {value:%Y.%m.%d-%H:%M:%S} -> {getattr(message,key):%Y.%m.%d-%H:%M:%S}')
                continue
            if key in ('application','activity','attachments','embeds'):
                result.append(f'{key} changed:')
                if value is None:
                    result.append('From None')
                else:
                    result.extend(pretty_print(value))
                value=getattr(message,key)
                if value is None:
                    result.append('To None')
                else:
                    result.extend(pretty_print(value))
                continue
            if key in ('content',):
                result.append(f'{key} changed from:')
                content=value
                break_=False
                while True:
                    content_ln=len(content)
                    result.append(f'{key}: (len={content_ln})')
                    if content_ln>500:
                        content=content[:500].replace('`','\\`')
                        result.append(f'--------------------\n{content}\n... +{content_ln-500} more\n--------------------')
                    else:
                        content=content.replace('`','\\`')
                        result.append(f'--------------------\n{content}\n--------------------')
                    if break_:
                        break
                    break_=True
                    content=getattr(message,key)
                    result.append('To:')
                continue
            if key in ('user_mentions','role_mentions','cross_mentions'):
                removed, added = listdifference(value,getattr(message,key))
                if removed:
                    result.append(f'{key} removed : {len(removed)}')
                    for obj in removed:
                        result.append(f'- {obj.name} {obj.id}')
                        
                if added:
                    result.append(f'{key} added : {len(added)}')
                    for obj in added:
                        result.append(f'- {obj.name} {obj.id}')
                    
                continue
            
            if key in ('flags',):
                old=list(value)
                old.sort()
                value=getattr(message,key)
                new=list(value)
                new.sort()
                removed,added=listdifference(old,new)
                if removed:
                    result.append(f'{key} removed : {len(removed)}')
                    for name in removed:
                        result.append(f'- {name}')
                        
                if added:
                    result.append(f'{key} added : {len(added)}')
                    for name in added:
                        result.append(f'- {name}')
                    
                continue

        text=cchunkify(result)
        pages=[Embed(description=chunk) for chunk in text]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def embed_update(self,client,message,flag):
        Task(self.old_events['embed_update'](client,message,flag),client.loop)
        if self.channel is None:
            return
        
        result=[f'Message {message.id} got embed update:']

        channel=message.channel
        result.append(f'At channel : {channel:d} {channel.id}')
        guild=channel.guild
        if guild is not None:
            result.append(f'At guild : {guild.name} {guild.id}')
        
        if flag==3:
            result.append('Less embeds than before???')
        else:
            if flag==1:
                result.append('Only sizes were update.')
            elif flag==2:
                result.append('Links! Links everywhere...')
            
            embeds=message.embeds
            if embeds is None:
                result.append('This should not happen, there are no embeds...')
            else:
                if flag==1:
                    for index,embed in enumerate(embeds,1):
                        if flag==1:
                            collected=[]
                            image=embed.image
                            if image is not None:
                                collected.append(('image.height',image.height))
                                collected.append(('image.width',image.width))
                            thumbnail=embed.thumbnail
                            if thumbnail is not None:
                                collected.append(('thumbnail.height',thumbnail.height))
                                collected.append(('thumbnail.width',thumbnail.width))
                            video=embed.video
                            if video is not None:
                                collected.append(('video.height',video.height))
                                collected.append(('video.width',video.width))
                            if collected:
                                result.append(f'Sizes got update at embed {index}:')
                                for name,value in collected:
                                    result.append(f'- {name} : {value}')
                elif flag==2:
                    for index,embed in enumerate(embeds,1):
                        if embed.type in EXTRA_EMBED_TYPES:
                            result.append(f'New embed appeared at index {index}:')
                            result.extend(pretty_print(embed))

        text=cchunkify(result)
        pages=[Embed(description=chunk) for chunk in text]
        await Pagination(client,self.channel,pages,120.)

        
    @classmethod
    async def reaction_clear(self,client,message,old):
        Task(self.old_events['reaction_clear'](client,message,old),client.loop)
        if self.channel is None:
            return
        
        text=pretty_print(old)
        text.insert(0,f'Reactions got cleared from message {message.id}:')
        pages=[Embed(description=chunk) for chunk in cchunkify(text)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def reaction_delete_emoji(self,client,message,emoji,users):
        Task(self.old_events['reaction_delete_emoji'](client,message,emoji,users),client.loop)
        if self.channel is None:
            return
        
        text=pretty_print(users)
        text.insert(0,f'{emoji:e} were removed from message {message.id}:')
        pages=[Embed(description=chunk) for chunk in cchunkify(text)]
        await Pagination(client,self.channel,pages,120.)
        
    @classmethod
    async def user_presence_update(self,client,user,old):
        Task(self.old_events['user_presence_update'](client,user,old),client.loop)
        if self.channel is None:
            return
        
        result=[f'Presence update on user: {user:f} {user.id}']
        try:
            statuses=old['statuses']
        except KeyError:
            pass
        else:
            for key in ('desktop','mobile','web'):
                result.append(f'{key} status: {statuses.get(key,Status.offline)} -> {user.statuses.get(key,Status.offline)}')

            try:
                status=old['status']
            except KeyError:
                pass
            else:
                result.append(f'status changed: {status} -> {user.status}')
            
        try:
            activities=old['activities']
        except KeyError:
            pass
        else:
            ignore=[]
            for activity in activities:
                if type(activity) is dict:
                    ignore.append(activity)
                    
            for activity in ignore:
                result.append('Activity updated:')
                real_activity=activity.pop('activity')
                for key,value in activity.items():
                    result.append(f'- {key} : {value} -> {getattr(real_activity,key)}')
            
            if len(ignore)!=len(activities):
                for activity in activities:
                    if activity in ignore:
                        continue
                    result.append('Removed activity:')
                    result.extend(pretty_print(activity))

            if len(ignore)!=len(user.activities):
                for activity in user.activities:
                    if activity in ignore:
                        continue
                    result.append('Added activity:')
                    result.extend(pretty_print(activity))

        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def user_edit(self,client,user,old):
        Task(self.old_events['user_edit'](client,user,old),client.loop)
        if self.channel is None:
            return
        
        result=[f'A user was updated: {user:f} {user.id}']
        for key,value in old. items():
            result.append(f'{key} : {value} -> {getattr(user,key)}')

        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)
    
    @classmethod
    async def user_profile_edit(self,client,user,old,guild):
        Task(self.old_events['user_profile_edit'](client,user,old,guild),client.loop)
        if self.channel is None:
            return
        
        result=[f'{user.full_name} {user.id} profile was edited at guild {guild.name!r} {guild.id}:']
        profile=user.guild_profiles[guild]
        for key,value in old.items():
            if key in ('nick','boosts_since'):
                result.append(f'{key} changed: {value!r} -> {getattr(profile,key)!r}')
                continue
            
            if key=='roles':
                removed, added = listdifference(value,profile.roles)
                if removed:
                    result.append(f'Roles removed: ({len(removed)})')
                    for role in removed:
                        result.append(f'- {role.name} {role.id}')
                
                if added:
                    result.append(f'Roles added: ({len(added)})')
                    for role in added:
                        result.append(f'- {role.name} {role.id}')
                continue
            
            raise RuntimeError(key)

        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def channel_delete(self,client,channel,guild):
        Task(self.old_events['channel_delete'](client,channel,guild),client.loop)
        if self.channel is None:
            return
        
        text=f'```\nA channel was deleted: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})```'
        pages=[Embed(description=text)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def channel_edit(self,client,channel,old):
        Task(self.old_events['channel_edit'](client,channel,old),client.loop)
        if self.channel is None:
            return
        
        result=[f'A channel was edited: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} {("(text) ","","(news) ")[(3+channel.type)//4]}({channel.type})']
        for key,value in old.items():
            if key=='overwrites':
                removed,added=listdifference(sorted(value),sorted(channel.overwrites))
                if removed:
                    result.append(f'Overwrites removed : ({len(removed)})')
                    for value in removed:
                        result.append(f'- {value.target!r} : {value.allow} {value.deny}')
                if added:
                    result.append(f'Overwrites added: ({len(added)})')
                    for value in added:
                        result.append(f'- {value.target!r} : {value.allow} {value.deny}')
                continue
            
            result.append(f'{key} changed: {value!r} -> {getattr(channel,key)!r}')
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def channel_create(self,client,channel):
        Task(self.old_events['channel_create'](client,channel),client.loop)
        if self.channel is None:
            return
        
        result=pretty_print(channel)
        result.insert(0,f'A channel was created: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})')
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def channel_pin_update(self,client,channel):
        Task(self.old_events['channel_pin_update'](client,channel),client.loop)
        if self.channel is None:
            return
        
        text=f'```\nA channel\'s pins changed: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})```'
        pages=[Embed(description=text)]
        await Pagination(client,self.channel,pages,120.)
    
    @classmethod
    async def emoji_create(self,client,emoji):
        Task(self.old_events['emoji_create'](client,emoji),client.loop)
        if self.channel is None:
            return
    
        result=pretty_print(emoji)
        result.insert(0,f'Emoji created: {emoji.name} {emoji.id} at guild {emoji.guild!r}')
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)
    
    @classmethod
    async def emoji_delete(self,client,emoji,guild):
        Task(self.old_events['emoji_delete'](client,emoji,guild),client.loop)
        if self.channel is None:
            return
        
        result=pretty_print(emoji)
        result.insert(0,f'Emoji deleted: {emoji.name} {emoji.id} at guild {guild!r}')
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)
        
    @classmethod
    async def emoji_edit(self,client,emoji,old):
        Task(self.old_events['emoji_edit'](client,emoji,old),client.loop)
        if self.channel is None:
            return
    
        result=[]
        result.append(f'Emoji edited: {emoji.name} {emoji.id} at guild {emoji.guild!r}')
        for key, value in old.items():
            if key=='roles':
                removed, added = listdifference(value,emoji.roles)
                
                if removed:
                    result.append(f'Removed roles: ({len(removed)})')
                    for role in removed:
                        result.append(f'- {role.name} {role.id}')
                
                if added:
                    result.append(f'Added roles: ({len(added)})')
                    for role in added:
                        result.append(f'- {role.name} {role.id}')
                
                continue
            
            result.append(f'{key}: {value} -> {getattr(emoji,key)}')
            continue
        
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def guild_user_add(self,client,guild,user):
        Task(self.old_events['guild_user_add'](client,guild,user),client.loop)
        if self.channel is None:
            return
        
        await client.message_create(self.channel,f'Welcome to the Guild {user:f}!\nThe guild reached {guild.user_count} members!')

    @classmethod
    async def guild_user_delete(self,client,guild,user,profile):
        Task(self.old_events['guild_user_delete'](client,guild,user,profile),client.loop)
        if self.channel is None:
            return
        
        text=[f'Bai bai {user.full_name}! with your {len(profile.roles)} roles.']
        if profile.boosts_since is not None:
            text.append('Also rip your boost :c')
        text.append(f'The guild is down to {guild.user_count} members!')
        
        await client.message_create(self.channel,'\n'.join(text))
        
    @classmethod
    async def guild_create(self,client,guild):
        Task(self.old_events['guild_create'](client,guild,),client.loop)
        if self.channel is None:
            return
        
        result=pretty_print(guild)
        result.insert(0,f'Guild created: {guild.id}')
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    #Unknown:
    #guild_sync
        
    @classmethod
    async def guild_edit(self,client,guild,old):
        
        Task(self.old_events['guild_edit'](client,guild,old),client.loop)
        if self.channel is None:
            return
        
        result=[f'A guild got edited {guild.name} {guild.id}']
        for key,value in old.items():
            if key in ('name', 'icon', 'splash', 'user_count', 'afk_timeout', 'available', 'has_animated_icon',
                    'description', 'vanity_code', 'banner', 'max_members', 'max_presences', 'premium_tier',
                    'booster_count', 'widget_enabled', 'embed_enabled', 'preferred_language', 'discovery_splash',
                    'max_video_channel_users', ):
                result.append(f'- {key} : {value} - > {getattr(guild,key)}')
                continue
            
            if key in ('verification_level','message_notification','mfa','content_filter','region','preferred_language'):
                other=getattr(guild,key)
                result.append(f'- {key} : {value!s} {value.value} -> {other!s} {other.value}')
                continue
            
            if key=='features':
                removed, added = listdifference(value,guild.features)
                if removed:
                    result.append(f'Features removed: ({len(removed)}')
                    for feature in removed:
                        result.append(f'- {feature.value}')
                
                if added:
                    result.append(f'Features added: ({len(added)})')
                    for feature in added:
                        result.append(f'- {feature.value}')
                
                continue
            
            if key in ('system_channel','afk_channel','widget_channel','embed_channel','rules_channel','public_updates_channel'):
                other=getattr(guild,key)
                if value is None:
                    result.append(f'{key} : None -> {other.name} {other.id}')
                elif other is None:
                    result.append(f'{key} : {value.name} {value.id} -> None')
                else:
                    result.append(f'{key} : {value.name} {value.id} -> {other.name} {other.id}')
                continue
            
            if key in ('system_channel_flags',):
                old=list(value)
                old.sort()
                new=list(getattr(guild,key))
                new.sort()
                removed, added = listdifference(old,new)
                
                if removed:
                    result.append(f'{key} removed : ({len(removed)})')
                    for name in removed:
                        result.append(f' - {name}')
                
                if added:
                    result.append(f'{key} added : ({len(added)})')
                    for name in added:
                        result.append(f' - {name}')
                continue
            
            if key in ('owner',):
                other=getattr(guild,'owner')
                result.append(f'{key} : {value.full_name} {value.id} -> {other.full_name} {other.id}')
                continue
            
            raise RuntimeError(key)

        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)
        
    @classmethod
    async def guild_delete(self,client,guild,profile):
        Task(self.old_events['guild_delete'](client,guild,profile),client.loop)
        if self.channel is None:
            return
        
        result=pretty_print(guild)
        result.insert(0,f'Guild deleted {guild.id}')
        result.insert(1,f'I had {len(profile.roles)} roles there')
        result.insert(2,'At least i did not boost' if (profile.boosts_since is None) else 'Rip by boost ahhhh...')

        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)


    @classmethod
    async def guild_ban_add(self,client,guild,user):
        Task(self.old_events['guild_ban_add'](client,guild,user),client.loop)
        if self.channel is None:
            return
        
        text=f'```\nUser {user:f} {user.id} got banned at {guild.name} {guild.id}.```'
        pages=[Embed(description=text)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def guild_ban_delete(self,client,guild,user):
        Task(self.old_events['guild_ban_delete'](client,guild,user),client.loop)
        if self.channel is None:
            return
        
        text=f'```\nUser {user:f} {user.id} got UNbanned at {guild.name} {guild.id}.```'
        pages=[Embed(description=text)]
        await Pagination(client,self.channel,pages,120.)

    #Auto dispatched:
    #guild_user_chunk
    #Need integartion:
    #integration_edit

    @classmethod
    async def role_create(self,client,role):
        Task(self.old_events['role_create'](client,role,),client.loop)
        if self.channel is None:
            return
        
        result=pretty_print(role)
        result.insert(0,f'A role got created at {role.guild.name} {role.guild.id}')
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def role_delete(self,client,role,guild):
        Task(self.old_events['role_delete'](client,role,guild),client.loop)
        if self.channel is None:
            return
        
        text=f'```\nA role got deleted at {role.guild.name} {role.guild.id}\nRole: {role.name} {role.id}```'
        pages=[Embed(description=text)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def role_edit(self,client,role,old):
        Task(self.old_events['role_edit'](client,role,old),client.loop)
        if self.channel is None:
            return
        
        result=[f'A role got edited at {role.guild.name} {role.guild.id}\nRole: {role.name} {role.id}']
        for key,value in old.items():
            if key in ('name','separated','managed','mentionable','position',):
                result.append(f'{key} : {value} -> {getattr(role,key)}')
                continue
            if key=='color':
                result.append(f'{key} : {value.as_html} -> {role.color.as_html}')
                continue
            if key=='permissions':
                result.append('permissions :')
                other=role.permissions
                for name,index in Permission.__keys__.items():
                    old_value=(value>>index)&1
                    new_value=(other>>index)&1
                    if old_value!=new_value:
                        result.append(f'{name} : {bool(old_value)} -> {bool(new_value)}')
                continue
        
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)
    
    @classmethod
    async def webhook_update(self,client,channel):
        Task(self.old_events['webhook_update'](client,channel),client.loop)
        if self.channel is None:
            return
        
        text=f'```\nwebhooks got updated at guild: {channel.name} {channel.id}```'
        pages=[Embed(description=text)]
        await Pagination(client,self.channel,pages,120.)
        
    @classmethod
    async def voice_state_update(self,client,state,action,old):
        Task(self.old_events['voice_state_update'](client,state,action,old),client.loop)
        if self.channel is None:
            return
        
        result=[]
        user=state.user
        if action=='l':
            result.append('Voice state update, action: leave')
            result.extend(pretty_print(state))
        elif action=='j':
            result.append('Voice state update, action: join')
            result.extend(pretty_print(state))
        else:
            result.append('Voice state update, action: update')
            user=state.user
            if user.partial:
                result.append(f'user : Parital user {user.id}')
            else:
                result.append(f'user : {user.full_name} ({user.id})')
            guild=state.channel.guild
            if guild is not None:
                result.append(f'guild : {guild.name} ({guild.id})')
            result.append(f'session_id : {state.session_id!r}')
            result.append('Changes:')
            for key,value in old.items():
                if key=='channel':
                    other=state.channel
                    result.append(f'channel : {value.name} {value.id} -> {other.name} {other.id}')
                    continue
                result.append(f'{key} : {value} -> {getattr(state,key)}')

        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)
            
    @classmethod
    async def typing(self,client,channel,user,timestamp):
        Task(self.old_events['typing'](client,channel,user,timestamp),client.loop)
        if self.channel is None:
            return
        
        result=['Typing:']
        if user.partial:
            result.append(f'user : Parital user {user.id}')
        else:
            result.append(f'user : {user.full_name} ({user.id})')
        result.append(f'channel : {channel.name} {channel.id}')
        result.append(f'timestamp : {timestamp:%Y.%m.%d-%H:%M:%S}')
        
        pages=[Embed(description=chunk) for chunk in cchunkify(result)]
        await Pagination(client,self.channel,pages,120.)

    @classmethod
    async def client_edit_settings(self,client,old):
        Task(self.old_events['client_edit_settings'](client,old),client.loop)
        if self.channel is None:
            return
        
        result=['The client\'s settings were updated:','```']
        for key,value in old.items():
            result.append(f' {key} : {value!r} -> {getattr(client.settings,key)!r}')
        result.append('```')
        await client.message_create(self.channel,'\n'.join(result))
    
    @classmethod
    async def invite_create(self,client,invite):
        Task(self.old_events['invite_create'](client,invite),client.loop)
        if self.channel is None:
            return
    
        text=pretty_print(invite)
        text.insert(0,f'Invite created:')
        pages=[Embed(description=chunk) for chunk in cchunkify(text)]
        await Pagination(client,self.channel,pages,120.)
    
    @classmethod
    async def invite_delete(self,client,invite):
        Task(self.old_events['invite_delete'](client,invite),client.loop)
        if self.channel is None:
            return
    
        text=pretty_print(invite)
        text.insert(0,f'Invite deleted:')
        pages=[Embed(description=chunk) for chunk in cchunkify(text)]
        await Pagination(client,self.channel,pages,120.)

async def here_description(client,message):
    prefix=client.command_processer.prefix(message)
    embed=Embed('here',(
        'I set the dispatch tester commands\' output to this channel.\n'
        f'Usage: `{prefix}here`\n'
        'By calling the command again, I ll remove the current channel.\n'
        'You can switch the dispatch testers, like:\n'
        f'`{prefix}switch *event_name*`\n'
        'For the event names, use:\n'
        f'`{prefix}help switch`'
            ),color=DISPTACH_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

async def switch_description(client,message):
    prefix=client.command_processer.prefix(message)
    embed=Embed('here',(
        'I can turn on a dispatch tester for you.\n'
        f'`{prefix}switch *event_name*`\n'
        'The list of defined testers:\n'
        '- `channel_create`\n'
        '- `channel_delete`\n'
        '- `channel_edit`\n'
        '- `channel_pin_update`\n'
        '- `client_edit_settings`\n'
        '- `client_edit`\n'
        '- `embed_update`\n'
        '- `emoji_create`\n'
        '- `emoji_delete`\n'
        '- `emoji_edit`\n'
        '- `guild_ban_add`\n'
        '- `guild_ban_delete`\n'
        '- `guild_create`\n'
        '- `guild_delete`\n'
        '- `guild_edit`\n'
        '- `guild_user_add`\n'
        '- `guild_user_delete`\n'
        '- `invite_create`\n'
        '- `invite_delete`\n'
        '- `message_delete`\n'
        '- `message_edit`\n'
        '- `reaction_clear`\n'
        '- `reaction_delete_emoji`\n'
        '- `role_create`\n'
        '- `role_delete`\n'
        '- `role_edit`\n'
        '- `typing`\n'
        '- `user_edit`\n'
        '- `user_presence_update`\n'
        '- `user_profile_edit`\n'
        '- `voice_state_update`\n'
        '- `webhook_update`\n'
        'The full list of events can be found [here]'
        '(https://github.com/HuyaneMatsu/hata/blob/master/docs/ref/EventDescriptor.md).\n'
        f'For setting channel, use: `{prefix}here`'
            ),color=DISPTACH_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

DISPATCH_TESTS(dispatch_tester.here,description=here_description,category='TEST COMMANDS')
DISPATCH_TESTS(dispatch_tester.switch,description=switch_description,category='TEST COMMANDS')
