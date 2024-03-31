__all__ = ('Nitori',)

import functools, re
from enum import Enum
from random import choice, random
from time import perf_counter

from bs4 import BeautifulSoup
from hata import (
    BUILTIN_EMOJIS, Channel, Client, DATETIME_FORMAT_CODE, DiscordException, ERROR_CODES, Embed, Emoji, IntentFlag,
    Permission, Role, elapsed_time, id_to_datetime, parse_emoji
)
from hata.ext.slash import (
    Button, ButtonStyle, Form, InteractionResponse, Option, P, Row, Select, TextInput, TextInputStyle, abort,
    configure_parameter, iter_component_interactions, wait_for_component_interaction
)
from scarletio import sleep

import config

from ..bot_utils.constants import GUILD__SUPPORT as TEST_GUILD, ROLE__SUPPORT__MODERATOR
from ..bot_utils.utils import random_error_message_getter


Nitori = Client(
    config.NITORI_TOKEN,
    client_id = config.NITORI_ID,
    application_id = config.NITORI_ID,
    extensions = 'slash',
    random_error_message_getter = random_error_message_getter,
)


MODERATOR_ROLE_ID = ROLE__SUPPORT__MODERATOR.id


# command start slash perms

@Nitori.interactions(guild = TEST_GUILD, show_for_invoking_user_only = True)
async def perms(event):
    """Shows your permissions."""
    user_permissions = event.user_permissions
    if user_permissions:
        content = '\n'.join(permission_name.replace('_', '-') for permission_name in user_permissions)
    else:
        content = '*none*'
    
    return content

# command end
# command start slash cookie

@Nitori.interactions(guild = TEST_GUILD)
async def cookie(
    event,
    user: ('user', 'To who?'),
):
    """Gifts a cookie!"""
    return Embed(description = f'{event.user:f} just gifted a cookie to {user:f} !')

# command end
# command start slash cake

CAKES = [
    'https://tenor.com/view/chocolate-cake-candles-gif-15613028',
    'https://tenor.com/view/cake-yummy-hungry-eating-birthday-cake-gif-18507935',
    'https://tenor.com/view/cake-fat-slice-gif-4931308',
]

@Nitori.interactions(guild = TEST_GUILD)
async def cake(event,
    user: P('user', 'To who?'),
):
    """Gifts a cake!"""
    return Embed(description = f'{event.user:f} just gifted a cookie to {user:f} !').add_image(choice(CAKES))

# command end
# command start slash cola

@Nitori.interactions(guild = TEST_GUILD)
async def cola(
    client,
    event,
    user: ('user', 'To who?') = None,
):
    """Gifts a bottle of cola!"""
    if user is None:
        source_user = client
        target_user = event.user
    else:
        source_user = event.user
        target_user = user
    
    return Embed(description = f'{source_user:f} just gifted a bottle of cola to {target_user:f} !')

# command end
# command start slash guild-icon

GUILD_ICON_CHOICES = [
    ('Icon'             , 'icon'             ),
    ('Banner'           , 'banner'           ),
    ('Discovery-splash' , 'discovery_splash' ),
    ('Invite-splash'    , 'invite_splash'    ),
]

@Nitori.interactions(guild = TEST_GUILD)
async def guild_icon(
    event,
    choice: (GUILD_ICON_CHOICES, 'Which icon of the guild?' ) = 'icon',
):
    """Shows the guild's icon."""
    guild = event.guild
    if (guild is None) or guild.partial:
        return Embed('Error', 'The command unavailable in guilds, where the application\'s bot is not in.')
    
    if choice == 'icon':
        name = 'icon'
        url = guild.icon_url_as(size = 4096)
        hash_value = guild.icon_hash
    
    elif choice == 'banner':
        name = 'banner'
        url = guild.banner_url_as(size = 4096)
        hash_value = guild.banner_hash
    
    elif choice == 'discovery_splash':
        name = 'discovery splash'
        url = guild.discovery_splash_url_as(size = 4096)
        hash_value = guild.discovery_splash_hash
    
    else:
        name = 'invite splash'
        url = guild.invite_splash_url_as(size = 4096)
        hash_value = guild.invite_splash_hash
    
    if url is None:
        color = (event.id >> 22) & 0xFFFFFF
        return Embed(f'{guild.name} has no {name}', color = color)
    
    color = hash_value & 0xFFFFFF
    return Embed(f'{guild.name}\'s {name}', color = color, url = url).add_image(url)

# command end
# command start slash roll

@Nitori.interactions(guild = TEST_GUILD)
async def roll(
    dice_count: (range(1, 7), 'With how much dice do you wanna roll?') = 1,
):
    """Rolls with dices."""
    amount = 0
    for _ in range(dice_count):
        amount += round(1.0 + (random() * 5.0))
    
    return str(amount)

# command end
# command start slash pet-info

class PetInfoFieldType(Enum):
    all = 'all'
    starve = 'hunger'
    love = 'love'
    energy = 'energy'


def create_pet_info_field(field, user):
     return f'**{field.value}**: {(user.id >> (22 + len(field.value))) % 101}'


@Nitori.interactions(guild = TEST_GUILD)
async def pet_info(client, event, field: PetInfoFieldType = PetInfoFieldType.all):
    user = event.user
    
    if field == PetInfoFieldType.all:
        description = '\n'.join(
            create_pet_info_field(field, user) for field in PetInfoFieldType
            if field != PetInfoFieldType.all
        )
    
    else:
        description = create_pet_info_field(field, user)
    
    
    return Embed(
        f'{event.user}\'s pet info',
        description,
    )

# command end
# command start slash id-to-time

@Nitori.interactions(guild = TEST_GUILD)
async def id_to_datetime_(
    snowflake: ('int', 'Id please!'),
):
    """Converts the given Discord snowflake to time."""
    time = id_to_datetime(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'

# command end
# command start slash pat
# command start slash hug
# command start slash lick
# command start slash slap

class Action:
    __slots__ = ('action_name', 'embed_color', )
    def __init__(self, action_name, embed_color):
        self.action_name = action_name
        self.embed_color = embed_color
    
    async def __call__(self, client, event,
        user: ('user', 'Who?') = None,
    ):
        if user is None:
            source_user = client
            target_user = event.user
        else:
            source_user = event.user
            target_user = user
        
        return Embed(description = f'{source_user:f} {self.action_name}s {target_user:f} !', color = self.embed_color)

for action_name, embed_color in (('pat', 0x325b34), ('hug', 0xa4b51b), ('lick', 0x7840c3), ('slap', 0xdff1dc),):
    Nitori.interactions(Action(action_name, embed_color),
        name = action_name,
        description = f'Do you want some {action_name}s, or to {action_name} someone?',
        guild = TEST_GUILD,
    )

# command end
# command start slash repeat

@Nitori.interactions(guild = TEST_GUILD)
async def repeat(
    text: ('str', 'The content to repeat')
):
    """What should I exactly repeat?"""
    if not text:
        text = 'nothing to repeat'
    
    return InteractionResponse(text, allowed_mentions = None)

# command end
# command start slash channel-create

@Nitori.interactions(guild = TEST_GUILD, required_permissions = Permission().update_by_keys(manage_channels = True))
async def channel_create(
    client, event, name: (str, 'The channel\'s name to create.')
):
    """Creates a channel"""
    
    name_length = len(name)
    if (name_length < 2) or (name_length > 32):
        return 'Please keep name length between 2 and 32 characters.'
    
    try:
        await client.channel_create(event.guild, name, parent = event.channel.parent)
    except DiscordException as err:
        # Error message can be over 2k length
        reason = str(err)
        if len(reason) > 1900:
            reason = reason[:1900] + '...'
        
        return f'Creating channel failed:\n{reason}'
    
    return 'Successfully created the channel.'

# command end
# command start slash improvise

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

@Nitori.interactions(guild = TEST_GUILD)
async def improvise():
    """Improvises some derpage"""
    yield '*Thinks*'
    await sleep(1.0 + random() * 4.0)
    yield choice(IMPROVISATION_CHOICES)

# command end
# command start slash resend

@Nitori.interactions(guild = TEST_GUILD)
async def resend(
    client,
    attachment: ('attachment', 'File!'),
):
    yield
    file = await client.download_attachment(attachment)
    yield InteractionResponse(file = (attachment.name, file))

# command end
# command start slash collect-reactions

@Nitori.interactions(guild = TEST_GUILD)
async def collect_reactions():
    """Collects reactions"""
    message = yield InteractionResponse('Collecting reactions for 1 minute!')
    await sleep(60.0)
    
    reactions = message.reactions
    if (reactions is not None) and reactions:
        emojis = list(reactions)
        # Limit reactions to 16 to avoid error from Discord
        del emojis[16:]
        
        yield ' '.join(emoji.as_emoji for emoji in emojis)
    else:
        yield 'No reactions were collected.'

# command end
# command start slash text-cat
# command start slash why

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
# command start slash text-cat

@Nitori.interactions(guild = TEST_GUILD)
async def text_cat(client):
    """I will send text cats :3"""
    return get_neko_life(client, 'cat')

# command end
# command start slash why

@Nitori.interactions(guild = TEST_GUILD)
async def why(client):
    """why are you using this commands?"""
    yield get_neko_life(client, 'why')

# command end
# command start slash is-banned

@Nitori.interactions(guild = TEST_GUILD)
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
# command start slash user

@Nitori.interactions(guild = TEST_GUILD)
async def user_id(
    event,
    user_id: ('user_id', 'Get the id of an other user?', 'user') = None,
):
    """Shows your or the selected user's id."""
    if user_id is None:
        user_id = event.user.id
    
    return str(user_id)

# command end
# command start slash ping

@Nitori.interactions(wait_for_acknowledgement = True)
async def ping():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter() - start) * 1000.0
    
    yield f'{delay:.0f} ms'

