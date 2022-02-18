import sys, re
from random import random, choice, randint
from time import perf_counter
from functools import partial as partial_func
from io import StringIO

try:
    import watchdog
except ImportError:
    watchdog = None

from hata import Embed, Client, KOKORO, BUILTIN_EMOJIS, DiscordException, ERROR_CODES, CHANNELS, MESSAGES, Emoji, \
    parse_message_reference, parse_emoji, parse_rdelta, parse_tdelta, cchunkify, ClientWrapper, GUILDS, \
    ChannelThread, mention_channel_by_id, ButtonStyle, format_loop_time, TIMESTAMP_STYLES, CHANNEL_TYPES, \
    INTERACTION_RESPONSE_TYPES, MessageFlag, InteractionResponseContext
from scarletio import sleep, alchemy_incendiary, LOOP_TIME, Task, WaitTillAll, Future, WaitTillExc
from hata.ext.slash import InteractionResponse, abort, set_permission, Form, TextInput, \
    wait_for_component_interaction, Button, Row, iter_component_interactions, configure_parameter, Select, Option
from scarletio.utils.trace import render_exception_into
from hata.ext.command_utils import UserMenuFactory, UserPagination
from hata.ext.slash.menus import Pagination
from hata.ext.commands_v2 import checks, cooldown, CommandCooldownError
from hata.ext.commands_v2.helps.subterranean import SubterraneanHelpCommand
from hata.ext.extension_loader import EXTENSION_LOADER, EXTENSIONS

from bot_utils.constants import COLOR__MARISA_HELP, GUILD__SUPPORT, CHANNEL__SUPPORT__DEFAULT_TEST, \
    ROLE__SUPPORT__TESTER
from bot_utils.utils import command_error
from bot_utils.syncer import sync_request_command
from bot_utils.interpreter_v2 import Interpreter

Marisa: Client

try:
    SOLARLINK_VOICE = Marisa.solarlink.add_node('127.0.0.1', 2333, 'youshallnotpass', None)
except BaseException as err:
    sys.stderr.write(f'Failed to connect to lavalink server: {err!r}.\n')
    SOLARLINK_VOICE = False

EXTENSION_LOADER.add_default_variables(SOLARLINK_VOICE=SOLARLINK_VOICE)
EXTENSION_LOADER.add('bots.modules.solar_voice')

Marisa.command_processor.create_category('TEST COMMANDS', checks=checks.owner_only())
Marisa.command_processor.create_category('VOICE', checks=checks.guild_only())
Marisa.command_processor.get_default_category().checks = checks.owner_only()

def marisa_help_embed_postprocessor(command_context, embed):
    if embed.color is None:
        embed.color = COLOR__MARISA_HELP
    
    embed.add_thumbnail(command_context.client.avatar_url)


@Marisa.events
async def track_end(client, event):
    print(repr(event))

@Marisa.events
async def track_exception(client, event):
    print(repr(event))

@Marisa.events
async def track_start(client, event):
    print(repr(event))

@Marisa.events
async def track_stuck(client, event):
    print(repr(event))

@Marisa.events
async def player_websocket_closed(client, event):
    print(repr(event))


Marisa.commands(
    SubterraneanHelpCommand(
        embed_postprocessor = marisa_help_embed_postprocessor,
    ),
    name = 'help',
    category = 'HELP',
)

@Marisa.command_processor.error
async def command_error_handler(ctx, exception):
    if ctx.guild is not GUILD__SUPPORT:
        return False
    
    with StringIO() as buffer:
        await KOKORO.render_exception_async(exception,[
            ctx.client.full_name,
            ' ignores an occurred exception at command ',
            repr(ctx.command),
            '\n\nMessage details:\nGuild: ',
            repr(ctx.guild),
            '\nChannel: ',
            repr(ctx.channel),
            '\nAuthor: ',
            ctx.author.full_name,
            ' (',
            repr(ctx.author.id),
            ')\nContent: ',
            repr(ctx.content),
            '\n```py\n'], '```', file=buffer)
        
        buffer.seek(0)
        lines = buffer.readlines()
    
    pages = []
    
    page_length = 0
    page_contents = []
    
    index = 0
    limit = len(lines)
    
    while True:
        if index == limit:
            embed = Embed(description=''.join(page_contents))
            pages.append(embed)
            page_contents = None
            break
        
        line = lines[index]
        index = index + 1
        
        line_length = len(line)
        # long line check, should not happen
        if line_length > 500:
            line = line[:500]+'...\n'
            line_length = 504
        
        if page_length + line_length > 1997:
            if index == limit:
                # If we are at the last element, we don\'t need to shard up,
                # because the last element is always '```'
                page_contents.append(line)
                embed = Embed(description=''.join(page_contents))
                pages.append(embed)
                page_contents = None
                break
            
            page_contents.append('```')
            embed = Embed(description=''.join(page_contents))
            pages.append(embed)
            
            page_contents.clear()
            page_contents.append('```py\n')
            page_contents.append(line)
            
            page_length = 6 + line_length
            continue
        
        page_contents.append(line)
        page_length += line_length
        continue
    
    limit = len(pages)
    index = 0
    while index < limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(ctx.client, ctx.channel, pages)
    return True


