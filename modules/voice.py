__all__ = ()

import re, os

from scarletio import Task, AsyncIO, TaskGroup
from hata import Client, Embed, eventlist, Color, YTAudio, DownloadError, LocalAudio, VoiceClient, \
    KOKORO, is_url, InteractionEvent
from hata.ext.slash.menus import Pagination

from config import AUDIO_PATH, AUDIO_PLAY_POSSIBLE, MARISA_MODE

from bot_utils.constants import GUILD__SUPPORT
from hata.ext.commands_v2 import checks

if not MARISA_MODE:
    from bots.flan import COLOR__FLAN_HELP, CHESUTO_FOLDER, get_bgm, get_random_bgm

SOLARLINK_VOICE: bool

VOICE_COLORS = {}

SLASH_CLIENT : [type(None), Client]

if MARISA_MODE:
    from bots import Marisa
    VOICE_COMMANDS_MARISA = eventlist(category='VOICE', )
    VOICE_COMMAND_CLIENT = Marisa
    
    MAIN_VOICE_COLOR = Color.from_rgb(121, 231, 78)
    VOICE_COLORS[Marisa] = MAIN_VOICE_COLOR
else:
    from bots import Flan, Koishi
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

if SOLARLINK_VOICE:
    async def do_join_voice(client, channel):
        return await client.solarlink.join_voice(channel)
else:
    async def do_join_voice(client, channel):
        return await client.join_voice(channel)

if SOLARLINK_VOICE:
    async def do_set_volume(player, volume):
        await player.set_volume(volume)
else:
    async def do_set_volume(voice_client, volume):
        voice_client.volume = volume

if SOLARLINK_VOICE:
    async def do_get_volume(player):
        return player.get_volume()
else:
    async def do_get_volume(voice_client):
        return voice_client.volume


if SOLARLINK_VOICE:
    async def do_pause(player):
        await player.pause()
else:
    async def do_pause(voice_client):
        voice_client.pause()

if SOLARLINK_VOICE:
    def get_voice_client(client, event_or_message):
        return client.solarlink.get_player(event_or_message.guild_id)
else:
    def get_voice_client(client, event_or_message):
        return client.voice_clients.get(event_or_message.guild_id, None)

if SOLARLINK_VOICE:
    async def do_resume(player):
        await player.resume()
else:
    async def do_resume(voice_client):
        await voice_client.resume()

if SOLARLINK_VOICE:
    async def do_disconnect(player):
        await player.resume()
else:
    async def do_disconnect(voice_client):
        await voice_client.resume()

if SOLARLINK_VOICE:
    async def get_from_youtube(client, name):
        if not is_url(name):
            name = f'ytsearch:{name}'
        
        tracks = await client.solarlink.get_tracks(name)
        if tracks:
            track = tracks[0]
        else:
            track = None
        
        return track
else:
    async def get_from_youtube(client, name):
        return await YTAudio(name, stream=True)

if SOLARLINK_VOICE:
    async def do_skip(player, index):
        return await player.skip(index)
else:
    async def do_skip(voice_client, index):
        return voice_client.skip(index)

if SOLARLINK_VOICE:
    async def do_stop(player):
        await player.stop()
else:
    async def do_stop(voice_client):
        voice_client.stop()

if SOLARLINK_VOICE:
    async def do_add_on_queue(player, track):
        return await player.append(track)
else:
    async def do_add_on_queue(voice_client, source):
        return voice_client.append(source)

if SOLARLINK_VOICE:
    async def do_get_current(player):
        return player.get_current()
else:
    async def do_get_current(player):
        return player.source


if SOLARLINK_VOICE:
    async def do_get_looping_behavior(player):
        if player.is_repeating_current():
            description = 'Looping over the actual audio.'
        elif player.is_repeating_queue():
            description = 'Looping over the whole queue.'
        else:
            description = 'Not looping.'
        
        return description
    
    async def do_set_looping_behavior(player, behaviour):
        if behaviour == 'queue':
            player.set_repeat_queue(True)
            description = 'Started looping over the whole queue.'
        elif behaviour == 'actual':
            player.set_repeat_current(False)
            description = 'Started looping over the actual audio.'
        elif behaviour == 'stop':
            player.set_repeat_queue(False)
            player._set_repeat_actual(False)
            description = 'Stopped looping.'
        else:
            description = '*confused screaming*'
        
        return description