# command end
# command start slash enable-ping

@Nitori.interactions(is_global = True)
async def enable_ping(
    client,
    event,
    allow: ('bool', 'Enable?') = True,
):
    """Enables the ping command in your guild."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if not event.user_permissions.can_administrator:
        abort('You must have administrator permission to invoke this command.')
    
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
# command start slash scarlet

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
        async with client.http.get(SAFE_BOORU + tags) as response:
            if response.status != 200:
                return Embed('Error', 'Safe-booru unavailable', color = color)
            
            result = await response.read()
        
        # Read response and get image urls.
        soup = BeautifulSoup(result, 'lxml')
        image_urls = [post['file_url'] for post in soup.find_all('post')]
        
        if not image_urls:
            return Embed('Error', 'No images found.\nPlease try again later.', color = color)
        
        # If we received image urls, cache them
        IMAGE_URL_CACHE[tags] = image_urls
    
    image_url = choice(image_urls)
    return Embed(name, color = color, url = image_url).add_image(image_url)


SCARLET = Nitori.interactions(None, name = 'scarlet', description = 'Scarlet?', guild = TEST_GUILD)

@SCARLET.interactions(is_default = True)
async def devil(client, event):
    """Flandre & Remilia!"""
    yield
    yield await get_image_embed(client, 'flandre_scarlet+remilia_scarlet', 'Scarlet Flandre & Remilia', 0xa12a2a)

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
# command start slash kaboom

@Nitori.interactions(guild = TEST_GUILD)
async def kaboom(client, event):
    """Kabooom!!"""
    await client.interaction_application_command_acknowledge(event)
    
    messages = []
    for x in reversed(range(1, 4)):
        message = await client.interaction_followup_message_create(event, x)
        messages.append(message)
        await sleep(1.0)
    
    await client.interaction_followup_message_create(event, 'KABOOM!!')
    
    for message in messages:
        await sleep(1.0)
        await client.interaction_followup_message_delete(event, message)

# command end
# command start slash kaboom-mixed

@Nitori.interactions(guild = TEST_GUILD)
async def kaboom_mixed(client, event):
    """Kabooom!!"""
    yield
    
    messages = []
    for x in reversed(range(1, 4)):
        message = yield str(x)
        messages.append(message)
        await sleep(1.0)
    
    yield 'KABOOM!!'
    
    for message in messages:
        await sleep(1.0)
        await client.interaction_followup_message_delete(event, message)

# command end
# command start slash about

@Nitori.interactions(is_global = True)
async def about(client):
    return Embed('about', client.application.description, color = 0x508CB5).add_thumbnail(client.avatar_url)

# command end
# command start slash thread-channel-name-length

@Nitori.interactions(guild = TEST_GUILD)
async def thread_channel_name_length(
    channel: ('channel_group_thread', 'Select a thread channel.')
):
    """Returns the selected thread channel's name's length."""
    return len(channel.name)

# command end
# command start slash voice-channel-name-length

from hata import ChannelType
from hata.ext.slash import P

@Nitori.interactions(guild = TEST_GUILD)
async def voice_channel_name_length(
    channel: P('channel', 'Select a voice channel', channel_types = [ChannelType.guild_voice])
):
    """Returns the selected voice channel's name's length."""
    return len(channel.name)

# command end
# command start slash character-popularity

MOST_POPULAR_TOUHOU_CHARACTERS = [
    'Konpaku Youmu',
    'Kirisame Marisa',
    'Hakurei Reimu',
    'Komeiji Koishi',
    'Scarlet Flandre',
    'Izayoi Sakuya',
    'Scarlet Remilia',
    'Fujiwara no Mokou',
    'Komeiji Satori',
    'Saigyouji Yuyuko',
    'Shameimaru Aya',
    'Margatroid Alice',
    'Kochiya Sanae',
    'Reisen Udongein Inaba',
    'Hinanawi Tenshi',
    'Yakumo Yukari',
    'Hata no Kokoro',
    'Chiruno',
    'Patchouli Knowledge',
    'Tatara Kogasa',
]

@Nitori.interactions(guild = TEST_GUILD)
async def character_popularity(
    position: P('number', 'Please select a number between 1 and 20', min_value = 1, max_value = 20)
):
    """Returns the name of the touhou character by it's popularity position."""
    return MOST_POPULAR_TOUHOU_CHARACTERS[position - 1]


# command end
# command start slash set-nick

@Nitori.interactions(
    guild = TEST_GUILD,
    required_permissions = Permission().update_by_keys(manage_nicknames = True),
)
async def set_nick(
    client,
    event,
    user: ('user', 'Who\'s?'),
    nick: P(str, 'Their new nick', min_length = 1, max_length = 32) = None,
):
    """Edit's the selected user's nick."""
    yield
    await client.user_guild_profile_edit(event.guild, user, nick = nick)
    yield f'{user:f}\'s nick has been updated'

# command end
# command start context avatar

@Nitori.interactions(guild = TEST_GUILD, target = 'user')
async def avatar(target):
    avatar_url = target.avatar_url_as(size = 4096)
    return Embed(f'{target.full_name}\'s avatar', url = avatar_url).add_image(avatar_url)

# command end
# command start context length

@Nitori.interactions(guild = TEST_GUILD, target = 'message')
async def length(target):
    return len(target)

# command end
# command start slash command-count

