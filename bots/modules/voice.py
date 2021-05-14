# -*- coding: utf-8 -*-
import re, os

from hata import Client, Task, Embed, eventlist, Color, YTAudio, DownloadError, LocalAudio, VoiceClient, \
    KOKORO, ChannelVoice, AsyncIO, WaitTillAll, ChannelStage
from hata.ext.command_utils import Pagination

from config import AUDIO_PATH, AUDIO_PLAY_POSSIBLE, MARISA_MODE

from bot_utils.shared import GUILD__NEKO_DUNGEON

if MARISA_MODE:
    from hata.ext.commands_v2 import checks
else:
    from bots.flan import COLOR__FLAN_HELP, CHESUTO_FOLDER, get_bgm, get_random_bgm
    from hata.ext.commands import checks


VOICE_COLORS = {}

SLASH_CLIENT : [type(None), Client]

if MARISA_MODE:
    Marisa: Client
    VOICE_COMMANDS_MARISA = eventlist(category='VOICE', )
    VOICE_COMMAND_CLIENT = Marisa
    
    MAIN_VOICE_COLOR = Color.from_rgb(121, 231, 78)
    VOICE_COLORS[Marisa] = MAIN_VOICE_COLOR
else:
    Flan: Client
    Koishi: Client
    VOICE_COMMANDS_FLAN = eventlist(checks=checks.guild_only())
    VOICE_COMMAND_CLIENT = Flan
    
    MAIN_VOICE_COLOR = Color.from_rgb(235, 52, 207)
    VOICE_COLORS[Flan] = COLOR__FLAN_HELP
    VOICE_COLORS[Koishi] = MAIN_VOICE_COLOR


if AUDIO_PATH is not None:
    FILE_NAMES = []
    def collect_local_audio():
        for filename in os.listdir(AUDIO_PATH):
            if filename.endswith('.mp3'):
                FILE_NAMES.append(filename)
    
    collect_local_audio()



async def join(client, user, guild, volume):
    state = guild.voice_states.get(user.id, None)
    if state is None:
        yield 'You are not at a voice channel!'
        return
    
    channel = state.channel
    if not channel.cached_permissions_for(client).can_connect:
        yield 'I have no permissions to connect to that channel'
        return
    
    yield
    try:
        voice_client = await client.join_voice(channel)
    except TimeoutError:
        yield 'Timed out meanwhile tried to connect.'
        return
    except RuntimeError:
        yield 'The client cannot play voice, some libraries are not loaded.'
        return
    
    content = f'Joined to {state.channel.name}'
    if (volume is not None):
        if volume < 0:
            volume = 0
        elif volume > 200:
            volume = 200
        voice_client.volume = volume/100.
        content = f'{content}; Volume set to {volume}%'
    
    yield content
    return


async def join_speakers(client, event_or_message):
    voice_client = client.voice_client_for(event_or_message)
    if voice_client is None:
        yield 'There is no voice client at your guild.'
        return
    
    if not isinstance(voice_client.channel, ChannelStage):
        yield 'Can perform this action only in stage channel.'
        return
    
    yield
    await voice_client.join_speakers()
    yield 'Joined speakers.'


async def join_audience(client, event_or_message):
    voice_client = client.voice_client_for(event_or_message)
    if voice_client is None:
        yield 'There is no voice client at your guild.'
        return
    
    if not isinstance(voice_client.channel, ChannelStage):
        yield 'Can perform this action only in stage channel.'
        return
    
    yield
    await voice_client.join_audience()
    yield 'Joined audience.'


async def pause(client, event_or_message):
    voice_client = client.voice_client_for(event_or_message)
    if voice_client is None:
        content = 'There is no voice client at your guild.'
    else:
        voice_client.pause()
        content = 'Voice paused.'
    
    return content


async def resume(client, event_or_message):
    voice_client = client.voice_client_for(event_or_message)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    source = voice_client.source
    if source is None:
        content = 'Nothing to resume.'
    else:
        voice_client.resume()
        content = f'{source.title!r} resumed.'
    
    return content


async def leave(client, message_or_event):
    voice_client = client.voice_client_for(message_or_event)
    if voice_client is None:
        yield 'There is no voice client at your guild.'
        return
    
    yield
    await voice_client.disconnect()
    yield f'{client.name_at(message_or_event.guild)} out.'
    return


