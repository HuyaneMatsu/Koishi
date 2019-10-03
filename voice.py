# -*- coding: utf-8 -*-
import re
from hata import player
from hata.parsers import eventlist
from hata.others import filter_content
from hata.futures import sleep,Task
from help_handler import HELP
import pers_data
import os
from hata.reader import AudioReader
from hata.dereaddons_local import alchemy_incendiary
import wave

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
            amount=PERCENT_RP.fullmatch(content[0])
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
        if player.youtube_dl is None:
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
                source = await player.YTaudio(client.loop,' '.join(content),message.channel.guild.id)
        except player.DownloadError as err: #raised by YTdl
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
            source = await player.LocalAudio(client.loop,path)   
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
        
        amount=PERCENT_RP.fullmatch(content[0])
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
            text='There is no voice client at your guild'
            break
        
        if voice_client.player is None:
            text='There is nothing to skip now'
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
            text='I dont play anything, so i cant stop it.'
            break
        
        text='Stopped playing'
        voice_client.stop()
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['stop']=voice_stop

async def voice_move(client,message,content):
    guild=message.channel.guild
    while True:
        if content:
            name=content[0]
            channel=guild.get_channel(name)
            if channel is None:
                text=f'Not existing channel: "{name}"!'
                break
            
            if channel.type!=2:
                text='Not voice channel.'
                break
            
        else:
            state=guild.voice_states.get(message.author.id,None)
            if state is None:
                text='You must be in vocie channel, or you must add a voice channel name to join to'
                break
            
            channel=state.channel
            if not message.channel.cached_permissions_for(client).can_connect:
                test='I have no permissions to connect to that channel'
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
    while True:
        voice_client=client.voice_client_for(message)
        if voice_client is None:
            text='I dont see any parties arround me.'
            break
        
        if guild.permissions_for(message.author).can_move_users and guild.cached_permissions_for(client).can_move_users:
            channel=voice_client.channel
            for state in guild.voice_states.values():
                if state.channel is channel and state.user is not client:
                    Task(client.user_voice_kick(state.user,guild),client.loop)

            Task(voice_client.disconnect(),client.loop)
            return
        
        text='Missing permissions.'
        break

    message = await client.message_create(message.channel,text)
    await sleep(30.,client.loop)
    await client.message_delete(message,reason='Voice messages expire after 30s.')

VOICE_SUBCOMMANDS['partyisover']=voice_partyisover


async def voice_save(client,message,content):
    if not client.is_owner(message.author):
        await client.message_create(message.channel,'Owner only desu')
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

async def voice(client,message,content):
    guild=message.guild
    if guild is None:
        return
    content=filter_content(content)
    
    if not content:
        await client.message_create(message.channel,embed=HELP['voice'])
        return
    
    key=content.pop(0).lower()

    try:
        command=VOICE_SUBCOMMANDS[key]
    except KeyError:
        await client.message_create(message.channel,embed=HELP['voice'])
        return

    await command(client,message,content)
    