@Nitori.interactions(guild = TEST_GUILD)
async def command_count(client, event):
    global_command_count = client.slasher.get_global_command_count()
    
    guild_id = event.guild_id
    if guild_id:
        guild_command_count = client.slasher.get_guild_command_count(guild_id)
    else:
        guild_command_count = 0
    
    return Embed(
        f'{client.full_name}\'s command count'
    ).add_field(
        'Global',
        (
            f'```\n'
            f'{global_command_count}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Guild',
        (
            f'```\n'
            f'{guild_command_count}\n'
            f'```'
        ),
        inline = True,
    )

# command end
# command start autocomplete cake-love
# command start autocomplete pick-cake
# command start forms rate-cakes

CAKE_NAMES = [
    'butter', 'pound', 'sponge', 'genoise', 'biscuit', 'angel food', 'chiffon', 'baked flourless', 'unbaked flourless',
    'carrot', 'red velvet'
]

# command end
# command start autocomplete cake-love

EMOJI_CAKE = BUILTIN_EMOJIS['cake']



@Nitori.interactions(guild = TEST_GUILD)
async def cake_love(
    cake_name: ('str', 'Please pick a cake.')
):
    """Do I love the cake or nah?"""
    return f'Hmmm, yes, I love {cake_name} {EMOJI_CAKE} as well.'


@cake_love.autocomplete('cake_name') # Define which parameter we want to auto-complete.
async def autocomplete_cake_name(value):
    if value is None:
        return CAKE_NAMES[:25]
    
    value = value.casefold()
    return [cake_name for cake_name in CAKE_NAMES if (value in cake_name)]

# command end
# command start autocomplete pick-cake

# Define `get_one_like˙ function
def get_cake_name_like(name):
    name = name.casefold()
    
    for cake_name in CAKE_NAMES:
        if name in cake_name:
            return cake_name


# Define `get_multiple_like` function
def get_cake_names_like(name):
    name = name.casefold()
    
    return [cake_name for cake_name in CAKE_NAMES if (name in cake_name)]


@Nitori.interactions(guild = TEST_GUILD)
async def pick_cake(
    cake_name_1: ('str', 'Select a cake!'),
    cake_name_2: ('str', 'Another one.'),
    cake_name_3: ('str', 'Another one.') = None,
    cake_name_4: ('str', 'Another one.') = None,
    cake_name_5: ('str', 'Another one.') = None,
):
    """Picks a cake."""
    cakes = []
    
    for cake_name in (cake_name_1, cake_name_2, cake_name_3, cake_name_4, cake_name_5):
        if cake_name is not None:
            cake_name = get_cake_name_like(cake_name)
            if cake_name is not None:
                cakes.append(cake_name)
    
    if not cakes:
        abort('No valid choices provided.')
    
    return f'I choose: {choice(cakes)}'


@pick_cake.autocomplete('cake_name_1', 'cake_name_2', 'cake_name_3', 'cake_name_4', 'cake_name_5')
async def exclusive_autocomplete_cake_name(event, actual_cake_name):
    excluded_cake_names = set()
    
    for cake_name in event.interaction.get_non_focused_values().values():
        if cake_name is not None:
            cake_name = get_cake_name_like(cake_name)
            if cake_name is not None:
                excluded_cake_names.add(cake_name)
    
    
    if actual_cake_name is None:
        if excluded_cake_names:
            return [cake_name for cake_name in CAKE_NAMES if cake_name not in excluded_cake_names]
        
        else:
            return CAKE_NAMES[:25]
    
    else:
        cake_names = get_cake_names_like(actual_cake_name)
        if excluded_cake_names:
            return [cake_name for cake_name in cake_names if cake_name not in excluded_cake_names]
        
        else:
            return cake_names

# command end
# command start autocomplete shop


PRODUCT_TYPES = {
    'pudding': ['choco', 'dark choco', 'strawberry', 'vanilla'],
    'croissant': ['choco', 'cherry', 'hazelnut', 'strawberry', 'vanilla'],
}


def get_option_like(options, name):
    name = name.casefold()
    
    for option in options:
        if name in option:
            return option


def get_options_like(options, name):
    name = name.casefold()
    
    return [option for option in options if name in option]


@Nitori.interactions(guild = TEST_GUILD)
async def shop(
    product: ([*PRODUCT_TYPES], 'Select a product to buy.'),
    type_: ('str', 'Select a type'),
):
    """Buy some sweets."""
    type_ = get_option_like(PRODUCT_TYPES[product], type_)
    if type_ is None:
        abort('Invalid product type.')
    
    return f'You just bought a {type_} {product}'


@shop.autocomplete('type_')
async def autocomplete_product_type(event, value):
    product = event.interaction.get_value_of('product')
    if product is None:
        return
    
    options = PRODUCT_TYPES[product]
    
    if value is None:
        return options[:25]
    
    return get_options_like(options, value)

# command end
# command start autocomplete spell


SPELLS = [
    'ankle snare', 'blade of wind', 'blast', 'blessing', 'bottomless swamp', 'break spell', 'burning flash',
    'control of weather', 'create earth', 'create earth golem', 'create water', 'crystal prison', 'cursed lighting',
    'detonation', 'earthshaker', 'energy ignition', 'exorcism', 'explosion', 'fireball', 'flash', 'force fire',
    'freeze', 'freeze bind', 'freeze gust', 'heal', 'inferno', 'light of reflection', 'light of saber', 'lighting',
    'lightning strike', 'lock', 'magic canceller', 'paralyze', 'powered', 'puppet', 'purification', 'reflect',
    'resurrection', 'sacred shell', 'silent', 'sleep', 'teleport', 'tinder', 'tornado', 'turn undead', 'unlock',
    'versatile actor', 'wind breath', 'wind curtain'
]


def get_spell_or_abort(name):
    name = name.casefold()
    
    for spell in SPELLS:
        if name in spell:
            break
    
    else:
        abort('Unknown spell.')
    
    return name


def get_spells_like(name):
    name = name.casefold()
    
    return [spell for spell in SPELLS if name in spell]



SPELL_COMMANDS = Nitori.interactions(
    None,
    name = 'spell',
    description = 'Magic!',
    guild = TEST_GUILD,
)


@SPELL_COMMANDS.interactions
async def cast(
    event,
    spell: ('str', 'select a spell'),
):
    """Uses the selected spell"""
    spell = get_spell_or_abort(spell)
    
    return f'{event.user:f} just used {spell}; It is super effective!'


@SPELL_COMMANDS.interactions
async def upgrade(
    event,
    spell: ('str', 'select a spell'),
):
    """Uses the selected spell"""
    spell = get_spell_or_abort(spell)
    
    return f'{event.user:f} just upgraded their {spell}; It was a *next* level move!'


@cast.autocomplete('spell')
@upgrade.autocomplete('spell')
async def auto_complete_spell_name(value):
    if value is None:
        return SPELLS[:25]
    
    return get_spells_like(value)

# command end
# command start autocomplete get-sticker-id

async def autocomplete_sticker_name(event, value):
    guild = event.guild
    if guild is None:
        return None
    
    
    if value is None:
        return sorted(sticker.name for sticker in guild.stickers.values())
    
    return sorted(sticker.name for sticker in guild.get_stickers_like(value))


@Nitori.interactions(guild = TEST_GUILD)
async def get_sticker_id(
    event,
    sticker: P('str', 'Sticker\'s name', autocomplete = autocomplete_sticker_name),
):
    guild = event.guild
    if guild is None:
        abort('Please use the command inside of a guild')
    
    sticker = guild.get_sticker_like(sticker)
    if sticker is None:
        abort('Unknown sticker')
    
    return f'{sticker.name}\'s id: `{sticker.id}`'

# command end
# command start components ping-pong

EMOJI_PING_PONG = BUILTIN_EMOJIS['ping_pong']

CUSTOM_ID_PING = 'ping_pong.ping'
CUSTOM_ID_PONG = 'ping_pong.pong'

BUTTON_PING = Button('ping', EMOJI_PING_PONG, custom_id = CUSTOM_ID_PING, style = ButtonStyle.green)
BUTTON_PONG = Button('pong', EMOJI_PING_PONG, custom_id = CUSTOM_ID_PONG, style = ButtonStyle.blue)


@Nitori.interactions(guild = TEST_GUILD)
async def ping_pong():
    if random() < 0.5:
        button = BUTTON_PING
    else:
        button = BUTTON_PONG
    
    return InteractionResponse(f'**ping {EMOJI_PING_PONG} pong**', components = button)


@Nitori.interactions(custom_id = CUSTOM_ID_PING)
async def ping_pong_ping():
    return InteractionResponse(components = BUTTON_PONG)

@Nitori.interactions(custom_id = CUSTOM_ID_PONG)
async def ping_pong_pong():
    return InteractionResponse(components = BUTTON_PING)

# command end
# command start components cat-feeder

# Static variables
CAT_FEEDER_CAT_EMOJI = Emoji.precreate(853998730071638056)
CAT_FEEDER_FOOD_EMOJI = BUILTIN_EMOJIS['fish']
CAT_FEEDER_CUSTOM_ID = 'cat_feeder.click'


# Command
@Nitori.interactions(guild = TEST_GUILD)
async def cat_feeder():
    """Hungry cat feeder!"""
    return InteractionResponse(
        f'Please feed my cat {CAT_FEEDER_CAT_EMOJI}, she is hungry.',
        components = Button(
            'Feed cat', CAT_FEEDER_FOOD_EMOJI, custom_id = CAT_FEEDER_CUSTOM_ID, style = ButtonStyle.green
        )
    )


# Component interaction
@Nitori.interactions(custom_id = CAT_FEEDER_CUSTOM_ID)
async def cat_fed(event):
    return (
        f'Please feed my cat {CAT_FEEDER_CAT_EMOJI}, she is hungry.\n'
        f'\n'
        f'Thanks, {event.user:f} for feeding my cat.'
    )

# command end
# command start components role-claimer


ROLE_NSFW_ACCESS = Role.precreate(828576094776590377)
ROLE_ANNOUNCEMENTS = Role.precreate(538397994421190657)

BUTTON_NSFW_ACCESS = Button('Nsfw access', custom_id = f'role_claimer.{ROLE_NSFW_ACCESS.id}')
BUTTON_ANNOUNCEMENTS = Button('Announcements', custom_id = f'role_claimer.{ROLE_ANNOUNCEMENTS.id}')

ROLE_CLAIMER_COMPONENTS = Row(BUTTON_NSFW_ACCESS, BUTTON_ANNOUNCEMENTS)

ROLE_CLAIMER_ROLES = {
    ROLE_NSFW_ACCESS.id: ROLE_NSFW_ACCESS,
    ROLE_ANNOUNCEMENTS.id: ROLE_ANNOUNCEMENTS,
}


@Nitori.interactions(guild = TEST_GUILD, required_permissions = Permission().update_by_keys(administrator = True))
async def role_claimer(event):
    """Role claimer message. (Owner only)"""
    
    # Double check.
    if not event.user_permissions.can_administrator:
        abort('Admin only')
    
    return InteractionResponse('Claim role by clicking on it', components = ROLE_CLAIMER_COMPONENTS)


@Nitori.interactions(custom_id = re.compile('role_claimer\.(\d+)'))
async def give_role(client, event, role_id):
    role_id = int(role_id)
    
    role = ROLE_CLAIMER_ROLES.get(role_id, None)
    if (role is not None) and (not event.user.has_role(role)):
        await client.user_role_add(event.user, role)

# command end
# command start components choose-your-poison

CUSTOM_ID_CAKE = 'choose_your_poison.cake'
CUSTOM_ID_CAT = 'choose_your_poison.cat'
CUSTOM_ID_SNAKE = 'choose_your_poison.snake'
CUSTOM_ID_EGGPLANT = 'choose_your_poison.eggplant'

EMOJI_CAKE = BUILTIN_EMOJIS['cake']
EMOJI_CAT = BUILTIN_EMOJIS['cat']
EMOJI_SNAKE = BUILTIN_EMOJIS['snake']
EMOJI_EGGPLANT = BUILTIN_EMOJIS['eggplant']

CHOOSE_YOUR_POISON_ROW = Row(
    Button('cake', custom_id = CUSTOM_ID_CAKE, style = ButtonStyle.blue),
    Button('cat', custom_id = CUSTOM_ID_CAT, style = ButtonStyle.gray),
    Button('snake', custom_id = CUSTOM_ID_SNAKE, style = ButtonStyle.green),
    Button('eggplant', custom_id = CUSTOM_ID_EGGPLANT, style = ButtonStyle.red),
)

CHOOSE_YOUR_POISON_CUSTOM_ID_TO_EMOJI = {
    CUSTOM_ID_CAKE: EMOJI_CAKE,
    CUSTOM_ID_CAT: EMOJI_CAT,
    CUSTOM_ID_SNAKE: EMOJI_SNAKE,
    CUSTOM_ID_EGGPLANT: EMOJI_EGGPLANT,
}


@Nitori.interactions(guild = TEST_GUILD)
async def choose_your_poison():
    """What is your weakness?"""
    return InteractionResponse(embed = Embed('Choose your poison'), components = CHOOSE_YOUR_POISON_ROW)


@Nitori.interactions(custom_id = [CUSTOM_ID_CAKE, CUSTOM_ID_CAT, CUSTOM_ID_SNAKE, CUSTOM_ID_EGGPLANT])
async def poison_edit_cake(event):
    emoji = CHOOSE_YOUR_POISON_CUSTOM_ID_TO_EMOJI.get(event.interaction.custom_id, None)
    if (emoji is not None):
        return emoji.as_emoji

# command end
# command start components add-emoji
# command start components zoo

def check_is_user_same(user, event):
    return (user is event.user)

# command end
# command start components add-emoji

ADD_EMOJI_BUTTON_ADD = Button('Add!', style = ButtonStyle.green)
ADD_EMOJI_BUTTON_CANCEL = Button('Nah.', style = ButtonStyle.red)

ADD_EMOJI_COMPONENTS = Row(ADD_EMOJI_BUTTON_ADD, ADD_EMOJI_BUTTON_CANCEL)

@Nitori.interactions(guild = TEST_GUILD)
async def add_emoji(
    client,
    event,
    emoji: ('str', 'The emoji to add.'),
    name: ('str', 'Custom name to add the emoji with.') = None
):
    """Adds an emoji to the guild."""
    if not client.is_owner(event.user):
        abort('Owner only!')
    
    emoji = parse_emoji(emoji)
    if emoji is None:
        abort('That\'s not an emoji.')
    
    if emoji.is_unicode_emoji():
        abort('Cannot add unicode emojis')
    
    if name is None:
        name = emoji.name
    else:
        if len(name) > 32:
            abort('Name length can be max 32.')
    
    embed = Embed('Are you sure to add this emoji?').add_field('Name:', name).add_image(emoji.url)
    
    message = yield InteractionResponse(embed = embed, components = ADD_EMOJI_COMPONENTS)
    
    try:
        component_interaction = await wait_for_component_interaction(
            message,
            timeout = 300.0,
            check = functools.partial(check_is_user_same, event.user)
        )
    
    except TimeoutError:
        component_interaction = None
        cancelled = True
    else:
        if component_interaction.interaction == ADD_EMOJI_BUTTON_CANCEL:
            cancelled = True
        else:
            cancelled = False
    
    if cancelled:
        embed.title = 'Adding emoji has been cancelled.'
    else:
        embed.title = 'Emoji has been added!'
        
        async with client.http.get(emoji.url) as response:
            emoji_data = await response.read()
        
        await client.emoji_create(event.guild, name, emoji_data)
    
    yield InteractionResponse(embed = embed, components = None, message = message, event = component_interaction)

# command end
# command start components pick

BUTTON_ATTEND = Button('Attend', style = ButtonStyle.green)

def check_is_user_unique(users, event):
    return (event.user not in users)

def render_joined_users(users):
    content_parts = ['I will pick who I like the most from the attenders.\n\nAttenders:']
    for user in users:
        content_parts.append('\n')
        content_parts.append(user.mention)
    
    return ''.join(content_parts)

def get_liking(client_id, user_id):
    if user_id > client_id:
        liking = user_id - client_id
    else:
        liking = client_id - user_id
    
    return liking

def pick_most_liked(client, users):
    client_id = client.id
    
    most_liked = users[0]
    most_liking = get_liking(client_id, most_liked.id)
    
    for user in users[1:]:
        liking = get_liking(client_id, user.id)
        if liking < most_liking:
            most_liking = liking
            most_liked = user
    
    return most_liked


@Nitori.interactions(guild = TEST_GUILD)
async def pick(client, event):
    """Picks who I like the most from the attenders."""
    users = [event.user]
    message = yield InteractionResponse(render_joined_users(users), allowed_mentions = None, components = BUTTON_ATTEND)
    
    try:
        async for component_interaction in iter_component_interactions(
            message, timeout = 60.0, check = functools.partial(check_is_user_unique, users)
        ):
            users.append(component_interaction.user)
            
            # limit the amount of users to 10.
            if len(users) == 10:
                break
            
            yield InteractionResponse(
                render_joined_users(users), allowed_mentions = None, event = component_interaction
            )
    
    except TimeoutError:
        component_interaction = None
    
    most_liked = pick_most_liked(client, users)
    
    content_parts = ['From:']
    for user in users:
        content_parts.append('\n')
        content_parts.append(user.mention)
    
    content_parts.append('\n\nI like ')
    content_parts.append(most_liked.mention)
    content_parts.append(' the most.')
    
    content = ''.join(content_parts)
    
    yield InteractionResponse(
        content, allowed_mentions = most_liked, components = None, message = message, event = component_interaction
    )

# command end
# command start components waifu

WAIFU_API_BASE_URL = 'https://api.waifu.pics'

WAIFU_API_HEADERS = {
    'Content-Type': 'application/json',
}
WAIFU_API_REQUEST_DATA = b'{}'


WAIFU_CUSTOM_ID = 'waifu_api'

WAIFU_TYPES = [
    'waifu',
    'neko',
    'shinobu',
    'megumin',
]

# We will cache responses
WAIFU_CACHE_BY_KEY = {waifu_type: [] for waifu_type in WAIFU_TYPES}


@Nitori.interactions(guild = TEST_GUILD)
async def waifu():
    """Ships waifus!"""
    embed = Embed('Please select a waifu type to ship.')
    select = Select(
        [Option(waifu_type, waifu_type) for waifu_type in WAIFU_TYPES],
        custom_id = WAIFU_CUSTOM_ID,
    )
    
    return InteractionResponse(embed = embed, components = select)


@Nitori.interactions(custom_id = WAIFU_CUSTOM_ID)
async def handle_waifu_select(client, event):
    # We filter out 3rd party users based on original and current invoking user.
    if event.message.interaction.user_id != event.user_id:
        return
    
    # Second we filter out incorrect selected values.
    # You can change the command over time and the can return bad option as well.
    selected_waifu_types = event.values
    if (selected_waifu_types is None):
        return
    
    selected_waifu_type = selected_waifu_types[0]
    if (selected_waifu_type not in WAIFU_TYPES):
        return
    
    
    # Try to get url from cache
    cache = WAIFU_CACHE_BY_KEY[selected_waifu_type]
    if cache:
        url = cache.pop()
    else:
        # We could not get url from cache
        
        # Do 1 yield to acknowledge the event.
        yield
        
        # We could use a Lock to avoid parallel requests, but that would expose us to other edge cases.
        async with client.http.post(
            f'{WAIFU_API_BASE_URL}/many/sfw/{selected_waifu_type}',
            headers = WAIFU_API_HEADERS,
            data = WAIFU_API_REQUEST_DATA,
        ) as response:
            
            if response.status == 200:
                data = await response.json()
            else:
                data = None
        
        url = None
        
        if (data is not None):
            try:
                files = data['files']
            except KeyError:
                pass
            else:
                cache.extend(files)
                
                if cache:
                    url = cache.pop()
    
    
    # Url defaults to `None`, so passing it to `url` field is fine.
    embed = Embed('Please select a waifu type to ship.', url = url)
    
    if url is None:
        embed.description = (
            f'*Could not find any free {selected_waifu_type} now.\n'
            f'Please try again later.*'
        )
    else:
        embed.add_image(url)
    
    # We re-build the select again with one difference, we mark the used one as default.
    select = Select(
        [Option(waifu_type, waifu_type, default = (waifu_type == selected_waifu_type)) for waifu_type in WAIFU_TYPES],
        custom_id = WAIFU_CUSTOM_ID,
    )
    
    yield InteractionResponse(embed = embed, components = select)

# command end
# command start components zoo

EMOJI_ELEPHANT = BUILTIN_EMOJIS['elephant']
LABEL_ELEPHANT = 'elephant'
DESCRIPTION_ELEPHANT = (
    f'Visiting big elephants.\n'
    f'{EMOJI_ELEPHANT} sugoi {EMOJI_ELEPHANT}'
)

EMOJI_LION = BUILTIN_EMOJIS['lion']
LABEL_LION = 'lion'
DESCRIPTION_LION = (
    f'Peeking at scary lions.\n'
    f'(I love cats {EMOJI_LION})'
)

EMOJI_ZEBRA = BUILTIN_EMOJIS['zebra']
LABEL_ZEBRA = 'zebra'
DESCRIPTION_ZEBRA = (
    f'Watching prison horses be like.\n'
    f'{EMOJI_ZEBRA} are cute!'
)

ANIMAL_IDENTIFIER_TO_DESCRIPTION = {
    LABEL_ELEPHANT: DESCRIPTION_ELEPHANT,
    LABEL_LION: DESCRIPTION_LION,
    LABEL_ZEBRA: DESCRIPTION_ZEBRA,
}

ZOO_SELECT = Select(
    [
        Option(LABEL_ELEPHANT, LABEL_ELEPHANT, emoji = EMOJI_ELEPHANT),
        Option(LABEL_LION, LABEL_LION, emoji = EMOJI_LION),
        Option(LABEL_ZEBRA, LABEL_ZEBRA, emoji = EMOJI_ZEBRA),
    ],
    placeholder = 'Select animals!',
    min_values = 0,
    max_values = 3,
)


@Nitori.interactions(guild = TEST_GUILD)
async def zoo(event):
    """Visiting zoo!"""
    
    message = yield InteractionResponse('Please select animals to visit!', components = ZOO_SELECT)

    try:
        component_interaction = await wait_for_component_interaction(
            message, timeout = 300.0, check = functools.partial(check_is_user_same, event.user)
        )
    
    except TimeoutError:
        content = 'You didn\'t decide which animals to visit and the zoo closed, see ya tomorrow!'
        component_interaction = None
    else:
        selected_animals = component_interaction.values
        if selected_animals is None:
            content = 'Going to zoo only to buy icecream?'
        else:
            content_parts = ['Visiting animals in the zoo!']
            
            for selected_animal in selected_animals:
                try:
                    description = ANIMAL_IDENTIFIER_TO_DESCRIPTION[selected_animal]
                except KeyError:
                    continue
                
                content_parts.append(description)
            
            content = '\n\n'.join(content_parts)
    
    yield InteractionResponse(content, components = None, message = message, event = component_interaction)

# command end
# command start components user-info


CUSTOM_ID_USER_INFO_CLOSE = 'user_info.close'
EMOJI_X = BUILTIN_EMOJIS['x']

BUTTON_USER_INFO_CLOSE = Button(
    emoji = EMOJI_X,
    custom_id = CUSTOM_ID_USER_INFO_CLOSE,
)

@Nitori.interactions(guild = TEST_GUILD)
async def user_info(
    client,
    event,
    user: ('user', 'Check out someone other user?') = None,
):
    if user is None:
        user = event.user
    
    embed = Embed(
        user.full_name,
    ).add_thumbnail(
        user.avatar_url,
    )
    
    created_at = user.created_at
    embed.add_field(
        'User Information',
        (
            f'Created: {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
            f'Profile: {user:m}\n'
            f'ID: {user.id}'
        ),
    )
    
    # We ignore guild specific information to keep it short.
    
    return InteractionResponse(
        embed = embed,
        components = BUTTON_USER_INFO_CLOSE,
    )

@Nitori.interactions(custom_id = CUSTOM_ID_USER_INFO_CLOSE)
async def close_user_info(client, event):
    # Allow closing for the source user
    if event.user is not event.message.interaction.user:
        return
    
    # We can use `yield` as well for acknowledging it.
    await client.interaction_component_acknowledge(event)
    await client.interaction_response_message_delete(event)

# command end
# command start components orindance

ORIN_DANCE_IMAGES = [
    'https://cdn.discordapp.com/attachments/850843243695439892/850843328127959060/5e672f97dc555.gif',
    'https://cdn.discordapp.com/attachments/850843243695439892/850843331516039218/1559518453_Ringood.gif',
    'https://cdn.discordapp.com/attachments/850843243695439892/850843831967547402/orin.gif',
    'https://cdn.discordapp.com/attachments/850843243695439892/850843849642606612/orinpok.gif',
    'https://cdn.discordapp.com/attachments/753424871760855122/884417334427660348/what-the-orin.gif',
    'https://cdn.discordapp.com/attachments/753424871760855122/886549772457095198/orin-dance-0000.gif',
]

CUSTOM_ID_ORIN_DANCE = 'orin_dance_please'
EMOJI_ORIN_DANCE = Emoji.precreate(704392145330634812)

BUTTON_ORIN_DANCE = Button(
    emoji = EMOJI_ORIN_DANCE,
    custom_id = CUSTOM_ID_ORIN_DANCE,
    style = ButtonStyle.green,
)

@Nitori.interactions(guild = TEST_GUILD)
async def orindance():
    return InteractionResponse(
        embed = Embed('Party!', url = 'https://orindance.party/').add_image(choice(ORIN_DANCE_IMAGES)),
        components = BUTTON_ORIN_DANCE,
    )

@Nitori.interactions(custom_id = CUSTOM_ID_ORIN_DANCE)
async def party(client, event):
    if event.user_id == event.message.interaction.user_id:
        
        old_url = event.message.embed.image.url
        orin_dance_images = ORIN_DANCE_IMAGES.copy()
        try:
            orin_dance_images.remove(old_url)
        except ValueError:
            pass
        
        return Embed('Party!', url = 'https://orindance.party/').add_image(choice(orin_dance_images))
    
    # Notify the user
    await client.interaction_response_message_create(
        event,
        'Please start your own party to dance!',
        show_for_invoking_user_only = True,
    )

# command end
# command start forms introduce-myself

INTRODUCTION_FORM = Form(
    'Introduce yourself',
    [
        TextInput(
            'What is your name?',
            min_length = 2,
            max_length = 128,
            custom_id = 'name',
        ),
        TextInput(
            'Something about you?',
            style = TextInputStyle.paragraph,
            min_length = 64,
            max_length = 1024,
            custom_id = 'bio',
        ),
    ],
    custom_id = 'introduction',
)


@Nitori.interactions(guild = TEST_GUILD)
async def introduce_myself():
    """Creates an introduction embed after filling a form."""
    return INTRODUCTION_FORM


@Nitori.interactions(custom_id = 'introduction', target = 'form')
async def introduction_form_submit(event, *, name, bio):
    return Embed(
        f'Hi, my name is {name}',
    ).add_field(
        'About me',
        bio,
    ).add_thumbnail(
        event.user.avatar_url,
    )

# command end
# command start forms add-role

ADD_ROLE_FORM = Form(
    'Add role', # Any dummy title does it
    [
        TextInput(
            'Additional message to send?',
            style = TextInputStyle.paragraph,
            max_length = 512,
            custom_id = 'message',
        ),
    ],
)


@Nitori.interactions(guild = TEST_GUILD)
async def add_role(
    client,
    event,
    user: ('user', 'User to add role to'),
    role: ('role', 'The role to give'),
):
    """Add role to a user."""
    # Check for permissions
    if not event.user_permissions.can_manage_roles:
        abort('You need `manage roles` permission to invoke this command.')
    
    if not event.guild.cached_permissions_for(client).can_manage_roles:
        abort('I need `manage roles` permission to execute this command.')
    
    if not event.user.has_higher_role_than(role):
        abort('You must have higher role than the role you are trying to give.')
    
    if not client.has_higher_role_than(role):
        abort('I must have higher role than the role you are trying to give.')
    
    # Using `.copy_to` on forms works as well.
    return ADD_ROLE_FORM.copy_with(
        title = f'Add role {role.name} to {user.full_name}',
        custom_id = f'add_role.{user.id}.{role.id}',
    )


@Nitori.interactions(custom_id = re.compile('add_role\.(\d+)\.(\d+)'), target = 'form')
async def add_role(client, event, user_id, role_id, *, message):
    user_id = int(user_id)
    role_id = int(role_id)
    
    yield # acknowledge the even
    
    await client.user_role_add(user_id, (event.guild_id, role_id), reason = message)
    
    # Try to send DM to the poor being.
    channel = await client.channel_private_create(user_id)
    
    guild = event.guild
    role = guild.roles[role_id]
    
    embed = Embed(
        description = f'You have received role {role.name} in {guild.name}.',
    )
    
    # Since message doesn't have `required` nor `min_length` passed it can be `None`.
    if (message is not None):
        embed.add_field(
            'Message',
            message,
        )
    
    try:
        await client.message_create(channel, embed = embed)
    except DiscordException as err:
        # Ignore the exception if the user has dm-s disabled.
        if err.code != ERROR_CODES.cannot_message_user: # user has dm-s disabled
            raise
    
    # Note: The user might not be cached at this point. Request it.
    # If you have user caching enabled + intent, it will do nothing.
    user = await client.user_get(user_id)
    
    embed = Embed(
        description = f'You gave {role.name} to {user.full_name}',
    )
    
    if (message is not None):
        embed.add_field(
            'Message',
            message,
        )
    
    yield embed

# command end
# command start forms add-waifu

WAIFUS = {}

CUSTOM_ID_WAIFU_FORM = 'waifu.form'
CUSTOM_ID_WAIFU_AGE = 'waifu.age'
CUSTOM_ID_WAIFU_BIO = 'waifu.bio'
CUSTOM_ID_WAIFU_HAIR = 'waifu.hair'
CUSTOM_ID_WAIFU_NAME = 'waifu.name'

CUSTOM_ID_WAIFU_BIO_REGEX = re.compile('waifu\.(?:description|bio)')

class Waifu:
    __slots__ = ('age', 'bio', 'hair', 'name', 'user')
    
    def __init__(self, age, bio, hair, name, user):
        self.age = age
        self.bio = bio
        self.hair = hair
        self.name = name
        self.user = user
    
    @property
    def embed(self):
        return Embed(
            self.name,
            self.bio,
        ).add_field(
            'age',
            self.age,
            inline = True,
        ).add_field(
            'hair',
            self.hair,
            inline = True,
        ).add_footer(
            f'Added by: {self.user:f}'
        )

# We will need these 3 in an example later

TEXT_INPUT_WAIFU_BIO = TextInput(
    'Bio',
    style = TextInputStyle.paragraph,
    min_length = 64,
    max_length = 1024,
    custom_id = CUSTOM_ID_WAIFU_BIO,
)

TEXT_INPUT_WAIFU_AGE = TextInput(
    'Age',
    min_length = 1,
    max_length = 1024,
    custom_id = CUSTOM_ID_WAIFU_AGE,
)

TEXT_INPUT_WAIFU_HAIR = TextInput(
    'hair',
    min_length = 1,
    max_length = 1024,
    custom_id = CUSTOM_ID_WAIFU_HAIR,
)


WAIFU_FORM = Form(
    'Describe your waifu',
    [
        TextInput(
            'Name',
            min_length = 2,
            max_length = 64,
            custom_id = CUSTOM_ID_WAIFU_NAME,
        ),
        TEXT_INPUT_WAIFU_BIO,
        TEXT_INPUT_WAIFU_AGE,
        TEXT_INPUT_WAIFU_HAIR,
    ],
    custom_id = CUSTOM_ID_WAIFU_FORM,
)


@Nitori.interactions(guild = TEST_GUILD)
async def add_waifu():
    """Add a new waifu to the database!"""
    return WAIFU_FORM


@Nitori.interactions(custom_id = CUSTOM_ID_WAIFU_FORM, target = 'form')
async def waifu_add_form_submit(
    event,
    *,
    age: CUSTOM_ID_WAIFU_AGE,
    bio: CUSTOM_ID_WAIFU_BIO_REGEX,
    hair: CUSTOM_ID_WAIFU_HAIR,
    name: CUSTOM_ID_WAIFU_NAME,
):
    key = name.casefold()
    if key in WAIFUS:
        abort('A waifu with the given name is already added.')
    
    WAIFUS[key] = waifu = Waifu(age, bio, hair, name, event.user)
    
    return waifu.embed

# command end
# command start get-waifu

@Nitori.interactions(guild = TEST_GUILD)
async def get_waifu(
    name: ('str', 'Their name?')
):
    """Returns an added waifu."""
    try:
        waifu = WAIFUS[name.casefold()]
    except KeyError:
        abort(f'There is no waifu named like: {name}.')
    
    return waifu.embed


@get_waifu.autocomplete('name')
async def autocomplete_waifu_name(value):
    if (value is None):
        # Return the 20 oldest
        return [waifu.name for waifu, _ in zip(WAIFUS.values(), range(20))]
    
    value = value.casefold()
    return [waifu.name for key, waifu in WAIFUS.items() if value in key]

# command end
# command start edit-waifu

CUSTOM_ID_WAIFU_EDIT_BASE = 'waifu.edit.'
CUSTOM_ID_WAIFU_EDIT_REGEX = re.compile('waifu\.edit\.(.*)')
CUSTOM_ID_WAIFU_FIELD_ALL = re.compile('waifu\.(?P<field>age|bio|hair)')

FIELD_TO_TEXT_INPUT = {
    'age': TEXT_INPUT_WAIFU_AGE,
    'bio': TEXT_INPUT_WAIFU_BIO,
    'hair': TEXT_INPUT_WAIFU_HAIR,
}

FIELD_TO_ATTRIBUTE = {
    'age': Waifu.age,
    'bio': Waifu.bio,
    'hair': Waifu.hair,
}


@Nitori.interactions(guild = TEST_GUILD)
async def edit_waifu(
    event,
    name: ('str', 'Their name?'),
    field : (['age', 'bio', 'hair'], 'Which field to edit?'),
):
    """Edits a waifu. | You must own her."""
    key = name.casefold()
    try:
        waifu = WAIFUS[key]
    except KeyError:
        abort(f'There is no waifu named like: {name}.')
    
    if waifu.user is not event.user:
        abort('You can only edit waifus added by yourself.')
    
    text_input = FIELD_TO_TEXT_INPUT[field]
    
    # We auto-fill the current value
    text_input = text_input.copy_with(value = FIELD_TO_ATTRIBUTE[field].__get__(waifu, Waifu))
    
    return Form(
        f'Editing {waifu.name}',
        [text_input],
        custom_id = f'{CUSTOM_ID_WAIFU_EDIT_BASE}{key}',
    )


@edit_waifu.autocomplete('name')
async def autocomplete_waifu_name(event, value):
    user = event.user
    
    if (value is None):
        # Return the 20 newest oldest
        return [waifu.name for waifu, _ in zip((waifu for waifu in WAIFUS.values() if waifu.user is user), range(20))]
    
    value = value.casefold()
    return [waifu.name for key, waifu in WAIFUS.items() if value in key and waifu.user is user]


@Nitori.interactions(custom_id = CUSTOM_ID_WAIFU_EDIT_REGEX, target = 'form')
async def waifu_edit_form_submit(
    key,
    *,
    edited_field: CUSTOM_ID_WAIFU_FIELD_ALL,
):
    # Both `group_dict` and `value` might be `None` at cases, so check them if you are not sure.
    group_dict, value = edited_field
    field = group_dict['field']
    
    waifu = WAIFUS[key]
    FIELD_TO_ATTRIBUTE[field].__set__(waifu, value)
    
    return waifu.embed

# command end
# command start forms rate-cakes

EMOJI_CAKE = BUILTIN_EMOJIS['cake']

CUSTOM_ID_RATE_CAKE = 'rate_cake'
CUSTOM_ID_RATE_CAKE_FIELD = 'rate_cake.field'


@Nitori.interactions(guild = TEST_GUILD)
async def rate_cakes(
    cake_1: ('str', 'Please rate this cake'),
    cake_2: ('str', 'Please rate this cake') = None,
    cake_3: ('str', 'Please rate this cake') = None,
    cake_4: ('str', 'Please rate this cake') = None,
    cake_5: ('str', 'Please rate this cake') = None,
):
    """Rate cakes."""
    # Filter
    cakes = {cake for cake in (cake_1, cake_2, cake_3, cake_4, cake_5) if (cake is not None)}
    
    return Form(
        'Rate your cakes',
        [
            TextInput(
                f'Please rate {cake}',
                min_length = 2,
                max_length = 128,
                custom_id = f'{CUSTOM_ID_RATE_CAKE_FIELD}[{cake}]',
            ) for cake in cakes
        ],
        custom_id = CUSTOM_ID_RATE_CAKE,
    )

@rate_cakes.autocomplete('cake-1', 'cake-2', 'cake-3', 'cake-4', 'cake-5')
async def autocomplete_cake_name(value):
    if value is None:
        return CAKE_NAMES[:25]
    
    value = value.casefold()
    return [cake_name for cake_name in CAKE_NAMES if (value in cake_name)]


@Nitori.interactions(custom_id = CUSTOM_ID_RATE_CAKE, target = 'form')
async def rate_cake_form_submit(
    event,
    *cakes: re.compile(f'{CUSTOM_ID_RATE_CAKE_FIELD}\[(\w+)\]'),
):
    user = event.user
    embed = Embed(f'{user:f}\'s cake ratings').add_thumbnail(user.avatar_url)
    
    for (cake, ), rating in cakes:
        embed.add_field(cake, rating)
    
    return embed

# command end
# command start typing-interactions show-emoji

@Nitori.interactions(guild = TEST_GUILD)
@configure_parameter('emoji_name', 'str', 'Yes?', 'emoji')
async def show_emoji(
    emoji_name: str
):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji_name)
    if emoji is None:
        abort('Please give an emoji')
    
    if emoji.is_unicode_emoji():
        abort('Cannot link unicode emojis.')
    
    return f'**Name:** {emoji} **Link:** {emoji.url}'