Marisa.commands(command_error, checks=[checks.is_guild(GUILD__SUPPORT)])

ALL = ClientWrapper()

@ALL.events
async def ready(client):
    sys.stdout.write(f'{client:f} logged in.\n')
    sys.stdout.write(
        f'guild count: {len(GUILDS)}\n'
        f'channel count: {len(CHANNELS)}\n'
    )

async def execute_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('execute', (
        'Use an interpreter trough me :3\n'
        'Usages:\n'
        f'{prefix}execute # code goes here\n'
        '# code goes here\n'
        '# code goes here\n'
        '\n'
        f'{prefix}execute\n'
        '```\n'
        '# code goes here\n'
        '# code goes here\n'
        '```\n'
        '*not code*\n'
        '\n'
        '... and many more ways.'
            ), color=COLOR__MARISA_HELP).add_footer(
            'Owner only!')

Marisa.commands(Interpreter(locals().copy()), name='execute', description=execute_description, category='UTILITY',
    checks=[checks.owner_only()])

Marisa.commands(sync_request_command, name='sync', category='UTILITY', checks=[checks.owner_only()])

@ALL.events(overwrite=True)
async def error(client, name, err):
    extracted = [
        client.full_name,
        ' ignores occurred exception at ',
        name,
        '\n',
    ]
    
    if isinstance(err, BaseException):
        await KOKORO.run_in_executor(alchemy_incendiary(render_exception_into, (err, extracted)))
    else:
        if not isinstance(err, str):
            err = repr(err)
        
        extracted.append(err)
        extracted.append('\n')
    
    extracted = ''.join(extracted).split('\n')
    for chunk in cchunkify(extracted, lang='py'):
        await client.message_create(CHANNEL__SUPPORT__DEFAULT_TEST, chunk)



# You might wanna add `-tag`-s to surely avoid nsfw pictures
SAFE_BOORU = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='

# Use a cache to avoid repeated requests.
# Booru also might ban ban you for a time if you do too much requests.
IMAGE_URL_CACHE = {}

@Marisa.interactions(guild=GUILD__SUPPORT)
async def retardify(client, event,
    text : ('str', 'Some text to retardify.'),
):
    """Translates the given text to retard language."""
    if text:
        description_parts = []
        chance = 0.5
        
        for char in text:
            if random() > chance:
                if chance > 0.5:
                    chance = 1.0 - (chance * 0.5)
                else:
                    chance = 0.5
                
                char = char.lower()
            else:
                if chance <= 0.5:
                    chance = chance * 0.5
                else:
                    chance = 0.5
                
                char = char.upper()
            
            description_parts.append(char)
        
        description = ''.join(description_parts)
    else:
        description = 'Nothing to retardify.'
    
    embed = Embed(description=description)
    user = event.user
    embed.add_author(user.avatar_url, user.full_name)
    
    await client.interaction_response_message_create(event, embed=embed, allowed_mentions=None)


@Marisa.interactions(guild=GUILD__SUPPORT)
async def test_channel_and_role(client, event,
    user : ('user', 'Please input a user') = None,
    channel : ('channel', 'Please input a channel') = None,
    role : ('role', 'Please input a role') = None,
):
    """Testing entities."""
    return \
        f'resolved_users = {event.resolved_users!r}\n' \
        f'resolved_channels = {event.resolved_channels!r}\n' \
        f'resolved_roles = {event.resolved_roles!r}\n' \
        f'user = {user!r}\n' \
        f'channel = {channel!r}\n' \
        f'role = {role!r}'


@Marisa.interactions(guild=GUILD__SUPPORT, show_for_invoking_user_only=True)
async def invoking_user_only(client, event):
    """SHows for the invoking user only, maybe?"""
    return 'Beep-boop'

async def async_gen():
    yield 'beep'
    yield 'boop'
    
@Marisa.interactions(guild=GUILD__SUPPORT)
async def yield_async_gen(client, event):
    """Yields an async gen."""
    yield async_gen()

@Marisa.interactions(guild=GUILD__SUPPORT)
async def return_async_gen(client, event):
    """Returns an async gen."""
    return async_gen()