else:
    VOICE_LOOPER_FUNCTIONS_TO_DESCRIPTIONS = {
        VoiceClient._loop_queue  : 'Looping over the whole queue.'  ,
        VoiceClient._loop_actual : 'Looping over the actual audio.' ,
        VoiceClient._play_next   : 'Not looping.'                   ,
    }
    
    async def do_get_looping_behavior(voice_client):
        return VOICE_LOOPER_FUNCTIONS_TO_DESCRIPTIONS.get(
            voice_client.call_after,
            'Error 404, Unknown looping behaviour.'
        )
    
    VOICE_LOOPER_BEHAVIOUR_TO_FUNCTIONS_AND_JOIN_DESCRIPTIONS = {
        'queue'  : (VoiceClient._loop_queue  , 'Started looping over the whole queue.'  ) ,
        'actual' : (VoiceClient._loop_actual , 'Started looping over the actual audio.' ),
        'stop'   : (VoiceClient._play_next   , 'Stopped looping.'                       ),
    }
    
    async def do_set_looping_behavior(voice_client, behaviour):
        function, description = VOICE_LOOPER_BEHAVIOUR_TO_FUNCTIONS_AND_JOIN_DESCRIPTIONS[behaviour]
        voice_client.call_after = function
        return description


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
        voice_client = await do_join_voice(client, channel)
    except TimeoutError:
        yield 'Timed out meanwhile tried to connect.'
        return
    except RuntimeError:
        yield 'The client cannot play voice, some libraries are not loaded.'
        return
    
    content = f'Joined to {state.channel.name}'
    
    if (volume is not None):
        if volume <= 0:
            volume = 0.0
        elif volume >= 200:
            volume = 2.0
        else:
            volume /= 100.0
        
        await do_set_volume(voice_client, volume)
        content = f'{content}; Volume set to {volume * 100.:.0f}%'
    
    yield content
    return


async def join_speakers(client, event_or_message):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        yield 'There is no voice client at your guild.'
        return
    
    if not voice_client.channel.is_guild_stage():
        yield 'Can perform this action only in stage channel.'
        return
    
    yield
    await voice_client.join_speakers()
    yield 'Joined speakers.'


async def join_audience(client, event_or_message):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        yield 'There is no voice client at your guild.'
        return
    
    if not voice_client.channel.is_guild_stage():
        yield 'Can perform this action only in stage channel.'
        return
    
    yield
    await voice_client.join_audience()
    yield 'Joined audience.'


async def pause(client, event_or_message):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        content = 'There is no voice client at your guild.'
    else:
        await do_pause(voice_client)
        content = 'Voice paused.'
    
    return content


async def resume(client, event_or_message):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    source = await do_get_current(voice_client)
    if source is None:
        content = 'Nothing to resume.'
    else:
        await do_resume(voice_client)
        content = f'{source.title!r} resumed.'
    
    return content


async def leave(client, event_or_message):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        yield 'There is no voice client at your guild.'
        return
    
    yield
    await voice_client.disconnect()
    yield f'{client.name_at(event_or_message.guild)} out.'
    return


if AUDIO_PLAY_POSSIBLE:
    async def yt_play(client, event_or_message, name):
        if (not SOLARLINK_VOICE) and (YTAudio is None):
            yield 'This option in unavailable :c'
            return
        
        voice_client = get_voice_client(client, event_or_message)
        
        if voice_client is None:
            yield 'There is no voice client at your guild'
            return
        
        if not name:
            current = await do_get_current(voice_client)
            if (current is None):
                yield 'Nothing is playing now Good Sir!'
                return
            
            if voice_client.is_paused():
                await do_resume(voice_client)
                yield f'Resumed playing: {current.title}'
                return
            
            yield f'Now playing: {current.title}'
            return
        
        yield
        try:
            source = await get_from_youtube(client, name)
        except DownloadError: # Raised by YTdl
            yield 'Error meanwhile downloading'
            return
        
        if source is None:
            yield 'Nothing found.'
            return
        
        if await do_add_on_queue(voice_client, source):
            content = 'Now playing'
        else:
            content = 'Added to queue'
        
        yield f'{content} {source.title}!'
        return