if AUDIO_PLAY_POSSIBLE:
    async def yt_play(client, message_or_event, name):
        if YTAudio is None:
            yield 'This option in unavailable :c'
            return
        
        voice_client = client.voice_client_for(message_or_event)
        
        if voice_client is None:
            yield 'There is no voice client at your guild'
            return
        
        if not name:
            if voice_client.player is None:
                yield 'Nothing is playing now Good Sir!'
                return
            
            if voice_client.is_paused():
                voice_client.resume()
                yield f'Resumed playing: {voice_client.player.source.title}'
                return
            
            yield f'Now playing: {voice_client.player.source.title}'
            return
        
        yield
        try:
            source = await YTAudio(name, stream=True)
        except DownloadError: # Raised by YTdl
            yield 'Error meanwhile downloading'
            return
        
        if voice_client.append(source):
            content = 'Now playing'
        else:
            content = 'Added to queue'
        
        yield f'{content} {source.title}!'
        return


if (AUDIO_PATH is not None) and AUDIO_PLAY_POSSIBLE:
    async def local_play(client, message_or_event, content):
        voice_client = client.voice_client_for(message_or_event)
        if voice_client is None:
            yield 'There is no voice client at your guild'
            return
        
        if not content:
            if voice_client.player is None:
                yield 'Nothing is playing now Good Sir!'
                return
            
            if voice_client.is_paused():
                voice_client.resume()
                yield f'Resumed playing: {voice_client.player.source.title}'
                return
            
            yield f'Now playing: {voice_client.player.source.title}'
            return
        
        content = content.split(' ')
        for index in range(len(content)):
            word = content[index]
            word = re.escape(word)
            content[index] = word

        pattern = re.compile('.*?'.join(content),re.I)
        
        most_accurate = None
        
        index = 0
        limit = len(FILE_NAMES)
        
        while True:
            if index == limit:
                break
            
            name = FILE_NAMES[index]
            parsed = pattern.search(name)
            
            if parsed is None:
                index += 1
                continue
            
            start = parsed.start()
            length = parsed.end()-start
            most_accurate = (start, length, len(name), name)
            break
        
        if most_accurate is None:
            yield 'Not found anything matching.'
            return
        
        while True:
            index +=1
            if index==limit:
                break
            
            name = FILE_NAMES[index]
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
        
        yield
        
        try:
            source = await LocalAudio(path)
        except PermissionError:
            yield 'Internal permission error occurred, what a derpy cats working here.'
            return
        
        if voice_client.append(source):
            yield f'Now playing {source.title}!'
            return
        
        yield f'Added to queue {source.title}!'
        return


async def volume_(client, event_or_message, volume):
    voice_client = client.voice_client_for(event_or_message)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    if volume is None:
        return f'{voice_client.volume*100.:.0f}%'
    
    if volume < 0:
        volume = 0
    elif volume > 200:
        volume = 200
    
    voice_client.volume = volume/100.
    return f'Volume set to {volume}%.'


async def skip(client, message, index):
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    source = voice_client.skip(index)
    if source is None:
        return 'Nothing was skipped.'
    else:
        return f'Skipped {source.title!r}.'


async def stop(client, message_or_event):
    voice_client = client.voice_client_for(message_or_event)
    if voice_client is None:
        return 'There is no voice client at your guild'
    
    voice_client.stop()
    return 'Stopped playing'


async def move(client, message_or_event, user, voice_channel):
    if voice_channel is None:
        
        state = GUILD__NEKO_DUNGEON.voice_states.get(user.id, None)
        if state is None:
            yield 'You must be in voice channel, or you should pass a voice channel.'
            return
        
        voice_channel = state.channel
    
    if not voice_channel.cached_permissions_for(client).can_connect:
        yield 'I have no permissions to connect to that channel.'
        return
    
    voice_client = client.voice_client_for(message_or_event)
    
    yield
    if voice_client is None:
        await client.join_voice(voice_channel)
    else:
        # `client.join_voice` works too, if u wanna move, but this is an option as well
        await voice_client.move_to(voice_channel)
    
    yield f'Joined to channel: {voice_channel.name}.'