@Marisa.interactions(guild=GUILD__SUPPORT)
async def raffle(client, event,
    message : ('str', 'The message to raffle from'),
    emoji : ('str', 'The reactor users to raffle from.'),
):
    """Raffles an user out who reacted on a message."""
    guild = event.guild
    if (client.get_guild_profile_for(guild) is None):
        abort('The command unavailable in guilds, where the application\'s bot is not in.')
    
    emoji = parse_emoji(emoji)
    if emoji is None:
        abort('That\'s not an emoji.')
    
    message_reference = parse_message_reference(message)
    if message_reference is None:
        abort('Could not identify the message.')
    
    guild_id, channel_id, message_id = message_reference
    try:
        message = MESSAGES[message_id]
    except KeyError:
        if channel_id:
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                abort('I have no access to the channel.')
                return
        else:
            channel = event.channel
        
        if not channel.cached_permissions_for(client).can_read_message_history:
            abort('I have no permission to get that message.')
        
        yield
        
        try:
            message = await client.message_get(channel, message_id)
        except ConnectionError:
            # No internet
            return
        except DiscordException as err:
            if err.code in (
                ERROR_CODES.unknown_channel, # message deleted
                ERROR_CODES.unknown_message, # channel deleted
            ):
                # The message is already deleted.
                abort('The referenced message is already yeeted.')
                return
            
            if err.code == ERROR_CODES.missing_access: # client removed
                # This is not nice.
                return
            
            if err.code == ERROR_CODES.missing_permissions: # permissions changed meanwhile
                abort('I have no permission to get that message.')
                return
            
            raise
    
    yield
    
    users = await client.reaction_user_get_all(message, emoji)
    
    if users:
        user = choice(users)
        content = user.mention
    else:
        content = 'Could not find any user.'
    
    yield content
    return

@Marisa.interactions(guild=GUILD__SUPPORT)
async def loading(client, event):
    """Loading screen nya!"""
    if not client.is_owner(event.user):
        return 'Owner only.'
    
    await client.interaction_response_message_create(event)
    await sleep(0.5)
    await client.interaction_response_message_edit(event, content='loaded')

@Marisa.interactions(guild=GUILD__SUPPORT)
async def number(client, event, number:('number', 'number')):
    """Loading screen nya!"""
    return str(number)


async def async_gen_2():
    abort('beep')
    yield

@Marisa.interactions(guild=GUILD__SUPPORT)
async def abort_from_async_gen(client, event):
    """Aborts from an async gen."""
    return async_gen_2()

@Marisa.interactions(guild=GUILD__SUPPORT)
async def parse_time_delta(client, event,
    delta: (str, 'The delta to parse'),
):
    """Tries to parse a time delta."""
    delta = parse_tdelta(delta)
    if delta is None:
        result = 'Parsing failed.'
    else:
        result = repr(delta)
    
    return result

@Marisa.interactions(guild=GUILD__SUPPORT)
async def parse_relative_delta(client, event,
    delta: (str, 'The delta to parse'),
):
    """Tries to parse a relative delta."""
    delta = parse_rdelta(delta)
    if delta is None:
        result = 'Parsing failed.'
    else:
        result = repr(delta)
    
    return result

@Marisa.interactions(guild=GUILD__SUPPORT)
async def user_id(client, event,
    user_id: ('user_id', 'Get the id of an other user?', 'user') = None,
):
    """Shows your or the selected user's id."""
    if user_id is None:
        user_id = event.user.id
    
    return str(user_id)

@Marisa.interactions(guild=GUILD__SUPPORT)
async def collect_reactions(client, event):
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

@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def tester_only(client, event):
    """Tester only hopefully."""
    return 'Noice'

@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def Late_abort(client, event):
    """Aborts after acknowledging."""
    yield
    abort('Nice?')


@Marisa.interactions(guild=GUILD__SUPPORT)
async def debug_command(client, event,
    command_name: (str, 'The command\'s name.')
):
    """Gets debug information about the given command."""
    if not client.is_owner(event.user):
        abort('Owner only.')
    
    if not command_name:
        abort('Empty command name.')
    
    application_commands = await client.application_command_guild_get_all(GUILD__SUPPORT)
    for application_command in application_commands:
        if application_command.name == command_name:
            break
    else:
        abort('Command could not be found.')
    
    try:
        permission = await client.application_command_permission_get(GUILD__SUPPORT, application_command)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_application_command_permissions:
            permission = None
        else:
            raise
    
    text_parts = [
        '**Application command**:\n'
        'Name : `', application_command.name, '`\n'
        'Id : `', repr(application_command.id), '`\n'
        'Allow by default : `', repr(application_command.allow_by_default), '`\n'
        '**Permission overwrites**:\n'
    ]
    
    if permission is None:
        permission_overwrites = None
    else:
        permission_overwrites = permission.permission_overwrites
    
    if permission_overwrites is None:
        text_parts.append('*none*')
    else:
        for index, permission_overwrite in enumerate(permission_overwrites):
            text_parts.append(repr(index))
            text_parts.append('.: type: `')
            text_parts.append(permission_overwrite.target_type.name)
            text_parts.append('`; id: `')
            text_parts.append(repr(permission_overwrite.target_id))
            
            target_name = permission_overwrite.target.name
            if target_name:
                text_parts.append('`; name: `')
                text_parts.append(target_name)
            
            text_parts.append('`; allowed: `')
            text_parts.append(repr(permission_overwrite.allow))
            text_parts.append('`\n')
    
    return ''.join(text_parts)

