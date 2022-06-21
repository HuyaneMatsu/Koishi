# -*- coding: utf-8 -*-
import json, os
from time import perf_counter
from random import random
from datetime import datetime
from audioop import add as add_voice

from io import BytesIO
from PIL import Image as PIL
from PIL.ImageSequence import Iterator as ImageSequenceIterator

from hata import eventlist, RATE_LIMIT_GROUPS, Embed, cchunkify, User, random_id, chunkify, Webhook, \
    KOKORO, VoiceRegion, parse_custom_emojis, UserBase, Channel, datetime_to_id, Client, \
    ApplicationCommand, ApplicationCommandOption, ApplicationCommandOptionType, \
    ApplicationCommandOptionChoice, LocalAudio, AudioSource, OpusDecoder, PrivacyLevel

from scarletio import Future, future_or_timeout, WaitTillAll, sleep, ReuBytesIO, ReuAsyncIO, enter_executor

from hata.ext.command_utils import ChooseMenu, Pagination, Closer
from hata.ext.commands_v2 import Command, checks, configure_converter, ConverterFlag, CommandContext
from hata.discord.events.core import PARSERS
from hata.ext.prettyprint import pchunkify
from hata.ext.patchouli import map_module, MAPPED_OBJECTS


from config import AUDIO_PATH, AUDIO_PLAY_POSSIBLE, MARISA_MODE

from bot_utils.constants import PATH__KOISHI

TEST_COMMANDS = eventlist(type_=Command, category='TEST COMMANDS',)

MAIN_CLIENT : Client

map_module('hata')

def setup(lib):
    MAIN_CLIENT.commands.extend(TEST_COMMANDS)
    
def teardown(lib):
    MAIN_CLIENT.commands.unextend(TEST_COMMANDS)

def test_choose_menu_repr_choose_menu_selector( * args):
    return Future(KOKORO)


@TEST_COMMANDS
async def test_choose_menu_repr(client, message):
    """
    Creates a ChooseMenu and returns it's repr.
    """
    choices = ['nice', 'cat']
    choose_menu = await ChooseMenu(client, message.channel, choices, test_choose_menu_repr_choose_menu_selector)
    await client.message_create(message.channel, repr(choose_menu))

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_role_create(client, message):
    """
    Creates and deletes a role.
    """
    guild = message.guild
    role = await client.role_create(guild, 'Mokou')
    await client.role_delete(role)
    await client.message_create('done')

@TEST_COMMANDS
async def test_allowed_edit(client, message):
    """
    Creates a message and edits it. Should not ping you.
    """
    user = message.author
    message = await client.message_create(message.channel, 'Test')
    await client.message_edit(message, user.mention, allowed_mentions=None)

@TEST_COMMANDS(checks = [checks.guild_only()])
async def test_rate_limit(client, message):
    """
    A fast rate limit test for next patch to validate anything.
    """
    guild = message.guild
    if guild is None:
        return
    
    proxy = client.get_rate_limits_of(RATE_LIMIT_GROUPS.role_edit, limiter = guild)
    if (not proxy.is_alive()) or (not proxy.has_size_set()):
        if not guild.cached_permissions_for(client).can_manage_roles:
            await client.message_create(message.channel, 'Current state unknown -> No permissions.')
            return
        
        roles = message.guild.role_list
        if len(roles)==1:
            await client.message_create(message.channel, 'Current state unknown -> Need more roles.')
            return
        
        role = roles[-2]
        if not client.has_higher_role_than(role):
            await client.message_create(message.channel, 'Current state unknown -> No lower role')
            return
        
        proxy.keep_alive = True
        task = client.loop.create_task(client.role_edit(role, color=role.color))
        future_or_timeout(task, 2.5)
        try:
            await task
        except TimeoutError:
            pass
    
        if not proxy.has_info():
            await client.message_create(message.channel, 'Current state unknown -> Need more roles.')
            return
        
    next_reset = proxy.next_reset_after
    used = proxy.used_count
    free = proxy.free_count
    proxy = None # allows GC, not needed to turn keep alive to turn off either
    
    await client.message_create(message.channel, f'Next reset after : {next_reset!r}, used : {used!r}, free : {free!r}.')
    return
    
@TEST_COMMANDS
async def test_user_data(client, message, user:User):
    """
    Prints out user data as received json
    """
    data = await client.http.user_get(user.id)
    await Pagination(client, message.channel,[Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())])

@TEST_COMMANDS
async def test_100_messages(client, message):
    """
    Sends 100 messages, like a boss!
    """
    tasks = []
    for x in range(100):
        task = KOKORO.create_task(client.message_create(message.channel, repr(x)))
        tasks.append(task)
    
    start = perf_counter()
    await WaitTillAll(tasks,client.loop)
    end = perf_counter()
    
    await client.message_create(message.channel, repr(end - start))

@TEST_COMMANDS
async def crosspost(client, message, message_id:int):
    """
    Crossposts, pls pass a mssage id from the current channel!
    """
    to_message = await client.message_get(message.channel, message_id)
    await client.message_crosspost(to_message)
    
    await client.message_create(message.channel, 'success')

@TEST_COMMANDS
async def get_guild(client, message):
    """
    Gets the current guild.
    """
    guild = message.guild
    if guild is None:
        await client.message_create(message.channel, 'Please use this command at a guild.')
    
    data = await client.http.guild_get(guild.id)
    await Pagination(client, message.channel,[Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())])