async def party_is_over(client, message_or_event):
    voice_client = client.voice_client_for(message_or_event)
    if voice_client is None:
        yield 'I don\'t see any parties around me.'
        return
    
    channel = voice_client.channel
    if not channel.cached_permissions_for(client).can_move_users:
        yield 'I must have move users permission in the respective channel to invoke this command.'
        return
    
    yield
    tasks = []
    task = Task(voice_client.disconnect(), KOKORO)
    tasks.append(task)
    
    users = []
    for state in GUILD__NEKO_DUNGEON.voice_states.values():
        if (state.channel is not channel):
            continue
            
        user = state.user
        if (user is client):
            continue
        
        users.append(user)
    
    for user in users:
        task = Task(client.user_voice_kick(user, GUILD__NEKO_DUNGEON), KOKORO)
        tasks.append(task)
    
    await WaitTillAll(tasks, KOKORO)
    
    yield 'Nooo, the party is over nyaaa~~h!'
    return


async def queue(client, message_or_event, channel, guild):
    yield
    
    voice_client = client.voice_client_for(message_or_event)
    color = VOICE_COLORS.get(client, None)
    
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
                index += 1
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
    
    await Pagination(client, message_or_event, pages)


VOICE_LOOPER_BEHAVIOUR_TO_FUNCTIONS_AND_JOIN_DESCRIPTIONS = {
    'queue'  : (VoiceClient._loop_queue  , 'Started looping over the whole queue.'  ) ,
    'actual' : (VoiceClient._loop_actual , 'Started looping over the actual audio.' ),
    'stop'   : (VoiceClient._play_next   , 'Stopped looping.'                       ),
        }

VOICE_LOOPER_FUNCTIONS_TO_DESCRIPTIONS = {
    VoiceClient._loop_queue  : 'Looping over the whole queue.'  ,
    VoiceClient._loop_actual : 'Looping over the actual audio.' ,
    VoiceClient._play_next   : 'Not looping.'                   ,
        }

VOICE_LOOPER_BEHAVIOURS = (
    'queue'  ,
    'actual' ,
    'stop'   ,
        )

VOICE_LOOPER_BEHAVIOURS_PAIRS = [
    ('Loop over the queue'  , 'queue'  ,),
    ('Loop over the actual' , 'actual' ,),
    ('Stop looping'         , 'stop'   ,),
        ]

async def loop(client, message_or_event, behaviour):
    voice_client = client.voice_client_for(message_or_event)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    if behaviour is None:
        description = VOICE_LOOPER_FUNCTIONS_TO_DESCRIPTIONS.get(voice_client.call_after, None)
        if description is None:
            return 'Error 404, Unknown looping behaviour.'
        
        return description
    
    function, description = VOICE_LOOPER_BEHAVIOUR_TO_FUNCTIONS_AND_JOIN_DESCRIPTIONS[behaviour]
    voice_client.call_after = function
    return description


if AUDIO_PLAY_POSSIBLE and (not MARISA_MODE):
    async def chesuto_play(client, voice_client, bgm):
        path = os.path.join(os.path.abspath(''), CHESUTO_FOLDER, bgm.source_name)
        if not os.path.exists(path):
            data = await client.download_url(bgm.url)
            with await AsyncIO(path, 'wb') as file:
                await file.write(data)
        
        source = await LocalAudio(path, title=bgm.display_name)
        
        if voice_client.append(source):
            text = 'Now playing'
        else:
            text = 'Added to queue'
        
        return f'{text} {bgm.display_name!r}!'
    
    async def chesuto_play_by_name(client, message, name):
        voice_client = client.voice_client_for(message)
        
        if voice_client is None:
            yield 'There is no voice client at your guild.'
            return
        
        bgm = get_bgm(name)
        
        if bgm is None:
            yield 'Nothing found.'
            return
        
        yield
        yield await chesuto_play(client, voice_client, bgm)
        return

    
    async def chesuto_play_random(client, message):
        voice_client = client.voice_client_for(message)
        
        if voice_client is None:
            yield 'There is no voice client at your guild.'
            return
        
        bgm = get_random_bgm()
        
        if bgm is None:
            yield 'No bgms added, something is messed up.'
            return
        
        yield
        yield await chesuto_play(client, voice_client, bgm)
        return
    