@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ('user', 707113350785400884), True)
@set_permission(GUILD__SUPPORT, ('user', 385575610006765579), True)
async def zeref_and_sleep_only(client, event):
    """Zeref and sleep only."""
    return 'LuL'

@Marisa.interactions(guild=GUILD__SUPPORT)
@set_permission(GUILD__SUPPORT, ('user', 707113350785400884), False)
async def only_zeref_not(client, event):
    """Loli Police"""
    return 'Lets go nekos.'


@Marisa.interactions(guild=GUILD__SUPPORT)
async def roll(client, event,
    dice_count: (set(range(1, 7)), 'With how much dice do you wanna roll with?') = 1,
):
    """Loli Police"""
    value = 0
    for dice in range(dice_count):
        value += randint(1, 6)
    
    return str(value)


@UserMenuFactory
class ZerefPagination(UserPagination):
    cake = BUILTIN_EMOJIS['cake']
    emojis = ( * UserPagination.emojis[:-1], cake, *UserPagination.emojis[-1:])
    
    __slots__ = ('user',)
    
    def __init__(self, menu, pages, user):
        UserPagination.__init__(self, menu, pages)
        self.user = user
    
    def check(self, event):
        return (self.user is event.user)
    
    async def invoke(self, event):
        if event.emoji is self.cake:
            menu = self.menu
            await menu.client.message_create(menu.channel, menu.message.content)
            return None
        
        return await UserPagination.invoke(self, event)

@Marisa.interactions(guild=GUILD__SUPPORT)
async def zeref_pagination(client, event):
    """Zeref's cake paginator."""
    await ZerefPagination(client, event, ['hi', 'hello'], event.user)


@UserMenuFactory
class CatFeeder:
    
    cat = BUILTIN_EMOJIS['cat']
    eggplant = BUILTIN_EMOJIS['eggplant']
    
    emojis = (cat, )
    timeout = 300.0
    
    allow_third_party_emojis = True
    
    def __init__(self, menu):
        self.menu = menu
        self.reacted = set()
    
    
    async def initial_invoke(self):
        return f'Please react with {self.cat:e} to feed her!\n' \
               f'If no new person reacts for 5 minutes the cat will be sad.'
    
    
    async def invoke(self, event):
        emoji = event.emoji
        user = event.user
        reacted = self.reacted
        if emoji is self.cat:
            
            if user in reacted:
                return None
            
            reacted.add(user)
            
            return f'Please react with {self.cat:e} to feed her!\n' \
                   f'If no no new unique person reacts for 5 minutes the cat will be sad.\n' \
                   f'\n' \
                   f'{len(reacted)} people gave the cat a slice of cake!'
        
        if emoji is self.eggplant:
            return f'Please react with {self.cat:e} to feed her!\n' \
                   f'If no no new unique person reacts for 5 minutes the cat will be sad.\n' \
                   f'\n' \
                   f'{len(reacted)} people gave the cat a slice of cake!\n' \
                   f'\n' \
                   f'{user:m} you wot mate?'
    
        return None
    
    async def close(self, exception):
        if exception is None:
            return
        
        if isinstance(exception, TimeoutError):
            menu = self.menu
            
            content = f'The {self.cat:e}has been fed by {len(self.reacted)} people.'
            await menu.client.message_edit(menu.message, content)
            
            if menu.channel.cached_permissions_for(menu.client).can_manage_messages:
                await menu.client.reaction_clear(menu.message)


@Marisa.interactions(guild=GUILD__SUPPORT)
async def cat_feeder(client, event):
    """Feed the cat!"""
    await CatFeeder(client, event)


def check_user(user, event):
    return user is event.user


@Marisa.interactions(guild=GUILD__SUPPORT)
async def getting_good(client, event):
    """Getting there."""
    main_component = Row(
        Button('cake', custom_id='cake', style=ButtonStyle.violet),
        Button('cat', custom_id='cat', style=ButtonStyle.gray),
        Button('snake', custom_id='snake', style=ButtonStyle.green),
        Button('eggplant', custom_id='eggplant', style=ButtonStyle.red),
        Button('eggplant', custom_id='eggplant', style=ButtonStyle.red, enabled=False),
    )
    
    yield InteractionResponse(embed=Embed('Choose your poison.'), components=main_component, show_for_invoking_user_only=True)
    
    try:
        component_interaction = await wait_for_component_interaction(event,
            timeout=4500., check=partial_func(check_user, event.user))
    except TimeoutError:
        await client.message_edit(event.message, components=None)
    else:
        emoji = BUILTIN_EMOJIS[component_interaction.interaction.custom_id]
        await client.message_edit(event.message, emoji.as_emoji, embed=None, components=None)