@TEST_COMMANDS
async def test_webhook_response(client, message, user:User, use_user_avatar:int=1):
    """
    Creates a message with a webhook for checking whether avatar is included.
    
    Also pass user maybe?
    """
    channel = message.channel
    result = ['']
    
    content = str(random_id())
    
    http_type = type(client.http)
    original_webhook_message_create = http_type.webhook_message_create
    
    async def replace_webhook_message_create(client, *args):
        data = await original_webhook_message_create(client, *args)
        if (data is not None) and (data.get('content', '') == content):
            result[0] = str(data)
        return data
    
    http_type.webhook_message_create = replace_webhook_message_create
    
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'tester')
    
    if not use_user_avatar:
        async with client.http.get(user.avatar_url) as response:
            webhook_avatar_data = await response.read()
        
        await client.webhook_edit(executor_webhook, avatar = webhook_avatar_data)
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content', '') == content:
            result.append(str(data))
        
        return source_MESSAGE_CREATE(client, data)
    
    PARSERS['MESSAGE_CREATE'] = replace_MESSAGE_CREATE
    
    if use_user_avatar:
        avatar_url = user.avatar_url
    else:
        avatar_url = None
    
    message = await client.webhook_message_create(executor_webhook,content,avatar_url=avatar_url, wait=True)
    
    http_type.webhook_message_create = original_webhook_message_create
    
    await sleep(1.0)
    
    if PARSERS['MESSAGE_CREATE'] is replace_MESSAGE_CREATE:
        PARSERS['MESSAGE_CREATE'] = source_MESSAGE_CREATE
    
    await Pagination(client, channel, [Embed(description=description) for description in chunkify(result)])

@TEST_COMMANDS
async def test_webhook_response_with_url(client, message, url):
    """
    Creates a message with a webhook for checking whether avatar is included.
    """
    channel = message.channel
    result = ['']
    
    content = str(random_id())
    
    http_type = type(client.http)
    original_webhook_message_create = http_type.webhook_message_create
    
    async def replace_webhook_message_create(client, *args):
        data = await original_webhook_message_create(client, *args)
        if data.get('content', '') == content:
            result[0] = str(data)
        return data
    
    http_type.webhook_message_create = replace_webhook_message_create
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content', '') == content:
            result.append(str(data))
        
        return source_MESSAGE_CREATE(client, data)
    
    PARSERS['MESSAGE_CREATE'] = replace_MESSAGE_CREATE
    
    executor_webhook = Webhook.from_url(url)
    
    message = await client.webhook_message_create(executor_webhook, content, wait=True)
    
    http_type.webhook_message_create = original_webhook_message_create
    
    await sleep(1.0)
    
    if PARSERS['MESSAGE_CREATE'] is replace_MESSAGE_CREATE:
        PARSERS['MESSAGE_CREATE'] = source_MESSAGE_CREATE
    
    await Pagination(client, channel, [Embed(description=description) for description in chunkify(result)])

@TEST_COMMANDS
async def test_webhook_response_avatar_url(client, message, avatar_url):
    """
    Creates a message with a webhook for checking whether avatar is included. Please include avatr url, hehe.
    """
    channel = message.channel
    result = ['']
    
    content = str(random_id())
    
    http_type = type(client.http)
    original_webhook_message_create = http_type.webhook_message_create
    
    async def replace_webhook_message_create(client, *args):
        data = await original_webhook_message_create(client, *args)
        if (data is not None) and (data.get('content', '') == content):
            result[0] = str(data)
        return data
    
    http_type.webhook_message_create = replace_webhook_message_create
    
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'tester')
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content', '') == content:
            result.append(str(data))
        
        return source_MESSAGE_CREATE(client, data)
    
    PARSERS['MESSAGE_CREATE'] = replace_MESSAGE_CREATE
    
    message = await client.webhook_message_create(executor_webhook,content,avatar_url=avatar_url, wait=True)
    
    http_type.webhook_message_create = original_webhook_message_create
    
    await sleep(1.0)
    
    if PARSERS['MESSAGE_CREATE'] is replace_MESSAGE_CREATE:
        PARSERS['MESSAGE_CREATE'] = source_MESSAGE_CREATE
    
    await Pagination(client, channel, [Embed(description=description) for description in chunkify(result)])

@TEST_COMMANDS
async def test_webhook_response_avatar_url_nowait(client, message, avatar_url):
    """
    Creates a message with a webhook for checking whether avatar is included. Please include avatr url, hehe.
    """
    channel = message.channel
    result = []
    
    content = str(random_id())
    
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'tester')
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content', '') == content:
            result.append(str(data))
        
        return source_MESSAGE_CREATE(client, data)
    
    PARSERS['MESSAGE_CREATE'] = replace_MESSAGE_CREATE
    
    message = await client.webhook_message_create(executor_webhook,content,avatar_url=avatar_url, wait=False)
    
    await sleep(1.0)
    
    if PARSERS['MESSAGE_CREATE'] is replace_MESSAGE_CREATE:
        PARSERS['MESSAGE_CREATE'] = source_MESSAGE_CREATE
    
    await Pagination(client, channel, [Embed(description=description) for description in chunkify(result)])