# command end
# command start typing-interactions text-channel-name-length

@Nitori.interactions(guild = TEST_GUILD)
@configure_parameter('channel', 'channel', 'Select a text channel', channel_types = [ChannelType.guild_text])
async def text_channel_name_length(
    channel: Channel
):
    """Returns the selected text channel's name's length."""
    return len(channel.name)

# command end

class TypingMeta(type):
    def __getitem__(cls, parameters):
        if isinstance(parameters, tuple):
            return cls(*parameters)
        else:
            return cls(parameters)


class Annotated(metaclass = TypingMeta):
    __slots__ = ('__args__', '__metadata__')
    
    def __new__(cls, pep_484, *metadata):
        if not metadata:
            raise TypeError(
                f'Metadata is required.'
            )
        
        if not isinstance(pep_484, tuple):
            pep_484 = (pep_484, )
        
        self = object.__new__(cls)
        self.__args__ = pep_484
        self.__metadata__ = metadata
        return self


# command start typing-interactions grocery-bag

@Nitori.interactions(guild = TEST_GUILD)
async def grocery_bag(
    cucumber: Annotated[int, P('int', 'How much cucumbers to buy?', min_value = 0, max_value = 1000)] = 0,
    strawberry: Annotated[int, P('int', 'How much oranges to buy?', min_value = 0, max_value = 1000)] = 0,
    orange: Annotated[int, P('int', 'How much oranges to buy?', min_value = 0, max_value = 1000)] = 0,
    watermelon: Annotated[int, P('int', 'How much watermelons to buy?', min_value = 0, max_value = 1000)] = 0,
):
    in_bag = []
    
    for count, name in zip(
        (cucumber, strawberry, orange, watermelon),
        ('cucumber', 'strawberry', 'orange', 'watermelon'),
    ):
        if count:
            in_bag.append(f'{name}: {count}')
    
    if in_bag:
        description = '\n'.join(in_bag)
    else:
        description = '*nothing*'
    
    return Embed(
        'In bag',
        description,
    )