@Marisa.interactions(guild=GUILD__SUPPORT)
async def we_gucci(client, event):
    """Getting there."""
    components = [
        Button('cake', custom_id='cake', style=ButtonStyle.violet),
        Button('cat', custom_id='cat', style=ButtonStyle.gray),
        Button('snake', custom_id='snake', style=ButtonStyle.green),
        Button('eggplant', custom_id='eggplant', style=ButtonStyle.red),
    ]
    
    yield InteractionResponse(embed=Embed('Choose your poison.'), components=components)
    
    try:
        async for component_interaction in iter_component_interactions(event, timeout=10.0, count=3):
            emoji = BUILTIN_EMOJIS[component_interaction.interaction.custom_id]
            yield InteractionResponse(emoji.as_emoji, components=components, event=component_interaction)
    except TimeoutError:
        await client.interaction_response_message_edit(event, components=None)
        return
    
    yield InteractionResponse(embed=Embed('Choose your poison.', 'Interaction exhausted.'),
        components=None, message=event.message)


@Marisa.interactions(guild=GUILD__SUPPORT)
async def link():
    """Melo Melo!"""
    component = Button(
        'melo melo',
        url='https://www.youtube.com/watch?v=gYGqcORGqIw&ab_channel=ShoopTouhouEurobeatShoopTouhouEurobeat',
    )
    
    return InteractionResponse('_ _',
        components = component,
        show_for_invoking_user_only = True,
    )


@Marisa.interactions(guild=GUILD__SUPPORT)
async def slash_edit(client, event):
    """Editing slashes, bakana!"""
    yield InteractionResponse(embed=Embed('Choose your poison.'))
    await sleep(2.0, KOKORO)
    yield InteractionResponse(embed=Embed('Choose your cake.'), message=None)
    await sleep(2.0, KOKORO)
    yield InteractionResponse(embed=Embed('Choose your neko.'), message=None)

@Marisa.interactions(guild=GUILD__SUPPORT)
async def embed_abort(client, event):
    """embed abortion."""
    abort(embed=Embed('cake'))

@Marisa.interactions(guild=GUILD__SUPPORT)
async def mentionable_check(client, event,
    entity: ('mentionable', 'New field hype!'),
):
    """Roles and users."""
    yield repr(entity)


@Marisa.interactions(guild=GUILD__SUPPORT)
@configure_parameter('emoji', str, 'Yes?')
async def configured_show_emoji(emoji):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji)
    if emoji is None:
        return 'That\'s not an emoji.'
    
    if emoji.is_unicode_emoji():
        return 'That\' an unicode emoji, cannot link it.'
    
    return f'**Name:** {emoji:e} **Link:** {emoji.url}'


@Marisa.interactions(guild=GUILD__SUPPORT)
async def select_test():
    main_component = [
        Select([
                Option('cake', 'cake', default=True),
                Option('cat', 'cat'),
                Option('sugoi', 'sugoi'),
            ],
            placeholder = 'dunno',
            min_values = 2,
            max_values = 3,
        ),
    ]
    
    yield InteractionResponse(embed=Embed('Choose your poison.'), components=main_component,
        show_for_invoking_user_only=True)

@Marisa.commands
@cooldown('user', 30.0)
async def test_cooldown():
    return 'cake'

@test_cooldown.error
async def handle_cooldown_error(command_context, exception):
    if isinstance(exception, CommandCooldownError):
        await command_context.send(f'You are on cooldown. Try again after {exception.expires_after:.2f} seconds.')
        return True
    
    return False


@Marisa.interactions(guild=GUILD__SUPPORT)
async def nine():
    components = [
        [Button(f'{index_1}x{index_2}', custom_id=f'nine.{index_1}.{index_2}') for index_1 in range(1, 4)]
            for index_2 in range(1, 4)
    ]
    
    yield InteractionResponse('Select a nyan', components=components)

@Marisa.interactions(custom_id=re.compile('nine\.(\d)\.(\d)'))
async def poison_edit_cake(index_1, index_2):
    return f'You selected: {index_1}x{index_2}'


@Marisa.interactions(guild=GUILD__SUPPORT)
async def pagination_or_something(client, event):
    """Pagination or something"""
    await Pagination(client, event, ['cake', 'lewd'])

@Marisa.interactions(guild=GUILD__SUPPORT)
async def test_response_message(client, event):
    await client.interaction_application_command_acknowledge(event)
    message = await client.interaction_followup_message_create(event, 'cake')
    print(repr(message))
    print(repr(event.message))


# Dunno, meow-master stuff
now = perf_counter()

@Marisa.events
async def ready(client):
    print(perf_counter() - now)
    Marisa.events.remove(ready)