#### #### #### #### Add as normal commands #### #### #### ####

async def command_join_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('join', (
        'Joins me to your voice channel.\n'
        f'Usage: `{prefix}join *n*`\n'
        'You can also tell me how loud I should sing for you.'
        ), color=VOICE_COLORS.get(client, None))


@VOICE_COMMAND_CLIENT.commands(name='join', description=command_join_description, category='VOICE')
async def command_join(client, message, volume:int=None):
    async for content in join(client, message.author, message.guild, volume):
        if (content is not None):
            yield content


async def command_pause_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('pause',(
        'Pauses the currently playing audio.\n'
        f'Usage: `{prefix}pause`\n'
        ), color=VOICE_COLORS.get(client, None))


@VOICE_COMMAND_CLIENT.commands(name='pause', description=command_pause_description, category='VOICE')
async def command_resume(client, message):
    return await pause(client, message)


async def command_resume_description(client, event_or_message):
    prefix = client.command_processor.get_prefix_for(event_or_message)
    return Embed('resume', (
        'Resumes the currently playing audio.\n'
        f'Usage: `{prefix}resume`\n'
        ), color=VOICE_COLORS.get(client, None))

@VOICE_COMMAND_CLIENT.commands(name='resume', description=command_resume_description, category='VOICE')
async def command_resume(client, message):
    return await resume(client, message)


async def command_leave_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('leave', (
        'Leaves me from the voice channel.\n'
        f'Usage: `{prefix}leave`'
        ), color=VOICE_COLORS.get(client, None))

@VOICE_COMMAND_CLIENT.commands(name='leave', description=command_leave_description, category='VOICE')
async def command_leave(client, message):
    async for content in leave(client, message):
        if (content is not None):
            yield content

if AUDIO_PLAY_POSSIBLE and MARISA_MODE:
    async def command_yt_play_description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('play', (
            'Do you want me to search me some audio to listen to?.\n'
            f'Usage: `{prefix}play <name>`\n'
            'If you do not say anything to play, I ll tell, want I am currently playing instead > <.'
            ), color=MAIN_VOICE_COLOR)
    
    @VOICE_COMMAND_CLIENT.commands(
        name = 'play',
        description = command_yt_play_description,
        checks = checks.is_guild(GUILD__NEKO_DUNGEON),
        category = 'VOICE',
            )
    async def command_yt_play(client, message, name):
        async for content in yt_play(client, message, name):
            if (content is not None):
                yield content


async def command_move_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('move', (
        'Should I move to an other channel, or next to You, my Love??\n'
        f'Usage: `{prefix}move <channel>`'
        ), color=VOICE_COLORS.get(client, None))

@VOICE_COMMAND_CLIENT.commands(name='move', description=command_move_description, category='VOICE')
async def command_move(client, message, voice_channel: ChannelVoice=None):
    async for content in move(client, message, message.author, voice_channel):
        if (content is not None):
            yield content


async def party_is_over_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('party-is-over', (
        'Should I mark the talking party as done?\n'
        f'Usage: `{prefix}party-is-over`'
        ), color=MAIN_VOICE_COLOR).add_footer(
            'Administrator only!')

@VOICE_COMMAND_CLIENT.commands(
    name = 'party-is-over',
    description = party_is_over_description,
    checks = checks.owner_or_has_guild_permissions(administrator=True),
    aliases = 'partyisover',
    category = 'VOICE',
        )
async def command_party_is_over(client, message):
    async for content in party_is_over(client, message):
        if (content is not None):
            yield content

if (AUDIO_PATH is not None) and AUDIO_PLAY_POSSIBLE:
    async def command_local_description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('local',(
            'Plays a local audio from my collection.\n'
            f'Usage: `{prefix}local <name>`\n'
            'If you do not say anything to play, I ll tell, want I am currently playing instead > <.'
            ), color=MAIN_VOICE_COLOR)
    
    @VOICE_COMMAND_CLIENT.commands(
        name = 'local',
        description = command_local_description,
        checks = checks.is_guild(GUILD__NEKO_DUNGEON),
        category = 'VOICE',
            )
    async def command_local(client, message, name):
        async for content in local_play(client, message, name):
            if (content is not None):
                yield content