# command end
# command start typing-interactions set-difficulty

@Nitori.interactions(guild = TEST_GUILD)
async def set_difficulty(
    difficulty: Annotated[str, ['easy', 'lunatic'], 'difficulty'],
):
    if difficulty == 'easy':
        return 'Only kids play on easy mode.\nHow lame!'
    
    return 'Crazy moon rabbit mode activated!'

# command end
# command start integration banner

@Nitori.interactions(integration_types = ['guild_install', 'user_install'], target = 'user')
async def banner(target):
    banner_url = target.banner_url_as(size = 4096)
    
    embed = Embed(f'{target.full_name}\'s banner')
    if banner_url is None:
        embed.description = 'The user has no banner'
    
    else:
        embed.url = banner_url
        embed.add_image(banner_url)
    
    return embed

# command end
# command start integration guild-features

@Nitori.interactions(integration_context_types = ['guild'], is_global = True)
async def guild_features(event):
    """Shows the guild's features."""
    guild = event.guild
    
    return Embed(
        f'{guild.name}\'s features',
        ', '.join(sorted(feature.name for feature in guild.iter_features())),
    ).add_thumbnail(
        guild.icon_url
    )

# command end

#### >@<>@<>@<>@< Source command >@<>@<>@<>@<>@< ####

COMMAND_START_RP = re.compile('# command start ([a-z\-]+) ([a-z\-]+)')
COMMAND_END_RP = re.compile('# command end')