@Marisa.commands
@checks.owner_only()
async def count_message_fields(client, message):
    
    message_count = 0
    
    field_count_activity = 0
    field_count_application = 0
    field_count_application_id = 0
    field_count_attachments = 0
    field_count_components = 0
    field_count_content = 0
    field_count_cross_mentions = 0
    field_count_referenced_message = 0
    field_count_deleted = 0
    field_count_edited_at = 0
    field_count_embeds = 0
    field_count_everyone_mention = 0
    field_count_interaction = 0
    field_count_nonce = 0
    field_count_pinned = 0
    field_count_reactions = 0
    field_count_role_mention_ids = 0
    field_count_stickers = 0
    field_count_thread = 0
    field_count_tts = 0
    field_count_user_mentions = 0
    
    total_fields_by_count = {}
    
    async for message in await client.message_iterator(message.channel):
        message_count += 1
        total_fields = 0
        
        if message.has_activity():
            field_count_activity += 1
            total_fields += 1
        
        if message.has_application():
            field_count_application += 1
            total_fields += 1
        
        if message.has_application_id():
            field_count_application_id += 1
            total_fields += 1
        
        if message.has_attachments():
            field_count_attachments += 1
            total_fields += 1
        
        if message.has_components():
            field_count_components += 1
            total_fields += 1
        
        if message.has_content():
            field_count_content += 1
            total_fields += 1
        
        if message.has_cross_mentions():
            field_count_cross_mentions += 1
            total_fields += 1
        
        if message.has_referenced_message():
            field_count_referenced_message += 1
            total_fields += 1
        
        if message.has_deleted():
            field_count_deleted += 1
            total_fields += 1
        
        if message.has_edited_at():
            field_count_edited_at += 1
            total_fields += 1
        
        if message.has_embeds():
            field_count_embeds += 1
            total_fields += 1
        
        if message.has_everyone_mention():
            field_count_everyone_mention += 1
            total_fields += 1
        
        if message.has_interaction():
            field_count_interaction += 1
            total_fields += 1
        
        if message.has_nonce():
            field_count_nonce += 1
            total_fields += 1
        
        if message.has_pinned():
            field_count_pinned += 1
            total_fields += 1
        
        if message.has_reactions():
            field_count_reactions += 1
            total_fields += 1
        
        if message.has_role_mention_ids():
            field_count_role_mention_ids += 1
            total_fields += 1
        
        if message.has_stickers():
            field_count_stickers += 1
            total_fields += 1
        
        if message.has_thread():
            field_count_thread += 1
            total_fields += 1
        
        if message.has_tts():
            field_count_tts += 1
            total_fields += 1
        
        if message.has_user_mentions():
            field_count_user_mentions += 1
            total_fields += 1
        
        try:
            by_count = total_fields_by_count[total_fields]
        except KeyError:
            by_count = 1
        else:
            by_count += 1
        
        total_fields_by_count[total_fields] = by_count
        
        if message_count == 1000:
            break
    
    description_parts = []
    
    fields_array = [
        (field_count_activity, 'activity'),
        (field_count_application, 'application'),
        (field_count_application_id, 'application_id'),
        (field_count_attachments, 'attachments'),
        (field_count_components, 'components'),
        (field_count_content, 'content'),
        (field_count_cross_mentions, 'cross_mentions'),
        (field_count_referenced_message, 'referenced_message'),
        (field_count_deleted, 'deleted'),
        (field_count_edited_at, 'edited_at'),
        (field_count_embeds, 'embeds'),
        (field_count_everyone_mention, 'everyone_mention'),
        (field_count_interaction, 'interaction'),
        (field_count_nonce, 'nonce'),
        (field_count_pinned, 'pinned'),
        (field_count_reactions, 'reactions'),
        (field_count_role_mention_ids, 'role_mention_ids'),
        (field_count_stickers, 'stickers'),
        (field_count_thread, 'thread'),
        (field_count_tts, 'tts'),
        (field_count_user_mentions, 'user_mentions'),
    ]
    
    fields_array.sort(reverse=True)
    
    for field_count, field_name in fields_array:
        description_parts.append('**')
        description_parts.append(field_name)
        description_parts.append('**: ')
        description_parts.append(repr(field_count))
        description_parts.append('\n')
    
    description_parts.append('\n')
    
    total_fields_array = list(total_fields_by_count.items())
    total_fields_array.sort(reverse=True)
    
    for total_fields, message_amount in total_fields_array:
        description_parts.append('**')
        description_parts.append(repr(total_fields))
        description_parts.append(' fields**: ')
        description_parts.append(repr(message_amount))
        description_parts.append('\n')
    
    description_parts.append('\n')
    
    if message_count:
        total_total_fields = 0
        for total_fields, message_amount in total_fields_array:
            total_total_fields += total_fields * message_amount
        
        average_fields = total_total_fields / message_count
    else:
        average_fields = 0.0
    
    description_parts.append('**Total messages**: ')
    description_parts.append(repr(message_count))
    description_parts.append('\n**Average fields**:' )
    description_parts.append(average_fields.__format__('.02f'))
    description_parts.append('\n**Total fields**: 22 (including cache)')
    
    return ''.join(description_parts)