@TEST_COMMANDS
async def discovery_validate_randoms(client, message):
    """
    Does 30 discovery validate request with random terms. 10 of them is duped tho.
    """
    words = [''.join(chr(97 + int(random() * 25.0)) for _ in range(10)) for _ in range(20)]
    for index in range(10):
        words.append(words[index])
    
    collected = []
    for word in words:
        start = perf_counter()
        result = await client.discovery_validate_term(word)
        end = perf_counter()
        
        collected.append(f'{word} : {result} ({end - start:.2f}s)')
    
    await client.message_create(message.channel, '\n'.join(collected))

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_receive_voice(client, message, target: User = None):
    """
    Receives 10 seconds of sound, then plays it. Also please define a user as well, who I will listen to.
    """
    channel = message.channel
    guild = channel.guild
    if guild is None:
        return
    
    if target is None:
        await client.message_create(channel, 'Please define a user as well')
        return
    
    state = guild.voice_states.get(message.author.id, None)
    if state is None:
        await client.message_create(channel, 'You are not at a voice channel!')
        return
    
    channel = state.channel
    if not channel.cached_permissions_for(client).can_connect:
        await client.message_create(message.channel, 'I have no permissions to connect to that channel')
        return
    
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        try:
            voice_client = await client.join_voice(channel)
        except BaseException as err:
            if isinstance(err, TimeoutError):
                text = 'Timed out meanwhile tried to connect.'
            elif isinstance(err, RuntimeError):
                text = 'The client cannot play voice, some libraries are not loaded'
            else:
                text = repr(err)
            
            await client.message_create(message.channel, text)
            return
    
    audio_stream = voice_client.listen_to(target)
    
    await client.message_create(message.channel, 'Started listening')
    await sleep(10.0, KOKORO)
    audio_stream.stop()
    
    voice_client.append(audio_stream)

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_receive_voice_decoded(client, message, target: User = None):
    """
    Receives 10 seconds of sound, then plays it. Also please define a user as well, who I will listen to.
    """
    channel = message.channel
    guild = channel.guild
    if guild is None:
        return
    
    if target is None:
        await client.message_create(channel, 'Please define a user as well')
        return
    
    state = guild.voice_states.get(message.author.id, None)
    if state is None:
        await client.message_create(channel, 'You are not at a voice channel!')
        return
    
    channel = state.channel
    if not channel.cached_permissions_for(client).can_connect:
        await client.message_create(message.channel, 'I have no permissions to connect to that channel')
        return
    
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        try:
            voice_client = await client.join_voice(channel)
        except BaseException as err:
            if isinstance(err, TimeoutError):
                text = 'Timed out meanwhile tried to connect.'
            elif isinstance(err, RuntimeError):
                text = 'The client cannot play voice, some libraries are not loaded'
            else:
                text = repr(err)
            
            await client.message_create(message.channel, text)
            return
    
    audio_stream = voice_client.listen_to(target, auto_decode=True, yield_decoded=True)
    
    await client.message_create(message.channel, 'Started listening')
    await sleep(10.0, KOKORO)
    audio_stream.stop()
    
    voice_client.append(audio_stream)

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_receive_voice_repeat(client, message, target: User = None):
    """
    Repeats your audio for 30 seconds. Please define who's audio to repeat as well.
    """
    channel = message.channel
    guild = channel.guild
    if guild is None:
        return
    
    if target is None:
        await client.message_create(channel, 'Please define a user as well')
        return
    
    state = guild.voice_states.get(message.author.id, None)
    if state is None:
        await client.message_create(channel, 'You are not at a voice channel!')
        return
    
    channel = state.channel
    if not channel.cached_permissions_for(client).can_connect:
        await client.message_create(message.channel, 'I have no permissions to connect to that channel')
        return
    
    voice_client = client.voice_client_for(message)
    if voice_client is None:
        try:
            voice_client = await client.join_voice(channel)
        except BaseException as err:
            if isinstance(err, TimeoutError):
                text = 'Timed out meanwhile tried to connect.'
            elif isinstance(err, RuntimeError):
                text = 'The client cannot play voice, some libraries are not loaded'
            else:
                text = repr(err)
            
            await client.message_create(message.channel, text)
            return
    
    audio_stream = voice_client.listen_to(target)
    
    await client.message_create(message.channel, 'Started listening')
    voice_client.append(audio_stream)
    
    await sleep(30.0, KOKORO)
    audio_stream.stop()
    
@TEST_COMMANDS
async def test_raise(client, message):
    """
    Just raises an error.
    """
    raise ValueError('umm?')

@TEST_COMMANDS
async def test_multytype_annotation(client, message, value:('channel', 'role') = None):
    """
    Tries to parse role and channel at the same time, lets go boiz!
    """
    await client.message_create(message.channel, repr(value))

@TEST_COMMANDS
@configure_converter('message', everywhere=True)
async def test_message_converter(client, message, value:'message'=True):
    """
    Tries to parse the message from the content of the message.
    """
    await client.message_create(message.channel, repr(value))

@TEST_COMMANDS
async def test_invite_converter(client, message, value:'invite'):
    """
    Tries to parse an invite from the content of the message.
    """
    await client.message_create(message.channel, repr(value))

@TEST_COMMANDS(separator='|')
async def test_command_parameter_single(client, message, *words):
    """
    Separates words by `|' character.
    """
    result = ', '.join(words)
    if len(result) > 2000:
        result = result[:2000]
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS(separator=('[', ']'))
async def test_command_parameter_area(client, message, *words):
    """
    Separates words by space, but between `[]` count as one.
    """
    result = ', '.join(words)
    if len(result) > 2000:
        result = result[:2000]
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS(separator=('*', '*'))
async def test_command_parameter_inter(client, message, *words):
    """
    Separates words by space, but the ones between `*` character are one.
    """
    result = ', '.join(words)
    if len(result) > 2000:
        result = result[:2000]
    
    await client.message_create(message.channel, result)

def rule_upper(name):
    if name is None:
        return 'UNCATEGORIZED'
    
    return name.upper()

def rule_capu(name):
    if name is None:
        return 'Uncategorized'
    
    return name.capitalize()

def rule_lower(name):
    if name is None:
        return 'uncategorized'
    
    return name.lower()

