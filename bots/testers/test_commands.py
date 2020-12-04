import json, os
from time import perf_counter
from random import random
from datetime import datetime

from io import BytesIO
from PIL import Image as PIL
from PIL.ImageSequence import Iterator as ImageSequenceIterator

from hata import eventlist, Future, RATELIMIT_GROUPS, future_or_timeout, Embed, cchunkify, WaitTillAll, User, sleep, \
    istr, imultidict, random_id, WebhookType, chunkify, ICON_TYPE_NONE, Webhook, KOKORO, DiscordEntity, ReuBytesIO, \
    IconSlot, CHANNELS, ChannelText, VoiceRegion, parse_custom_emojis, UserBase, ChannelBase, time_to_id, Client, \
    ReuAsyncIO, enter_executor

from hata.discord.http import URLS
from hata.backend.hdrs import AUTHORIZATION
from hata.ext.commands import Command, ChooseMenu, checks, Pagination, Converter, ConverterFlag, Closer, \
    FlaggedAnnotation
from hata.discord.utils import Discord_hdrs
from hata.discord.http import API_ENDPOINT, CONTENT_TYPE
from hata.discord.parsers import PARSERS
from hata.ext.prettyprint import pchunkify
from hata.discord.emoji import create_partial_emoji
from hata.ext.patchouli import map_module, MAPPED_OBJECTS

from bot_utils.shared import KOISHI_PATH

TEST_COMMANDS = eventlist(type_=Command, category='TEST COMMANDS',)

map_module('hata')

def setup(lib):
    main_client.commands.extend(TEST_COMMANDS)
    
def teardown(lib):
    main_client.commands.unextend(TEST_COMMANDS)

@TEST_COMMANDS
async def test_choose_menu_repr(client, message):
    '''
    Creates a ChooseMenu and returns it's repr.
    '''
    choices = ['nice', 'cat']
    choose_menu = await ChooseMenu(client, message.channel, choices, lambda *args: Future(KOKORO))
    await client.message_create(message.channel, repr(choose_menu))

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_role_create(client, message):
    '''
    Creates and deletes a role.
    '''
    guild = message.guild
    role = await client.role_create(guild, 'Mokou')
    await client.role_delete(role)
    await client.message_create('done')

@TEST_COMMANDS
async def test_allowed_edit(client, message):
    '''
    Creates a message and edits it. Shoult not ping you.
    '''
    user = message.author
    message = await client.message_create(message.channel, 'Test')
    await client.message_edit(message, user.mention,allowed_mentions=None)

@TEST_COMMANDS(checks = [checks.guild_only()])
async def test_ratelimit(client, message):
    '''
    A fast ratelimit test for next patch to validate anything.
    '''
    guild = message.guild
    if guild is None:
        return
    
    proxy = client.get_ratelimits_of(RATELIMIT_GROUPS.role_edit, limiter = guild)
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
    '''
    Prints out user data as received json
    '''
    data = await client.http.user_get(user.id)
    await Pagination(client, message.channel,[Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())])

@TEST_COMMANDS
async def test_100_messages(client, message):
    '''
    Sends 100 messages, like a boss!
    '''
    tasks = []
    for x in range(100):
        task = KOKORO.create_task(client.message_create(message.channel, repr(x)))
        tasks.append(task)
    
    start = perf_counter()
    await WaitTillAll(tasks,client.loop)
    end = perf_counter()
    
    await client.message_create(message.channel, repr(end-start))

@TEST_COMMANDS
async def crosspost(client, message, message_id:int):
    '''
    Crossposts, pls pass a mssage id from the current channel!
    '''
    to_message = await client.message_get(message.channel, message_id)
    await client.message_crosspost(to_message)
    
    await client.message_create(message.channel, 'success')

@TEST_COMMANDS
async def get_guild(client, message):
    '''
    Gets the current guild.
    '''
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
        if (data is not None) and (data.get('content') == content):
            result[0] = str(data)
        return data
    
    http_type.webhook_message_create = replace_webhook_message_create
    
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.avatar_type is ICON_TYPE_NONE:
            continue
        
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = None
    
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'tester')
    
    if not use_user_avatar:
        webhook_avatar_data = await client.download_url(user.avatar_url)
        await client.webhook_edit(executor_webhook, avatar = webhook_avatar_data)
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content') == content:
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
        if data.get('content') == content:
            result[0] = str(data)
        return data
    
    http_type.webhook_message_create = replace_webhook_message_create
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content') == content:
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
        if (data is not None) and (data.get('content') == content):
            result[0] = str(data)
        return data
    
    http_type.webhook_message_create = replace_webhook_message_create
    
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = None
    
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'tester')
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content') == content:
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
    
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = None
    
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'tester')
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content') == content:
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
    words = [''.join(chr(97+int(random()*25.0)) for _ in range(10)) for _ in range(20)]
    for index in range(10):
        words.append(words[index])
    
    collected = []
    for word in words:
        start = perf_counter()
        result = await client.discovery_validate_term(word)
        end = perf_counter()
        
        collected.append(f'{word} : {result} ({end-start:.2f}s)')
    
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
            voice_client = await client.join_voice_channel(channel)
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
            voice_client = await client.join_voice_channel(channel)
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
            voice_client = await client.join_voice_channel(channel)
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
async def test_message_converter(client, message, value:Converter('message',
        flags=ConverterFlag.message_default.update_by_keys(everywhere=True), default=None)):
    """
    Tries to parse the message from the content of the message.
    """
    await client.message_create(message.channel, repr(value))

