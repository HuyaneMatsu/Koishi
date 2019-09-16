# -*- coding: utf-8 -*-
import re
from hata import player
from hata.parsers import eventlist
from hata.others import filter_content
from hata.futures import sleep,Task
from help_handler import HELP
import pers_data
import os

AUDIO_PATH=pers_data.AUDIO_PATH

FILENAMES=[]
def collect_local_audio():
    for filename in os.listdir(AUDIO_PATH):
        if filename.endswith('.mp3'):
            FILENAMES.append(filename)
            
collect_local_audio()
    
PERCENT_RP=re.compile('(\d*)[%]?')

async def voice(client,message,content):
    guild=message.guild
    if guild is None:
        return
    content=filter_content(content)
    text=None
    while True:
        if not content:
            break
        key=content.pop(0)

        if key=='join':
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
            else:
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
        
        if key=='pause':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
                break
            else:
                voice_client.pause()
                text='Voice paused.'
                break
        if key=='resume':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
            else:
                voice_client.resume()
                text='Voice resumed'
            break
        if key=='leave':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
            else:
                await voice_client.disconnect()
                text=f'{client.name} disconnects, bai bai nya!'
            break
        
        if key=='play':
            if player.youtube_dl is None:
                text='You need to install youtube_dl 1st!'
                break
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
                break
            if not content:
                if not voice_client.player:
                    text='Nothing is playing now Good Sir!'
                elif voice_client.is_paused():
                    voice_client.resume()
                    text=f'Resumed playing: {voice_client.player.source.title}'
                else:
                    text=f'Now playing: {voice_client.player.source.title}'
                break
            try:
                with client.keep_typing(message.channel,7200.):
                    source = await player.YTaudio(client.loop,' '.join(content),guild.id)   
            except player.DownloadError as err: #raised by YTdl
                text='Error meanwhile downloading'
            except ReferenceError: #raised by executor
                text='There is an active download from the guild already.' 
            except PermissionError: #raised by YTdl
                text='The file is already playing somewhere'
            else:
                if voice_client.append(source):
                    text=f'Now playing {source.title}!'
                else:
                    text=f'Added to queue {source.title}!'
            break

        if key=='local':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
                break
            if not content:
                if not voice_client.player:
                    text='Nothing is playing now Good Sir!'
                elif voice_client.is_paused():
                    voice_client.resume()
                    text=f'Resumed playing: {voice_client.player.source.title}'
                else:
                    text=f'Now playing: {voice_client.player.source.title}'
                break
            pattern=re.compile(' '.join(content),re.I)
            for name in FILENAMES:
                if pattern.search(name) is None:
                    continue
                break
            else:
                text='Not found anything to match'
                break
            
            path=os.path.join(AUDIO_PATH,name)
            
            try:
                source = await player.LocalAudio(client.loop,path)   
            except PermissionError: #raised by YTdl
                text='The file is already playing somewhere'
            else:
                if voice_client.append(source):
                    text=f'Now playing {source.title}!'
                else:
                    text=f'Added to queue {source.title}!'
            break
                
        
        if key=='volume':
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
        if key=='skip':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
                break
            if not voice_client.player:
                text='There is nothing to skip now'
                break
            text=f'Skipping: {voice_client.player.source.title}'
            voice_client.skip()
            break
        if key=='stop':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
                break
            if not voice_client.player:
                text='I dont play anything, so i cant stop it.'
                break
            text='Stopped playing'
            voice_client.stop()
            break
        
        if key=='move':
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
                voice_client = await client.join_voice_channel(channel)
            else:
                #client.join_voice_channel works too, if u wanna move, but this is an option too
                await voice_client.move_to(channel)
            text=f'Joined channel: {channel.name}.'
            break
        
        if key=='partyisover':
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

        break

    if text is None:
        await client.message_create(message.channel,embed=HELP['voice'])
    else:
        message = await client.message_create(message.channel,text)
        await sleep(30.,client.loop)
        await client.message_delete(message,reason='Voice messages expire after 30s.')