@TEST_COMMANDS
async def set_upper_category_names(client, message):
    """
    Sets the category names of the client to upper case.
    """
    client.command_processor.category_name_rule = rule_upper
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_upper_command_names(client, message):
    """
    Sets the command names of the client to upper case.
    """
    client.command_processor.command_name_rule = rule_upper
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_capu_category_names(client, message):
    """
    Sets the category names of the client to capitalized form.
    """
    client.command_processor.category_name_rule = rule_capu
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_capu_command_names(client, message):
    """
    Sets the command names of the client to capitalized form.
    """
    client.command_processor.command_name_rule = rule_capu
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_lower_category_names(client, message):
    """
    Sets the category names of the client to lower case.
    """
    client.command_processor.category_name_rule = rule_lower
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_lower_command_names(client, message):
    """
    Sets the command names of the client to lower case.
    """
    client.command_processor.command_name_rule = rule_lower
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_get_integrations(client, message):
    """
    Gets the integrations of the guild.
    
    Guild only!
    """
    # make sure
    guild = message.guild
    if guild is None:
        return
    
    integrations = await client.integration_get_all(guild)
    pages = [Embed(description=chunk) for chunk in pchunkify(integrations)]
    await Pagination(client, message.channel, pages,)

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_get_webhooks(client, message):
    """
    Gets the webhooks of the guild.
    
    Guild only!
    """
    # make sure
    guild = message.guild
    if guild is None:
        return
    
    webhooks = await client.webhook_get_all_guild(guild,)
    pages = [Embed(description=chunk) for chunk in pchunkify(webhooks)]
    await Pagination(client, message.channel, pages,)

@TEST_COMMANDS
async def test_channel_pretty_render(client, message):
    """
    Renders the local channels.
    """
    channel = message.channel
    guild = channel.guild
    if guild is None:
        to_render = channel
    else:
        to_render = guild.channels
    
    pages = [Embed(description=chunk) for chunk in pchunkify(to_render)]
    await Pagination(client, message.channel, pages,)

# DiscordException Forbidden (403), code=20001: Bots cannot use this endpoint
# 2020 10 09:
# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_start_channel_thread(client, message):
    """
    Does a post request to the channel's threads.
    """
    data = await client.http.thread_create_private(message.channel.id, None)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_get_channel_thread_user_get_all(client, message):
    """
    Gets the channel's threads' users probably, no clue.
    """
    data = await client.http.thread_user_get_all(message.channel.id)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_add_channel_thread_user(client, message):
    """
    Adds you to the channel's threads.
    """
    data = await client.http.thread_user_add(message.channel.id, message.author.id)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_delete_channel_thread_user(client, message):
    """
    Deletes you to the channel's threads.
    """
    data = await client.http.thread_user_delete(message.channel.id, message.author.id)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_application_get_all_detectable(client, message):
    """
    Requests the detectable applications.
    """
    data = await client.http.applications_detectable()
    
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_get_eula(client, message):
    """
    Gets an eula.
    """
    data = await client.http.eula_get(542074049984200704)
    
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_render_application(client, message):
    """
    Renders the client's application.
    """
    pages = [Embed(description=chunk) for chunk in pchunkify(client.application)]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_render_applications(client, message):
    """
    Renders the detectable applications.
    """
    applications = await client.applications_detectable()
    pages = [Embed(description=chunk) for chunk in pchunkify(applications)]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_get_welcome_screen(client, message):
    """
    Gets an eula.
    """
    guild = message.guild
    if guild is None:
        return
    
    data = await client.http.welcome_screen_get(guild.id)
    
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_regions(client, message):
    """
    Returns the difference between the predefined and the request-able voice regions.
    
    Note, this command should be called only once to yield the new regions.
    """
    old_ones = set(VoiceRegion.INSTANCES.values())
    await client.voice_region_get_all()
    new_ones = set(VoiceRegion.INSTANCES.values())
    
    difference = new_ones - old_ones
    if not difference:
        embeds = [Embed(description='*There are no new voice regions added*')]
    else:
        embeds = [Embed(description= (
            f'Voice region : {region.name!r}\n'
            f'id : {region.value!r}\n'
            f'vip : {region.vip!r}\n'
            f'deprecated : {region.deprecated!r}\n'
            f'custom : {region.custom!r}'
                )) for region in difference]
    
    await Pagination(client, message.channel, embeds)

@TEST_COMMANDS
async def test_closer(client, message):
    """
    Creates a new closer.
    """
    await Closer(client, message.channel, Embed('cake?'), timeout=5.0)

@TEST_COMMANDS
async def test_list_invites(client, message):
    """
    Lists the invites of the respective guild.
    """
    guild = message.guild
    if guild is None:
        return
    
    invites = await client.invite_get_all_guild(guild)
    embeds = [Embed('Invites', chunk) for chunk in pchunkify(invites)]
    await Pagination(client, message.channel, embeds)

@TEST_COMMANDS(separator=',')
async def autohelp_singles(client, message, name:str, user:'user', *words):
    pass

@TEST_COMMANDS(aliases=['autohelp-defaulted-alt'])
async def autohelp_defaulted(client, message, name:str=None, channel:Channel=None, rest=None):
    pass

@TEST_COMMANDS(separator=('[', ']'))
async def autohelp_multy(client, message, value:{int, str}, user:{User, 'invite'}, *cakes:{Channel, 'tdelta'}):
    pass

@TEST_COMMANDS(separator=('[', ']'))
async def auto_sub_help(client, message, cake:str):
    pass

@auto_sub_help.commands
async def sugoi_dekai(ayaya:str):
    pass

@TEST_COMMANDS
async def detect_custom_emojis(client, message):
    """
    Detects the custom emojis at the given message's content.
    """
    emojis = parse_custom_emojis(message.content)
    if emojis:
        content_lines = []
        for x, emoji in zip(range(1, 21), emojis):
            content_lines.append(f'{x}.: {emoji}')
        
        truncated = len(emojis) - 20
        if truncated > 0:
            content_lines.append(f'*{truncated} truncated*')
        
        content = '\n'.join(content_lines)
    else:
        content = '*no custom emojis detected*'
    
    await client.message_create(message.channel, content)

