from datetime import datetime, timedelta
from random import random, choice
from time import perf_counter

from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

from hata import Client, Embed, parse_emoji, sleep, id_to_time, DATETIME_FORMAT_CODE, elapsed_time, DiscordException, \
    ERROR_CODES, Role
from hata.ext.slash import configure_parameter, InteractionResponse, abort, set_permission

from bot_utils.shared import GUILD__NEKO_DUNGEON as TEST_GUILD, ROLE__NEKO_DUNGEON__MODERATOR
MODERATOR_ROLE_ID = ROLE__NEKO_DUNGEON__MODERATOR.id

Nitori: Client


# command start perms

@Nitori.interactions(guild=TEST_GUILD, show_for_invoking_user_only=True)
async def perms(event):
    """Shows your permissions."""
    user_permissions = event.user_permissions
    if user_permissions:
        content = '\n'.join(permission_name.replace('_', '-') for permission_name in user_permissions)
    else:
        content = '*none*'
    
    return content

# command end
# command start cookie

@Nitori.interactions(guild=TEST_GUILD)
async def cookie(event,
        user : ('user', 'To who?'),
            ):
    """Gifts a cookie!"""
    return Embed(description=f'{event.user:f} just gifted a cookie to {user:f} !')

# command end
# command start show-emoji

@Nitori.interactions(guild=TEST_GUILD)
@configure_parameter('emoji', str, 'Yes?')
async def show_emoji(emoji):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji)
    if emoji is None:
        return 'That\'s not an emoji.'
    
    if emoji.is_unicode_emoji():
        return 'That\' an unicode emoji, cannot link it.'
    
    return f'**Name:** {emoji:e} **Link:** {emoji.url}'

# command end
# command start guild-icon

GUILD_ICON_CHOICES = [
    ('Icon'             , 'icon'             ),
    ('Banner'           , 'banner'           ),
    ('Discovery-splash' , 'discovery_splash' ),
    ('Invite-splash'    , 'invite_splash'    ),
]

@Nitori.interactions(guild=TEST_GUILD)
async def guild_icon(event,
        choice: (GUILD_ICON_CHOICES, 'Which icon of the guild?' ) = 'icon',
            ):
    """Shows the guild's icon."""
    guild = event.guild
    if (guild is None) or guild.partial:
        return Embed('Error', 'The command unavailable in guilds, where the application\'s bot is not in.')
    
    if choice == 'icon':
        name = 'icon'
        url = guild.icon_url_as(size=4096)
        hash_value = guild.icon_hash
    elif choice == 'banner':
        name = 'banner'
        url = guild.banner_url_as(size=4096)
        hash_value = guild.banner_hash
    elif choice == 'discovery_splash':
        name = 'discovery splash'
        url = guild.discovery_splash_url_as(size=4096)
        hash_value = guild.discovery_splash_hash
    else:
        name = 'invite splash'
        url = guild.invite_splash_url_as(size=4096)
        hash_value = guild.invite_splash_hash
    
    if url is None:
        color = (event.id>>22)&0xFFFFFF
        return Embed(f'{guild.name} has no {name}', color=color)
    
    color = hash_value&0xFFFFFF
    return Embed(f'{guild.name}\'s {name}', color=color, url=url).add_image(url)

# command end
# command start roll

@Nitori.interactions(guild=TEST_GUILD)
async def roll(
        dice_count: (range(1, 7), 'With how much dice do you wanna roll?') = 1,
            ):
    """Rolls with dices."""
    amount = 0
    for _ in range(dice_count):
        amount += round(1.+(random()*5.))
    
    return str(amount)

# command end
# command start id-to-time