if (AUDIO_PATH is not None) and AUDIO_PLAY_POSSIBLE and (not SOLARLINK_VOICE):
    async def local_play(client, event_or_message, content):
        voice_client = get_voice_client(client, event_or_message)
        if voice_client is None:
            yield 'There is no voice client at your guild'
            return
        
        if not content:
            current = await do_get_current(voice_client)
            if (current is None):
                yield 'Nothing is playing now Good Sir!'
                return
            
            if voice_client.is_paused():
                voice_client.resume()
                yield f'Resumed playing: {current.title}'
                return
            
            yield f'Now playing: {current.title}'
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
            length = parsed.end() - start
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
                most_accurate = (start, parsed.end() - start, len(name), name)
                continue
            
            length = parsed.end() - start
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
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    if volume is None:
        volume = await do_get_volume(voice_client)
        return f'{volume * 100.:.0f}%'
    
    if volume <= 0:
        volume = 0.0
    elif volume >= 200:
        volume = 2.0
    else:
        volume /= 100.0
    
    await do_set_volume(voice_client, volume)
    return f'Volume set to {volume * 100.:.0f}%.'


async def skip(client, event_or_message, index):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    source = await do_skip(voice_client, index)
    if source is None:
        return 'Nothing was skipped.'
    else:
        return f'Skipped {source.title!r}.'


async def stop(client, event_or_message):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        return 'There is no voice client at your guild'
    
    await do_stop(voice_client)
    return 'Stopped playing'


async def move(client, event_or_message, user, voice_channel):
    if voice_channel is None:
        
        state = GUILD__SUPPORT.voice_states.get(user.id, None)
        if state is None:
            yield 'You must be in voice channel, or you should pass a voice channel.'
            return
        
        voice_channel = state.channel
    
    if not voice_channel.cached_permissions_for(client).can_connect:
        yield 'I have no permissions to connect to that channel.'
        return
    
    voice_client = get_voice_client(client, event_or_message)
    
    yield
    if voice_client is None:
        await do_join_voice(client, voice_channel)
    else:
        # `client.join_voice` works too, if u wanna move, but this is an option as well
        await voice_client.move_to(voice_channel)
    
    yield f'Joined to channel: {voice_channel.name}.'


async def party_is_over(client, event_or_message):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        yield 'I don\'t see any parties around me.'
        return
    
    channel = voice_client.channel
    if not channel.cached_permissions_for(client).can_move_users:
        yield 'I must have move users permission in the respective channel to invoke this command.'
        return
    
    yield
    tasks = []
    task = Task(KOKORO, voice_client.disconnect())
    tasks.append(task)
    
    users = []
    for state in GUILD__SUPPORT.voice_states.values():
        if (state.channel is not channel):
            continue
            
        user = state.user
        if (user is client):
            continue
        
        users.append(user)
    
    for user in users:
        task = Task(KOKORO, client.user_voice_kick(user, GUILD__SUPPORT))
        tasks.append(task)
    
    await TaskGroup(KOKORO, tasks).wait_all()
    
    yield 'Nooo, the party is over nyaaa~~h!'
    return


async def queue(client, event_or_message, guild):
    yield
    
    voice_client = get_voice_client(client, event_or_message)
    color = VOICE_COLORS.get(client, None)
    
    title = f'Playing queue for {guild}'
    page = Embed(title, color = color)
    pages = [page]
    while True:
        if voice_client is None:
            page.description = '*none*'
            break
        
        source = await do_get_current(voice_client)
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
                
                if index % 10 == 0:
                    page = Embed(title, color = color)
                    pages.append(page)
            
        else:
            if source is None:
                page.description = '*none*'
        
        break
    
    if isinstance(event_or_message, InteractionEvent):
        target = event_or_message
    else:
        target = event_or_message.channel
    
    await Pagination(client, target, pages)


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

async def loop(client, event_or_message, behaviour):
    voice_client = get_voice_client(client, event_or_message)
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    if behaviour is None:
        return await do_get_looping_behavior(voice_client)
    
    return await do_set_looping_behavior(voice_client, behaviour)


