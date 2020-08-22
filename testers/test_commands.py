import json
from time import perf_counter
from random import random

from hata import eventlist, Future, RATELIMIT_GROUPS, future_or_timeout, Embed, cchunkify, WaitTillAll, User, sleep, \
    titledstr, multidict_titled, random_id, WebhookType, chunkify, ICON_TYPE_NONE, Webhook, KOKORO, DiscordEntity, \
    IconSlot, CHANNELS, ChannelText, VoiceRegion

from hata.discord.http import URLS
from hata.backend.hdrs import AUTHORIZATION
from hata.ext.commands import Command, ChooseMenu, checks, Pagination, Converter, ConverterFlag
from hata.discord.others import Discord_hdrs
from hata.discord.http import API_ENDPOINT, CONTENT_TYPE
from hata.discord.parsers import PARSERS
from hata.ext.prettyprint import pchunkify
from hata.discord.emoji import PartialEmoji
from hata.ext.patchouli import map_module, MAPPED_OBJECTS

TEST_COMMANDS = eventlist(type_=Command, category='TEST COMMANDS',)

map_module('hata')

def setup(lib):
    Koishi.commands.extend(TEST_COMMANDS)
    
def teardown(lib):
    Koishi.commands.unextend(TEST_COMMANDS)

@TEST_COMMANDS
async def test_choose_menu_repr(client, message):
    '''
    Creates a ChooseMenu and returns it's repr.
    '''
    choices = ['nice', 'cat']
    choose_menu = await ChooseMenu(client, message.channel, choices, lambda *args:Future(client.loop))
    await client.message_create(message.channel,repr(choose_menu))

@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_role_create(client, message):
    '''
    Creates and deletes a role.
    '''
    guild = message.guild
    role = await client.role_create(guild,'Mokou')
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
    
    proxy = client.get_ratelimits_of(RATELIMIT_GROUPS.role_edit,limiter = guild)
    if (not proxy.is_alive()) or (not proxy.has_size_set()):
        if not guild.cached_permissions_for(client).can_manage_roles:
            await client.message_create(message.channel, 'Current state unknown -> No permissions.')
            return
        
        roles = message.guild.roles
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
    await Pagination(client,message.channel,[Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())])

@TEST_COMMANDS
async def test_100_messages(client, message):
    '''
    Sends 100 messages, like a boss!
    '''
    tasks = []
    for x in range(100):
        task = client.loop.create_task(client.message_create(message.channel,repr(x)))
        tasks.append(task)
    
    start = perf_counter()
    await WaitTillAll(tasks,client.loop)
    end = perf_counter()
    
    await client.message_create(message.channel,repr(end-start))

@TEST_COMMANDS
async def crosspost(client, message, message_id:int):
    '''
    Crossposts, pls pass a mssage id from the current channel!
    '''
    to_message = await client.message_get(message.channel,message_id)
    await client.message_crosspost(to_message)
    
    await client.message_create(message.channel, 'success')

@TEST_COMMANDS
async def get_guild(client, message):
    '''
    Gets the current guild.
    '''
    guild = message.guild
    if guild is None:
        await client.message_create(message.channel,'Please use this command at a guild.')
    
    data = await client.http.guild_get(guild.id)
    await Pagination(client,message.channel,[Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())])