@Nitori.interactions(guild=TEST_GUILD)
async def id_to_time_(
        snowflake : ('int', 'Id please!'),
            ):
    """Converts the given Discord snowflake id to time."""
    time = id_to_time(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'

# command end
# command start pat
# command start hug
# command start lick
# command start slap

class Action:
    __slots__ = ('action_name', 'embed_color', )
    def __init__(self, action_name, embed_color):
        self.action_name = action_name
        self.embed_color = embed_color
    
    async def __call__(self, client, event,
            user : ('user', 'Who?') = None,
                ):
        if user is None:
            source_user = client
            target_user = event.user
        else:
            source_user = event.user
            target_user = user
        
        return Embed(description=f'{source_user:f} {self.action_name}s {target_user:f} !', color=self.embed_color)

for action_name, embed_color in (('pat', 0x325b34), ('hug', 0xa4b51b), ('lick', 0x7840c3), ('slap', 0xdff1dc),):
    Nitori.interactions(Action(action_name, embed_color),
        name = action_name,
        description = f'Do you want some {action_name}s, or to {action_name} someone?',
        guild = TEST_GUILD,
    )

# command end
# command start repeat

@Nitori.interactions(guild=TEST_GUILD)
async def repeat(
        text : ('str', 'The content to repeat')
            ):
    """What should I exactly repeat?"""
    if not text:
        text = 'nothing to repeat'
    
    return InteractionResponse(text, allowed_mentions=None)

# command end
# command start improvise

IMPROVISATION_CHOICES = [
    'Did Marisa really adopt Reimu?',
    'Yuuka beat Goku.',
    'Marisa! You know what you did!',
    'Thick cucumber Nitori',
    'Nitori Kappashiro',
    'Suwako\'s secret family technique is so lovely.',
    'Reimu\'s armpits, yeeaaa...',
    'Have you heard of Izaoyi love-shop?',
    'Marisa\'s underskirt shrooms are poggers'
]

@Nitori.interactions(guild=TEST_GUILD)
async def improvise():
    """Improvises some derpage"""
    yield '*Thinks*'
    await sleep(1.0+random()*4.0)
    yield choice(IMPROVISATION_CHOICES)

# command end
# command start collect-reactions

@Nitori.interactions(guild=TEST_GUILD)
async def collect_reactions():
    """Collects reactions"""
    message = yield InteractionResponse('Collecting reactions for 1 minute!')
    await sleep(60.0)
    
    reactions = message.reactions
    if reactions:
        emojis = list(reactions)
        # Limit reactions to 16 to avoid error from Discord
        del emojis[16:]
        
        yield ' '.join(emoji.as_emoji for emoji in emojis)
    else:
        yield 'No reactions were collected.'

# command end
# command start text-cat
# command start why

NEKO_LIFE = 'https://nekos.life/api/v2'

async def get_neko_life(client, keyword):
    yield
    url = f'{NEKO_LIFE}/{keyword}'
    
    async with client.http.get(url) as response:
        if response.status == 200:
            data = await response.json()
            content = data[keyword]
        else:
            content = 'Couldn\'t contact the API right now... OwO'
    
    yield content

# command end
# command start text-cat

@Nitori.interactions(guild=TEST_GUILD)
async def text_cat(client):
    """I will send text cats :3"""
    return get_neko_life(client, 'cat')

# command end
# command start why

@Nitori.interactions(guild=TEST_GUILD)
async def why(client):
    """why are you using this commands?"""
    yield get_neko_life(client, 'why')

# command end
# command start is-banned

@Nitori.interactions(guild=TEST_GUILD)
async def is_banned(client, event,
        user: ('user', 'Who should I check?')
            ):
    """Checks whether the user is banned."""
    if not event.user_permissions.can_ban_users:
        abort('You need to have `ban users` permissions to do this.')
    
    if not event.channel.cached_permissions_for(client).can_ban_users:
        abort('I need to have `ban users` permissions to do this.')
    
    yield # Acknowledge the event.
    
    try:
        ban_entry = await client.guild_ban_get(event.guild, user)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_ban:
            ban_entry = None
        else:
            raise
    
    embed = Embed(f'Ban entry for {user:f}').add_thumbnail(user.avatar_url)
    
    if ban_entry is None:
        embed.description = 'The user **NOT YET** banned.'
    
    else:
        embed.description = 'The user is banned.'
        
        reason = ban_entry.reason
        if reason is None:
            reason = '*No reason was specified.*'
        
        embed.add_field('Reason:', reason)
    
    yield embed

# command end
# command start user

@Nitori.interactions(guild=TEST_GUILD)
async def user_id(event,
        user_id: ('user_id', 'Get the id of an other user?', 'user') = None,
            ):
    """Shows your or the selected user's id."""
    if user_id is None:
        user_id = event.user.id
    
    return str(user_id)

# command end
# command start latest-users

MODERATOR_ROLE = Role.precreate(MODERATOR_ROLE_ID)

@Nitori.interactions(guild=TEST_GUILD, allow_by_default=False)
@set_permission(TEST_GUILD, MODERATOR_ROLE, True)
async def latest_users(event):
    """Shows the new users of the guild."""
    date_limit = datetime.now() - timedelta(days=7)
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        # `joined_at` might be set as `None` if the user is a lurker.
        # We can ignore lurkers, so use `created_at` which defaults to Discord epoch.
        created_at = user.guild_profiles[guild].created_at
        if created_at > date_limit:
            users.append((created_at, user))
    
    users.sort(reverse=True)
    del users[10:]
    
    embed = Embed('Recently joined users')
    if users:
        for index, (joined_at, user) in enumerate(users, 1):
            created_at = user.created_at
            embed.add_field(
                f'{index}. {user.full_name}',
                f'Id: {user.id}\n'
                f'Mention: {user.mention}\n'
                '\n'
                f'Joined : {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]\n'
                f'Created : {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
                f'Difference : {elapsed_time(relativedelta(created_at, joined_at))}',
            )
    
    else:
        embed.description = '*none*'
    
    return InteractionResponse(embed=embed, allowed_mentions=None)

# command start ping

@Nitori.interactions(guild=TEST_GUILD)
async def ping():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'

# command end
# command start enable-ping

@Nitori.interactions(is_global=True)
async def enable_ping(client, event,
        allow: ('bool', 'Enable?')=True,
            ):
    """Enables the ping command in your guild."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if not event.user_permissions.can_administrator:
        abort('You must have administrator permission to use this command.')
    
    application_commands = await client.application_command_guild_get_all(guild)
    for application_command in application_commands:
        # If you are not working with overlapping names, a name check should be enough.
        if application_command.name == ping.name:
            command_present = True
            break
    else:
        command_present = False
    
    if allow:
        if command_present:
            content = 'The command is already present.'
        else:
            await client.application_command_guild_create(guild, ping.get_schema())
            content = 'The command has been added.'
    else:
        if command_present:
            await client.application_command_guild_delete(guild, application_command)
            content = 'The command has been disabled.'
        else:
            content = 'The command is not present.'
    
    return Embed('Success', content)

# command end
# command start scarlet

# `bs4` requires `lxml` library or you will get an error.

# You might wanna add `-tag`-s to surely avoid nsfw pictures
SAFE_BOORU = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='

# Use a cache to avoid repeated requests.
# Booru also might ban ban you for a time if you do too much requests.
IMAGE_URL_CACHE = {}

async def get_image_embed(client, tags, name, color):
    image_urls = IMAGE_URL_CACHE.get(tags, None)
    if image_urls is None:
        
        # Request image information
        async with client.http.get(SAFE_BOORU+tags) as response:
            if response.status != 200:
                return Embed('Error', 'Safe-booru unavailable', color=color)
            
            result = await response.read()
        
        # Read response and get image urls.
        soup = BeautifulSoup(result, 'lxml')
        image_urls = [post['file_url'] for post in soup.find_all('post')]
        
        if not image_urls:
            return Embed('Error', 'No images found.\nPlease try again later.', color=color)
        
        # If we received image urls, cache them
        IMAGE_URL_CACHE[tags] = image_urls
    
    image_url = choice(image_urls)
    return Embed(name, color=color, url=image_url).add_image(image_url)


SCARLET = Nitori.interactions(None, name='scarlet', description='Scarlet?', guild=TEST_GUILD)

@SCARLET.interactions(is_default=True, show_for_invoking_user_only=True)
async def devil(client, event):
    """Flandre & Remilia!"""
    return get_image_embed(client, 'flandre_scarlet+remilia_scarlet', 'Scarlet Flandre & Remilia', 0xa12a2a)

@SCARLET.interactions
async def flandre(client):
    """Flandre!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'flandre_scarlet', 'Scarlet Flandre', 0xdc143c)

