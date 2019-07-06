# -*- coding: utf-8 -*-
import re
from hata import player
from hata.parsers import eventlist
from hata.others import filter_content
from hata.futures import sleep,Task
from help_handler import HELP

async def voice(client,message,content):
    guild=message.guild
    if guild is None:
        return
    content=filter_content(content)
    text=''
    while True:
        if not content:
            break
        key=content.pop(0)
        if key=='join':
            state=guild.voice_states.get(message.author.id,None)
            if not state:
                text='You are not at a voice channel!'
                break
            voice_client = await client.join_voice_channel(state.channel)
            text=f'Joined to {state.channel.name}'
            if content:
                amount=re.match(r'^(\d*)[%]{0,1}$',content[0])
                if amount:
                    amount=int(amount.groups()[0])
                    if amount<0:
                        amount=0
                    elif amount>100:
                        amount=100
                    voice_client.volume=amount/100.
                    text=f'{text}; Volume set to {amount}%'
            break
        if key=='pause':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
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
            if not player.youtube_dl:
                text='You need to install youtube_dl 1st!'
                break
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='There is no voice client at your guild'
                break
            if not content:
                if not voice_client.player:
                    text='Nothing is playing now Good Sir!'
                elif voice_client.is_paused:
                    voice_client.resume()
                    text=f'Resumed playing: {voice_client.player.source.title}'
                else:
                    text=f'Now playing: {voice_client.player.source.title}'
                break
            try:
                #works too:
                #source=player.PCM_volume_transformer(player.FFmpegPCMaudio('songname.mp3'))
                with client.keep_typing(message.channel,7200.):
                    source = await player.YTaudio(client.loop,' '.join(content),guild.id,voice_client.channel.bitrate)   
            except player.DownloadError as err: #raised by YTdl
                text='Error meanwhile downloading'
            except ReferenceError: #raised by executor
                text='There is an active download from the guild already.' 
            except PermissionError: #raised by YTdl
                text='The file is already playing'
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
            amount=re.match(r'^(\d*)[%]{0,1}$',content[0])
            if not amount:
                text='*Number*% pls'
                break
            amount=int(amount.groups()[0])
            if amount<0:
                amount=0
            elif amount>100:
                amount=100
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
                if not state:
                    text='You must be in vocie channel, or you must add a voice channel name to join to'
                    break
                channel=state.channel
            
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                voice_client = await client.join_voice_channel(channel)
            else:
                #client.join_voice_channel works too, if u wanna move, but this is an option too
                await voice_client.move_to(message.channel)
            text=f'Joined channel: {channel.name}.'
            break
        if key=='partyisover':
            voice_client=client.voice_client_for(message)
            if voice_client is None:
                text='I dont see any parties arround me.'
                break
            
            if guild.permissions_for(message.author).can_move_users and guild.permissions_for(client).can_move_users:
                channel=voice_client.channel
                for state in guild.voice_states.values():
                    if state.channel is channel and state.user is not client:
                        Task(client.user_voice_kick(state.user,guild),client.loop)
                Task(voice_client.disconnect(),client.loop)
                return
            
            text='Missing permissions.'
            break

        break

    if text:
        message = await client.message_create(message.channel,text)
        await sleep(30.,client.loop)
        await client.message_delete(message,reason='Voice messages expire after 30s.')
    else:
        await client.message_create(message.channel,embed=HELP['voice'])