EMPTY_UNICODE = '\u200b'
CODE_BLOCK_MARKER = '```'
ESCAPED_CODE_BLOCK_MARKER = f'{EMPTY_UNICODE}`{EMPTY_UNICODE}`{EMPTY_UNICODE}`'

def build_command_string(command_lines):
    # Remove empty line from end
    while command_lines:
        if command_lines[-1]:
            break
        
        del command_lines[-1]
    
    if not command_lines:
        return None
    
    # Remove 2+ continuous empty lines.
    continuous_empty = 0
    
    for index in reversed(range(1, len(command_lines) - 1)):
        if command_lines[index]:
            continuous_empty = 0
            continue
        
        continuous_empty += 1
        if continuous_empty > 2:
            del command_lines[index]
    
    
    # Remove empty line from start
    while command_lines:
        if command_lines[0]:
            break
        
        del command_lines[0]
    
    # collect chunks
    chunks = []
    
    chunk_start_index = 0
    
    index = 1
    limit = len(command_lines) - 2
    
    while index < limit:
        if command_lines[index]:
            index += 1
            continue
        
        if command_lines[index + 1]:
            index += 2
            continue
        
        chunk = command_lines[chunk_start_index:index]
        chunks.append(chunk)
        
        index += 2
        chunk_start_index = index
        continue
    
    chunk = command_lines[chunk_start_index:]
    chunks.append(chunk)
    
    # Group chunks
    chunks_with_length = []
    for chunk in chunks:
        chunk_length = 12 + len(chunk)
        
        for line in chunk:
            chunk_length += len(line)
        
        if chunk_length > 2000:
            raise RuntimeError(f'chunk_length over 2000 characters: {chunk_length!r}: {chunk_length!r}.')
        
        chunks_with_length.append((chunk_length, chunk))
        continue
    
    connected_chunks = []
    connected_chunk_lines = ['```py']
    connected_chunk_length = 0
    
    for chunk_length, chunk in chunks_with_length:
        connected_chunk_length += chunk_length
        if connected_chunk_length > 1500:
            if len(connected_chunk_lines) > 1:
                connected_chunk_lines[-1] = '```'
            
            connected_chunk = '\n'.join(connected_chunk_lines)
            connected_chunks.append(connected_chunk)
            
            connected_chunk_lines.clear()
            connected_chunk_lines.append('```py')
            connected_chunk_lines.extend(chunk)
            connected_chunk_lines.append('')
            connected_chunk_length = chunk_length
        else:
            connected_chunk_lines.extend(chunk)
            connected_chunk_lines.append('')
    
    connected_chunk_lines[-1] = '```'
    connected_chunk = '\n'.join(connected_chunk_lines)
    connected_chunks.append(connected_chunk)
    
    return tuple(connected_chunks)