@TEST_COMMANDS
async def test_new_discord_headers(client, message):
    '''
    Checks whether Discord ignores header casing.
    '''
    headers = multidict_titled()
    headers[AUTHORIZATION] = f'Bot {client.token}' if client.is_bot else client.token
    headers[CONTENT_TYPE]='application/json'
    
    precision = str.__new__(titledstr,Discord_hdrs.RATELIMIT_PRECISION.lower())
    headers[precision]='millisecond'
    
    async with client.http.request('POST', f'{API_ENDPOINT}/channels/{message.channel.id}/messages',data='{"content":"testing"}', headers=headers) as response:
        result = response.headers[Discord_hdrs.RATELIMIT_RESET_AFTER]
    
    await client.message_create(message.channel, f'If float, ignored: {result}')

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
    original_webhook_send = http_type.webhook_send
    
    async def replace_webhook_send(client, *args):
        data = await original_webhook_send(client, *args)
        if (data is not None) and (data.get('content') == content):
            result[0] = str(data)
        return data
    
    http_type.webhook_send = replace_webhook_send
    
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
    
    message = await client.webhook_send(executor_webhook,content,avatar_url=avatar_url, wait=True)
    
    http_type.webhook_send = original_webhook_send
    
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
    original_webhook_send = http_type.webhook_send
    
    async def replace_webhook_send(client, *args):
        data = await original_webhook_send(client, *args)
        if data.get('content') == content:
            result[0] = str(data)
        return data
    
    http_type.webhook_send = replace_webhook_send
    
    source_MESSAGE_CREATE = PARSERS['MESSAGE_CREATE']
    
    def replace_MESSAGE_CREATE(client, data):
        if data.get('content') == content:
            result.append(str(data))
        
        return source_MESSAGE_CREATE(client, data)
    
    PARSERS['MESSAGE_CREATE'] = replace_MESSAGE_CREATE
    
    executor_webhook = Webhook.from_url(url)
    
    message = await client.webhook_send(executor_webhook, content, wait=True)
    
    http_type.webhook_send = original_webhook_send
    
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
    original_webhook_send = http_type.webhook_send
    
    async def replace_webhook_send(client, *args):
        data = await original_webhook_send(client, *args)
        if (data is not None) and (data.get('content') == content):
            result[0] = str(data)
        return data
    
    http_type.webhook_send = replace_webhook_send
    
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
    
    message = await client.webhook_send(executor_webhook,content,avatar_url=avatar_url, wait=True)
    
    http_type.webhook_send = original_webhook_send
    
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
    
    message = await client.webhook_send(executor_webhook,content,avatar_url=avatar_url, wait=False)
    
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
    
    integrations = await client.integration_get_all(guild, include_applications=True)
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
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_start_channel_thread(client, message):
    """
    Does a post request to the channel's threads.
    """
    data = await client.http.channel_thread_start(message.channel.id, None)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())]
    await Pagination(client,message.channel, pages)

# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_get_channel_thread_users(client, message):
    """
    Gets the channel's threads' users probably, no clue.
    """
    data = await client.http.thread_users(message.channel.id)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())]
    await Pagination(client,message.channel, pages)

# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_add_channel_thread_user(client, message):
    """
    Adds you to the channel's threads.
    """
    data = await client.http.thread_user_add(message.channel.id, message.author.id)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())]
    await Pagination(client,message.channel, pages)

# DiscordException Not Found (404): 404: Not Found
@TEST_COMMANDS(checks=[checks.guild_only()])
async def test_delete_channel_thread_user(client, message):
    """
    Deletes you to the channel's threads.
    """
    data = await client.http.thread_user_delete(message.channel.id, message.author.id)
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())]
    await Pagination(client,message.channel, pages)

@TEST_COMMANDS
async def test_get_applications_detectable(client, message):
    """
    Requests the detectable applications.
    """
    data = await client.http.applications_detectable()
    
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())]
    await Pagination(client,message.channel, pages)

@TEST_COMMANDS
async def test_get_eula(client, message):
    """
    Gets an eula.
    """
    data = await client.http.eula_get(542074049984200704)
    
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_render_application(client, message):
    """
    Renders the client's application.
    """
    pages = [Embed(description=chunk) for chunk in pchunkify(client.application)]
    await Pagination(client,message.channel, pages)

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
    
    pages = [Embed(description=chunk) for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())]
    await Pagination(client, message.channel, pages)

@TEST_COMMANDS
async def test_regions(client, message):
    old_ones = set(VoiceRegion.INSTANCES.values())
    await client.voice_regions()
    new_ones = set(VoiceRegion.INSTANCES.values())
    print(new_ones)
    difference = new_ones - old_ones
    if not difference:
        embeds = [Embed(description='*There are no new voice regions added*')]
    else:
        embeds = [Embed(description=(
            f'Voice region : {region.name!r}\n'
            f'id : {region.id!r}\n'
            f'vip : {region.vip!r}\n'
            f'deprecated : {region.deprecated!r}\n'
            f'custom : {region.custom!r}'
                )) for region in difference]
    
    await Pagination(client, message.channel, embeds)
