# -*- coding: utf-8 -*-

# - : - # infos.py # - : - #

@infos.add('list')
async def parse_list_command(client,message,content):
    guild=message.guild
    if guild is None or not guild.permissions_for(message.author).can_administrator:
        return
    key=''
    text=''
    while True:
        content=filter_content(content)
        if len(content)==0:
            break
        key=content.pop(0)
        if key=='emojis':
            list_=[str(emoji) for emoji in guild.emojis.values()]
            iterator=iter(list_)
            lines=[''.join(v for v,c in zip(iterator,range(10))) for i in range((len(list_)+9)//10)]
            text=chunkify(lines)
            break
        if key=='channels':
            text=pchunkify(guild.channels,write_parents=False)
            break
        if key=='roles':
            text=pchunkify(guild.roles,write_parents=False)
            break
        if key=='pins':
            messages = await client.channel_pins(message.channel)
            if not messages:
                text='There are no pinned messages at the channel.'
                break
            ln_c_l=len(str(len(messages)-1))+2
            lines=[f'{f"{index}.:": >{ln_c_l}} {message:c} id={message.id} length={len(message.content)} author={message.author:f}' for index,message in enumerate(messages,1)]
            text=cchunkify(lines)
            break
        if key=='webhooks':
            channel=None
            if content:
                if message.channel_mentions and is_channel_mention(content[0]):
                    channel=message.channel_mentions[0]
                else:
                    channel=guild.get_channel(channel)
            if channel is None:
                webhooks = await client.webhook_get_guild(guild)
            else:
                webhooks = await client.webhook_get_channel(channel)

            text=pchunkify(webhooks,write_parents=False)
            break
        break
    if type(text) is not str:
        pages=[{'content':chunk} for chunk in text]
        pagination(client,message.channel,pages,120.)
    elif text:
        await client.message_create(message.channel,text)
    else:
        await client.message_create(message.channel,embed=HELP['list'])

@infos.add('details')
async def parse_details_command(client,message,content):
    guild=message.guild
    if guild is None or not guild.permissions_for(message.author).can_administrator:
        return
    text=''
    key=''
    while True:
        content=filter_content(content)
        if len(content)==0:
            break
        key=content.pop(0)
        if key=='message':
            #alternative function definition right here
            while True:
                if not content:
                    index=1
                elif content[0].isdigit():
                    index=int(content[0])
                else:
                    text='Invalid index'
                    break
                if index>4194304:
                    #id propably
                    try:
                        target_message = await client.message_get(message.channel,index)
                    except (Forbidden,HTTPException):
                        text='Acces denied or not existing message'
                        break
                else:
                    if index>=message.channel.MC_GC_LIMIT and message.author is not client.owner:
                        text='NO U will read that!'
                        break
                    try:
                        target_message = await message_at_index(client,message.channel,index)
                    except IndexError:
                        text='I am not able to reach that message!'
                        break
                    except PermissionError:
                        text='Permission denied!'
                        break
                text=pchunkify(target_message)
                break
            break
        
        if key=='guild':
            text=pchunkify(guild)
            break
        
        if key=='pin':
            while True:
                if not content:
                    index=0
                elif content[0].isdigit():
                    index=int(content[0])
                else:
                    text='Invalid index'
                    break
                messages = await client.channel_pins(message.channel)
                if not messages:
                    text='There are no pins at this channel'
                    break
                if len(messages)<=index:
                    text=f'Index out of range, there is only {len(messages)} pins at the channel'
                    break
                text=pchunkify(messages[index])
                break
            break

        if key=='role':
            if not content:
                role=guild.roles[0]
            elif content[0].isdigit():
                index=int(content[0])
                if index>=len(guild.roles):
                    index=len(guild.roles)-1
                role=guild.roles[index]
            else:
                role=guild.get_role(content[0])
                if role is None:
                    text='Couldnt find that role by index/name.'
                    break

            text=pchunkify(role)
            break
        if key=='channel':
            if not content:
                text='Channel name or mention too pls?'
                break
            name=content.pop(0)
            if is_channel_mention(name) and message.channel_mentions:
                channel=message.channel_mentions[0]
            else:
                channel=guild.get_channel(name)
                if channel is None:
                    text='Unknown channel name.'
                    
            if len(content)<2:
                text=pchunkify(channel,overwrites=True)
                break
            
            name=content.pop(0)
            if name not in ('ow','overwrite'):
                text='After channel the next posible key is "ow"/"overwrite with an index!'
                break
            if not channel.overwrites:
                text='The channel has no overwrites desu'
                break
            name=content.pop(0)
            if name.isdigit():
                try:
                    overwrite=channel.overwrites[int(name)]
                except IndexError:
                    text=f'The channel has only {len(channel.overwrites)} overwirtes'
                    break
            else:
                value=guild.get_role(name)
                if value is None:
                    value=guild.get_user(name)
                if value is None:
                    text='There is no user/role like that'
                    break
                overwrite=None
                for x in channel.overwrites:
                    if x.target is value:
                        overwrite=x
                        break
                del x
                if overwrite is None:
                    text='No overwrite found for that user/role'
                    break
            
            text=pchunkify(overwrite,detailed=True)
            break
        
        if key=='permission':
            if len(content)&1 or len(content)>4:
                text='Getting info about sometihing should contain user <user> channel <channel> pairs'
                break
            
            user=None
            channel=None
            
            while True:
                if not content:
                    break
                type_=content.pop(0)
                name=content.pop(0)
                if type_=='user':
                    if user is not None:
                        text='User mentioned more times'
                        break
                    if is_user_mention(name) and message.user_mentions:
                        user=message.user_mentions[0]
                    else:
                        user=guild.get_user(name)
                        if user is None:
                            text='User not found'
                            break
                    continue
                
                if type_=='channel':
                    if channel is not None:
                        text='Channel mentioned more times'
                        break
                    if is_channel_mention(name) and message.channel.user_mentions:
                        channel=message.channel_mentions[0]
                    else:
                        channel=guild.get_channel(name)
                        if channel is not None:
                            text='Channel not found'
                            break
                    continue

                text=f'Invalid key "{type_}"'
                break

            if text:
                break
            
            if user is None:
                user=message.author
            if channel is None:
                channel=message.channel
                
            text=pchunkify(channel.permissions_for(user))
            break
        
        break
    
    if type(text) is not str:
        pages=[{'content':chunk} for chunk in text]
        pagination(client,message.channel,pages,120.)
    elif text:
        await client.message_create(message.channel,text)
    else:
        await client.message_create(message.channel,embed=HELP['details'])

# - : - # koishi.py # - : - #


##class pinner:
##    reset=BUILTIN_EMOJIS['arrows_counterclockwise']
##    __slots__=['cancel', 'channel',]
##    def __init__(self,client,channel):
##        self.channel=channel
##        self.cancel=type(self)._default_cancel
##        waitfor_wrapper(client,self,240.)
##        
##    async def start(self,wrapper):
##        client=wrapper.client
##
##        #we add the finishing details to the wrapper
##        wrapper.event=client.events.reaction_add
##        wrapper.target=message= await client.message_create(self.channel,content='Click on the emoji bellow')
##        
##        await client.reaction_add(message,self.reset)
##
##    async def __call__(self,wrapper,args):
##        emoji,user=args
##        if emoji is not self.reset or not self.channel.guild.permissions_for(user).can_administrator:
##            return
##        
##        client=wrapper.client
##        message=wrapper.target
##
##        try:
##            await client.reaction_delete(message,emoji,user)
##        except (Forbidden,HTTPException):
##            pass
##        
##        if message.pinned:
##            await client.message_unpin(message)
##        else:
##            await client.message_pin(message)
##
##        if wrapper.timeout<240.:
##            wrapper.timeout+=30.
##    
##    _default_cancel=pagination._default_cancel


##    @on_command.add('print')
##    async def on_print_command(client,message,content):
##        try:
##            await client.message_delete(message,reason='Used print command')
##        except Forbidden:
##            pass
##        else:
##            await client.message_create(message.channel,content)

##    @on_command
##    async def pong(client,message,content):
##        guild=message.channel.guild
##        if guild is not None:
##            user=guild.get_user(content)
##            if user is not None:
##                await client.message_create(message.channel,user.mention_at(guild))


##    @on_command
##    async def pm(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        content=filter_content(content)
##        while True:
##            if len(content)!=1:
##                text='The 1st line must contain a mention/username of the "lucky" person.'
##                break
##            content=content[0]
##            if message.user_mentions and is_user_mention(content):
##                user=message.user_mentions[0]
##            else:
##                user=guild.get_user(content)
##                if user is None:
##                    text='Could not find that user!'
##                    break
##
##            index=message.content.find('\n')+1
##            if not index:
##                text='Unable to send empty message'
##                break
##            text=message.content[index:]
##            if not text:
##                text='Unable to send empty message'
##                break
##            if user is client:
##                text='Ok, i got it!'
##                break
##            channel = await client.channel_private_create(user)
##            try:
##                await client.message_create(channel,text)
##                text='Big times! Message sent!'
##            except Forbidden:
##                text='Access denied'
##            break
##                                    
##        await client.message_create(message.channel,text)

            
    @on_command
    async def edit(client,message,content):
        guild=message.guild
        if guild is None:
            return
        text=''
        content=filter_content(content)
        key=''
        reason=''
        
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            if not content:
                break
            key=content.pop(0)
            if key=='user':
                if not content:
                    text='You can edit "nick", "role", "deaf", "mute", "voice_channel".'
                    break
                limit=len(content)
                if (limit&1)^1:
                    text='Pls send 1 mention, then key, value pairs.'
                    break
                if limit==1:
                    text='You can edit "nick", "role", "deaf", "mute", "voice_channel".'
                    break
                if message.user_mentions:
                    if len(message.user_mentions)>1:
                        text='Pls send 1 mention or 1 name and stuffs to change.'
                        break
                    if not is_user_mention(content[0]):
                        text='1st value must be mention.'
                        break
                    user=message.user_mentions[0]
                else:
                    user=guild.get_user(content[0])
                    if user is None:
                        text='Could not find a user with that name.'
                        break

                if message.channel_mentions:
                    if message.channel_mentions>1 or 'voice_channel' not in content[::2]:
                        text='Not in place channel mention found'
                        break

                result={}
                
                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break

                    if name=='nick':
                        result[name]=value
                        continue
                        
                    if name in ('deaf','mute'):
                        value=value.lower()
                        if value=='true':
                            result[name]=True
                            continue
                        elif value=='false':
                            result[name]=False
                            continue
                        else:
                            text=f'Invalid value for {name}, it can be either True or False'
                            break
                        
                    if name=='voice_channel':
                        if is_channel_mention(value):
                            channel=message.channel_mentions[0]
                        else:
                            channel=guild.get_channel(value)
                            if channel is None:
                                text='Did not find that channel name'
                                break
                        if type(channel) is not Channel_voice:
                            text='Bad channel type, it must to be voice channel!'
                            break
                        result[name]=channel
                        continue

                    if name=='role':
                        role=guild.get_role(value)
                        if role is None:
                            text='Did not find that role name!'
                            break
                        user_roles=user.guild_profiles[guild].roles
                            
                        if role in user_roles:
                            new_roles=user_roles.copy()
                            new_roles.remove(role)
                            result['roles']=new_roles
                        else:
                            new_roles=user_roles.copy()
                            new_roles.append(role)
                            result['roles']=new_roles
                        continue

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text=f'Invalid attribute to change {name}. You can change "nick", "deaf", "mute", "voice channel", "role" of a user. Additionally you can add "reason" too.'
                    break
                
                if not text:
                    text=(user,result)
                break
            
            if key=='role':
                limit=len(content)
                if (limit&1)^1:
                    text='Pls write a role\'s name, then key, value pairs.'
                    break
                if limit==1:
                    text='And anything to change?'
                    break
                role=guild.get_role(content[0])
                if role is None:
                    text='Could not find a role with that name.'
                    break

                result={}
                
                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break

                    if name=='name':
                        result[name]=value
                        continue
                        
                    if name in ('mentionable','separated'):
                        value=value.lower()
                        if value=='true':
                            result[name]=True
                            continue
                        elif value=='false':
                            result[name]=False
                            continue
                        else:
                            text=f'Invalid value for {name}, it can be either True or False'
                            break
                        
                    if name=='color':
                        try:
                            result[name]=Color.from_html(value)
                        except ValueError:
                            text='Invalid color'
                            break
                        continue

                    if name=='permissions':
                        if value=='voice':
                            result[name]=Permission.voice
                            continue
                        if value=='text':
                            result[name]=Permission.text
                            continue
                        if value=='none':
                            result[name]=Permission.none
                            continue
                        if value=='general':
                            result[name]=Permission.general
                            continue
                        text='Not predefined permission name'
                        break

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text='Invalid attribute to change. You can change a role\'s name, "separated" and "mentonable" "value", "color" and "permissions" (to preset "voice", "text", "none", "general".'
                    break
                
                if not text: 
                    text=(role,result)
                break

            if key=='emoji':
                if not len(content)&1:
                    text='After emoji pls type key-value pairs'
                    break
                if len(content)==1:
                    text='Done!!'
                    break

                value=content.pop(0)
                
                emoji=parse_emoji(value)
                if emoji:
                    try:
                        emoji=guild.emojis[emoji.id]
                    except KeyError:
                        text='Can not edit that emoji'
                        break
                else:
                    emoji=guild.get_emoji(value)
                    if emoji is None:
                        text='Thats not an emoji'
                        break

                roles=[]
                ename=None

                while content:
                    name=content.pop(0)
                    value=content.pop(0)

                    if name=='name':
                        if not (1<len(value)<33):
                            text='Name too long or short'
                            break
                        
                        if ename is not None:
                            text='Name cannot be duped only role.'

                        ename=value
                        continue

                    if name=='role':
                        role=guild.get_role(value)
                        if role is None:
                            text=f'Could not find role {value}.'
                            break
                        
                        if role in roles:
                            text='You cant add 1 role more times'
                            break

                        roles.append(role)
                        continue

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text=f'Invalid value to change {name}, you can change an emoji\'s "name", "role" (more too) and give a "reason" too.'
                    break


                if not text: 
                    text=(emoji,ename,roles)
                break
                
            if key=='guild':
                limit=len(content)
                if limit&1:
                    text='Pls write key, value pairs.'
                    break
                if limit==0:
                    text='And anything to change?'
                    break

                result={}
                
                index=0
                attach_index=0
                channel_index=0
                
                while index!=limit:
                    name=content[index].lower()
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break

                    if name=='owner':
                        if message.user_mentions and is_user_mention(value):
                            user=message.user_mentions[0]
                        else:
                            user=guild.get_user(value)
                            if user is None:
                                text='Could not find that user!'
                                break
                        
                        if client is guild.owner:
                            if message.author is client.owner:
                                result[name]=user
                            else:
                                text='You do not have permission to do it'
                                break
                        else:
                            'I must be the server owner to change the ownership.'
                            break
                        
                        continue
                    
                    if name=='name':
                        result[name]=value
                        continue

                    if name=='icon':

                        if value.lower()=='none':
                            result[name]=None
                            continue
                            
                        if len(message.attachments)<=attach_index:
                            text='The message has no attachments to change icon'
                            break
                        
                        ext=os.path.splitext(message.attachments[attach_index].name)[1]
                        if len(ext)<2:
                            text='Missing extension.'
                            break
                        ext=ext[1:].lower()
                        
                        if ext not in VALID_ICON_FORMATS:
                            text='Invalid format.'
                            break
                        
                        result[name] = await client.download_attachment(message.attachments[attach_index])
                        attach_index+=1
                        continue

                    if name=='splash':
                        if guild_features.splash not in guild.features:
                            text='The guild has no splash feature.'
                            break

                        if value.lower()=='none':
                            result[name]=None
                            continue

                        if len(message.attachments)<=attach_index:
                            text='The message has no attachments to change splash'
                            break
                        
                        ext=os.path.splitext(message.attachments[attach_index].name)[1]
                        if len(ext)<2:
                            text='Missing extension.'
                            break
                        ext=ext[1:].lower()
                        
                        if ext not in VALID_ICON_FORMATS:
                            text='Invalid format'
                            break
                        
                        result[name] = await client.download_attachment(message.attachments[attach_index])
                        attach_index+=1
                        continue

                    if name=='afk_channel':
                        
                        if value.lower()=='none':
                            result[name]=None
                            continue

                        if message.channel_mentions and is_channel_mention(value):
                            channel=message.channel_mentions[channel_index]
                        else:
                            channel=guild.get_channel(value)
                            if channel is None:
                                text='Could not find that channel!'
                                break

                        if type(channel) is not Channel_voice:
                            text='Afk channel can be only voice channel'
                            break
                        
                        result[name]=channel
                        channel_index+=1
                        continue

                    if name=='system_channel':
                        
                        if value.lower()=='none':
                            result[name]=None
                            continue

                        if message.channel_mentions and is_channel_mention(value):
                            channel=message.channel_mentions[channel_index]
                        else:
                            channel=guild.get_channel(value)
                            if channel is None:
                                text='Could not find that channel!'
                                break

                        if type(channel) is not Text_voice:
                            text='System channel can be only text channel'
                            break
                        
                        result[name]=channel
                        channel_index+=1
                        continue

                    if name in ('region','voice_region'):
                        try:
                            region=voice_regions.values[value.lower()]
                        except KeyError:
                            text='Unknown voice region'
                            continue

                        result[name]=region
                        continue

                    if name=='afk_timeout':
                        try:
                            afk_timeout=int(value)
                        except ValueError:
                            text='Timeout must be integer.'
                            break

                        if afk_timeout not  in (60,300,900,1800,3600):
                            text='Afk timeout should be 60, 300, 900, 1800, 3600 seconds.'
                            break

                        result[name]=afk_timeout
                        continue

                    if name in ('verification','verification_level'):
                        try:
                            level=verification_levels.values[int(value)]
                        except KeyError:
                            text='Invalid verification_level'
                            break
                        except ValueError:
                            for element in verification_levels.values.values():
                                if value in element.names:
                                    level=element
                                    break
                            else:
                                text='Invalid verification_level'
                                break
                            
                        result['verification_level']=level
                        continue

                    if name=='content_filter': 
                        try:
                            level=content_filter_levels.values[int(value)]
                        except KeyError:
                            text='Invalid content filter'
                            break
                        except ValueError:
                            for element in content_filter_levels.values.values():
                                if value in element.names:
                                    level=element
                                    break
                            else:
                                text='Invalid content filter'
                                break
                            
                        result[name]=level
                        continue
                        
                    if name in ('message_notification_level','message_notification'):
                        try:
                            level=message_notification_levels.values[int(value)]
                        except KeyError:
                            text='Invalid message notification level'
                            break
                        except ValueError:
                            for element in message_notification_levels.values.values():
                                if value in element.names:
                                    level=element
                                    break
                            else:
                                text='Invalid message notification level'
                                break
                            
                        result['message_notification']=level
                        continue
                    
                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text='Invalid attribute to change. You can change: "name", "icon", "splash", ' \
                        '"afk_channel", "system_channel", "owner", "region", "afk_timeout", ' \
                        '"verification_level", "content_filter", "message_notification_level", ' \
                        'and add an additional "reason" too.'
                    break
                
                if not text: 
                    text=result
                break
            
            break
        if type(text) is not str:
            try:
                if reason:
                    reason=smart_join([f'Executed by {message.author:f}, with reason:',*reason.split()],255)
                else:
                    reason=f'Executed by {message.author:f}'
                if key=='user':
                    await client.user_edit(guild,text[0],**text[1],reason=reason)
                elif key=='role':
                    await client.role_edit(text[0],**text[1],reason=reason)
                elif key=='emoji':
                    await client.emoji_edit(*text,reason=reason)
                elif key=='guild':
                    await client.guild_edit(guild,**text,reason=reason)
            except Forbidden:
                text='Access denied'
            except ValueError as err:
                text=err.args[0]
            else:
                text='OwO'
                
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['edit'])

    @on_command
    async def move(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        key=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            if not content:
                break
            key=content.pop(0)
            if key=='channel':
                if len(content) not in (2,3):
                    text='Moving channel\n formula: "channel name" ("category name") "position"'
                    break
                if is_channel_mention(content[0]):
                    channel=message.channel_mentions[0] 
                else:
                    channel=guild.get_channel(content[0])
                    if channel is None:
                        try:
                            channel=guild.all_channel[int(content[0])]
                        except (KeyError,ValueError):
                            text='Channel not found.'
                            break
                if len(content)==3:
                    index=content[2]
                else:
                    index=content[1]
                try:
                    index=int(index)
                except KeyError:
                    text='Index should be number, right?'
                    break
                if len(content)==2:
                    category=None
                else:
                    category=content[1]
                    if category=='guild':
                        category=guild
                    else:
                        if is_channel_mention(content[2]):
                            category=message.channel_mentions[-1]
                        else:
                            category=guild.get_channel(category)
                            if category is None:
                                try:
                                    category=guild.all_channel[int(content[1])]
                                except (KeyError,ValueError):
                                    pass
                        if category is None:
                            text='Category not found.'
                            break
                        if category.type!=4:
                            text='You can move channels only to Category channel or to the guild.'
                            break

                if not text:
                    text=(channel,index,category)
                break
            if key=='role':
                if len(content)!=2:
                    text='"Role name" and "index" please!'
                    break
                role=guild.get_role(content[0])
                if role is None:
                    text='Role not found.'
                    break
                try:
                    index=int(content[1])
                except ValueError:
                    text='Valid number desu!'
                    break
                text=(role,index)
                break
            if key=='user':
                if len(content) not in (1,2):
                    text='("user name/ping") and "Channel name/ping" desu!'
                    break

                if len(content)==2:
                    name=content.pop(0)
                    if message.user_mentions and is_user_mention(name):
                        user=message.user_mentions[0]
                    else:
                        user=guild.get_user(name)
                        if user is None:
                            text='Could not find a user with that name!'
                            break
                else:
                    user=message.author
                    
                state=guild.voice_states.get(user.id,None)
                if not state:
                    text='Can move only a user from voice channel'
                    break
                
                name=content[0]
                if message.channel_mentions and is_channel_mention(name):
                    channel=message.channel_mentions[0]
                else:
                    channel=guild.get_channel(name)
                    if channel is None:
                        text='Could not find that channel!'
                        break
                if channel.type!=2:
                    text='Can move user only from voice channel to voice channel!'
                    break
                if channel is state.channel:
                    text='Done, i guess (?)'
                    break
                text=(user,channel)
                
            break
        
        if type(text) is not str:
            try:
                reason=f'Executed by {message.author:f}'
                if key=='channel':
                    await client.channel_move(*text,reason=reason)
                elif key=='role':
                    await client.role_move(*text,reason=reason)
                elif key=='user':
                    await client.user_move(*text,reason=reason)
            except Forbidden:
                text='Access denied!'
            else:
                text='yayyyy'
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['move'])

    
    @on_command
    async def delete(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        key=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            if len(content) not in (2,3):
                text='type, value, then reason if you wish to.'
                break
            
            key=content.pop(0)
            value=content.pop(0)
            if key=='role':
                role=guild.get_role(value)
                if role is None:
                    text='Role not found'
                    break
                text=role
                break
            if key=='channel':
                channel=guild.get_channel(value)
                if channel is None:
                    text='Channel not found'
                    break
                text=channel
                break
            if key=='emoji':
                text=parse_emoji(value)
                if text:
                    try:
                        text=guild.emojis[text.id]
                    except KeyError:
                        text='Can not edit that emoji'
                        break
                else:
                    text=guild.get_emoji(value)
                    if text is None:
                        text='Thats not an emoji'
                        break

                break
            
            break
        
        if type(text) is str:
            if text:
                await client.message_create(message.channel,text)
            else:
                await client.message_create(message.channel,embed=HELP['delete'])
            return
        
        if content:
            reason=smart_join([f'Executed by {message.author:f}, with reason:',*content[0].split()],255)
        else:
            reason=f'Executed by {message.author:f}'
            
        try:
            if key=='role':
                await client.role_delete(text,reason)
            elif key=='channel':
                await client.channel_delete(text,reason)
            elif key=='emoji':
                await client.emoji_delete(text,reason)
        except Forbidden:
            text='Access denied!'
        else:
            text='yayyyy'
        await client.message_create(message.channel,text)
            
        

##    @on_command.add('book')
##    async def on_command_book(client,message,content):
##        pages=({'content':'import base64\n\npage1/3'},{'content':'uwu\n\npage2/3'},{'content':'text2\n\npage3/3'})
##        pagination(client,message.channel,pages)


##    @on_command
##    async def satania(client,message,content):
##        message = await client.message_create(message.channel,'waiting for satania emote')
##        try:
##            emoji,user = await wait_for_emoji(client,message,lambda emoji,user:('satania' in emoji.name.lower()),60.)
##        except TimeoutError:
##            return
##        finally:
##            try:
##                await client.message_delete(message)
##            except (Forbidden,HTTPException):
##                pass
##        await client.message_create(message.channel,str(emoji)*5)

##    @on_command.add('embed')
##    async def on_command_embed(client,message,content):
##        content='Here\'s a hug for Nyansia ! OwO'
##        embed=Embed( \
##            title='Nyanmatsu hugs Nyansia',
##            url='https://discordapp.com',
##            color=Color.from_html('#ff4465'),
##                )
##        embed.image=Embed_image('https://cdn.discordapp.com/embed/avatars/0.png')
##        
##        await client.message_create(message.channel,content,embed)



    @on_command
    async def create(client,message,content):
        guild=message.guild
        if guild is None:
            return
        text=''
        content=filter_content(content)
        key=''
        reason=''
        
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            
            key=content.pop(0)
            
            if not content:
                break
            
            if key=='role':
                limit=len(content)
                if limit&1==0:
                    text='role name, then key-value pairs.'
                    break

                result={}
                
                value=content[0]
                
                role=guild.get_role(value)
                if role is not None:
                    text='A role already has that name!'
                    break
                
                result[key]=value
                    
                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break
                        
                    if name in ('mentionable','separated'):
                        value=value.lower()
                        if value=='true':
                            result[name]=True
                            continue
                        elif value=='false':
                            result[name]=False
                            continue
                        else:
                            text=f'Invalid value for {name}, it can be either True or False'
                            break
                        
                    if name=='color':
                        try:
                            result[name]=Color.from_html(value)
                        except ValueError:
                            text='Invalid color'
                            break
                        continue

                    if name=='permissions':
                        if value=='voice':
                            result[name]=Permission.voice
                            continue
                        if value=='text':
                            result[name]=Permission.text
                            continue
                        if value=='none':
                            result[name]=Permission.none
                            continue
                        if value=='general':
                            result[name]=Permission.general
                            continue
                        text='Not predefined permission name'
                        break

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue
                    
                    text=f'You can not set {key}, but you can set additionally: "mentionable", "separated",' \
                          '"color" <html format>, "permissions" <voice/text/nne/genera>, "reason" for now'
                    break
                
                if not text: 
                    text=result
                    
                break
            if key=='emoji':
                limit=len(content)
                
                if limit&1==0:
                    text='Emoji name followed by key - value pairs (role <rolename> / reason <reason>)'
                
                value=content[0]
                
                if not (1<len(value)<33):
                    text='Too short or too long name'
                    break
                
                count_animated=0
                for emoji in guild.emojis.values():
                    if emoji.name==value:
                        exists=True
                        break
                    if emoji.animated:
                        count_animated+=1
                else:
                    exists=False

                if exists:
                    text='An emoji already exists with that name at the guild'
                    break
                
                if not message.attachments:
                    text='The message has no attachments'
                    break

                ext=os.path.splitext(message.attachments[0].name)[1]
                if len(ext)<2:
                    text='Missing extension'
                    break
                ext=ext[1:].lower()
                
                if ext in VALID_ICON_FORMATS:
                    if len(guild.emojis)-count_animated==50:
                        text='The guild already reached the limit of non animated emojis'
                        break
                    
                elif ext in VALID_ICON_FORMATS_EXTENDED:
                    if count_animated==50:
                        text='The guild already reached the limit of animated emojis'
                        break
                else:
                    text='Invalid format'
                    break

                roles=[]
                ename=value

                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1
                    
                    if name=='role':
                        role=guild.get_role(value)
                        if role is None:
                            text=f'Could not find role: {value}.'
                            break
                        
                        if role in roles:
                            text='You cant add 1 role more times'
                            break

                        roles.append(role)
                        continue

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text=f'Invalid value {name}, you can use "role" (more too) and give a "reason" too.'
                    break

                if text:
                    break
                
                image = await client.download_attachment(message.attachments[0])
                
                text=(ename,image,roles)

                break
                
            break
        
        if type(text) is not str:
            try:
                if reason:
                    reason=smart_join([f'Executed by {message.author:f}, with reason:',*reason.split()],255)
                else:
                    reason=f'Executed by {message.author:f}'
                
                if key=='role':
                    await client.role_create(guild,**text,reason=reason)
                elif key=='emoji':
                    await client.emoji_create(guild,*text,reason)
                    
            except Forbidden:
                text='Access denied!'
            except ValueError as err:
                text=err.args[0]
            else:
                text='yayyyy'
        
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['create'])
        
    @on_command
    async def invite_by_code(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return
        
        err=False
        if not content:
            err=True
        elif len(content)>8:
            err=True
        else:
            try:
                invite = await client.invite_get(content)
            except Forbidden:
                invite=None
            except HTTPException:
                err=True

        if err:
            text='Invalid Invite code'
        elif invite:
            text=f'{pchunkify(invite,show_code=True)[0]}\n{invite.url}'
        else:
            text='Permissions denied'

        await client.message_create(message.channel,text)

    @on_command
    async def invite_delete_by_code(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return

        err=False
        if not content:
            err=True
        elif len(content)>16:
            err=True
        else:
            try:
                invite = await client.invite_delete_by_code(content)
            except Forbidden:
                invite=None
            except HTTPException:
                err=True

        if err:
            text='Invalid Invite code'
        elif invite:
            text=f'{pchunkify(invite,show_code=True)[0]}\n{invite.url}'
        else:
            text='Permissions denied'

        await client.message_create(message.channel,text)

    @on_command
    async def invite_clear(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return
        
        try:
            with client.keep_typing(message.channel):
                invites = await client.invite_get_guild(guild)
                for invite in invites:
                    try:
                        await client.invite_delete(invite)
                    except HTTPException:
                        pass
        except Forbidden:
            text='Failed'
        else:
            text=f'Succes, {len(invites)} got deleted'
            
        await client.message_create(message.channel,text)

    #client side only. Discord clients request with_count always anyways
##    @on_command
##    async def invite_mod(client,message,content):
##        guild=message.guild
##        if guild is None or not guild.permissions_for(message.author).can_administrator:
##            return
##        
##        try:
##            with client.keep_typing(message.channel):
##                invites = await client.invite_get_guild(guild)
##                for invite in invites:
##                    if invite.online_count is not None:
##                        value=False
##                    else:
##                        value=True
##                    try:
##                        await client.invite_update(invite,value)
##                    except HTTPException:
##                        pass
##        except Forbidden:
##            text='Failed'
##        else:
##            text=f'Succes'
##            
##        await client.message_create(message.channel,text)
            
##    @on_command
##    async def wait2where(client,message,content):
##        channel=message.channel
##        private = await client.channel_private_create(message.author)
##        await client.message_create(channel,'Waiting on any message from you here and at dm')
##
##        
##        future=wait_one(client.loop)
##        case=lambda message,author=message.author:message.author is author
##        event=client.events.message_create
##        
##        wrapper1=waitfor_wrapper(client,wait_and_continue(future,case,channel,event),60.)
##        wrapper2=waitfor_wrapper(client,wait_and_continue(future,case,private,event),60.)
##        
##        try:
##            result = await future
##        except TimeoutError:
##            await client.message_create(channel,'Time is over')
##            return
##        
##        wrapper1.cancel()
##        wrapper2.cancel()
##        
##        await client.message_create(channel,result.content)


##    @on_command
##    async def language(client,message,content):
##        guild=message.guild
##        target=None
##        if content:
##            if message.user_mentions:
##                target=message.user_mentions[0]
##            elif guild is not None:
##                target=guild.get_user(content)
##        if target is None:
##            target=message.author
##        
##        await client.message_create(message.channel,f'If i can have a guess {target.mention_at(guild)}\' client\'s language is: {target.language}')


##    @on_command.add('pinner')
##    async def on_command_pinner(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if guild.permissions_for(message.author).can_administrator:
##            pinner(client,message.channel)


    @on_command
    async def guild_delete(client,message,content):
        guild=message.guild
        if guild is None or guild.owner is not client or message.author is not client.owner:
            return
        await client.guild_delete(guild)

    @on_command
    async def guild_create(client,message,content):
        if message.author is not client.owner and len(client.guilds)>9:
            return
        guild = await client.guild_create(name='uwu yayyyy',
            channels=[cr_pg_channel_object(name='channel1',type_=Channel_text),
                      cr_pg_channel_object(name='channel2',type_=Channel_text),
                      cr_pg_channel_object(name='channel3',type_=Channel_text),])

        await sleep(2.,client.loop) #wait for dispatch
        invite = await client.invite_create_pref(guild,0,0)
        channel = await client.channel_private_create(message.author)
        await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')

    @on_command
    async def transfer_ownership(client,message,content):
        guild=message.guild
        if guild is None or message.author is not client.owner or guild.owner is not client:
            return
        await client.guild_edit(guild,owner=client.owner)
        
##    @on_command
##    async def load_emotes(client,message,content):
##        with client.keep_typing(message.channel):
##            while True:
##                try:
##                    id_=int(content)
##                except ValueError:
##                    text='Thats not an id.'
##                    break
##                try:
##                    message = await client.message_get(message.channel,id_)
##                except Forbidden:
##                    text='I have no permission to do that!'
##                    break
##                except HTTPException:
##                    text='The message does not exsists!'
##                    break
##                
##                #this might take for a while
##                await client.reaction_load_all(message)
##
##                if message.reactions is None:
##                    text='None'
##                    break
##
##                result=[]
##                for emoji,line in message.reactions.items():
##                    for user in line:
##                        if len(result)==20:
##                            break
##                        result.append(f'{emoji:e} - {user:f}')
##
##                text='\n'.join(result)
##                break
##
##        await client.message_create(message.channel,text)
##
##    @on_command
##    async def webhook_test(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##        
##        webhooks = await client.webhook_get_guild(guild)
##
##        if not webhooks:
##            return
##        
##        webhook=webhooks[0]
##        
##        await client.webhook_send(webhook,embed=Embed('OwO whats this?'),name=message.author.name,avatar_url=message.author.avatar_url,file=b'UwU',filename='UwU')
##
##    @on_command
##    async def webhook_get_by_id(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        try:
##            id_=int(content)
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_get_by_token(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        await client.message_delete(message)
##        
##        content=filter_content(content)
##        try:
##            id_=int(content[0])
##        except ValueError:
##            return
##
##        token=content[1]
##        
##        webhook = await client.webhook_get_token(id_,token)
##
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_create(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        if not (1<len(content)<33):
##            return
##        
##        if message.attachments:
##            ext=os.path.splitext(message.attachments[0].name)[1]
##            if len(ext)<2:
##                return
##            ext=ext[1:].lower()
##            
##            if ext not in VALID_ICON_FORMATS:
##                return
##            
##            image = await client.download_attachment(message.attachments[0])
##        else:
##            image=b''
##
##        webhook = await client.webhook_create(message.channel,content,image)
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_delete_by_id(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##        
##        try:
##            id_=int(content)
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##        
##        await client.webhook_delete(webhook)
##
##        await client.message_create(message.channel,webhook.name)
##        
##        
##    @on_command
##    async def webhook_delete_by_token(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##        
##        content=filter_content(content)
##        try:
##            id_=int(content[0])
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##
##        await client.webhook_delete_token(webhook)
##
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_edit(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        content=filter_content(content)
##
##        if len(content)<2:
##            return
##
##        try:
##            id_=int(content[0])
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##        
##        if 'name' in content:
##            name=''.join([chr(random(65,90)) for i in range(10)])
##        else:
##            name=''
##
##        if 'avatar' in content:
##            if message.attachments:
##                ext=os.path.splitext(message.attachments[0].name)[1]
##                if len(ext)<2:
##                    return
##                ext=ext[1:].lower()
##                
##                if ext not in VALID_ICON_FORMATS:
##                    return
##                    
##                avatar = await client.download_attachment(message.attachments[0])
##            else:
##                avatar=None
##        else:
##            avatar=b''
##
##        token=('token' in content)
##
##        if 'channel' in content:
##            channels=guild.text_channels
##            try:
##                channels.remove(webhook.channel)
##            except ValueError:
##                pass
##            channel=choice(channels)
##        else:
##            channel=None
##         
##        if token:
##            await client.webhook_edit_token(webhook,name,avatar,channel)
##        else:
##            await client.webhook_edit(webhook,name,avatar,channel)
##
##        await client.message_create(message.channel,webhook.name,)
##
##    @on_command
##    async def webhook_from_url(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        await client.message_delete(message)
##        
##        webhook = await client.webhook_get(Webhook.from_url(content).id)
##
##        await client.message_create(message.channel,webhook.name,)

#TODO: get a working integation id for make tests with it

##    @on_command
##    async def create_integration(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        integration = await client.integration_create(guild,'twitch',456456)
##
##        await client.message_create('owo')


##    @on_command
##    async def guild_get(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        if not content:
##            return
##        
##        try:
##            id_=int(content)
##        except ValueError:
##            return
##
##        try:
##            guild = await client.guild_get(id_)
##        except Forbidden:
##            return
##        
##        await client.message_create(message.channel,f'{guild.name}\n{guild.icon_url}')

##    @on_command
##    async def emoji_get(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None or not content:
##            return
##
##        content=filter_content(content)
##        
##        try:
##            emoji_id=int(content[0])
##        except ValueError:
##            pass
##
##        #for testing purpose
##        if len(content)>1:
##            try:
##                guild_id=int(content[1])
##            except ValueError:
##                pass
##            try:
##                guild=GUILDS[guild_id]
##            except KeyError:
##                guild=Unknown('Guild',guild_id) #we will get forbidden
##        try:
##            emoji = await client.emoji_get(guild,emoji_id)
##        except Forbidden:
##            await client.message_create(message.channel,'not part of that guild')
##        else:
##            await client.message_create(message.channel,emoji.as_emoji)
##
##    @on_command
##    async def all_emojis(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None:
##            return
##
##        emojis = await client.guild_emojis(guild)
##        await client.message_create(message.channel,smart_join((emoji.as_emoji for emoji in emojis.values()),2000))


    @on_command
    @cooldown(30.,'user',handler=cooldown_handler())
    async def cheer(client,message,content):
        await client.message_create(message.channel,embed=Embed('CHEERS!',color=Color.d_purple))

    @on_command
    @cooldown(60.,'c',case='cheers')
    async def almost_cheer(client,message,content):
        await client.message_create(message.channel,embed=Embed(BUILTIN_EMOJIS['cheese'].as_emoji,color=Color.d_purple))

    @on_command
    @cooldown(60.,'g',)
    async def cheese(client,message,content):
        await client.message_create(message.channel,embed=Embed(BUILTIN_EMOJIS['cheese'].as_emoji,color=Color.d_purple))

##    #if we use prefix as str/list
##    @on_command
##    async def add_prefix(client,message,content):
##        if message.author is not client.owner:
##            return
##        prefixes=client.events.message_create.prefix
##        if type(prefixes) is str:
##            prefixes=[prefixes]
##        prefixes.append(content)
##        client.events.message_create.update_prefix(prefixes)
##        await client.message_create(message.channel,'OwO')


    @on_command
    async def create_pow(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command.'
                break
            if len(content)<4:
                text='And who\'s / what\'s to change and to what to change?\nThe correct formula is the following:\n"Channel Target Allow Deny <reason>".'
                break

            channel_name=content[0]                            
            
            target_name=content[1]

            try:
                allow=int(content[2])
            except ValueError:
                text='Allow must be number'
                break

            try:
                deny=int(content[3])
            except ValueError:
                text='Deny must be number'
                break

            if message.channel_mentions is not None and is_channel_mention(channel_name):
                channel=message.channel_mentions[0]
            else:
                if channel_name.isdigit():
                    try:
                        channel=guild.all_channel[int(channel_name)]
                    except KeyError:
                        channel=guild.get_channel(channel_name)
                        if channel is None:
                            text='Could not find that channel'
                            break
            while True:
                if target_name.isdigit():
                    target_id=int(target_name)
                    try:
                        target=guild.users[target_id]
                        break
                    except KeyError:
                        pass
                    try:
                        target=guild.all_role[target_id]
                        break
                    except KeyError:
                        pass

                if message.role_mentions is not None and is_role_mention[target_name]:
                    target=message.role_mentions[0]
                    break
                
                if message.user_mentions is not None and is_user_mention(target_name):
                    target=message.user_mentions[0]
                    break
                
                target=guild.get_role(target_name)
                if target is not None:
                    break

                target=guild.get_user(target_name)
                if target is not None:
                    break
                
                text='Could not find that target!'
                break
            
            if text:
                break

            if len(content)>4:
                reason=content[4]
            else:
                reason=None

            try:
                await client.permission_ow_create(channel,target,allow,deny,reason)
            except Forbidden:
                text='Access denied'
            except HTTPException:
                text='Cannot do that!'
            else:
                text='Pat me!'
            break

        await client.message_create(message.channel,text)

    @on_command
    async def edit_pow(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command.'
                break
            if len(content)<4:
                text='And who\'s / what\'s to change and to what to change?\nThe correct formula is the following:\n"Channel Target Allow Deny <reason>".'
                break

            channel_name=content[0]                            
            
            target_name=content[1]

            try:
                allow=int(content[2])
            except ValueError:
                text='Allow must be number'
                break

            try:
                deny=int(content[3])
            except ValueError:
                text='Deny must be number'
                break

            if message.channel_mentions is not None and is_channel_mention(channel_name):
                channel=message.channel_mentions[0]
            else:
                if channel_name.isdigit():
                    try:
                        channel=guild.all_channel[int(channel_name)]
                    except KeyError:
                        channel=guild.get_channel(channel_name)
                        if channel is None:
                            text='Could not find that channel'
                            break
            while True:
                if target_name.isdigit():
                    target_id=int(target_name)
                    try:
                        target=guild.users[target_id]
                        break
                    except KeyError:
                        pass
                    try:
                        target=guild.all_role[target_id]
                        break
                    except KeyError:
                        pass

                if message.role_mentions is not None and is_role_mention[target_name]:
                    target=message.role_mentions[0]
                    break
                
                if message.user_mentions is not None and is_user_mention(target_name):
                    target=message.user_mentions[0]
                    break
                
                target=guild.get_role(target_name)
                if target is not None:
                    break

                target=guild.get_user(target_name)
                if target is not None:
                    break
                
                text='Could not find that target!'
                break
            
            if text:
                break

            for overwrite in channel.overwrites:
                if overwrite.target is target:
                    break
            else:
                text='Could not find permission overwrite on that user'
                break
            
            if len(content)>4:
                reason=content[4]
            else:
                reason=None

            try:
                await client.permission_ow_edit(channel,overwrite,allow,deny,reason)
            except Forbidden:
                text='Access denied'
            except HTTPException:
                text='Cannot do that!'
            else:
                text='Pat me!'
            break

        await client.message_create(message.channel,text)

    @on_command
    async def delete_pow(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command.'
                break
            if len(content)<4:
                text='And who\'s / what\'s to change and to what to change?\nThe correct formula is the following:\n"Channel Target Allow Deny <reason>".'
                break

            channel_name=content[0]                            
            
            target_name=content[1]

            if message.channel_mentions is not None and is_channel_mention(channel_name):
                channel=message.channel_mentions[0]
            else:
                if channel_name.isdigit():
                    try:
                        channel=guild.all_channel[int(channel_name)]
                    except KeyError:
                        channel=guild.get_channel(channel_name)
                        if channel is None:
                            text='Could not find that channel'
                            break
            while True:
                if target_name.isdigit():
                    target_id=int(target_name)
                    try:
                        target=guild.users[target_id]
                        break
                    except KeyError:
                        pass
                    try:
                        target=guild.all_role[target_id]
                        break
                    except KeyError:
                        pass

                if message.role_mentions is not None and is_role_mention[target_name]:
                    target=message.role_mentions[0]
                    break
                
                if message.user_mentions is not None and is_user_mention(target_name):
                    target=message.user_mentions[0]
                    break
                
                target=guild.get_role(target_name)
                if target is not None:
                    break

                target=guild.get_user(target_name)
                if target is not None:
                    break
                
                text='Could not find that target!'
                break
            
            if text:
                break

            for overwrite in channel.overwrites:
                if overwrite.target is target:
                    break
            else:
                text='Could not find permission overwrite on that user'
                break
            
            if len(content)>2:
                reason=content[2]
            else:
                reason=None

            try:
                await client.permission_ow_delete(channel,overwrite,reason)
            except Forbidden:
                text='Access denied'
            except HTTPException:
                text='Cannot do that!'
            else:
                text='Pat me!'
            break

        await client.message_create(message.channel,text)

    @on_command
    async def test_download(client,message,content):
        if message.attachments is None or message.author is not client.owner:
            return

        file = await client.download_url(message.attachments[0].url)
        await client.message_create_file(message.channel,file,filename=message.attachments[0].name,content='Here is your file!')

    @on_command
    async def test_files(client,message,content):
        if message.author is not client.owner:
            return
        files=[(b'UwU','UwU'),(b'OwO','OwO'),(b'0w0',None)]
        await client.message_create_files(message.channel,files,'Did it work OwO?')

    @on_command
    async def test_files1(client,message,content):
        if message.author is not client.owner:
            return
        files=[(b'UwU','UwU')]
        await client.message_create_files(message.channel,files,'Did it work OwO?')
        
    @on_command
    async def bypass_connection_check(client,message,content):
        if message.author is not client.owner:
            return
        try:
            data = await client.http.client_connections(client)
        except Exception as err:
            content=repr(err)
        else:
            content=repr(data)
            
        await client.message_create(message.channel,content)

    @on_command
    async def test_connection(client,message,content):
        if message.author is not client.owner:
            return
        try:
            connections = await client.client_connections()
        except Exception as err:
            content=repr(err)
        else:
            content=connect(list(connections.values()))

        await client.message_create(message.channel,content)

    @on_command
    async def edit_name(client,message,content):
        try:
            await client.client_edit(name=content)
        except ValueError as err:
            text=err.args[0]
        except HTTPException as err:
            text=err.args[0]
        except Forbidden:
            text='Forbidden'
        else:
            text='Kyaaaa'
            update_about(client)
        await client.message_create(message.channel,text)

    @on_command
    async def edit_avatar(client,message,content):
        if message.author is not client.owner:
            return

        if message.attachments is not None:
            file = await client.download_url(message.attachments[0].url)
        else:
            file=None

        try:
            await client.client_edit(avatar=file)
        except ValueError as err:
            text=err.args[0]
        except HTTPException as err:
            text=err.args[0]
        except Forbidden:
            text='Forbidden'
        else:
            text='Kyaaaa'
            update_about(client)
        await client.message_create(message.channel,text)


##    @on_command
##    async def sleeper(client,message,content):
##        try:
##            minutes=int(content)
##        except ValueError:
##            return
##
##        if minutes<5:
##            await client.message_create(message.channel,f'Minimum time is 5 minutes!')
##            return
##        
##        target=time.monotonic()+minutes*60.
##        
##        message = await client.message_create(message.channel,f'Game starts in: {minutes} minutes')
##        while True:
##            await sleep((target-time.monotonic())%60,client.loop)
##            minutes-=1
##            if minutes==0:
##                break
##            await client.message_edit(message,f'Game starts in: {minutes} minutes')
##            
##        await client.message_edit(message,'Game started')
##
##    @on_command
##    async def channel_create0(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None:
##            return
##        await client.channel_create(guild,None,'hey',Channel_text,nsfw=True,topic='rip')
##
##    @on_command
##    async def channel_create1(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None:
##            return
##        await client.channel_create(guild,None,'hay',Channel_category,reason='do u see this?')
##
##    @on_command
##    async def channel_create2(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None:
##            return
##        await client.channel_create(guild,message.channel.category,'hoy',Channel_voice,overwrites=[cr_p_overwrite_object(USERS[530447673610993674],0,5654546)],user_limit=1)
##
##    @on_command
##    async def channel_edit(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None:
##            return
##
##        channel=guild.get_channel('hey')
##        if channel is not None:
##            await client.channel_edit(channel,name='heeey',topic='owo',nsfw=False,slowmode=14)
##            return
##
##        channel=guild.get_channel('hay')
##        if channel is not None:
##            await client.channel_edit(channel,name='haaaaay',reason='is here anything?')
##            return
##
##        channel=guild.get_channel('hoy')
##        if channel is not None:
##            await client.channel_edit(channel,name='brah',bitrate=96000,user_limit=2)
##            return
##
##    #this command does cooldowned changes too, so pls comment out parts if u run it.
##    @on_command
##    async def edit_guild(client,message,content):
##        guild=message.guild
##        if guild is None or message.author is not client.owner:
##            return
##        toedit={}
##        text_channels=guild.text_channels
##        voice_channels=guild.voice_channels
##        for _ in range(len(text_channels),2):
##            channel = await client.channel_create(guild,None,random_id().__format__('x'),Channel_text)
##            text_channels.append(channel)
##        for _ in range(len(voice_channels),2):
##            channel = await client.channel_create(guild,None,random_id().__format__('x'),Channel_voice)
##            voice_channels.append(channel)
##        with open(os.path.join(os.path.abspath('.'),'images','0000000A_touhou_koishi_kokoro_reversed.png'),'rb') as file:
##            icon1=file.read()
##        with open(os.path.join(os.path.abspath('.'),'images','0000000C_touhou_koishi.png'),'rb') as file:
##            icon2=file.read()
##
##        #name
##        await client.guild_edit(guild,name=random_id().__format__('x'),reason='reason')
##        await sleep(.5,client.loop)
##
##        #icon
##        if guild.icon:
##            await client.guild_edit(guild,icon=icon1)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,icon=None)
##        else:
##            await client.guild_edit(guild,icon=icon1)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,icon=icon2)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,icon=None)
##        await sleep(.5,client.loop)
##
##        #afk_channel
##        if guild.afk_channel is None:
##            await client.guild_edit(guild,afk_channel=voice_channels[0])
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,afk_channel=voice_channels[1])
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,afk_channel=None)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,afk_channel=voice_channels[0])
##        else:
##            await client.guild_edit(guild,afk_channel=None)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,afk_channel=voice_channels[0])
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,afk_channel=voice_channels[1])
##        await sleep(.5,client.loop)
##            
##        #system channel
##        if guild.system_channel is None:
##            await client.guild_edit(guild,system_channel=text_channels[0])
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,system_channel=text_channels[1])
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,system_channel=None)
##        else:
##            await client.guild_edit(guild,system_channel=None)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,system_channel=text_channels[0])
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,system_channel=text_channels[1])
##        await sleep(.5,client.loop)
##
##        #region
##        if guild.region is voice_regions.eu_central:
##            await client.guild_edit(guild,region=voice_regions.eu_west)
##        else:
##            await client.guild_edit(guild,region=voice_regions.eu_central)
##        await sleep(.5,client.loop)
##
##        #afk_timeout
##        if guild.afk_timeout==300:
##            await client.guild_edit(guild,afk_timeout=60)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,afk_timeout=300)
##        else:
##            await client.guild_edit(guild,afk_timeout=300)
##            await sleep(.5,client.loop)
##            await client.guild_edit(guild,afk_timeout=60)
##        await sleep(.5,client.loop)
##
##        #verification level
##        if guild.verification_level is verification_levels.medium:
##            await client.guild_edit(guild,verification_level=verification_levels.low)
##        else:
##            await client.guild_edit(guild,verification_level=verification_levels.medium)
##        await sleep(.5,client.loop) 
##
##        #content filter
##        if guild.content_filter is content_filter_levels.disabled:
##            await client.guild_edit(guild,content_filter=content_filter_levels.no_role)
##        else:
##            await client.guild_edit(guild,content_filter=content_filter_levels.disabled)
##        await sleep(.5,client.loop)
##
##        #message notification
##        if guild.message_notification is message_notification_levels.all_messages:
##            await client.guild_edit(guild,message_notification=message_notification_levels.only_mentions)
##        else:
##            await client.guild_edit(guild,message_notification=message_notification_levels.all_messages)
##        await sleep(.5,client.loop)
##
##        await client.message_create(message.channel,'DONE')
##
##    @on_command
##    async def ban_and_milk(client,message,content):
##        guild=message.guild
##        if guild is None or message.author is not client.owner:
##            return
##        
##        await client.guild_ban_add(guild,client.owner)
##        await client.guild_ban_delete(guild,client.owner)
##        await client.guild_delete(guild)

    @on_command
    async def executor_test(client,message,content):
        if message.author is not client.owner:
            return
        
        def test_blocking():
            time.sleep(10)
            return 'Done'
            
        async def test_loop(client,channel):
            for _ in range(5):
                await client.message_create(channel,'works?')
                await sleep(2.,client.loop)
                
        channel=message.channel
        
        client.loop.create_task(test_loop(client,channel))
        result = await KOKORO.run_in_executor(test_blocking)
        await client.message_create(channel,result)

    @on_command
    async def test_kick(client,message,content):
        guild=message.guild
        if guild is None or message.author is not client.owner or not content:
            return
        content=filter_content(content)
        value=content[0]
        if message.user_mentions and is_user_mention(value):
            user=message.user_mentions[0]
        else:
            user=guild.get_user(value)
            if user is None:
                try:
                    user=guild.users[int(value)]
                except (ValueError,KeyError):
                    await client.message_create(message.channel,'User could not be found')
                    
        await client.guild_user_delete(guild,user)
        await client.message_create(message.channel,f'Kicked user {user:f} {user.id}')

    @on_command
    async def role_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        
        role = await client.role_create(guild,name='test',permissions=0,color=0x565656,
            separated=True,mentionable=True,reason='for the future!')

        await sleep(1.5,client.loop)
        await client.role_edit(role,name='nope',permissions=5465,color=0,
            separated=False,mentionable=False,position=5,reason='kyaaa')

        await sleep(1.5,client.loop)
        await client.role_delete(role)

    @on_command
    async def webhook_test(client,message,content):
        channel=message.channel
        guild=channel.guild
        if message.author is not client.owner or guild is None:
            return

        await client.message_create(channel,f'Webhooks up to date: {guild.webhooks_uptodate}, should be False')
        await client.webhook_get_guild(guild)
        await sleep(1.5,client.loop)
        await client.message_create(channel,f'Webhooks up to date: {guild.webhooks_uptodate}, should be True')
        webhook = await client.webhook_create(channel,'test')
        await sleep(1.5,client.loop)
        await client.message_create(channel,f'Webhooks up to date: {guild.webhooks_uptodate}, should be False')
        await client.webhook_get_guild(guild)
        await sleep(1.5,client.loop)
        await client.message_create(channel,f'Webhooks up to date: {guild.webhooks_uptodate}, should be True')
        await client.webhook_delete(webhook)
        await sleep(1.5,client.loop)
        await client.message_create(channel,f'Webhooks up to date: {guild.webhooks_uptodate}, should be False')
        await client.webhook_get_guild(guild)
        await sleep(1.5,client.loop)
        await client.message_create(channel,f'Webhooks up to date: {guild.webhooks_uptodate}, should be True')

    @on_command
    async def new_type_test(client,message,content):
        channel=message.channel
        if message.author is not client.owner or not isinstance(channel,channel_guild_superclass):
            return
        await client.channel_edit(channel,type_=(5,0)[channel.type&1])
        await client.message_create(channel,'yayyy')
    
    #didnt work out :c
##    class new_gateway_test_class1:
##        def __init__(self,client):
##            self.client=client
##            self.loop=client.loop
##            self.websokcket=None
##        def feed_websocket(self,websocket):
##            self.websocket=websocket
##            return self
##        #await it
##        def get_gateway(self):
##            return self.client.client_gateway()
##        
##    @on_command
##    async def new_gateway_test1(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner:
##            return
##        try:
##            for times in range(2):
##                gateway = await client.http.ws_connect(new_gateway_test_class1(client))
##                print('connected')
##                async for result in gateway.websocket:
##                    try:
##                        json=from_json(result)
##                    except TypeError as err:
##                        raise result
##                    ln=len(result)
##                    print(f'receaved {ln} bytes')
##                    print(str(json)[:300])
##                    if json['op']==10:
##                        json=to_json({'op':client.websocket.HEARTBEAT,'d':json['s'],})
##                        await gateway.websocket.send_str(json)
##
##                print('quit')
##        except BaseException as err:
##            print(err)
##            traceback.print_exc()

##    @on_command
##    async def channel_move2_test(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None:
##            return
##        await client.channel_move(message.channel,2,guild)
##        await client.channel_move(message.channel,2,message.channel.category)
##        await client.channel_move(message.channel,2,guild.get_channel('test_category'))
##        await client.channel_move(message.channel.category,2,guild)
##        await client.channel_move(guild.get_channel('Important'),4,guild)

##    @on_command #failed
##    async def test_oauth2_01(client,message,content):
##        if message.author is not client.owner:
##            return
##        data = await client.http.user_get(client,message.author.id)
##        await client.message_create(message.channel,repr(data))
##
##    @on_command # found typo, still wont work #<HTTPException METHOD NOT ALLOWED (405) : 405: Method Not Allowed>
##    async def test_oauth2_02(client,message,content):
##        if message.author is not client.owner:
##            return
##        if content:
##            id_=int(content)
##        else:
##            id_=message.author.id
##        data = await client.http.user_profle_by_id(client,id_)
##        await client.message_create(message.channel,repr(data))
##    @on_command #hata.exceptions.HTTPException: <HTTPException BAD REQUEST (400) : Bots cannot use this endpoint>
##    async def test_oauth2_03_group_create(client,message,content):
##        if message.author is not client.owner:
##            return
##        content=filter_content(content)
##
##        data={'recipients':[int(content[0]),int(content[1])]}
##        data=await client.http.channel_group_create(client,data)
##        await client.message_create(message.channel,repr(data))
##        channel=Channel_group(data,client)
##
##        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(channel)])
##
##    @on_command
##    async def test_oauth2_04(client,message,content):
##        if message.author is not client.owner:
##            return
##        data = await client.http.client_application_info(client)
##        await client.message_create(message.channel,repr(data))
##
##    @on_command
##    async def test_oauth2_04(client,message,content):
##        if message.author is not client.owner:
##            return
##
##        data={ \
##            'client_id': client.id,
##            'client_secret': CLIENT_SECRET,
##            'grant_type': 'authorization_code',
##            'code': content,
##            'redirect_uri': 'https://github.com/HuyaneMatsu', #i have no clue at all
##            'scope': 'guild',
##                }
##
##        async with Request_CM(client.http.client_tokens(data)) as response:
##            response_data = await response.text(encoding='utf-8')
##            data=from_json(response_data)
##            
##        await client.message_create(message.channel,repr(data))
##
##    @on_command
##    async def test_oauth2_05(client,message,content):
##        if message.author is not client.owner:
##            return
##
##        data={ \
##            'client_id': client.id,
##            'client_secret': CLIENT_SECRET,
##            'grant_type': 'client_credentials',
##            'scope': 'identify connections',
##                }
##
##        async with Request_CM(client.http.client_tokens(data)) as response:
##            response_data = await response.text(encoding='utf-8')
##            data=from_json(response_data)
##            
##        await client.message_create(message.channel,repr(data))
##        
##    @on_command
##    async def test_oauth2_06(client,message,content):
##        if message.author is not client.owner:
##            return
##
##        data={ \
##            'client_id': client.id,
##            'client_secret': CLIENT_SECRET,
##            'grant_type': 'client_credentials',
##            'scope': 'guild',
##                }
##        
##        async with Request_CM(client.http.client_tokens(data)) as response:
##            response_data = await response.text(encoding='utf-8')
##            data=from_json(response_data)
##            
##        url='https://discordapp.com/api/v7/users/@me/connections'
##
##        headers=type(client.header)() #for keeping the type
##        headers['Authorization']=f'Bearer {data["access_token"]}'
##            
##        async with Request_CM(client.http._request2('GET',url,headers=headers)) as response:
##            response_data = await response.text(encoding='utf-8')
##            data=from_json(response_data)
##            
##        await client.message_create(message.channel,repr(data))
##
##    @on_command
##    async def test_oauth2_07(client,message,content):
##        if message.author is not client.owner:
##            return
##
##        data={ \
##            'client_id': client.id,
##            'client_secret': CLIENT_SECRET,
##            'grant_type': 'client_credentials',
##            'scope': 'guild',
##                }
##        
##        async with Request_CM(client.http.client_tokens(data)) as response:
##            response_data = await response.text(encoding='utf-8')
##            data=from_json(response_data)
##            
##        url='https://discordapp.com/api/v7/users/@me'
##
##        headers=type(client.header)() #for keeping the type
##        headers['Authorization']=f'Bearer censored'
##        #f'Bearer {data["access_token"]}'
##            
##        async with Request_CM(client.http._request2('GET',url,headers=headers)) as response:
##            response_data = await response.text(encoding='utf-8')
##            data=from_json(response_data)
##            
##        await client.message_create(message.channel,repr(data))



##    @on_command
##    async def profile_test(client,message,content):
##        if message.author is not client.owner:
##            return
##        try:
##            data= await client.http.user_profile(message.author.id)
##            print(data)
##        except Exception as err:
##            print(err)


    @on_command
    async def guild_embed_edit_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        await client.guild_embed_edit(guild,True,message.channel)
        result=connect(guild.embed)
        
        await client.message_create(message.channel,result)

    @on_command
    async def guild_embed_get_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        guild_embed = await client.guild_embed_get(guild)

        result=connect(guild_embed)

        await client.message_create(message.channel,result)

    @on_command
    async def guild_embed_delete_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        
        guild_embed = await client.guild_embed_edit(guild,False,None)
        result=connect(guild.embed)

        await client.message_create(message.channel,result)

    @on_command
    async def guild_embed_image_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        
        guild_embed_image = await client.guild_embed_image(guild,'banner4')

        await client.message_create_file(message.channel,guild_embed_image,'owo.png')

    @on_command
    async def guild_widget_image_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        
        guild_widget_image = await client.guild_widget_image(guild,'banner4')

        await client.message_create_file(message.channel,guild_widget_image,'owo.png')

    @on_command
    async def spamit(client,message,content):
        if message.author is not client.owner:
            return
        for x in range(10):
            await client.message_create(message.channel,f'spam {x}')

    @on_command
    async def integration_get_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        ingegrations = await client.integration_get_all(guild)
        result=connect(ingegrations)
        await client.message_create(message.channel,result)

    @on_command
    async def channels_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        channels = await client.channel_private_get_all()
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(channels)])

    @on_command
    async def guild_get_all_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        guilds = await client.guild_get_all()
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(guilds)])

    @on_command
    async def client_edit_nick_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        await client.client_edit_nick(guild,'owo')
        await sleep(5.,client.loop)
        await client.client_edit_nick(guild,None)

    @on_command
    async def guild_create_role_test(client,message,content):
        if message.author is not client.owner:
            return
        try:
            guild = await client.guild_create(name='Luv ya',
                channels=[cr_pg_channel_object(name=f'Love u',type_=Channel_text),],
                roles=[ \
                    cr_p_role_object(name='test1',position=0),
                    cr_p_role_object(name='test2',position=1),
                        ])
        except HTTPException as err:
            response=err.response
            response_data = await response.text(encoding='utf-8')
            
            if response.headers['content-type']=='application/json':
                response_data=from_json(response_data)

            print(response_data)
            
        else:
            access = await client.owners_access(['guilds.join'])
            user = await client.user_info(access)
            await client.guild_user_add(guild,user)
            print(guild.roles)
            await sleep(60.,client.loop)
            await client.guild_delete(guild)

    @on_command
    async def guild_users_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return

        users = await client.guild_users(guild)
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(users)])

    #cannot create invite from category channel, we raise ValueError from now!
    @on_command
    async def scowez_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        
        invites=[]
        try:
            for channel in guild.all_channel.values():
                invite = await client.invite_create(channel)
                invites.append(invite)
        except Exception as err:
            print(err)
            print(f'channel name : {channel.name}\nchannel id : {channel.id}\nchannel type: {channel.type}')
            traceback.print_exc()

            response=err.response
            response_data = await response.text(encoding='utf-8')
            
            if response.headers['content-type']=='application/json':
                response_data=from_json(response_data)

            print(response_data)
            
        for invite in invites:
            await client.invite_delete(invite)
            
    @on_command
    async def region_check(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        
        regions,optimals = await client.guild_regions(guild)
        result=[f'```Guild\'s name : {guild.name}\nVoice region: {guild.region.name}\nThe guild has {len(regions)} regions available to choose from.']
        if not optimals:
            result.append('There is no optimal region available for this guild.')
        else:
            result.append('Optimal regions for this guild:')
            for index,optimal in enumerate(optimals,1):
                result.append(f'  {index}.: {optimal.name}')
        result.append('```')
        await client.message_create(message.channel,'\n'.join(result))
        
    @on_command
    async def guild_channels_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        channels = await client.guild_channels(guild)
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(channels,mixed=True,name='Channels')])

    @on_command
    async def guild_roles_test(client,message,content):
        guild=message.guild
        if message.author is not client.owner or guild is None:
            return
        roles = await client.guild_roles(guild)
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(roles)])

    @on_command
    async def users_test(client,message,content):
        if message.author is not client.owner:
            return
        users=message.channel.users
        result=[f'i see {len(users)} users at this channel:']
        
        index=0
        limit=len(users)-1
        while True:
            if index==20 or index>limit:
                break
            user=users[index]
            index=index+1
            result.append(f'{index:>2}.: {user:f}')

        if index!=len(users):
            result.append(f'And {len(users)-index} more')

        await client.message_create(message.channel,'\n'.join(result))

    @on_command
    async def get_user_from_channel_test(client,message,content):
        if message.author is not client.owner:
            return
        
        user=message.channel.get_user(content)
        if user is None:
            text='nope'
        else:
            text='yespls'
        
        await client.message_create(message.channel,text)

    @on_command
    async def embed_image_test(client,message,content):
        if message.author is not client.owner:
            return
        
        embed=Embed('pure test, no judge')
        embed.image=Embed_image('attachment://test.png')
        file=open(os.path.join(os.path.abspath('.'),'images','0000000C_touhou_koishi.png'),'rb')
        await client.message_create_file(message.channel,file,'test.png',embed=embed)

    @on_command
    async def bytes_io_test(client,message,content):
        if message.author is not client.owner:
            return

        embed=Embed('pure test, no judge')
        embed.image=Embed_image('attachment://guessme.png')
        buffer=ASBytesIO()
        with open(os.path.join(os.path.abspath('.'),'images','0000000C_touhou_koishi.png'),'rb') as file:
            buffer.write(file.read())
        buffer.seek(0)
        await client.message_create_file(message.channel,buffer,'guessme.png',embed=embed)

    @on_command
    async def paranoia(client,message,content):
        embed=Embed('Paranoia','',0x45E9A9,'https://www.youtube.com/watch?v=wnli28pjsn4')
        message = await client.message_create(message.channel,'',embed)


    @on_command
    async def owner_invite(client,message,content):
        if message.author is not client.owner:
            return
        
        guild=client.get_guild(content)
        
        if guild is None:
            return
        
        try:
            invite = await client.invite_create(guild.channels[0],0,1)
        except Forbidden:
            return
        
        channel = await client.channel_private_create(message.author)
        await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')

    @on_command
    async def ban(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_ban_user:
            return

        content=filter_content(content)
        if not content:
            await client.message_create(message.channel,'And who, if i can ask so?')
            return

        name=content.pop(0)
        if is_user_mention(name) and message.user_mentions:
            user=message.user_mentions[0]
        else:
            user=guild.get_user(name)
            if user is None:
                await client.message_create(message.channel,'Could not find that user')
                return
        days=0
        if content and content[0].isdigit():
            value=int(content[0])
            if -1<value<8:
                content.pop(0)
                days=value

        if content:
            content.insert(0,'Executed by {message.author:f}, reason:')
            reason=smart_join(content,255)
        else:
            reason=f'Executed by {message.author:f}'

        await client.guild_ban_add(guild,user,days,reason)
        await client.message_create('ExeCUTEd')

    @on_command
    async def ban_get_by_id(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_ban_user:
            return
        
        if not is_id(content):
            message = await client.message_create('Pls type an id too')
            await sleep(30.,client.loop)
            try:
                await client.message_delete(message)
            except (Forbidden,HTTPException):
                pass
            return
        
        id_=int(content)
        
        try:
            user,reason = await client.guild_ban_get(guild,id_)
        except HTTPException:
            embed=Embed(description=f'{guild.name} {guild.id} has no ban for id: {id_}')
        except Forbidden:
            return
        else:
            if reason is None:
                embed=Embed()
            else:
                embed=Embed(title='Reason:',description=reason)
            embed.author=Embed_author(user.avatar_url_as(size=64),user.full_name)

        await client.message_create(message.channel,embed=embed)

    @on_command
    async def unban(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_ban_user or not content:
            return
        
        content=filter_content(content)
        value=content.pop(0)
        
        if not is_id(value):
            message = await client.message_create('Pls type an id too')
            await sleep(30.,client.loop)
            try:
                await client.message_delete(message)
            except (Forbidden,HTTPException):
                pass
            return

        id_=int(value)

        try:
            await client.guild_user_unban(guild,Unknown('User',id_),reason)
        except HTTPException:
            embed=Embed(description=f'{guild.name} {guild.id} has no ban for id: {id_}')
        except Forbidden:
            return
        else:
            user = await client.user_get(id_)
            if len(content):
                embed=Embed('Unbanned with reason:',smart_join(content.split(),255))
            else:
                embed=Embed('Unbanned')
            embed.author=Embed_author(user.avatar_url_as(size=64),user.full_name)
        await client.message_create(message.channel,embed=embed)


    @on_command
    async def prune(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return
        try:
            if len(content)==5 and content.lower()=='prune':
                result = await client.guild_prune(guild,16,reason=f'Executed by {message.author:f}.')
                text=f'Pruned {result} users.'
            else:
                result = await client.guild_prune_estimate(guild,16)
                text=f'{result} users to be pruned'
        except Forbidden:
            text='Acces denied'

        await client.message_create(message.channel,text)

    @on_command
    async def kick(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_kick_user:
            return

        content=filter_content(content)
        if not content:
            await client.message_create(message.channel,'And who, if i can ask so?')
            return

        name=content.pop(0)
        if is_user_mention(name) and message.user_mentions:
            user=message.user_mentions[0]
        else:
            user=guild.get_user(name)
            if user is None:
                await client.message_create(message.channel,'Could not find that user')
                return

        reason=smart_join(content,170)
            
        if content:
            reason=f'Executed by {message.author:f}, reason: {reason}'
        else:
            reason=f'Executed by {message.author:f}'

        await client.guild_user_kick(guild,user,reason)
        await client.message_create('ExeCUTEd')

    @on_command.add('type')
    async def on_command_type(client,message,content):
        await client.typing(message.channel)


    
    @on_command
    async def hug(client,message,content):
        channel=message.channel
        guild=message.guild
        target=message.author
        if content:
            if message.user_mentions and is_user_mention(content):
                target=message.user_mentions[0]
            elif guild is not None:
                user=guild.get_user(content)
                if user is not None:
                    target=user
            
        await client.message_create(channel,'And what is the magic word?')
        try:
            await wait_for_message(client,message.channel,lambda message,pattern=MAGIC_PATTERN,author=message.author:message.author is author and re.match(pattern,message.content),30.)
        except TimeoutError:
            return
        await client.message_create(channel,f'{client.mention_at(guild)} hugs {target.mention_at(guild)}')

    @on_command
    async def say(client,message,content):
        channel=message.channel
        
        message_to_delete1 = await client.message_create(channel,'prepared')

        try:
            message_to_delete2 = await wait_for_message(client,channel,lambda message:True,30.)
        except TimeoutError:
            try:
                await client.message_delete(message_to_delete1)
            except Forbidden:
                pass
            return
        try:
            await client.message_delete_multiple([message_to_delete1,message_to_delete2])
        except Forbidden:
            pass
            
        await client.message_create(channel,message_to_delete2.content)

    async def failure_test_on_failure(self,message,args):
        if args:
            await self.message_create(message.channel,'My masuta!')
        else:
            await self.message_create(message.channel,'Guild only')
    @on_command
    @content_parser('guild',
                    'condition, default="message.author is client.owner"',
                    on_failure=failure_test_on_failure)
    async def failure_test(self,message,guild):
        await self.message_create(message.channel,'Nothing interesting here')

    @on_command
    async def file_test1(client,message,content):
        if message.author is not client.owner:
            return
        with open(os.path.join(os.path.abspath('.'),'images','0000000A_touhou_koishi_kokoro_reversed.png'),'rb') as file:
            await client.message_create_file(message.channel,file)
            await client.message_create_file(message.channel,file)

    @on_command
    async def file_test2(client,message,content):
        if message.author is not client.owner:
            return
        with ASFile(os.path.join(os.path.abspath('.'),'images','0000000A_touhou_koishi_kokoro_reversed.png')) as file:
            await client.message_create_file(message.channel,file)
            await client.message_create_file(message.channel,file)

    @on_command
    async def reaction_remove_test(client,message,content):
        if message.author is not client.owner:
            return

        await client.reaction_add(message,BUILTIN_EMOJIS['x'])
        await client.reaction_delete_own(message,BUILTIN_EMOJIS['x'])
        await client.reaction_delete_own(message,BUILTIN_EMOJIS['x'])
        #does not drops error

    @on_command
    @content_parser('condition, default="message.author is not client.owner"',
                'int',
                'channel, flags=mnig, default="message.channel"',)
    async def emojis_get_0(client,message,message_id,channel):
        try:
            target_message = await client.message_get(channel,message_id)
        except (Forbidden,HTTPException):
            await client.message_create(message.channel,'Access denied or not existing message')
            return
        if target_message.reactions is None:
            await client.message_create(message.channel,'No reaction on that message.')
            return
        
        await Koishi.reaction_users(target_message,target_message.reactions.__iter__().__next__())

        result=[]
        for emoji,list_ in target_message.reactions.items():
            for user in list_:
                result.append(f'{emoji:e} {user:f}')
            if list_.unknown:
                result.append(f'{emoji:e} + {list_.unknown}')
        
        pagination(client,message.channel,[{'content':chunk} for chunk in cchunkify(result)])
    
    @on_command
    @content_parser('condition, default="message.author is not client.owner"',
                'int',
                'channel, flags=mnig, default="message.channel"',)
    async def emojis_get_1(client,message,message_id,channel):
        try:
            target_message = await client.message_get(channel,message_id)
        except (Forbidden,HTTPException):
            await client.message_create(message.channel,'Access denied or not existing message')
            return
        if target_message.reactions is None:
            await client.message_create(message.channel,'No reaction on that message.')
            return
        
        await Koishi.reaction_users_all(target_message,target_message.reactions.__iter__().__next__())

        result=[]
        for emoji,list_ in target_message.reactions.items():
            for user in list_:
                result.append(f'{emoji:e} {user:f}')
            if list_.unknown:
                result.append(f'{emoji:e} + {list_.unknown}')
        
        pagination(client,message.channel,[{'content':chunk} for chunk in cchunkify(result)])

    @on_command
    @content_parser('condition, default="message.author is not client.owner"',
                'int',
                'channel, flags=mnig, default="message.channel"',)
    async def emojis_get_2(client,message,message_id,channel):
        try:
            target_message = await client.message_get(channel,message_id)
        except (Forbidden,HTTPException):
            await client.message_create(message.channel,'Access denied or not existing message')
            return
        
        if target_message.reactions is None:
            await client.message_create(message.channel,'No reaction on that message.')
            return
        
        await Koishi.reaction_load_all(target_message)

        result=[]
        for emoji,list_ in target_message.reactions.items():
            for user in list_:
                result.append(f'{emoji:e} {user:f}')
            if list_.unknown:
                result.append(f'{emoji:e} + {list_.unknown}')
        
        pagination(client,message.channel,[{'content':chunk} for chunk in cchunkify(result)])


    @on_command
    async def webhook_test00(client,message,content):
        if message.author is not client.owner:
            return
        webhook = await client.webhook_get(555476334210580508)
        result = await client.webhook_send(webhook,'test0',wait=False)
        await client.message_create(message.channel,f'test0: {result!r}')
        result = await client.webhook_send(webhook,'test1',wait=True)
        await client.message_create(message.channel,f'test1: {result!r}')


    @on_command
    async def message_file_test_00(client,message,content):
        if message.author is not client.owner:
            return
        await client.message_create(message.channel,'1 file no name',file=b'owo')
        await client.message_create(message.channel,'2 file with name',file=('owo.txt',b'owo'))
        await client.message_create(message.channel,'3 file in list',file=[b'owo'])
        await client.message_create(message.channel,'4 files in list',file=[b'owo',b'nom'])
        await client.message_create(message.channel,'5 files in list mixed pair',file=[('owo.txt',b'owo'),b'nom'])
        await client.message_create(message.channel,'6 files in list pair',file=[('owo.txt',b'owo'),('nom.txt',b'nom')])
        await client.message_create(message.channel,'7 file in dict',file={'owo.txt':b'owo'})
        await client.message_create(message.channel,'8 files in dict',file={'owo.txt':b'owo','nom.txt':b'nom'})

    @on_command
    async def typingbreak(client,message,content):
        if message.author is client.owner:
            with client.keep_typing(message.channel):
                await sleep(30.,client.loop)

    @on_command.add('emoji')
    async def emoji_command(client,message,content):
        guild=message.guild
        if guild is None:
            return
        
        try:
            await client.message_delete(message,reason='Used emoji command')
        except Forbidden:
            pass
        
        emoji=guild.get_emoji(content)
        if emoji:
            await client.message_create(message.channel,str(emoji))



# - : - # dungeon_sweeper.py # - : - #

##STAGE_NAME_PATTERN_RE=re.compile(
##    '^(chapter|chapte|chapt|chap|cha|ch|c)[ \-_\.\,;\+]*(\d)[ \-_\.\,;\+]*'
##    '(tutorial|tutoria|tutori|normal|tutor|norma|tuto|easy|norm|hard|'
##    'tut|eas|nor|har|tu|ea|no|ha|t|e|n|h)[ \-_\.\,;\+]*(\d{1,2})',re.I)
##
##def convert_stage_name(value):
##    parsed=re.match(STAGE_NAME_PATTERN_RE,value)
##    if parsed is None:
##        raise IndexError
##    
##    groups=parsed.groups()
##    
##    try:
##        i1=int(groups[1])
##        i2=('TNEH').index(groups[2][0].upper())
##        i3=int(groups[3])
##    except ValueError:
##        raise IndexError from None
##
##    return i1,i2,i3
