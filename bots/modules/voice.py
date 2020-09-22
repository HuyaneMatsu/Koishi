# -*- coding: utf-8 -*-
import re, os

from hata import alchemy_incendiary, sleep, Task, Embed, eventlist, Color, YTAudio, DownloadError, LocalAudio, \
    Permission, KOKORO, ChannelBase, ChannelVoice, AsyncIO
from hata.ext.commands import Command, checks, Pagination

from config import AUDIO_PATH, AUDIO_PLAY_POSSIBLE

from shared import DUNGEON
from flan import FLAN_HELP_COLOR, CHESUTO_FOLDER, get_bgm, FLAN_HELP_COLOR

KOISHI_VOICE_COLOR = Color.from_rgb(235, 52, 207)

VOICE_COLORS = {
    Flan : FLAN_HELP_COLOR,
    Koishi : KOISHI_VOICE_COLOR
        }
    
VOICE_COMMANDS_KOISHI = eventlist(category='VOICE', checks=[checks.guild_only()])
VOICE_COMMANDS_FLAN = eventlist(checks=[checks.guild_only()])

def setup(lib):
    Flan.commands.extend(VOICE_COMMANDS_FLAN)
    Koishi.commands.extend(VOICE_COMMANDS_KOISHI)

def teardown(lib):
    Flan.commands.unextend(VOICE_COMMANDS_FLAN)
    Koishi.commands.unextend(VOICE_COMMANDS_KOISHI)


if AUDIO_PATH is not None:
    FILENAMES = []
    def collect_local_audio():
        for filename in os.listdir(AUDIO_PATH):
            if filename.endswith('.mp3'):
                FILENAMES.append(filename)

    collect_local_audio()

PERCENT_RP = re.compile('(\d*)[%]?')


async def join_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('join', (
        'Joins me to your voice channel.\n'
        f'Usage: `{prefix}join *n%*`\n'
        'You can also tell me how loud I should sing for you.'
        ), color=VOICE_COLORS.get(client))
    
@VOICE_COMMANDS_FLAN(description=join_description)
@VOICE_COMMANDS_KOISHI(description=join_description)
async def join(client, message, content):
    channel = message.channel
    guild = channel.guild
    while True:
        state=guild.voice_states.get(message.author.id, None)
        if state is None:
            text='You are not at a voice channel!'
            break
        
        channel = state.channel
        if not channel.cached_permissions_for(client).can_connect:
            text = 'I have no permissions to connect to that channel'
            break
        
        try:
            voice_client = await client.join_voice_channel(channel)
        except TimeoutError:
            text = 'Timed out meanwhile tried to connect.'
            break
        except RuntimeError:
            text = 'The client cannot play voice, some libraries are not loaded'
            break
        
        text = f'Joined to {state.channel.name}'
        if content:
            amount = PERCENT_RP.fullmatch(content)
            if amount:
                amount = int(amount.groups()[0])
                if amount < 0:
                    amount = 0
                elif amount > 200:
                    amount = 200
                voice_client.volume = amount/100.
                text = f'{text}; Volume set to {amount}%'
        break
    
    await client.message_create(message.channel,text)