@Marisa.events
async def shutdown(client):
    await client.message_create(CHANNEL__SUPPORT__DEFAULT_TEST, 'dead')


@Marisa.commands
async def shutdown():
    await Marisa.stop()


PING = Marisa.interactions(
    None,
    name = 'ping',
    description = 'some random ping commands',
    guild = GUILD__SUPPORT,
)

@PING.interactions
async def no_wait():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'

@PING.interactions(wait_for_acknowledgement=True)
async def wait():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield InteractionResponse(f'{delay:.0f} ms')

@PING.interactions
async def no_wait_full():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield InteractionResponse(f'{delay:.0f} ms')
    
    delay = (perf_counter()-start)*1000.0
    yield f'{delay:.0f} ms'


@PING.interactions(wait_for_acknowledgement=True)
async def wait_full():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'

    delay = (perf_counter()-start)*1000.0
    yield f'{delay:.0f} ms'


@PING.interactions
async def extra_1():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    await sleep(1.0, KOKORO)
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@PING.interactions
async def extra_2():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    await sleep(0.1, KOKORO)
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@PING.interactions
async def extra_3():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    await sleep(0.1, KOKORO)
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'
    
    delay = (perf_counter()-start)*1000.0
    yield f'{delay:.0f} ms'


@PING.interactions
async def extra_4(client, event):
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    await client.message_create(event.channel, 'hoy!')
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def test_form(event):
    if not event.user.has_role(ROLE__SUPPORT__TESTER):
        abort('Tester only')
    
    return Form(
        'This does nothing',
        [
            TextInput('watch neko', custom_id='form_value')
        ],
        custom_id = 'watch_neko',
    )

@Marisa.interactions(custom_id='watch_neko', target='form', allowed_mentions=[])
async def watch_neko(*, form_value):
    return form_value


TEST_COMPONENT_RESPONSE_CUSTOM_ID = 'test.component_response'
TEST_COMPONENT_RESPONSE_BUTTON = Button(
    'click',
    custom_id = TEST_COMPONENT_RESPONSE_CUSTOM_ID,
)

@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def test_component_response():
    return InteractionResponse('_ _', components=TEST_COMPONENT_RESPONSE_BUTTON)


@Marisa.interactions(custom_id=TEST_COMPONENT_RESPONSE_CUSTOM_ID)
async def test_component_response_click(client, event):
    if event.user.has_role(ROLE__SUPPORT__TESTER):
        await client.interaction_response_message_create(event, 'ayyy', show_for_invoking_user_only=True)


TEST_FORM_RESPONSE_REPR_APPLICATION_COMMAND_CUSTOM_ID = 'test.form_response_repr.application_command'
TEST_FORM_RESPONSE_REPR_APPLICATION_COMMAND_FORM = Form(
    'Pls submit',
    [
        TextInput('pain')
    ],
    custom_id = TEST_FORM_RESPONSE_REPR_APPLICATION_COMMAND_CUSTOM_ID,
)

@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def test_form_response_repr_ac():
    return TEST_FORM_RESPONSE_REPR_APPLICATION_COMMAND_FORM

@Marisa.interactions(custom_id=TEST_FORM_RESPONSE_REPR_APPLICATION_COMMAND_CUSTOM_ID, target='form')
async def test_form_response_repr_ac_form_submit(event):
    return repr(event)


TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_CUSTOM_ID = 'test.form_response_repr.message_component'
TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_FORM = Form(
    'Pls submit',
    [
        TextInput('pain')
    ],
    custom_id = TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_CUSTOM_ID,
)

TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_BUTTON = Button(
    'click',
    custom_id = TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_CUSTOM_ID,
)

@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def test_form_response_repr_mc():
    return InteractionResponse('_ _', components=TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_BUTTON)

@Marisa.interactions(custom_id=TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_CUSTOM_ID)
async def test_form_response_repr_mc_form_submit(event):
    if event.user.has_role(ROLE__SUPPORT__TESTER):
        return TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_FORM

@Marisa.interactions(custom_id=TEST_FORM_RESPONSE_REPR_MESSAGE_COMPONENT_CUSTOM_ID, target='form')
async def test_form_response_repr_mc_form_submit(client, event):
    await client.interaction_component_message_edit(event, f'{event.user:f} submitted')
    return repr(event)


@Marisa.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__TESTER, True)
async def resend(
    client,
    event,
    attachment: ('attachment', 'File!'),
):
    yield
    file = await client.download_attachment(attachment)
    yield InteractionResponse(file=(attachment.name, file))


@Marisa.interactions(guild=GUILD__SUPPORT)
async def locale(event):
    return (
        f'Locale: {event.locale}\n'
        f'guild locale: {event.guild_locale}'
    )

MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY = MessageFlag().update_by_keys(invoking_user_only=True)
MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS = MessageFlag().update_by_keys(embeds_suppressed=True)