if AUDIO_PLAY_POSSIBLE and (not MARISA_MODE):
    async def command_chesuto_chesuto_play_by_name_description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('play', (
            'Plays the given chesuto bgm.\n'
            f'Usage: `{prefix}play <name>`\n'
            '\n'
            'Note that the given name can be also given as the position of the track.'
                ), color=COLOR__FLAN_HELP)
    
    @Flan.commands(name='play', description=command_chesuto_chesuto_play_by_name_description, category='VOICE')
    async def command_chesuto_play(client, message, name):
        if not name:
            yield await command_chesuto_chesuto_play_by_name_description(client, message)
            return
        
        async for content in chesuto_play_by_name(client, message, name):
            if (content is not None):
                yield content
    
    async def command_chesuto_play_random_description(client, message):
        prefix = client.command_processor.get_prefix_for(message)
        return Embed('play', (
            'Plays a random chesuto bgm.\n'
            f'Usage: `{prefix}random`\n'
                ), color=COLOR__FLAN_HELP)
    
    @Flan.commands(name='random', description=command_chesuto_play_random_description, category='VOICE')
    async def command_chesuto_random(client, message):
        async for content in chesuto_play_random(client, message):
            if (content is not None):
                yield content

async def command_loop_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('loop', (
        'Sets the voice client\'s looping behaviour or returns the current one.\n'
        f'Usage: `{prefix}loop <queue|actual|stop>`\n'
        ), color=VOICE_COLORS.get(client, None))

@VOICE_COMMAND_CLIENT.commands(name='loop', description=command_loop_description, category='VOICE')
async def command_loop(client, message, behaviour:'str' = None):
    if (behaviour is not None):
        state = behaviour.lower()
        if state not in VOICE_LOOPER_BEHAVIOURS:
            return f'Behaviour: {behaviour} is not any of the expected ones..'
    
    return await loop(client, message, behaviour)


async def command_queue_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('queue', (
        'Shows the voice client\'s queue of the guild.\n'
        f'Usage: `{prefix}queue`'
        ), color=VOICE_COLORS.get(client, None))


@VOICE_COMMAND_CLIENT.commands(name='queue', description=command_queue_description, category='VOICE')
async def command_queue(client, message):
    channel = message.channel
    guild = message.guild
    if guild is None:
        return
    
    async for content in queue(client, message, channel, guild):
        if (content is not None):
            yield content


async def command_volume_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('volume', (
        'Sets my volume to the given percentage.\n'
        f'Usage: `{prefix}volume *n*`\n'
        'If no volume is passed, then I will tell my current volume.'
        ), color=VOICE_COLORS.get(client, None))

@VOICE_COMMAND_CLIENT.commands(name='volume', description=command_volume_description, category='VOICE')
async def command_volume(client, message, volume:int=None):
    return await volume_(client, message, volume)


async def command_stop_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('stop', (
        'Well, if you really want I can stop playing audio.\n'
        f'Usage: `{prefix}stop`'
        ), color=VOICE_COLORS.get(client, None))


@VOICE_COMMAND_CLIENT.commands(name='stop', description=command_stop_description, category='VOICE')
async def command_stop(client, message):
    return await stop(client, message)

async def command_skip_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('skip', (
        'Skips the audio at the given index.\n'
        f'Usage: `{prefix}skip *index*`\n'
        'If not giving any index or giving it as `0`, will skip the currently playing audio.'
        ), color=VOICE_COLORS.get(client, None))

@VOICE_COMMAND_CLIENT.commands(name='skip', description=command_skip_description, category='VOICE')
async def command_skip(client, message, index:int=0):
    return await skip(client, message, index)

#### #### #### #### Add as slash commands #### #### #### ####

