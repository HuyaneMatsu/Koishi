# -*- coding: utf-8 -*-
import re
from discord_uwu import player
from discord_uwu.parsers import eventlist
from discord_uwu.others import filter_content
from help_handler import HELP
import asyncio

async def voice(client,message,content):
    guild=message.guild
    if not guild:
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
        elif key=='pause':
            voice_client=client.voice_client_for(message)
            if voice_client:
                voice_client.pause()
                text='Voice paused.'
            else:
                text='There is no voice client at your guild'
            break
        elif key=='stop':
            voice_client=client.voice_client_for(message)
            if voice_client:
                voice_client.stop()
                text='Voice stopped'
            else:
                text='There is no voice client at your guild'
            break
        elif key=='resume':
            voice_client=client.voice_client_for(message)
            if voice_client:
                voice_client.resume()
                text='Voice stopped'
            else:
                text='There is no voice client at your guild'
            break
        elif key=='leave':
            voice_client=client.voice_client_for(message)
            if voice_client:
                await voice_client.disconnect()
                text=f'{client.name} disconnects, bai bai nya!'
            else:
                text='There is no voice client at your guild'
            break
        elif key=='play':
            if not player.youtube_dl:
                text='You need to install youtube_dl 1st!'
                break
            voice_client=client.voice_client_for(message)
            if not voice_client:
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
                source = await player.YTaudio(client.loop,' '.join(content))
            except player.DownloadError as err:
                text=err.args[0]
            else:
                if voice_client.append(source):
                    text=f'Now playing {source.title}!'
                else:
                    text=f'Added to queue {source.title}!'
            break
        elif key=='volume':
            voice_client=client.voice_client_for(message)
            if not voice_client:
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
        elif key=='skip':
            voice_client=client.voice_client_for(message)
            if not voice_client:
                text='There is no voice client at your guild'
                break
            if not voice_client.player:
                text='There is nothing to skip now'
            text=f'Skipping: {voice_client.player.source.title}'
            voice_client.skip()
            break
        elif key=='move':
            if content:
                name=content[0]
                channel=guild.get_channel(name)
                if not channel:
                    text=f'Not existing channel: "{name}"!'
                    break
                if channel.type_lookup!=2:
                    text='Not voice channel.'
                    break
            else:
                state=guild.voice_states.get(message.author.id,None)
                if not state:
                    text='You must be in vocie channel, or you must add a voice channel name to join to'
                    break
                channel=state.channel
            
            voice_client=client.voice_client_for(message)
            if voice_client:
                #client.join_voice_channel works too, if u wanna move, but this is an option too
                await voice_client.move_to(message.channel)
            else:
                voice_client = await client.join_voice_channel(channel)
            text=f'Joined channel: {channel.name}.'
            break
        break
    if text:
        message = await client.message_create(message.channel,text)
        await asyncio.sleep(30.)
        await client.message_delete(message,reason='Voice messages expire after 30s.')
    else:
        await client.message_create(message.channel,HELP['voice'])

