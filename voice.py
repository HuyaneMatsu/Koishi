# -*- coding: utf-8 -*-
import re
from discord_uwu import player
from discord_uwu.parsers import eventlist

voice=eventlist()

@voice
async def join(client,message,content):
        user=message.author
        guild=message.guild
        if not guild:
            return
        state=guild.voice_states.get(user.id,None)
        if not state:
            return
        await client.join_voice_channel(state.channel)
        
        result=re.match(r'^([0-9]{1,3})[%]{0,1}$',content)

        if result:
            result=int(result.groups()[0])
            if 0<result<101:
                voice_client=client.voice_client_for(message)
                voice_client.volume=result/100.
                await client.message_create(message.channel,f'Volume set to {result}%')

@voice
async def pause(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client:
        voice_client.pause()

@voice
async def stop(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client:
        voice_client.stop()

@voice
async def resume(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client:
        voice_client.resume()
        
        
@voice
async def leave(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client:
        await voice_client.disconnect()

##@voice
##async def play(client,message,content):
##    voice_client=client.voice_client_for(message)
##    if voice_client:
##        source=player.PCM_volume_transformer(player.FFmpegPCMaudio('songname.mp3'))
##        voice_client.play(source,after=lambda : None)


if player.youtube_dl:
    @voice
    async def play(client,message,content):

        voice_client=client.voice_client_for(message)
        if voice_client:
            if not content:
                voice_client.resume()
            try:
                source = await player.YTaudio(client.loop,content)
            except player.DownloadError:
                text=DownloadError.args[0]
            else:
                if voice_client.append(source):
                    text='Now playing {source.title}!'
                else:
                    starter='Added to queue {source.title}!'
            await client.message_create(message.channel,f'{starter} {source.title}!')

@voice
async def volume(client,message,content):
    voice_client=client.voice_client_for(message)
    if not voice_client:
        return

    if not content:
        await client.message_create(message.channel,f'{round(voice_client.volume*100.)}% desu')
        return

    result=re.match(r'^([0-9]{1,3})[%]{0,1}$',content)
    if not result:
        await client.message_create(message.channel,'*Number*% pls')
        return
    result=int(result.groups()[0])
    if result>100 or result==0:
        await client.message_create(message.channel,'huh?')
        return
    voice_client.volume=result/100.
    await client.message_create(message.channel,f'Volume set to {result}%')


@voice
async def skip(client,message,content):
    voice_client=client.voice_client_for(message)
    if not voice_client:
        return
    voice_client.skip()
    await client.message_create(message.channel,'skipped')

@voice
async def move(client,message,content):
    voice_client=client.voice_client_for(message)
    if voice_client:
        await voice_client.move_to(message.channel)
    