if SLASH_CLIENT is not None:
    @SLASH_CLIENT.interactions(name='join', guild=GUILD__NEKO_DUNGEON)
    async def slash_join(client, event,
            volume : ('int', 'Any preset volume?')=None,
                ):
        """Joins the voice channel."""
        return join(client, event.user, event.guild, volume)
    
    @SLASH_CLIENT.interactions(name='pause', guild=GUILD__NEKO_DUNGEON)
    async def slash_pause(client, event):
        """Pauses the currently playing audio."""
        return await pause(client, event)
    
    @SLASH_CLIENT.interactions(name='resume', guild=GUILD__NEKO_DUNGEON)
    async def slash_resume(client, event):
        """Resumes the currently playing audio."""
        return await resume(client, event)
    
    @SLASH_CLIENT.interactions(name='leave', guild=GUILD__NEKO_DUNGEON)
    async def slash_leave(client, message):
        """Leaves me from the voice channel."""
        return leave(client, message)
    
    
    if AUDIO_PLAY_POSSIBLE:
        @SLASH_CLIENT.interactions(name='play', guild=GUILD__NEKO_DUNGEON)
        async def slash_yt_play(client, message,
                name:('str', 'The name of the audio to play.') = '',
                    ):
            """Plays the chosen audio or shows what is playing right now."""
            return yt_play(client, message, name)
    
    @SLASH_CLIENT.interactions(name='move', guild=GUILD__NEKO_DUNGEON)
    async def slash_move(client, message,
            voice_channel: ('channel', 'To which channel should I move to?') = None
                ):
        """Moves to the selected channel or next to You, my Love?"""
        if (voice_channel is not None) and (not isinstance(voice_channel, ChannelVoice)):
            return 'Please select a voice channel.'
        
        return move(client, message, message.author, voice_channel)
    
    @SLASH_CLIENT.interactions(name='party-is-over', guild=GUILD__NEKO_DUNGEON)
    async def slash_party_is_over(client, event):
        """I mark the talking party as done?"""
        if not event.user_permissions.can_administrator:
            return 'You must have administrator permission to invoke this command.'
        
        return party_is_over(client, event)
    
    if (AUDIO_PATH is not None) and AUDIO_PLAY_POSSIBLE:
        @SLASH_CLIENT.interactions(name='local', guild=GUILD__NEKO_DUNGEON)
        async def slash_local(client, event,
                name : ('str', 'The audio\'s name') = '',
                    ):
            """Plays a local audio file from my own collection UwU."""
            return local_play(client, event, name)
    
    @SLASH_CLIENT.interactions(name='loop', guild=GUILD__NEKO_DUNGEON)
    async def slash_loop(client, event,
            behaviour : (VOICE_LOOPER_BEHAVIOURS_PAIRS, 'Set looping as?') = None,
                ):
        """Sets the voice client's looping behaviour or returns the current one."""
        return await loop(client, event, behaviour)
    
    @SLASH_CLIENT.interactions(name='queue', guild=GUILD__NEKO_DUNGEON)
    async def slash_queue(client, event):
        """Shows the voice client\'s queue of the guild."""
        return queue(client, event, event.channel, GUILD__NEKO_DUNGEON)
    
    @SLASH_CLIENT.interactions(name='volume', guild=GUILD__NEKO_DUNGEON)
    async def slash_volume(client, event,
            volume: ('number', 'Percentage?') = None,
                ):
        """Sets my volume to the given percentage."""
        return await volume_(client, event, volume)
    
    @SLASH_CLIENT.interactions(name='stop', guild=GUILD__NEKO_DUNGEON)
    async def slash_stop(client, event):
        """Nyahh, if you really want I can stop playing audio."""
        return await stop(client, event)
    
    @SLASH_CLIENT.interactions(name='skip', guild=GUILD__NEKO_DUNGEON)
    async def slash_skip(client, event,
            index: ('int', 'Which audio to skip?') = 0,
                ):
        """I skip the audio at the given index."""
        return await skip(client, event, index)
    
    @SLASH_CLIENT.interactions(name='join-speakers', guild=GUILD__NEKO_DUNGEON)
    async def slash_join_speakers(client, event):
        """Joins the speakers in a stage channel."""
        return join_speakers(client, event)
    
    @SLASH_CLIENT.interactions(name='join-audience', guild=GUILD__NEKO_DUNGEON)
    async def slash_join_audience(client, event):
        """Joins the audience in a stage channel."""
        return join_audience(client, event)