@TEST_COMMANDS
async def test_message_reaction_clear(client, message, channel_id: int, message_id:int):
    """
    Removes the reactions from the given channel-id - message-id conbination.
    """
    await client.http.reaction_clear(channel_id, message_id)
    await client.message_create(message.channel, 'nya')

@TEST_COMMANDS
async def test_message_reaction_delete_emoji(client, message, channel_id: int, message_id: int, emoji:'emoji'):
    """
    Removes the reactions from the given channel-id - message-id - emoji conbination.
    """
    await client.http.reaction_delete_emoji(channel_id, message_id, emoji.as_reaction)
    await client.message_create(message.channel, 'nya')

@TEST_COMMANDS
@configure_converter('user', ConverterFlag.user_all)
async def avatar_1(client, message, user: 'user' = None):
    if user is None:
        user = message.author
    
    if user.avatar:
        color = user.avatar_hash & 0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)

@TEST_COMMANDS
async def what_is_it_1(client, message, entity: {'user', 'channel', 'role'} = None):
    if entity is None:
        result = 'Nothing is recognized.'
    elif isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, Channel):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS
@configure_converter('user', ConverterFlag.user_all)
async def avatar_2(client, message, user: 'user'=None):
    if user is None:
        user = message.author
    
    if user.avatar:
        color = user.avatar_hash & 0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)

@TEST_COMMANDS
@configure_converter('user', ConverterFlag.user_all)
async def avatar_3(client, message, user: 'user'=None):
    if user is None:
        user = message.author
    
    if user.avatar:
        color = user.avatar_hash & 0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)


@TEST_COMMANDS
@configure_converter('user', 0, name=True)
@configure_converter('channel', 0, name=True)
@configure_converter('role', 0, name=True)
async def what_is_it_2(client, message, entity: {'user', 'channel', 'role'}):
    if isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, Channel):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS(checks=[checks.owner_only()])