@TEST_COMMANDS
async def test_invite_converter(client, message, value:Converter('invite', default=None)):
    """
    Tries to parse an invite from the content of the message.
    """
    await client.message_create(message.channel, repr(value))

@TEST_COMMANDS(separator='|')
async def test_command_argument_single(client, message, *words):
    """
    Separates words by `|' character.
    """
    result = ', '.join(words)
    if len(result) > 2000:
        result = result[:2000]
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS(separator=('[', ']'))
async def test_command_argument_area(client, message, *words):
    """
    Separates words by space, but between `[]` count as one.
    """
    result = ', '.join(words)
    if len(result) > 2000:
        result = result[:2000]
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS(separator=('*', '*'))
async def test_command_argument_inter(client, message, *words):
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
    client.command_processer.category_name_rule = rule_upper
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_upper_command_names(client, message):
    """
    Sets the command names of the client to upper case.
    """
    client.command_processer.command_name_rule = rule_upper
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_capu_category_names(client, message):
    """
    Sets the category names of the client to capitalized form.
    """
    client.command_processer.category_name_rule = rule_capu
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_capu_command_names(client, message):
    """
    Sets the command names of the client to capitalized form.
    """
    client.command_processer.command_name_rule = rule_capu
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_lower_category_names(client, message):
    """
    Sets the category names of the client to lower case.
    """
    client.command_processer.category_name_rule = rule_lower
    await client.message_create(message.channel, 'nya!')

