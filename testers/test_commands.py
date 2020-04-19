import json
from time import perf_counter

from hata import eventlist, Future, RATELIMIT_GROUPS, future_or_timeout, Embed, cchunkify, WaitTillAll, User
from hata.ext.commands import Command, ChooseMenu, checks, Pagination

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


