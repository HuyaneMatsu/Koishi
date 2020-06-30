import json
from time import perf_counter
from random import random

from hata import eventlist, Future, RATELIMIT_GROUPS, future_or_timeout, Embed, cchunkify, WaitTillAll, User, \
    titledstr, multidict_titled, random_id, WebhookType, sleep, chunkify, ICON_TYPE_NONE, Webhook
from hata.backend.hdrs import AUTHORIZATION
from hata.ext.commands import Command, ChooseMenu, checks, Pagination
from hata.discord.others import Discord_hdrs
from hata.discord.http import API_ENDPOINT, CONTENT_TYPE
from hata.discord.parsers import PARSERS

TEST_COMMANDS=eventlist(type_=Command, category='TEST COMMANDS',)

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
async def test_webhook_response_with_url(client, message, url:'rest'):
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
async def test_webhook_response_avatar_url(client, message, avatar_url:'rest'):
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
async def test_webhook_response_avatar_url_nowait(client, message, avatar_url:'rest'):
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
