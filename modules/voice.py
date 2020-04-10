# -*- coding: utf-8 -*-
import re, os, wave

from hata import alchemy_incendiary, sleep, Task, Embed, eventlist, Color, YTaudio, DownloadError, LocalAudio
from hata.ext.commands import Command

import pers_data

VOICE_COLOR = Color.from_rgb(235, 52, 207)
VOICE_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(VOICE_COMMANDS)

def teardown(lib):
    Koishi.commands.unextend(VOICE_COMMANDS)

#await it
def save_voice(client,frames):
    return client.loop.run_in_executor(alchemy_incendiary(_save,(frames,),),)

def _save(frames):
    with wave.open('test.wav','wb') as wav_writer:
        wav_writer.setframerate(48000)
        wav_writer.setsampwidth(2)
        wav_writer.setnchannels(2)
        wav_writer.writeframes(b''.join(frames))
    
AUDIO_PATH=pers_data.AUDIO_PATH

FILENAMES=[]
def collect_local_audio():
    for filename in os.listdir(AUDIO_PATH):
        if filename.endswith('.mp3'):
            FILENAMES.append(filename)
            
collect_local_audio()
    
PERCENT_RP=re.compile('(\d*)[%]?')

VOICE_SUBCOMMANDS={}
            
async def voice_join(client,message,content):
    channel=message.channel
    guild=channel.guild
    while True:
        state=guild.voice_states.get(message.author.id,None)
        if state is None:
            text='You are not at a voice channel!'
            break

        channel=state.channel
        if not channel.cached_permissions_for(client).can_connect:
            text='I have no permissions to connect to that channel'
            break
        
        try:
            voice_client = await client.join_voice_channel(channel)
        except TimeoutError:
            text='Timed out meanwhile tried to connect.'
            break
        except RuntimeError:
            text='The client cannot play voice, some libraries are not loaded'
            break
        
        text=f'Joined to {state.channel.name}'
        if content:
            amount=PERCENT_RP.fullmatch(content)
            if amount:
                amount=int(amount.groups()[0])
                if amount<0:
                    amount=0
                elif amount>200:
                    amount=200
                voice_client.volume=amount/100.
                text=f'{text}; Volume set to {amount}%'
        break
    
    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['join']=voice_join