async def pause_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('pause',(
        'Pauses the currently playing audio.\n'
        f'Usage: `{prefix}pause`\n'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=pause_description)
@VOICE_COMMANDS_KOISHI(description=pause_description)
async def pause(client, message):
    voice_client=client.voice_client_for(message)
    if voice_client is None:
        text = 'There is no voice client at your guild.'
    else:
        voice_client.pause()
        text = 'Voice paused.'
    
    await client.message_create(message.channel, text)


async def resume_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('resume',(
        'Resumes the currently playing audio.\n'
        f'Usage: `{prefix}resume`\n'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=resume_description)
@VOICE_COMMANDS_KOISHI(description=resume_description)
async def resume(client, message):
    while True:
        voice_client = client.voice_client_for(message)
        if voice_client is None:
            text = 'There is no voice client at your guild.'
            break
        
        source = voice_client.source
        if source is None:
            text = 'Nothing to resume.'
        else:
            voice_client.resume()
            text = f'{source.title!r} resumed.'
        
        break
    
    await client.message_create(message.channel, text)


async def leave_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('leave', (
        'Leaves me from the voice channel..\n'
        f'Usage: `{prefix}leave`'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=leave_description)
@VOICE_COMMANDS_KOISHI(description=leave_description)
async def leave(client, message):
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        text = 'There is no voice client at your guild.'
    else:
        await voice_client.disconnect()
        text = f'{client.name_at(message.channel.guild)} out.'
    
    await client.message_create(message.channel, text)


if AUDIO_PLAY_POSSIBLE:
    async def koishi_play_description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('play',(
            'Do you want me to search me some audio to listen to?.\n'
            f'Usage: `{prefix}play <name>`\n'
            'If you do not say anything to play, I ll tell, want I am currently playing instead > <.'
            ), color=KOISHI_VOICE_COLOR)
    
    @VOICE_COMMANDS_KOISHI(description=koishi_play_description, name='play', checks=[checks.is_guild(DUNGEON)])
    async def koishi_play(client, message, content):
        while True:
            if YTAudio is None:
                text = 'This option in unavailable :c'
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
                with client.keep_typing(message.channel):
                    source = await YTAudio(content, stream=True)
            except DownloadError as err: #raised by YTdl
                text='Error meanwhile downloading'
                break
            
            if voice_client.append(source):
                text = f'Now playing {source.title}!'
            else:
                text = f'Added to queue {source.title}!'
            break
    
        await client.message_create(message.channel,text)

if (AUDIO_PATH is not None and AUDIO_PLAY_POSSIBLE):
    async def local_description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('local',(
            'Plays a local audio from my collection.\n'
            f'Usage: `{prefix}local <name>`\n'
            'If you do not say anything to play, I ll tell, want I am currently playing instead > <.'
            ), color=KOISHI_VOICE_COLOR)
    
    @VOICE_COMMANDS_KOISHI(name='local', description=local_description, checks=[checks.is_guild(DUNGEON)])
    async def local_(client, message, content):
        while True:
            voice_client=client.voice_client_for(message)
            
            if voice_client is None:
                text = 'There is no voice client at your guild'
                break
            
            if not content:
                if voice_client.player is None:
                    text = 'Nothing is playing now Good Sir!'
                    break
                
                if voice_client.is_paused():
                    voice_client.resume()
                    text = f'Resumed playing: {voice_client.player.source.title}'
                    break
                
                text = f'Now playing: {voice_client.player.source.title}'
                break
            
            content = content.split(' ')
            for index in range(len(content)):
                word = content[index]
                word = re.escape(word)
                content[index] = word
    
            pattern = re.compile('.*?'.join(content),re.I)
            
            most_accurate = None
            
            index = 0
            limit = len(FILENAMES)
            
            while True:
                if index == limit:
                    break
                
                name = FILENAMES[index]
                parsed = pattern.search(name)
                
                if parsed is None:
                    index +=1
                    continue
                
                start = parsed.start()
                length = parsed.end()-start
                most_accurate = (start, length, len(name), name)
                break
            
            if most_accurate is None:
                text = 'Not found anything, what matches.'
                break
            
            while True:
                index +=1
                if index==limit:
                    break
                
                name = FILENAMES[index]
                parsed = pattern.search(name)
                
                if parsed is None:
                    continue
    
                start = parsed.start()
                target = most_accurate[0]
                if start > target:
                    continue
                
                if start < target:
                    most_accurate = (start, parsed.end()-start, len(name), name)
                    continue
                
                length = parsed.end()-start
                target = most_accurate[1]
                
                if length > target:
                    continue
                
                if length < target:
                    most_accurate = (start, length, len(name), name)
                    continue
                
                name_length = len(name)
                target = most_accurate[2]
                if name_length > target:
                    continue
                
                if name_length < target:
                    most_accurate = (start, length, name_length, name)
                    continue
                
                target = most_accurate[3]
                if name > target:
                    continue
                
                most_accurate = (start, length, name_length, name)
                continue
            
            name = most_accurate[3]
            path = os.path.join(AUDIO_PATH, name)
            
            try:
                source = await LocalAudio(path)
            except PermissionError:
                text = 'The file is already playing somewhere'
                break
            
            if voice_client.append(source):
                text = f'Now playing {source.title}!'
            else:
                text = f'Added to queue {source.title}!'
            break
        
        await client.message_create(message.channel, text)


async def volume_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('volume',(
        'Sets my volume to the given percentage.\n'
        f'Usage: `{prefix}volume *n%*`\n'
        'If no volume is passed, then I will tell my current volume.'
        ), color=VOICE_COLORS.get(client))
    
@VOICE_COMMANDS_FLAN(description=volume_description)
@VOICE_COMMANDS_KOISHI(description=volume_description)
async def volume(client, message, content):
    while True:
        voice_client = client.voice_client_for(message)
        if voice_client is None:
            text = 'There is no voice client at your guild.'
            break
        
        if not content:
            text = f'{voice_client.volume*100.:.0f}%'
            break
        
        amount = PERCENT_RP.fullmatch(content)
        if not amount:
            text = 'Number please'
            break
        
        amount = int(amount.groups()[0])
        if amount < 0:
            amount = 0
        elif amount > 200:
            amount = 200
        
        voice_client.volume=amount/100.
        text = f'Volume set to {amount}%.'
        break
    
    await client.message_create(message.channel, text)


async def skip_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('skip',(
        'Skips the audio at the given index.\n'
        f'Usage: `{prefix}skip *index*`\n'
        'If not giving any index or giving it as `0`, will skip the currently playing audio.'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=skip_description)
@VOICE_COMMANDS_KOISHI(description=skip_description)
async def skip(client, message, index:int=0):
    while True:
        voice_client = client.voice_client_for(message)
        if voice_client is None:
            text = 'There is no voice client at your guild.'
            break
        
        source = voice_client.skip(index)
        if source is None:
            text = 'Nothing was skipped.'
        else:
            text = f'Skipped {source.title!r}.'
        break
    
    await client.message_create(message.channel, text)


async def stop_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('stop',(
        'Well, if you really want I can stop playing audio.\n'
        f'Usage: `{prefix}stop`'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=stop_description)
@VOICE_COMMANDS_KOISHI(description=stop_description)
async def stop(client, message):
    while True:
        voice_client=client.voice_client_for(message)
        if voice_client is None:
            text = 'There is no voice client at your guild'
            break
        
        if voice_client.player is None:
            text = 'I don\'t play anything, so I can not stop it.'
            break
        
        text = 'Stopped playing'
        voice_client.stop()
        break
    
    await client.message_create(message.channel, text)


async def move_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('move',(
        'Should I move to an other channel, or next to You, my Love??\n'
        f'Usage: `{prefix}move <channel>`'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=move_description)
@VOICE_COMMANDS_KOISHI(description=move_description)
async def move(client, message, channel:ChannelVoice = None):
    while True:
        if channel is None:
            guild = message.guild
            if guild is None:
                return
            
            state = guild.voice_states.get(message.author.id, None)
            if state is None:
                text = 'You must be in vocie channel, or you should pass a voice channel.'
                break
            
            channel = state.channel
        
        if not channel.cached_permissions_for(client).can_connect:
            text = 'I have no permissions to connect to that channel.'
            break
        
        voice_client = client.voice_client_for(message)
        if voice_client is None:
            await client.join_voice_channel(channel)
        else:
            #client.join_voice_channel works too, if u wanna move, but this is an option as well
            await voice_client.move_to(channel)
        
        text = f'Joined channel: {channel.name}.'
        break
    
    await client.message_create(message.channel, text)
    

async def party_is_over_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('party-is-over',(
        'Should I mark the talking party as done?\n'
        f'Usage: `{prefix}party-is-over`'
        ), color=KOISHI_VOICE_COLOR).add_footer(
            'Administartor only!')

@VOICE_COMMANDS_KOISHI(description=party_is_over_description, checks=[
    checks.has_guild_permissions(Permission().update_by_keys(administrator=True)),
    checks.client_has_guild_permissions(Permission().update_by_keys(move_users=True))
        ], aliases=['partyisover'])
async def party_is_over(client, message):
    guild = message.guild
    if guild is None:
        return
    
    while True:
        voice_client=client.voice_client_for(message)
        if voice_client is None:
            text = 'I don\'t see any parties arround me.'
            break

        Task(voice_client.disconnect(), KOKORO)
        
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
        
        for user in users:
            Task(client.user_voice_kick(user,guild), KOKORO)
        return
    
    await client.message_create(message.channel,text)
    

async def queue_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('queue',(
        'Shows the audio player queue of the current guild.\n'
        f'Usage: `{prefix}queue`'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=queue_description)
@VOICE_COMMANDS_KOISHI(description=queue_description)
async def queue(client, message):
    guild = message.guild
    if guild is None:
        return
    
    voice_client = client.voice_client_for(message)
    color =VOICE_COLORS.get(client)
    
    title = f'Playing queue for {guild}'
    page = Embed(title, color=color)
    pages = [page]
    while True:
        if voice_client is None:
            page.description = '*none*'
            break
        
        source = voice_client.source
        if (source is not None):
            page.add_field('Actual:', source.title)
        
        queue = voice_client.queue
        limit = len(queue)
        if limit:
            index = 0
            while True:
                source = queue[index]
                index +=1
                page.add_field(f'Track {index}.:', source.title)
                
                if index == limit:
                    break
                
                if index%10 == 0:
                    page = Embed(title, color=color)
                    pages.append(page)
            
        else:
            if source is None:
                page.description = '*none*'
        
        break
    
    await Pagination(client, message.channel, pages)

async def loop_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('loop', (
        'Loops over the currently playing audio.\n'
        f'Usage: `{prefix}loop`\n'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=loop_description)
@VOICE_COMMANDS_KOISHI(description=loop_description)
async def loop(client, message):
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        text = 'There is no voice client at your guild.'
    else:
        voice_client.call_after = voice_client._loop_actual
        text = 'Started looping over the actual audio.'
    
    await client.message_create(message.channel, text)



async def loop_stop_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('loop-stop',(
        'Stops looping over the actual audio or over the queue.\n'
        f'Usage: `{prefix}loop-stop`\n'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=loop_stop_description)
@VOICE_COMMANDS_KOISHI(description=loop_stop_description)
async def loop_stop(client, message):
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        text = 'There is no voice client at your guild.'
    else:
        voice_client.call_after = voice_client._play_next
        text = 'Stopped looping over the actual audio(s).'
    
    await client.message_create(message.channel, text)



async def loop_all_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('loop-all', (
        'Starts to loop over the queue.\n'
        f'Usage: `{prefix}loop-all`\n'
        ), color=VOICE_COLORS.get(client))

@VOICE_COMMANDS_FLAN(description=loop_all_description)
@VOICE_COMMANDS_KOISHI(description=loop_all_description)
async def loop_all(client, message):
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        text = 'There is no voice client at your guild.'
    else:
        voice_client.call_after = voice_client._loop_queue
        text = 'Started looping over the audio queue.'
    
    await client.message_create(message.channel, text)

if AUDIO_PLAY_POSSIBLE:
    async def flan_play_description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        return Embed('play', (
            'Plays the given chesuto bgm.\n'
            f'Usage: `{prefix}play <name>`\n'
            '\n'
            'Note that the given name can be also given as the position of the track.'
            ), color=FLAN_HELP_COLOR)
    
    @VOICE_COMMANDS_FLAN(description=flan_play_description, name='play')
    async def flan_play(client, message, content):
        if not content:
            await flan_play_description(client, message)
            return
        
        # GOTO
        while True:
            voice_client = client.voice_client_for(message)
            
            if voice_client is None:
                text = 'There is no voice client at your guild.'
                break
            
            bgm = get_bgm(content)
            
            if bgm is None:
                text = 'Nothing found.'
                break
            
            path = os.path.join(os.path.abspath('.'), CHESUTO_FOLDER, bgm.source_name)
            if not os.path.exists(path):
                data = await client.download_url(bgm.url)
                with await AsyncIO(path, 'wb') as file:
                    await file.write(data)
            
            source = await LocalAudio(path, title=bgm.display_name)
            
            if voice_client.append(source):
                text = 'Now playing'
            else:
                text = 'Added to queue'
            
            text = f'{text} {bgm.display_name!r}!'
            break
        
        await client.message_create(message.channel, text)