async def owner_1(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')

@TEST_COMMANDS(checks=[checks.owner_only()])
async def owner_2(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')

@TEST_COMMANDS(name='print_1')
async def print_1_(client, message, content):
    if content:
        await client.message_create(message.channel, content)

@TEST_COMMANDS(name='print_2', aliases=['say_2'])
async def print_2_(client, message, content):
    if content:
        await client.message_create(message.channel, content)

@TEST_COMMANDS
async def estimate_fast_delete_before_2020_02_00(client, message):
    target_channel = message.channel
    
    from config import KOISHI_ID, SATORI_ID, MARISA_ID
    
    COUNTER = 0
    OWNED = 0
    
    before = datetime_to_id(datetime(2020, 2, 1))
    
    while True:
        messages = await client.message_get_chunk(target_channel, before=before)
        if not messages:
            break
        
        for message in messages:
            user = message.author
            if user.id in (KOISHI_ID, SATORI_ID, MARISA_ID):
                OWNED += 1
            else:
                COUNTER += 1
            
        before = messages[-1].id
    
    PARALLELISM = 3
    RESET = 120
    LIMIT = 30
    DELAY = 0.1
    
    times, remainder = divmod(COUNTER, PARALLELISM * LIMIT)
    
    DURATION = DELAY + times * (RESET + DELAY)
    
    if remainder:
        DURATION += DELAY + DELAY * remainder / PARALLELISM
    else:
        DURATION -= RESET
        DURATION += LIMIT * DELAY / PARALLELISM
    
    await client.message_create(target_channel, f'Total messages: {COUNTER + OWNED}.\nEstimated duration {DURATION:.2f}')

@TEST_COMMANDS
async def do_delete(client, message):
    """
    from config import KOISHI_ID, SATORI_ID, KOISHI_TOKEN, SATORI_TOKEN
    Koishi = Client(KOISHI_TOKEN, client_id=KOISHI_ID)
    await Koishi.start()
    Satori = Client(SATORI_TOKEN, client_id=SATORI_ID)
    await Satori.start()
    await sleep(5., )
    """
    start = perf_counter()
    await client.multi_client_message_delete_sequence(message.channel, before=datetime(2020, 2, 1))
    end = perf_counter()
    """
    await Koishi.stop()
    await Satori.stop()
    await sleep(1., KOKORO)
    Koishi._delete()
    Satori._delete()
    Koishi = None
    Satori = None
    
    import gc
    gc.collect()
    """
    await client.message_create(message.channel, repr(end - start))


@TEST_COMMANDS
async def test_2_attachments(client, message):
    """
    Sends a message with 2 attachments.
    """
    with await ReuAsyncIO(os.path.join(PATH__KOISHI, 'images', '0000001E_yakumo_yukari_chen.gif')) as file1:
        with await ReuAsyncIO(os.path.join(PATH__KOISHI, 'images', '0000001F_yuri_hug.gif')) as file2:
            await client.message_create(message.channel, file=[file1, file2])

@TEST_COMMANDS
async def test_webhook_message_edit_0(client, message):
    """
    Creates a message with a webhook, then edits it's content out with `None`.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None)

@TEST_COMMANDS
async def test_webhook_message_edit_1(client, message):
    """
    Creates a message with a webhook, then edits it's content with `'ayaya''`.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, 'ayaya')

@TEST_COMMANDS
async def test_webhook_message_edit_2(client, message):
    """
    Creates a message with a webhook, then edits it's content out and changing sending it's embeds.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None, embed=Embed('cake'))

@TEST_COMMANDS
async def test_webhook_message_edit_3(client, message):
    """
    Creates a message with a webhook, then edits it's embeds out.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, embed=None)


@TEST_COMMANDS
async def test_webhook_message_edit_4(client, message):
    """
    Creates a message with a webhook, then edits it's content out.
    
    Note, that embed data is not included now.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None)

@TEST_COMMANDS
async def test_webhook_message_edit_5(client, message):
    """
    Creates a message with a webhook, then edits it to empty.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None, None)

@TEST_COMMANDS
async def test_webhook_message_edit_6(client, message):
    """
    Creates a message with a webhook, then removes it's embeds with `None`.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, embed=None)

@TEST_COMMANDS
async def test_webhook_message_delete(client, message):
    """
    Creates a message with a webhook, then deletes it.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_delete(executor_webhook, new_message)

@TEST_COMMANDS
async def test_webhook_message_edit_7(client, message):
    """
    Creates a message with a webhook, then sets allowed mentions to `None`?
    
    Note that this works only with the current implementation (2020.11.17 20:55).
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, message.author.mention, allowed_mentions=None, wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, allowed_mentions=None,)

@TEST_COMMANDS
async def test_webhook_message_edit_8(client, message):
    """
    Creates a message with a webhook, then edits it to the same value.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'ayaya', wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, 'ayaya')

@TEST_COMMANDS
async def test_webhook_message_edit_9(client, message):
    """
    Creates a message with a webhook, then edits it to the same value. (embed version)
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, embed=Embed('cake'))


@TEST_COMMANDS(checks=checks.guild_only())
async def update_and_display_roles(client, message):
    """
    Syncs the guild's roles then displays them.
    """
    guild = message.guild
    if guild is None:
        return
    
    await client.guild_role_get_all(guild)
    
    pages = [Embed(description=chunk) for chunk in pchunkify(guild.role_list, detailed=False)]
    await Pagination(client, message.channel, pages,)


@TEST_COMMANDS
async def half_size(client, message):
    """
    Halves the given gif's size.
    """
    attachments = message.attachments
    if attachments is None:
        await client.message_create(message.channel, 'The message has no attachments.')
        return
    
    for attachment in attachments:
        if attachment.name.endswith(('.gif', '.GIF')):
            break
    else:
        await client.message_create(message.channel, 'The message has no gif attachments.')
        return
    
    data = await client.download_attachment(attachment)
    
    async with enter_executor():
        source_gif = PIL.open(BytesIO(data))
        new_image = None
        frames = []
        
        for frame in ImageSequenceIterator(source_gif):
            frame = frame.convert('RGB')
            if new_image is None:
                size = frame.size
                size = (size[0]>>1, size[1]>>1)
                frame = frame.resize(size)
                new_image = frame
            else:
                frame = frame.resize(size)
                frames.append(frame)
        
        buffer = ReuBytesIO()
        new_image.save(buffer, format='gif', save_all=True, append_images=frames, loop=0, optimize=False,
            transparency=0, disposal=2)
        
        buffer.seek(0)
    
    await client.message_create(message, file=(attachment.name, buffer))

class check_interacter:
    __slots__ = ('user', 'channel', 'application_command')
    def __init__(self, channel, user, application_command):
        self.channel = channel
        self.user = user
        self.application_command = application_command
        
    def __call__(self, event):
        channel, user, interaction_command = event
        if channel is not self.channel:
            return False
        
        if user is not self.user:
            return False
        
        if interaction_command.id != self.application_command.id:
            return False
        
        return True

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_response_twice(client, message):
    """
    Tries to respond on an interaction twice, because why not.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0000',
        'ayaya',
            )
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0000`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        # Send twice, ayaya
        await client.interaction_response_message_create(interaction, 'Ayaya')
        await client.interaction_response_message_create(interaction, 'Ayaya')
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_response_multiple_embeds(client, message):
    """
    Tries to respond on an interaction with multiple embeds.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0001',
        'ayaya',
            )
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0001`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction, [Embed('cake'), Embed('Ayaya')])
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_followup_first(client, message):
    """
    Tries to respond on an interaction with followup.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0002',
        'ayaya',
            )
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0002`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        # ops
        await client.interaction_followup_message_create(interaction, 'ayaya')
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_followup(client, message):
    """
    Tries to respond on an interaction normally, then with followup.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0003',
        'ayaya',
            )
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0003`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction, 'Ayaya')
        await client.interaction_followup_message_create(interaction, 'ayaya')
    finally:
        await client.application_command_guild_delete(guild, application_command)

