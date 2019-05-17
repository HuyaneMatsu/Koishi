# -*- coding: utf-8 -*-
from hata.exceptions import HTTPException,Forbidden
from hata.parsers import EVENTS,default_event
from hata.prettyprint import pchunkify,pretty_print
from hata.events import pagination
from hata.others import cchunkify,Statuses
from hata.permission import PERM_KEYS

class dispatch_tester:
    channel=None

    @classmethod
    async def here(self,client,message,content):
        if message.author is not client.owner:
            return
        if message.channel is self.channel:
            try:
                await client.message_create(message.channel,'Current channel removed')
            except (HTTPException,Forbidden):
                return
            self.channel=None
        else:
            try:
                await client.message_create(message.channel,f'Channel set to {message.channel.name} {message.channel.id}')
            except (HTTPException,Forbidden):
                return
            self.channel=message.channel
            
    @classmethod
    async def switch(self,client,message,content):
        if message.author is not client.owner or not (5<len(content)<50):
            return
        if content not in EVENTS.defaults:
            await client.message_create(message.channel,f'Invalid dispatcher: {content}')
            return
        event=getattr(self,content,None)
        if event is None:
            await client.message_create(message.channel,f'Unallowed/undefined dispatcher: {content}')
            return
        
        actual=getattr(client.events,content)

        if actual is default_event:
            try:
                await client.message_create(message.channel,'Event set')
            except (HTTPException,Forbidden):
                return
            setattr(client.events,content,event)
        else:
            try:
                await client.message_create(message.channel,'Event removed')
            except (HTTPException,Forbidden):
                return
            setattr(client.events,content,default_event)

    @classmethod
    async def client_edit(self,client,old):
        if self.channel is None:
            return
        result=[]
        result.append(f'Me, {client:f} got edited')
        for key,value in old.items():
            result.append(f'- {key} got changed: {value} -> {getattr(client,key)}')

        try:
            await client.message_create(self.channel,'\n'.join(result))
        except (HTTPException,Forbidden):
            self.channel=None

    @classmethod
    async def message_delete(self,client,message):
        text=pretty_print(message)
        text.insert(0,f'Message {message.id} got deleted')
        pages=[{'content':chunk} for chunk in cchunkify(text)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def message_edit(self,client,message,old):
        if self.channel is None:
            return
        result=[f'Message {message.id} got edited']

        for key,value in old.items():
            if key in ('pinned','activity_party_id','everyone_mention'): 
                result.append(f'- {key} got changed: {value!r} -> {getattr(message,key)!r}')
                continue
            if key in ('edited',):
                if value is None:
                    result.append(f'- {key} got changed: None -> {getattr(message,key):%Y.%m.%d-%H:%M:%S}')
                else:
                    result.append(f'- {key} got changed: {value:%Y.%m.%d-%H:%M:%S} -> {getattr(message,key):%Y.%m.%d-%H:%M:%S}')
                continue
            if key in ('application','activity','attachments','embeds'):
                result.append(f'- {key} got changed:')
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
                result.append(f'- {key} got changed from:')
                content=value
                break_=False
                while True:
                    content_ln=len(content)
                    result.append(f'- content: (len={content_ln})')
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
            if key in ('user_mentions','role_mentions'):
                result.append(f'- {key} got changed from:')
                break_=False
                while True:
                    if vlaue is None:
                        resutl.append('    - None -')
                    else:
                        for index,obj in enumerate(1,value):
                            result.append(f'    - {obj.name} {obj.id}')
                if break_:
                    break
                result.append('To:')
                value=getattr(message,key)
                break_=True
                continue
            
        text=cchunkify(result)
        pages=[{'content':chunk} for chunk in text]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def reaction_clear(self,client,message,old):
        if self.channel is None:
            return
        text=pretty_print(old)
        text.insert(0,f'Reactions got cleared from message {message.id}:')
        pages=[{'content':chunk} for chunk in cchunkify(text)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def user_presence_update(self,client,user,old):
        result=[f'Presence update on user: {user:f} {user.id}']
        try:
            statuses=old['statuses']
        except KeyError:
            pass
        else:
            for key in ('desktop','mobile','web'):
                result.append(f'- {key} status: {statuses.get(key,Statuses.offline)} -> {user.statuses.get(key,Statuses.offline)}')

            try:
                status=old['status']
            except KeyError:
                pass
            else:
                result.append(f'- status changed: {status} -> {user.status}')
            
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
                activity=activity.pop('activity')
                for key,value in activity.items():
                    result.append(f'- {key} : {value} -> {getattr(activity,key)}')
            
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

        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def user_edit(self,client,user,old):
        result=[f'A user got updated: {user:f} {user.id}']
        for key,value in old. items():
            result.append(f'- {key} : {value} -> {getattr(user,key)}')

        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions
    
    @classmethod
    async def user_profile_edit(self,client,user,old,guild):
        result=[f'{user:f} {user.id} profile got edited at guild {guild.name!r} {guild.id}:']
        profile=user.guild_profiles[guild]
        for key,value in old.items():
            if key in ('nick',):
                result.append(f'{key} changed: {value!r} -> {getattr(profile,key)!r}')
                continue
            if key=='roles':
                removed=value[0]
                if removed:
                    result.append(f'Roles removed: ({len(removed)})')
                    for role in removed:
                        result.append(f'- {role.name} {role.id}')
                added=value[1]
                if added:
                    result.append(f'Roles added: ({len(added)})')
                    for role in added:
                        result.append(f'- {role.name} {role.id}')
            continue


        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def channel_delete(self,client,channel):
        text=f'```\nA channel got deleted: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})```'
        pages=[{'content':text}]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def channel_edit(self,client,channel,old):
        result=[f'A channel got edited: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} {("(text) ","","(news) ")[(3+channel.type)//4]}({channel.type})']
        for key,value in old.items():
            result.append(f'{key} changed: {value!r} -> {getattr(channel,key)!r}')
        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def channel_create(self,client,channel):
        result=pretty_print(channel)
        result.insert(0,f'A channel got created: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})')
        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def channel_pin_update(self,client,channel):
        text=f'```\nA channel\'s pins changed: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})```'
        pages=[{'content':text}]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

        
    @classmethod
    async def emoji_edit(self,client,guild,changes):
        if self.channel is None:
            return
    
        result=[]
        for modtype,emoji,diff in modifications:
            if modtype=='n':
                result.append(f'New emoji: "{emoji.name}" : {emoji}')
                continue
            if modtype=='d':
                result.append(f'Deleted emoji: "{emoji.name}" : {emoji}')
                continue
            if modtype=='e':
                result.append(f'Emoji edited: "{emoji.name}" : {emoji}\n')
                for key,value in diff.items():
                    result.append(f'- {key}: {value} -> {getattr(emoji,key)}')
                continue
            raise RuntimeError #bugged?
        
        pages=[{'content':chunk} for chunk in chunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def guild_user_add(self,client,guild,user):
        if guild.owner  is not client.owner:
            return
        channel=guild.system_channel
        if channel is None:
            return
        await client.message_create(channel,f'Welcome to the Guild {user:f}!\nThe guild reached {guild.user_count} members!')

    @classmethod
    async def guild_user_delete(self,client,guild,user,profile):
        if guild.owner is not client.owner:
            return
        channel=guild.system_channel
        if channel is None:
            return
        await client.message_create(channel,f'Bai bai {user:f}! with your {len(profile.roles)} roles.\nThe guild is down to {guild.user_count} members!')
        if guild in user.guild_profiles:
            raise RuntimeError
        
    @classmethod
    async def guild_create(self,client,guild):
        if self.channel is None:
            return
        result=pretty_print(guild)
        result.insert(0,f'Guild created: {guild.id}')
        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    #Unknown:
    #guild_sync
        
    @classmethod
    async def guild_edit(self,client,guild,old):
        if self.channel is None:
            return
        result=[f'A guild got edited {guild.name} {guild.id}']
        for key,value in old.items():
            if key in ('name','icon','splash','user_count','afk_timeout','available'):
                result.append(f' - {key} : {value} - > {getattr(guild,key)}')
                continue
            if key in ('verification_level','message_notification','mfa','content_filter','region'):
                other=getattr(guild,key)
                result.append(f' - {key} : {value!s} {value.value} -> {other!s} {other.value}')
                continue
            if key in ('features',):
                result.append(f'{key}:')
                removed=value[0]
                if removed:
                    result.append(f'- {key} removed: ({len(removed)}')
                    for subvalue in removed:
                        result.append(f'- {subvalue.value}')
                added=value[1]
                if added:
                    result.append(f'- {key} added: ({len(added)})')
                    for subvalue in added:
                        result.append(f'- {subvalue.value}')
                continue
            if key in ('system_channel','afk_channel','widget_channel','embed_channel'):
                other=getattr(guild,key)
                if value is None:
                    result.append(f'- {key} : None -> {other.name} {other.id}')
                elif other is None:
                    result.append(f'- {key} : {value.name} {value.id} -> None')
                else:
                    result.append(f'- {key} : {value.name} {value.id} -> {other.name} {other.id}')
                continue

            if key in ('owner',):
                other=getattr(guild,'owner')
                result.append(f'- {key} : {value:f} {value.id} -> {other:f} {other.id}')
                continue
            raise RuntimeError(key)

        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions
        
    @classmethod
    async def guild_delete(self,client,guild):
        if self.channel is None:
            return
        result=pretty_print(guild)
        result.insert(0,f'Guild deleted {guild.id}')
        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions


    @classmethod
    async def guild_ban_add(self,client,guild,user):
        if self.channel is None:
            return
        text=f'```\nUser {user:f} {user.id} got banned at {guild.name} {guild.id}.```'
        pages=[{'content':text}]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def guild_ban_delete(self,client,guild,user):
        if self.channel is None:
            return
        text=f'```\nUser {user:f} {user.id} got UNbanned at {guild.name} {guild.id}.```'
        pages=[{'content':text}]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    #Auto dispatched:
    #guild_user_chunk
    #Need integartion:
    #integration_edit

    @classmethod
    async def role_create(self,client,role):
        if self.channel is None:
            return
        result=pretty_print(role)
        result.insert(0,f'A role got created at {role.guild.name} {role.guild.id}')
        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def role_delete(self,client,role):
        if self.channel is None:
            return
        text=f'```\nA role got deleted at {role.guild.name} {role.guild.id}\nRole: {role.name} {role.id}```'
        pages=[{'content':text}]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def role_edit(self,client,role,old):
        if self.channel is None:
            return
        result=[f'A role got edited at {role.guild.name} {role.guild.id}\nRole: {role.name} {role.id}']
        for key,value in old.items():
            if key in ('name','separated','managed','mentionable','position',):
                result.append(f'- {key} : {value} -> {getattr(role,key)}')
                continue
            if key=='color':
                result.append(f'- {key} : {value.as_html} -> {role.color.as_html}')
                continue
            if key=='permissions':
                result.append('- permissions :')
                other=role.permissions
                for name,index in PERM_KEYS.items():
                    old_value=(value>>index)&1
                    new_value=(other>>index)&1
                    if old_value!=new_value:
                        result.append(f'   {name} : {bool(old_value)} -> {bool(new_value)}')
                continue

        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions

    @classmethod
    async def webhook_update(self,client,channel):
        if self.channel is None:
            return
        text=f'```\nwebhooks got updated at guild: {channel.name} {channel.id}```'
        pages=[{'content':text}]
        pagination(client,self.channel,pages,120.) #does not raises exceptions
        
    @classmethod
    async def voice_state_update(self,client,state,action,old):
        if self.channel is None:
            return
        result=[]
        user=state.user
        if user.partial:
            name='partail user'
        else:
            name=user.name
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
                result.append(f'- user : Parital user {user.id}')
            else:
                result.append(f'- user : {user:f} ({user.id})')
            guild=state.channel.guild
            if guild is not None:
                result.append(f'- guild : {guild.name} ({guild.id})')
            result.append(f'- session_id : {state.session_id!r}')
            result.append('Changes:')
            for key,value in old.items():
                if key=='channel':
                    other=state.channel
                    result.append(f'- channel : {value.name} {value.id} -> {other.name} {other.id}')
                    continue
                result.append(f'- {key} : {value} -> {getattr(state,key)}')

        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions
            
    @classmethod
    async def typing(self,client,channel,user,timestamp):
        if self.channel is None:
            return
        result=['Typing:']
        if user.partial:
            result.append(f'- user : Parital user {user.id}')
        else:
            result.append(f'- user : {user:f} ({user.id})')
        result.append(f'- channel : {channel.name} {channel.id}')
        result.append(f'- timestamp : {timestamp:%Y.%m.%d-%H:%M:%S}')
        
        pages=[{'content':chunk} for chunk in cchunkify(result)]
        pagination(client,self.channel,pages,120.) #does not raises exceptions        