def collect_commands():
    with open(__file__, 'r') as file:
        lines = file.read().splitlines()
    
    collected_lines_per_command = {}
    command_names = []
    
    for line in lines:
        matched = COMMAND_START_RP.fullmatch(line)
        if (matched is not None):
            command_names.append(matched.groups())
            continue
        
        matched = COMMAND_END_RP.fullmatch(line)
        if (matched is not None):
            command_names.clear()
            continue
        
        line = line.rstrip()
        line = line.replace(CODE_BLOCK_MARKER, ESCAPED_CODE_BLOCK_MARKER)
        
        for key in command_names:
            try:
                command_lines = collected_lines_per_command[key]
            except KeyError:
                command_lines = []
                collected_lines_per_command[key] = command_lines
            
            command_lines.append(line)
    
    collected_commands = {}
    
    for (command_type, command_name), command_lines in collected_lines_per_command.items():
        command_content = build_command_string(command_lines)
        if (command_content is not None):
            try:
                command_type_commands = collected_commands[command_type]
            except KeyError:
                command_type_commands = collected_commands[command_type] = {}
            
            command_type_commands[command_name] = command_content
    
    return collected_commands


COLLECTED_COMMANDS = collect_commands()


EMOJI_LEFT = BUILTIN_EMOJIS['arrow_left']
EMOJI_RIGHT = BUILTIN_EMOJIS['arrow_right']