# Name param is removed since it wont work.
'''
@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_followup_alt_name(client, message):
    """
    Tries to respond on an interaction with a different name.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0004',
        'ayaya',
            )
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0004`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction)
        await client.interaction_followup_message_create(interaction, 'ayaya', name='Not Marisa')
    finally:
        await client.application_command_guild_delete(guild, application_command)
'''

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_option_value_1(client, message):
    """
    Tests user type application command value.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0004',
        'ayaya',
            )
    
    application_command_schema.add_option(ApplicationCommandOption(
        'user',
        'Dunno something',
        ApplicationCommandOptionType.user,
            ))
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0004`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction,
            repr(interaction.interaction.options[0].value))
    finally:
        await client.application_command_guild_delete(guild, application_command)


@TEST_COMMANDS(checks=checks.guild_only())
async def load_messages(client, message, channel:Channel):
    start = perf_counter()
    collected = 0
    limit = 2000
    
    async for _ in await client.message_iterator(channel):
        collected += 1
        if collected == limit:
            break
    
    delay = (perf_counter() - start)
    
    return f'Loaded: {collected} messages (limit={limit}); Took: {delay:.3f} seconds.'
    
@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_option_choice_type_1(client, message):
    """
    Tests int type application command choice value.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0005',
        'ayaya',
            )
    
    application_command_schema.add_option(ApplicationCommandOption(
        'number',
        'Dunno something',
        ApplicationCommandOptionType.integer,
        choices = [ApplicationCommandOptionChoice('cake', '6'), ApplicationCommandOptionChoice('cookie', '8')]
            ))
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0005`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction,
            repr(interaction.interaction.options[0].value))
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_option_choice_type_2(client, message):
    """
    Tests big-int type application command choice value.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0005',
        'ayaya',
            )
    
    application_command_schema.add_option(ApplicationCommandOption(
        'number',
        'Dunno something',
        ApplicationCommandOptionType.integer,
        choices = [ApplicationCommandOptionChoice('cake', 798636232133181511), ApplicationCommandOptionChoice('cookie', 7986362321331815111545)]
            ))
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0006`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction,
            repr(interaction.interaction.options[0].value))
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_option_choice_type_3(client, message):
    """
    Tests 33 bit big-int type application command choice value.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0006',
        'ayaya',
            )
    
    application_command_schema.add_option(ApplicationCommandOption(
        'number',
        'Dunno something',
        ApplicationCommandOptionType.integer,
        choices = [ApplicationCommandOptionChoice('cake', 4294967296), ApplicationCommandOptionChoice('cookie', 4294967296)]
            ))
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0007`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction,
            repr(interaction.interaction.options[0].value))
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_option_choice_type_4(client, message):
    """
    Tests 61 bit big-int type application command choice value.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0007',
        'ayaya',
            )
    
    application_command_schema.add_option(ApplicationCommandOption(
        'number',
        'Dunno something',
        ApplicationCommandOptionType.integer,
        choices = [ApplicationCommandOptionChoice('cake', 1 << 60), ApplicationCommandOptionChoice('cookie', (1 << 60) + 1556656)]
            ))
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0007`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction,
            repr(interaction.interaction.options[0].value))
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_option_choice_type_5(client, message):
    """
    Tests 65 bit big-int type application command choice value.
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0008',
        'ayaya',
            )
    
    application_command_schema.add_option(
        ApplicationCommandOption(
            'number',
            'Dunno something',
            ApplicationCommandOptionType.integer,
            choices = [
                ApplicationCommandOptionChoice('cake', 1 << 64),
                ApplicationCommandOptionChoice('cookie', (1 << 64) + 4554656)
            ],
        )
    )
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0008`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction,
            repr(interaction.interaction.options[0].value))
    finally:
        await client.application_command_guild_delete(guild, application_command)