if AUDIO_PLAY_POSSIBLE and (not MARISA_MODE) and (not SOLARLINK_VOICE):
    async def chesuto_play(client, voice_client, bgm):
        path = os.path.join(os.path.abspath(''), CHESUTO_FOLDER, bgm.source_name)
        if not os.path.exists(path):
            async with client.http.get(bgm.url) as response:
                data = await response.read()
            with await AsyncIO(path, 'wb') as file:
                await file.write(data)
        
        source = await LocalAudio(path, title=bgm.display_name)
        
        if voice_client.append(source):
            text = 'Now playing'
        else:
            text = 'Added to queue'
        
        return f'{text} {bgm.display_name!r}!'
    
    async def chesuto_play_by_name(client, event_or_message, name):
        voice_client = get_voice_client(client, event_or_message)
        
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

    
    async def chesuto_play_random(client, event_or_message):
        voice_client = get_voice_client(client, event_or_message)
        
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

async def command_join_description(command_context):
    return Embed(
        'join',
        (
            'Joins me to your voice channel.\n'
            f'Usage: `{command_context.prefix}join *n*`\n'
            'You can also tell me how loud I should sing for you.'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )


@VOICE_COMMAND_CLIENT.commands(name = 'join', description = command_join_description, category='VOICE')
async def command_join(client, message, volume: int = None):
    async for content in join(client, message.author, message.guild, volume):
        if (content is not None):
            yield content


async def command_pause_description(command_context):
    return Embed(
        'pause',
        (
            'Pauses the currently playing audio.\n'
            f'Usage: `{command_context.prefix}pause`\n'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )


@VOICE_COMMAND_CLIENT.commands(name = 'pause', description = command_pause_description, category='VOICE')
async def command_resume(client, message):
    return await pause(client, message)


async def command_resume_description(command_context):
    return Embed(
        'resume',
        (
            'Resumes the currently playing audio.\n'
            f'Usage: `{command_context.prefix}resume`\n'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )

@VOICE_COMMAND_CLIENT.commands(name = 'resume', description = command_resume_description, category='VOICE')
async def command_resume(client, message):
    return await resume(client, message)


async def command_leave_description(command_context):
    return Embed(
        'leave',
        (
            'Leaves me from the voice channel.\n'
            f'Usage: `{command_context.prefix}leave`'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )

@VOICE_COMMAND_CLIENT.commands(name = 'leave', description = command_leave_description, category='VOICE')
async def command_leave(client, message):
    async for content in leave(client, message):
        if (content is not None):
            yield content

if AUDIO_PLAY_POSSIBLE and MARISA_MODE:
    async def command_yt_play_description(command_context):
        return Embed(
            'play',
            (
                'Do you want me to search me some audio to listen to?.\n'
                f'Usage: `{command_context.prefix}play <name>`\n'
                'If you do not say anything to play, I ll tell, want I am currently playing instead > <.'
            ),
            color = MAIN_VOICE_COLOR,
        )
    
    @VOICE_COMMAND_CLIENT.commands(
        name = 'play',
        description = command_yt_play_description,
        checks = checks.is_guild(GUILD__SUPPORT),
        category = 'VOICE',
    )
    async def command_yt_play(client, message, name):
        async for content in yt_play(client, message, name):
            if (content is not None):
                yield content


async def command_move_description(command_context):
    return Embed(
        'move',
        (
            'Should I move to an other channel, or next to You, my Love??\n'
            f'Usage: `{command_context.prefix}move <channel>`'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )

@VOICE_COMMAND_CLIENT.commands(name = 'move', description = command_move_description, category='VOICE')
async def command_move(client, message, voice_channel: 'channel' = None):
    if (voice_channel is not None) and (not voice_channel.is_in_group_guild_connectable()):
        yield 'Please select a voice channel.'
        return
    
    async for content in move(client, message, message.author, voice_channel):
        if (content is not None):
            yield content


async def party_is_over_description(command_context):
    
    return Embed('party-is-over', (
        'Should I mark the talking party as done?\n'
        f'Usage: `{command_context.prefix}party-is-over`'
        ), color = MAIN_VOICE_COLOR).add_footer(
            'Administrator only!')

@VOICE_COMMAND_CLIENT.commands(
    name = 'party-is-over',
    description = party_is_over_description,
    checks = checks.owner_or_has_guild_permissions(administrator = True),
    aliases = 'partyisover',
    category = 'VOICE',
)
async def command_party_is_over(client, message):
    async for content in party_is_over(client, message):
        if (content is not None):
            yield content

if (AUDIO_PATH is not None) and AUDIO_PLAY_POSSIBLE:
    async def command_local_description(command_context):
        return Embed('local',(
            'Plays a local audio from my collection.\n'
            f'Usage: `{command_context.prefix}local <name>`\n'
            'If you do not say anything to play, I ll tell, want I am currently playing instead > <.'
            ), color = MAIN_VOICE_COLOR)
    
    @VOICE_COMMAND_CLIENT.commands(
        name = 'local',
        description = command_local_description,
        checks = checks.is_guild(GUILD__SUPPORT),
        category = 'VOICE',
    )
    async def command_local(client, message, name):
        async for content in local_play(client, message, name):
            if (content is not None):
                yield content

if AUDIO_PLAY_POSSIBLE and (not MARISA_MODE):
    async def command_chesuto_chesuto_play_by_name_description(command_context):
        
        return Embed('play', (
            'Plays the given chesuto bgm.\n'
            f'Usage: `{command_context.prefix}play <name>`\n'
            '\n'
            'Note that the given name can be also given as the position of the track.'
                ), color = COLOR__FLAN_HELP)
    
    @Flan.commands(name = 'play', description = command_chesuto_chesuto_play_by_name_description, category='VOICE')
    async def command_chesuto_play(command_context, name):
        if not name:
            yield await command_chesuto_chesuto_play_by_name_description(command_context)
            return
        
        async for content in chesuto_play_by_name(command_context.client, command_context.message, name):
            if (content is not None):
                yield content
    
    async def command_chesuto_play_random_description(command_context):
        
        return Embed('play', (
            'Plays a random chesuto bgm.\n'
            f'Usage: `{command_context.prefix}random`\n'
                ), color = COLOR__FLAN_HELP)
    
    @Flan.commands(name = 'random', description = command_chesuto_play_random_description, category='VOICE')
    async def command_chesuto_random(client, message):
        async for content in chesuto_play_random(client, message):
            if (content is not None):
                yield content

async def command_loop_description(command_context):
    return Embed('loop', (
        'Sets the voice client\'s looping behaviour or returns the current one.\n'
        f'Usage: `{command_context.prefix}loop <queue|actual|stop>`\n'
        ), color = VOICE_COLORS.get(command_context.client, None))

@VOICE_COMMAND_CLIENT.commands(name = 'loop', description = command_loop_description, category='VOICE')
async def command_loop(client, message, behaviour:'str' = None):
    if (behaviour is not None):
        state = behaviour.lower()
        if state not in VOICE_LOOPER_BEHAVIOURS:
            return f'Behaviour: {behaviour} is not any of the expected ones..'
    
    return await loop(client, message, behaviour)


async def command_queue_description(command_context):
    return Embed('queue', (
        'Shows the voice client\'s queue of the guild.\n'
        f'Usage: `{command_context.prefix}queue`'
        ), color = VOICE_COLORS.get(command_context.client, None))


@VOICE_COMMAND_CLIENT.commands(name = 'queue', description = command_queue_description, category='VOICE')
async def command_queue(client, message):
    guild = message.guild
    if guild is None:
        return
    
    async for content in queue(client, message, guild):
        if (content is not None):
            yield content


async def command_volume_description(command_context):
    return Embed(
        'volume',
        (
            'Sets my volume to the given percentage.\n'
            f'Usage: `{command_context.prefix}volume *n*`\n'
            'If no volume is passed, then I will tell my current volume.'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )

@VOICE_COMMAND_CLIENT.commands(name = 'volume', description = command_volume_description, category='VOICE')
async def command_volume(client, message, volume: int = None):
    return await volume_(client, message, volume)


async def command_stop_description(command_context):
    return Embed(
        'stop',
        (
            'Well, if you really want I can stop playing audio.\n'
            f'Usage: `{command_context.prefix}stop`'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )


@VOICE_COMMAND_CLIENT.commands(name = 'stop', description = command_stop_description, category='VOICE')
async def command_stop(client, message):
    return await stop(client, message)

async def command_skip_description(command_context):
    return Embed(
        'skip',
        (
            'Skips the audio at the given index.\n'
            f'Usage: `{command_context.prefix}skip *index*`\n'
            'If not giving any index or giving it as `0`, will skip the currently playing audio.'
        ),
        color = VOICE_COLORS.get(command_context.client, None),
    )

@VOICE_COMMAND_CLIENT.commands(name = 'skip', description = command_skip_description, category='VOICE')
async def command_skip(client, message, index: int = 0):
    return await skip(client, message, index)

#### #### #### #### Add as slash commands #### #### #### ####

if SLASH_CLIENT is not None:
    VOICE_COMMANDS = SLASH_CLIENT.interactions(
        None,
        name = 'voice',
        description = 'Voice commands',
        guild = GUILD__SUPPORT,
    )
    
    @VOICE_COMMANDS.interactions(name = 'join')
    async def slash_join(client, interaction_event,
        volume: ('int', 'Any preset volume?') = None,
    ):
        """Joins the voice channel."""
        return join(client, interaction_event.user, interaction_event.guild, volume)
    
    @VOICE_COMMANDS.interactions(name = 'pause')
    async def slash_pause(client, interaction_event):
        """Pauses the currently playing audio."""
        return await pause(client, interaction_event)
    
    @VOICE_COMMANDS.interactions(name = 'resume')
    async def slash_resume(client, interaction_event):
        """Resumes the currently playing audio."""
        return await resume(client, interaction_event)
    
    @VOICE_COMMANDS.interactions(name = 'leave')
    async def slash_leave(client, interaction_event):
        """Leaves me from the voice channel."""
        return leave(client, interaction_event)
    
    
    if AUDIO_PLAY_POSSIBLE:
        @VOICE_COMMANDS.interactions(name = 'play')
        async def slash_yt_play(client, interaction_event,
            name: ('str', 'The name of the audio to play.') = '',
        ):
            """Plays the chosen audio or shows what is playing right now."""
            return yt_play(client, interaction_event, name)
    
    @VOICE_COMMANDS.interactions(name = 'move')
    async def slash_move(client, interaction_event,
        voice_channel: ('channel_group_guild_connectable', 'To which channel should I move to?') = None
    ):
        """Moves to the selected channel or next to You, my Love?"""
        return move(client, interaction_event, interaction_event.user, voice_channel)
    
    @VOICE_COMMANDS.interactions(name = 'party-is-over')
    async def slash_party_is_over(client, interaction_event):
        """I mark the talking party as done?"""
        if not interaction_event.user_permissions.can_administrator:
            return 'You must have administrator permission to invoke this command.'
        
        return party_is_over(client, interaction_event)
    
    if (AUDIO_PATH is not None) and AUDIO_PLAY_POSSIBLE:
        @VOICE_COMMANDS.interactions(name = 'local')
        async def slash_local(client, interaction_event,
            name: ('str', 'The audio\'s name') = '',
        ):
            """Plays a local audio file from my own collection UwU."""
            return local_play(client, interaction_event, name)
    
    @VOICE_COMMANDS.interactions(name = 'loop')
    async def slash_loop(client, interaction_event,
        behaviour: (VOICE_LOOPER_BEHAVIOURS_PAIRS, 'Set looping as?') = None,
    ):
        """Sets the voice client's looping behaviour or returns the current one."""
        return await loop(client, interaction_event, behaviour)
    
    @VOICE_COMMANDS.interactions(name = 'queue')
    async def slash_queue(client, interaction_event):
        """Shows the voice client\'s queue of the guild."""
        return queue(client, interaction_event, GUILD__SUPPORT)
    
    @VOICE_COMMANDS.interactions(name = 'volume')
    async def slash_volume(client, interaction_event,
        volume: ('number', 'Percentage?') = None,
    ):
        """Sets my volume to the given percentage."""
        return await volume_(client, interaction_event, volume)
    
    @VOICE_COMMANDS.interactions(name = 'stop')
    async def slash_stop(client, interaction_event):
        """Nyahh, if you really want I can stop playing audio."""
        return await stop(client, interaction_event)
    
    @VOICE_COMMANDS.interactions(name = 'skip')
    async def slash_skip(client, interaction_event,
        index: ('int', 'Which audio to skip?') = 0,
    ):
        """I skip the audio at the given index."""
        return await skip(client, interaction_event, index)
    
    @VOICE_COMMANDS.interactions(name = 'join-speakers')
    async def slash_join_speakers(client, interaction_event):
        """Joins the speakers in a stage channel."""
        return join_speakers(client, interaction_event)
    
    @VOICE_COMMANDS.interactions(name = 'join-audience')
    async def slash_join_audience(client, interaction_event):
        """Joins the audience in a stage channel."""
        return join_audience(client, interaction_event)