TO_SUPPRESS = 'https://www.youtube.com/watch?v=QO9CuvM-Pjk'

SUPPRESS_EMBEDS_TESTING = Marisa.interactions(
    None,
    guild = GUILD__SUPPORT,
    name = 'suppress-embeds-testing',
    description = 'we suppress some embeds',
)

@SUPPRESS_EMBEDS_TESTING.interactions
async def create(client, event):
    data = {
        'data': {
            'content': TO_SUPPRESS,
            'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
        },
        'type': INTERACTION_RESPONSE_TYPES.message_and_source,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_response_message_create(event.id, event.token, data)


@SUPPRESS_EMBEDS_TESTING.interactions
async def ack(client, event):
    await client.interaction_application_command_acknowledge(event)
    
    data = {
        'content': TO_SUPPRESS,
        'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_followup_message_create(client.application.id, event.id, event.token, data)


@SUPPRESS_EMBEDS_TESTING.interactions
async def ack_2(client, event):
    data = {
        'data': {
            'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
        },
        'type': INTERACTION_RESPONSE_TYPES.source,
    }
    
    async with InteractionResponseContext(event, True, False):
        await client.http.interaction_response_message_create(event.id, event.token, data)
    
    data = {
        'content': TO_SUPPRESS,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_followup_message_create(client.application.id, event.id, event.token, data)

@SUPPRESS_EMBEDS_TESTING.interactions
async def ack_3(client, event):
    data = {
        'data': {
            'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
        },
        'type': INTERACTION_RESPONSE_TYPES.source,
    }
    
    async with InteractionResponseContext(event, True, False):
        await client.http.interaction_response_message_create(event.id, event.token, data)
    
    data = {
        'content': TO_SUPPRESS,
        'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_followup_message_create(client.application.id, event.id, event.token, data)


@SUPPRESS_EMBEDS_TESTING.interactions
async def ack_4(client, event):
    data = {
        'data': {
            'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
        },
        'type': INTERACTION_RESPONSE_TYPES.source,
    }
    
    async with InteractionResponseContext(event, True, False):
        await client.http.interaction_response_message_create(event.id, event.token, data)
    
    data = {
        'content': TO_SUPPRESS,
        'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_response_message_edit(client.application.id, event.id, event.token, data)


@SUPPRESS_EMBEDS_TESTING.interactions
async def followup(client, event):
    yield 'cake'
    
    data = {
        'content': TO_SUPPRESS,
        'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_followup_message_create(client.application.id, event.id, event.token, data)


@SUPPRESS_EMBEDS_TESTING.interactions
async def edit(client, event):
    data = {
        'data': {
            'content': TO_SUPPRESS,
            # 'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
        },
        'type': INTERACTION_RESPONSE_TYPES.message_and_source,
    }
    
    async with InteractionResponseContext(event, True, False):
        await client.http.interaction_response_message_create(event.id, event.token, data)
    
    await sleep(2.0)
    
    data = {
        'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_response_message_edit(client.application.id, event.id, event.token, data)

@SUPPRESS_EMBEDS_TESTING.interactions
async def edit_2(client, event):
    data = {
        'data': {
            'content': TO_SUPPRESS,
            # 'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
        },
        'type': INTERACTION_RESPONSE_TYPES.message_and_source,
    }
    
    async with InteractionResponseContext(event, True, False):
        await client.http.interaction_response_message_create(event.id, event.token, data)
    
    message = await event.wait_for_response_message()
    
    await sleep(2.0)
    
    data = {
        'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
    }
    
    async with InteractionResponseContext(event, False, False):
        await client.http.interaction_followup_message_edit(client.application.id, event.id, event.token, message.id,
            data)

@SUPPRESS_EMBEDS_TESTING.interactions
async def webhook(client, event):
    channel = event.channel
    executor_webhook = await client.webhook_get_own_channel(channel)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel, 'marisad')
    
    data = {
        'content': TO_SUPPRESS,
        'flags': MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS,
    }
    
    await client.http.webhook_message_create(executor_webhook.id, executor_webhook.token, data, None)


if (watchdog is not None):
    
    from watchdog.events import FileModifiedEvent
    from watchdog.observers import Observer
    
    class WatchEventHandler:
        def dispatch(self, event):
            extension = EXTENSION_LOADER.get_extension(event.src_path)
            if (extension is not None) and (not extension.locked):
                EXTENSION_LOADER.reload(extension.name)
    
    @Marisa.events
    async def launch(client):
        observer = Observer()
        client.observer = observer
        
        event_handler = WatchEventHandler()
        
        for extension in EXTENSIONS.values():
            if extension.is_loaded() and (not extension.locked):
                observer.schedule(event_handler, extension.file_name, recursive=False)
        
        observer.start()
    
    @Marisa.events
    async def shutdown(client):
        client.observer.stop()