@TEST_COMMANDS(checks=checks.guild_only())
async def test_application_command_normal_edit(client, message):
    """
    Normally edits a sus message
    """
    guild = message.guild
    if guild is None:
        return
    
    application_command_schema = ApplicationCommand(
        'test_command0009',
        'ayaya',
            )
    
    application_command = await client.application_command_guild_create(guild, application_command_schema)
    
    try:
        await client.message_create(message.channel, 'Please use `/test_command0009`')
        
        # Wait
        try:
            interaction_event = await client.wait_for('interaction_create',
                check_interacter(message.channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await client.message_create(message.channel, 'timeout occurred')
            return
        
        await client.interaction_response_message_create(interaction_event)
        
        message = await client.interaction_followup_message_create(interaction_event, 'test')
        
        await client.message_edit(message, 'uhum?')
    
    finally:
        await client.application_command_guild_delete(guild, application_command)



async def voice_state(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('voice-state', (
        'Gets the voice state of the respective voice client.\n'
        f'Usage: `{prefix}voice-state`\n'
        )).add_footer('Owner only!')

@TEST_COMMANDS(description=voice_state, checks=checks.owner_only(), category='VOICE')
async def voice_state(client, message):
    voice_client = client.voice_client_for(message)
    lines = []
    guild = message.guild
    if voice_client is None:
        title = f'No client in {guild.name}.'
    else:
        title = f'Client info for {guild.name}.'
        
        source = voice_client.source
        queue = voice_client.queue
        if (source is not None) or queue:
            if (source is not None):
                lines.append(f'Actual: {source.title}')
            
            for index, source in enumerate(queue, 1):
                lines.append(f'Track {index}.: {source.title}')
        
        audio_streams = voice_client.get_audio_streams()
        if audio_streams:
            if lines:
                lines.append('')
            
            lines.append('Receives')
            
            for index, (user, stream) in enumerate(audio_streams):
                lines.append(f'Stream {index}.: {user.full_name}, {stream!r}')
        
        audio_sources = voice_client._audio_sources
        if audio_sources:
            if lines:
                lines.append('')
            
            for index, source in enumerate(audio_sources.values(), 1):
                lines.append(f'{index}.: {source}')
    
    pages = [Embed(title, chunk) for chunk in chunkify(lines)]
    
    await Pagination(client, message.channel, pages)

class MixerStream(AudioSource):
    __slots__ = ('_decoder', '_postprocess_called', 'sources', )
    def __init__(self, *sources):
        self.sources = list(sources)
        self._decoder = OpusDecoder()
        self._postprocess_called = False
    
    async def postprocess(self):
        if self._postprocess_called:
            return
        
        self._postprocess_called = True
        for source in self.sources:
            await source.postprocess()
    
    async def add(self, source):
        if self._postprocess_called:
            await source.postprocess()
        
        self.sources.append(source)
    
    async def read(self):
        sources = self.sources
        result = None
        
        for index in reversed(range(len(sources))):
            source = sources[index]
            data = await source.read()
            
            if data is None:
                del sources[index]
                await source.cleanup()
                continue
            
            if not source.NEEDS_ENCODE:
                data = self._decoder.decode(data)
            
            if result is None:
                result = data
            else:
                result = add_voice(result, data, 1)
            
            continue
        
        return result
    
    async def cleanup(self):
        self._postprocess_called = False
        sources = self.sources
        while sources:
            source = sources.pop()
            await source.cleanup()


if MARISA_MODE and AUDIO_PLAY_POSSIBLE:
    @TEST_COMMANDS(separator='|', checks=checks.owner_only(), category='VOICE')
    async def play_double(client, message):
        guild = message.guild
        if guild is None:
            return
        
        while True:
            voice_client = client.voice_client_for(message)
            if voice_client is None:
                text = 'I am not in a voice channel.'
                break
            
            source1 = await LocalAudio('/hdd/music/others/Ichigo - Tsuki made todoke, fushi no kemuri.mp3')
            source2 = await LocalAudio('/hdd/music/others/Nomico - IceBreak.mp3')
            
            source = MixerStream(source1, source2)

            if voice_client.append(source):
                text = f'Now playing {source.title}!'
            else:
                text = f'Added to queue {source.title}!'
            break
        
        await client.message_create(message.channel, text)

    @TEST_COMMANDS(separator='|', checks=checks.owner_only(), category='VOICE')
    @configure_converter(Channel, ConverterFlag.channel_all)
    async def play_from(client, message, voice_channel):
        
        while True:
            self_guild = message.guild
            if self_guild is None:
                text = 'Not in guild.'
                break
            
            other_guild = voice_channel.guild
            if other_guild is None:
                text = 'Other channel not in guild.'
                break
            
            self_voice_client = client.voice_client_for(message)
            if self_voice_client is None:
                voice_state = self_guild.voice_states.get(message.author.id, None)
                if voice_state is None:
                    text = 'You are not at a voice channel.'
                    break
                
                self_channel = voice_state.channel
                if not self_channel.cached_permissions_for(client).can_connect:
                    text = 'I have no permissions to connect to that channel'
                    break
                
                try:
                    self_voice_client = await client.join_voice(self_channel)
                except TimeoutError:
                    text = 'Timed out meanwhile tried to connect.'
                    break
                except RuntimeError:
                    text = 'The client cannot play voice, some libraries are not loaded'
                    break
            
            other_voice_states = list(other_guild.voice_states.values())
            for voice_state in other_voice_states:
                if voice_state.user is not client:
                    break
            else:
                text = 'No voice states in other guild.'
                break
            
            try:
                other_voice_client = client.voice_clients[other_guild.id]
            except KeyError:
                try:
                    other_voice_client = await client.join_voice(voice_channel)
                except TimeoutError:
                    text = 'Timed out meanwhile tried to connect.'
                    break
                except RuntimeError:
                    text = 'The client cannot play voice, some libraries are not loaded'
                    break
            
            mixer = MixerStream()
            for voice_state in other_voice_states:
                user = voice_state.user
                if user is client:
                    continue
                
                source = other_voice_client.listen_to(user, yield_decoded=True)
                await mixer.add(source)
            
            if self_voice_client.append(mixer):
                text = f'Now playing {mixer.title}!'
            else:
                text = f'Added to queue {mixer.title}!'
            break
        
        await client.message_create(message.channel, text)


@TEST_COMMANDS
async def test_webhook_message_edit_10(client, message):
    """
    Creates a message with a webhook, then adds attachments to it.
    """
    channel = message.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, file=('cake', b'cakes are great'))


@TEST_COMMANDS
async def test_stage_discovery_get(client, message):
    """
    Tries to get stage discovery.
    """
    data = await client.http.stage_discovery_get()
    chunks = cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
    pages = [Embed(description=chunk) for chunk in chunks]
    await Pagination(client, message.channel, pages)


@TEST_COMMANDS
async def test_stage_get_all(client, message):
    """
    Gets all the stages.
    """
    data = await client.http.stage_get_all()
    chunks = cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
    pages = [Embed(description=chunk) for chunk in chunks]
    await Pagination(client, message.channel, pages)


@TEST_COMMANDS
async def test_stage_edit(client, message):
    """
    Edits stage topic.
    """
    data = {'topic':'Ayaya'}
    data = await client.http.stage_edit(826912003452436510, data)
    chunks = cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
    pages = [Embed(description=chunk) for chunk in chunks]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_stage_create(client, message):
    """
    Edits stage.
    """
    data = {'channel_id':826912003452436510, 'topic':'Ayaya', 'privacy_level': PrivacyLevel.guild_only.value}
    data = await client.http.stage_create(data)
    chunks = cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
    pages = [Embed(description=chunk) for chunk in chunks]
    await Pagination(client, message.channel, pages)


@TEST_COMMANDS
async def test_stage_delete(client, message):
    """
    Deletes the stage topic?
    """
    data = await client.http.stage_delete(826912003452436510)
    chunks = cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())
    pages = [Embed(description=chunk) for chunk in chunks]
    await Pagination(client, message.channel, pages)


@TEST_COMMANDS
async def test_kwargs(ctx, **kwargs):
    """
    Kwargs?
    """
    await ctx.reply(repr(kwargs))


@TEST_COMMANDS
async def test_message_interaction(ctx, message:'message'):
    """
    Gets message interaction?
    """
    data = await ctx.client.http.message_interaction(message.channel.id, message.id)
    return str(data)


@TEST_COMMANDS
async def show_help_for(ctx, user:'user', content):
    """
    Shows help for the given user.
    """
    client = ctx.client
    message = ctx.message.custom(author=user)
    command = client.command_processor.command_name_to_command['help']
    context = CommandContext(client, message, ctx.prefix, content, command)
    await context.invoke()


@TEST_COMMANDS
async def voice_channels_only(channel: 'guild_voice' = None):
    return repr(channel)