async def voice_pause(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client is None:
        text='There is no voice client at your guild'
    else:
        voice_client.pause()
        text='Voice paused.'

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['pause']=voice_pause

async def voice_resume(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client is None:
        text='There is no voice client at your guild'
    else:
        voice_client.resume()
        text='Voice resumed'

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['resume']=voice_resume

async def voice_leave(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client is None:
        text='There is no voice client at your guild'
    else:
        await voice_client.disconnect()
        text=f'{client.name} disconnects, bai bai nya!'

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['leave']=voice_leave

async def voice_play(client,message,content):
    while True:
        if YTaudio is None:
            text='This option in unavailable :c'
            break
        
        voice_client=client.voice_client_for(message)
        
        if voice_client is None:
            text='There is no voice client at your guild'
            break
        
        if not content:
            if voice_client.player is None:
                text='Nothing is playing now Good Sir!'
                break
            
            if voice_client.is_paused():
                voice_client.resume()
                text=f'Resumed playing: {voice_client.player.source.title}'
                break

            text=f'Now playing: {voice_client.player.source.title}'
            break
        
        try:
            with client.keep_typing(message.channel,7200.):
                source = await YTaudio(content,message.channel.guild.id)
        except DownloadError as err: #raised by YTdl
            text='Error meanwhile downloading'
            break
        except ReferenceError: #raised by executor
            text='There is an active download from the guild already.'
            break
        except PermissionError: #raised by YTdl
            text='The file is already playing somewhere'
            break

        if voice_client.append(source):
            text=f'Now playing {source.title}!'
        else:
            text=f'Added to queue {source.title}!'
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')


VOICE_SUBCOMMANDS['play']=voice_play

async def voice_local(client,message,content):
    while True:
        voice_client=client.voice_client_for(message)
        
        if voice_client is None:
            text='There is no voice client at your guild'
            break
        
        if not content:
            if voice_client.player is None:
                text='Nothing is playing now Good Sir!'
                break
            
            if voice_client.is_paused():
                voice_client.resume()
                text=f'Resumed playing: {voice_client.player.source.title}'
                break
            
            text=f'Now playing: {voice_client.player.source.title}'
            break
        
        content=content.split(' ')
        for index in range(len(content)):
            word=content[index]
            word=re.escape(word)
            content[index]=word

        pattern=re.compile('.*?'.join(content),re.I)

        most_accurate=None

        index=0
        limit=len(FILENAMES)
        
        while True:
            if index==limit:
                break
            
            name=FILENAMES[index]
            parsed=pattern.search(name)
            
            if parsed is None:
                index=index+1
                continue

            start=parsed.start()
            length=parsed.end()-start
            most_accurate=(start,length,len(name),name)
            break
        
        if most_accurate is None:
            text='Not found anything, what matches.'
            break
        
        while True:
            index=index+1
            if index==limit:
                break

            name=FILENAMES[index]
            parsed=pattern.search(name)
            
            if parsed is None:
                continue

            start=parsed.start()
            target=most_accurate[0]
            if start>target:
                continue

            if start<target:
                most_accurate=(start,parsed.end()-start,len(name),name)
                continue

            length=parsed.end()-start
            target=most_accurate[1]
            
            if length>target:
                continue

            if length<target:
                most_accurate=(start,length,len(name),name)
                continue
            
            name_length=len(name)
            target=most_accurate[2]
            if name_length>target:
                continue

            if name_length<target:
                most_accurate=(start,length,name_length,name)
                continue
            
            target=most_accurate[3]
            if name>target:
                continue
            
            most_accurate=(start,length,name_length,name)
            continue
        
        name=most_accurate[3]
        path=os.path.join(AUDIO_PATH,name)
        
        try:
            source = await LocalAudio(path)
        except PermissionError:
            text='The file is already playing somewhere'
            break

        if voice_client.append(source):
            text=f'Now playing {source.title}!'
        else:
            text=f'Added to queue {source.title}!'
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['local']=voice_local

async def voice_volume(client,message,content):
    while True:
        voice_client=client.voice_client_for(message)
        if voice_client is None:
            text='There is no voice client at your guild'
            break
        
        if not content:
            text=f'{round(voice_client.volume*100.)}% desu'
            break
        
        amount=PERCENT_RP.fullmatch(content)
        if not amount:
            text='*Number*% pls'
            break
        
        amount=int(amount.groups()[0])
        if amount<0:
            amount=0
        elif amount>200:
            amount=200
        
        voice_client.volume=amount/100.
        text=f'Volume set to {amount}%'
        break

    await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['volume']=voice_volume

async def voice_skip(client,message,content):
    while True:
        voice_client=client.voice_client_for(message)
        if voice_client is None:
            text='There is no voice client at your guild.'
            break
        
        if voice_client.player is None:
            text='There is nothing to skip now.'
            break
        
        text=f'Skipping: {voice_client.player.source.title}'
        voice_client.skip()
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['skip']=voice_skip

async def voice_stop(client,message,content):
    while True:
        voice_client=client.voice_client_for(message)
        if voice_client is None:
            text='There is no voice client at your guild'
            break
        
        if voice_client.player is None:
            text='I don\'t play anything, so I can not stop it.'
            break
        
        text='Stopped playing'
        voice_client.stop()
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['stop']=voice_stop
async def voice_move(client,message,channel):
    guild=message.guild
    try:
        channel = guild.all_channel[int(channel)]
    except (KeyError,ValueError):
        channel=None
    while True:
        if channel is None:
            state=guild.voice_states.get(message.author.id,None)
            if state is None:
                text='You must be in vocie channel, or you should pass a voice channel.'
                break
            
            channel=state.channel
            if not message.channel.cached_permissions_for(client).can_connect:
                text='I have no permissions to connect to that channel.'
                break
            
        else:
            if channel.type!=2:
                text='Not voice channel.'
                break

        voice_client=client.voice_client_for(message)
        if voice_client is None:
            await client.join_voice_channel(channel)
        else:
            #client.join_voice_channel works too, if u wanna move, but this is an option too
            await voice_client.move_to(channel)
            
        text=f'Joined channel: {channel.name}.'
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['move']=voice_move

async def voice_partyisover(client,message,content):
    channel=message.channel
    guild=channel.guild
    
    if not client.is_owner(message.author):
        if not guild.permissions_for(message.author).can_administrator:
            return
    
    
    while True:
        voice_client=client.voice_client_for(message)
        if voice_client is None:
            text='I don\'t see any parties arround me.'
            break

        Task(voice_client.disconnect(),client.loop)
        
        channel=voice_client.channel
        users=[]
        for state in guild.voice_states.values():
            if (state.channel is not channel):
                continue
                
            user=state.user
            if (user==client):
                continue
            
            users.append(user)

        if not users:
            return
        
        if guild.cached_permissions_for(client).can_move_users:
            for user in users:
                Task(client.user_voice_kick(user,guild),client.loop)
            return
        
        text='I have no permission to disconnect other users.'
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['partyisover']=voice_partyisover


async def voice_save(client,message,content):
    if not client.is_owner(message.author):
        return

    voice_client=client.voice_client_for(message)
    if voice_client is None:
        await client.message_create(message.channel,'No clients found')
        return

    await client.message_create(message.channel,'Talk now')
    
    reader=voice_client.listen()
    await sleep(10.,client.loop)
    reader.stop()

    frames=reader.get_audio_frames_for(message.author,flush=True,fill=False)
    if not frames:
        await client.message_create(message.channel,'U sure, u talked?')
        return

    await save_voice(client,frames)

    await client.message_create(message.channel,'pat me!')
    return
    
VOICE_SUBCOMMANDS['save']=voice_save

async def voice_description(client,message):
    is_owner=client.is_owner(message.author)
    
    if is_owner:
        is_admin=True
    else:
        is_admin=message.channel.permissions_for(message.author).can_administrator
        
    prefix = client.command_processer.get_prefix_for(message)
    text=(
        'Voice related command colection!\n'
        f'Usage: `{prefix}voice (subcommand) ...`\n'
        'Subcommands:'
        f'- `{prefix}voice join <n%>` : Joins me to the voice channel, where '
        'you are. You can join me with a set % volume as well.\n'
        f'- `{prefix}voice move <channel>` : You can move me between voice '
        'channels. If you don\'t pass a channel, I\'ll check yours.\n'
        f'- `{prefix}voice leave` : Disconnects me from the channel :c\n'
        f'- `{prefix}voice pause` : Pauses my player.\n'
        f'- `{prefix}voice resume` : Resumes my player.\n'
        f'- `{prefix}voice skips` : Skips the actual source.\n'
        f'- `{prefix}voice stop` : Stops my player and clears the queue.\n'
        f'- `{prefix}voice play <link_or_title>` : I will search the link or '
        'title up and play it.  If you did not pass anymeow, I\'ll tell you, '
        'what I am currently playing.\n'
        f'- `{prefix}voice local <name>` : I\'ll try to search it at my '
        'local collection. If nothing is passed, I\'ll tell you, what I am '
        'currently playing.\n'
        f'- `{prefix}voice volume <n%>`: You can change my player\'s volume. '
        'If you not say any volume, I\'ll tell you the actual one.'
            )
    
    if is_owner or is_admin:
        connected=[text]
        if is_admin:
            connected.append(
                f'\n- `{prefix}voice partyisover`: I disconnect everyone, '
                'who is at the same channel as me. *Admin only.*',
                    )
        if is_owner:
            connected.append(
                f'\n- `{prefix}voice save`: I save 10s of your audio. '
                '*Owner only, experimental.*',
                    )
        text=''.join(connected)
    
    embed=Embed('voice',text,color=VOICE_COLOR)
    await client.message_create(message.channel,embed=embed)

@VOICE_COMMANDS(category='VOICE', description=voice_description)
async def voice(client,message,sub_command:str,rest):
    guild=message.guild
    if guild is None:
        return
    
    if not sub_command:
        await voice_description(client,message)
        return

    try:
        command=VOICE_SUBCOMMANDS[sub_command]
    except KeyError:
        await voice_description(client,message)
        return
    
    await command(client,message,rest)