@SCARLET.interactions
async def remilia(client):
    """Remilia!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'remilia_scarlet', 'Scarlet Remilia', 0x9400d3)

# command end
# command start about

@Nitori.interactions(is_global=True)
async def about(client):
    return Embed('about', client.application.description, color=0x508CB5).add_thumbnail(client.avatar_url)

# command end

def collect_commands():
    with open(__file__, 'r') as file:
        lines = file.read().splitlines()
    
    collected_lines_per_command = {}
    command_names = []
    
    for line in lines:
        if line.startswith('# command '):
            if line[len('# command '):] == 'end':
                command_names.clear()
                continue
            
            if line[len('# command '):len('# command ')+len('start ')] == 'start ':
                command_name = line[len('# command ')+len('start '):]
                command_names.append(command_name)
                continue
            
            continue
        
        line = line.rstrip()
        
        for command_name in command_names:
            try:
                command_lines = collected_lines_per_command[command_name]
            except KeyError:
                command_lines = []
                collected_lines_per_command[command_name] = command_lines
            
            command_lines.append(line)
    
    
    for command_lines in collected_lines_per_command.values():
        while command_lines:
            if command_lines[-1]:
                break
            
            del command_lines[-1]
        
        while command_lines:
            if command_lines[0]:
                break
            
            del command_lines[0]
    
    collective_command_lines_per_command = {}
    for command_name, command_lines in collected_lines_per_command.items():
        if command_lines:
            command_lines.insert(0, '```py')
            command_lines.append('```')
            collective_command_lines_per_command[command_name] = '\n'.join(command_lines)
    
    return collective_command_lines_per_command


COMMAND_CONTENTS = collect_commands()


SOURCE = Nitori.interactions(None,
    name = 'source',
    description ='The collective commands of Nitori.',
    guild=TEST_GUILD,
)

@SOURCE.interactions
async def slash_(
        command: (sorted(COMMAND_CONTENTS), 'Select a slash command to show')
            ):
    
    return COMMAND_CONTENTS[command]