@TEST_COMMANDS
async def set_lower_command_names(client, message):
    """
    Sets the command names of the client to lower case.
    """
    client.command_processer.command_name_rule = rule_lower
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
    
    webhooks = await client.webhook_get_guild(guild,)
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
    data = await client.http.channel_thread_start(message.channel.id, None)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data, indent=4, sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_get_channel_thread_users(client, message):
    """
    Gets the channel's threads' users probably, no clue.
    """
    data = await client.http.thread_users(message.channel.id)
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
async def test_get_applications_detectable(client, message):
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
    Returns the difference between the predefined and the requestable voice regions.
    
    Note, this command should be called only once to yield the new regions.
    """
    old_ones = set(VoiceRegion.INSTANCES.values())
    await client.voice_regions()
    new_ones = set(VoiceRegion.INSTANCES.values())
    
    difference = new_ones - old_ones
    if not difference:
        embeds = [Embed(description='*There are no new voice regions added*')]
    else:
        embeds = [Embed(description=(
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
    
    invites = await client.invite_get_guild(guild)
    embeds = [Embed('Invites', chunk) for chunk in pchunkify(invites)]
    await Pagination(client, message.channel, embeds)

@TEST_COMMANDS(separator=',')
async def autohelp_singles(client, message, name:str, user:'user', *words):
    pass

@TEST_COMMANDS(aliases=['autohelp-defaulted-alt'])
async def autohelp_defaulted(client, message, name:str=None, channel:ChannelText=None, rest=None):
    pass

@TEST_COMMANDS(separator=('[', ']'))
async def autohelp_multy(client, message, value:(int, str), user:(User, 'invite'), *cakes:(ChannelText, 'tdelta')):
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
            content_lines.append(f'{x}.: {emoji:e}')
        
        truncated = len(emojis)-20
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
async def avatar_1(client, message, user: FlaggedAnnotation('user', ConverterFlag.user_all) = None):
    if user is None:
        user = message.author
    
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)

@TEST_COMMANDS
async def what_is_it_1(client, message, entity: ('user', 'channel', 'role') = None):
    if entity is None:
        result = 'Nothing is recognized.'
    elif isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, ChannelBase):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)


@TEST_COMMANDS
async def what_is_it_2(client, message, entity: (
        FlaggedAnnotation('user', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('channel', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('role', ConverterFlag().update_by_keys(name=True)),
            ) = None):
    
    if entity is None:
        result = 'Nothing is recognized.'
    elif isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, ChannelBase):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS
async def avatar_2(client, message, user: Converter('user', ConverterFlag.user_all, default=None)):
    if user is None:
        user = message.author
    
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)

@TEST_COMMANDS
async def avatar_3(client, message, user: Converter('user', ConverterFlag.user_all, default_code='message.author')):
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)

async def what_is_it_parser_failure_handler(client, message, command, content, args):
    await client.message_create(message.channel, f'Please give the name of a user, role or of a channel.')

@TEST_COMMANDS(parser_failure_handler=what_is_it_parser_failure_handler)
async def what_is_it_2(client, message, entity: (
        FlaggedAnnotation('user', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('channel', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('role', ConverterFlag().update_by_keys(name=True)),
            )):
    
    if isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, ChannelBase):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)

@TEST_COMMANDS(checks=[checks.owner_only()])
async def owner_1(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')

# Note, this will be never called, because the category has a check already.
async def owner_only_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the bot to use the `{command}` command.')

@TEST_COMMANDS(checks=[checks.owner_only(handler=owner_only_handler)])
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
    
    before = time_to_id(datetime(2020, 2, 1))
    
    while True:
        messages = await client.message_logs(target_channel, before=before)
        if not messages:
            break
        
        for message in messages:
            user = message.author
            if user.id in (KOISHI_ID, SATORI_ID, MARISA_ID):
                OWNED += 1
            else:
                COUNTER += 1
            
        before = messages[-1].id
    
    PARARELLISM = 3
    RESET = 120
    LIMIT = 30
    DELAY = 0.1
    
    times, remainder = divmod(COUNTER, PARARELLISM*LIMIT)
    
    DURATION = DELAY + times*(RESET+DELAY)
    
    if remainder:
        DURATION += DELAY + DELAY*remainder/PARARELLISM
    else:
        DURATION -= RESET
        DURATION += LIMIT*DELAY/PARARELLISM
    
    await client.message_create(target_channel, f'Total messages: {COUNTER+OWNED}.\nEstimated duration {DURATION:.2f}')

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
    await client.message_create(message.channel, repr(end-start))


@TEST_COMMANDS
async def test_2_attachments(client, message):
    """
    Sends a message with 2 attachments.
    """
    with await ReuAsyncIO(os.path.join(KOISHI_PATH, 'images', '0000001E_yakumo_yukari_chen.gif')) as file1:
        with await ReuAsyncIO(os.path.join(KOISHI_PATH, 'images', '0000001F_yuri_hug.gif')) as file2:
            await client.message_create(message.channel, file=[file1, file2])

@TEST_COMMANDS
async def test_webhook_message_edit_0(client, message):
    """
    Creates a message with a webhook, then edits it's content out with `None`.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None)

@TEST_COMMANDS
async def test_webhook_message_edit_1(client, message):
    """
    Creates a message with a webhook, then edits it's content with `'ayaya''`.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, 'ayaya')

@TEST_COMMANDS
async def test_webhook_message_edit_2(client, message):
    """
    Creates a message with a webhook, then edits it's content out and changing sending it's embeds.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None, embed=Embed('cake'))

@TEST_COMMANDS
async def test_webhook_message_edit_3(client, message):
    """
    Creates a message with a webhook, then edits it's embeds out.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
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
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None)

@TEST_COMMANDS
async def test_webhook_message_edit_5(client, message):
    """
    Creates a message with a webhook, then edits it to empty.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
        
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, None, None)

@TEST_COMMANDS
async def test_webhook_message_edit_6(client, message):
    """
    Creates a message with a webhook, then removes it's embeds with `None`.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
    
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'testing', embed=Embed('cake'), wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, embed=None)

@TEST_COMMANDS
async def test_webhook_message_delete(client, message):
    """
    Creates a message with a webhook, then deletes it.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
    
    else:
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
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
    
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, message.author.mention, allowed_mentions=None, wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, allowed_mentions=None,)

@TEST_COMMANDS
async def test_webhook_message_edit_8(client, message):
    """
    Creates a message with a webhook, then edits it to the same value.
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
    
    else:
        executor_webhook = await client.webhook_create(channel, 'testing')
    
    new_message = await client.webhook_message_create(executor_webhook, 'ayaya', wait=True)
    await client.webhook_message_edit(executor_webhook, new_message, 'ayaya')

@TEST_COMMANDS
async def test_webhook_message_edit_9(client, message):
    """
    Creates a message with a webhook, then edits it to the same value. (embed version)
    """
    channel = message.channel
    webhooks = await client.webhook_get_channel(channel)
    for webhook in webhooks:
        if webhook.type is WebhookType.bot:
            executor_webhook = webhook
            break
    
    else:
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
    
    await client.guild_sync_roles(guild)
    
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