class InteractionCommandSource:
    __slots__ = ('command_type', 'sources',)
    
    def __init__(self, command_type, sources):
        self.command_type = command_type
        self.sources = sources
    
    async def __call__(self, command_name):
        command_source = self.sources.get(command_name, None)
        if (command_source is None):
            abort(f'Command not found: {command_name!r}')
        
        page = command_source[0]
        
        if len(command_source) > 1:
            components = Row(
                Button(
                    emoji = EMOJI_LEFT,
                    custom_id = f'source.{self.command_type}.{command_name}._',
                    enabled = False,
                ),
                Button(
                    emoji = EMOJI_RIGHT,
                    custom_id = f'source.{self.command_type}.{command_name}.1',
                    enabled = True,
                ),
            )
        
        else:
            components = None
        
        yield InteractionResponse(page, components = components)

class AutoCompleteInteractionCommandSource:
    __slots__ = ('command_names', )
    def __init__(self, command_type_commands):
        self.command_names = sorted(command_type_commands)
    
    async def __call__(self, value):
        if value is None:
            return self.command_names[:20]
        
        value = value.lower()
        return [command_name for command_name in self.command_names if command_name.startswith(value)]


SOURCE = Nitori.interactions(None,
    name = 'source',
    description = 'The collective commands of Nitori.',
    guild = TEST_GUILD,
)

for command_type, command_type_commands in COLLECTED_COMMANDS.items():
    
    SOURCE.interactions(
        configure_parameter('command_name', 'str', f'Select a {command_type} command to show')(
            InteractionCommandSource(command_type, command_type_commands)
        ),
        name = command_type,
    ).autocomplete(
        'command_name',
        function = AutoCompleteInteractionCommandSource(command_type_commands)
    )

@Nitori.interactions(custom_id = re.compile('source\.([a-z\-]+)\.([a-z\-]+)\.(_|[0-9]+)'))
async def switch_page(event, command_type, command_name, page_index):
    # Check for the same user
    if event.message.interaction.user_id != event.user_id:
        return
    
    # Check whether page is really valid.
    if not page_index.isdigit():
        return
    
    # Lookup command source
    command_type_commands = COLLECTED_COMMANDS.get(command_type, None)
    if command_type_commands is None:
        return
    
    command_source = command_type_commands.get(command_name, None)
    if command_source is None:
        return
    
    page_index = int(page_index)
    if page_index == 0:
        button_back_enabled = False
        button_back_page_index = '_'
        
        button_next_enabled = True
        button_next_page_index = str(page_index + 1)
    elif page_index > len(command_source) - 2:
        page_index = len(command_source) - 1
        
        button_back_enabled = True
        button_back_page_index = str(page_index - 1)
        
        button_next_enabled = False
        button_next_page_index = '_'
    else:
        button_back_enabled = True
        button_back_page_index = str(page_index - 1)
        
        button_next_enabled = True
        button_next_page_index = str(page_index + 1)
    
    page = command_source[page_index]
    
    components = Row(
        Button(
            emoji = EMOJI_LEFT,
            custom_id = f'source.{command_type}.{command_name}.{button_back_page_index}',
            enabled = button_back_enabled,
        ),
        Button(
            emoji = EMOJI_RIGHT,
            custom_id = f'source.{command_type}.{command_name}.{button_next_page_index}',
            enabled = button_next_enabled,
        ),
    )
    
    return InteractionResponse(page, components = components)
