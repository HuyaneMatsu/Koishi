__all__ = ()

from re import I as re_ignore_case, U as re_unicode, compile as re_compile, escape as re_escape

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import AnsiForegroundColor, BUILTIN_EMOJIS, Client, Embed, Permission, create_ansi_format_code, elapsed_time
from hata.ext.slash import Button, InteractionResponse, P, Row, abort

from .constants import DEFAULT_INTERVAL, FEEDERS, INTERVAL_MULTIPLIER, MAX_INTERVAL, MIN_INTERVAL
from .logic import get_feed_interval, join_names_of_touhou_characters, should_auto_post_in_channel, slowmode_to_interval


SLASH_CLIENT: Client


STYLE_RESET = create_ansi_format_code()
STYLE_RED = create_ansi_format_code(foreground_color=AnsiForegroundColor.red)
STYLE_GREEN = create_ansi_format_code(foreground_color=AnsiForegroundColor.green)

MIN_DELTA = elapsed_time(RelativeDelta(seconds = MIN_INTERVAL))
MAX_DELTA = elapsed_time(RelativeDelta(seconds = MAX_INTERVAL))
DEFAULT_INTERVAL = elapsed_time(RelativeDelta(seconds = DEFAULT_INTERVAL))

EMOJI_PAGE_PREVIOUS = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_NEXT = BUILTIN_EMOJIS['arrow_right']

CUSTOM_ID_PAGE_BASE = 'auto_post.page.'

CUSTOM_ID_PAGE_PREVIOUS_DISABLED = CUSTOM_ID_PAGE_BASE + 'd1'
CUSTOM_ID_PAGE_NEXT_DISABLED = CUSTOM_ID_PAGE_BASE + 'd2'

CUSTOM_ID_ABOUT_MAIN = 'auto_post.about.main'
CUSTOM_ID_ABOUT_EXAMPLES = 'auto_post.about.examples'
CUSTOM_ID_ABOUT_INTERVAL = 'auto_post.about.interval'


BUTTON_PREVIOUS_DISABLED = Button(
    emoji = EMOJI_PAGE_PREVIOUS,
    custom_id = CUSTOM_ID_PAGE_PREVIOUS_DISABLED,
    enabled = False,
)

BUTTON_NEXT_DISABLED = Button(
    emoji = EMOJI_PAGE_NEXT,
    custom_id = CUSTOM_ID_PAGE_NEXT_DISABLED,
    enabled = False,
)

BUTTON_ABOUT_MAIN = Button(
    'About',
    custom_id = CUSTOM_ID_ABOUT_MAIN,
)

BUTTON_ABOUT_EXAMPLES = Button(
    'Examples',
    custom_id = CUSTOM_ID_ABOUT_EXAMPLES,
)

BUTTON_ABOUT_INTERVAL = Button(
    'Interval',
    custom_id = CUSTOM_ID_ABOUT_INTERVAL,
)

COMPONENTS_ABOUT_MAIN = Row(
    BUTTON_ABOUT_MAIN.copy_with(enabled = False),
    BUTTON_ABOUT_EXAMPLES,
    BUTTON_ABOUT_INTERVAL,
)

COMPONENTS_ABOUT_EXAMPLES = Row(
    BUTTON_ABOUT_MAIN,
    BUTTON_ABOUT_EXAMPLES.copy_with(enabled = False),
    BUTTON_ABOUT_INTERVAL,
)

COMPONENTS_ABOUT_INTERVAL = Row(
    BUTTON_ABOUT_MAIN,
    BUTTON_ABOUT_EXAMPLES,
    BUTTON_ABOUT_INTERVAL.copy_with(enabled = False),
)


REQUIRED_PERMISSIONS = Permission().update_by_keys(manage_messages = True)

DISPLAY_PER_PAGE = 25 // 4


def _channel_sort_key(channel):
    """
    Sort key used to sort auto post channels.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to get it's sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    return channel.name


def iter_channels(guild):
    """
    Iterates over the forum's channels.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    
    Yields
    ------
    channel : ``Channel``
    """
    for channel in guild.threads.values():
        if should_auto_post_in_channel(channel):
            yield channel


def get_channels(guild):
    """
    Gets all the channels of the forum.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    
    Returns
    -------
    channels : `list` of ``Channel``
    """
    return [*iter_channels(guild)]


def _channel_match_sort_key(item):
    """
    Sort key used when sorting channels by match priority.
    
    Parameters
    ----------
    item : `tuple` (`int`, ``Channel``)
        Channel priority item to get their sort key of.
    
    Returns
    -------
    sort_key : `tuple` (`int`, `str`, `int`)
    """
    start, channel = item
    return (start, channel.name, channel.id)


def _channel_match_priority_queue(guild, channel_name):
    """
    Produces priority queue of channels which match the given input value.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    channel_name : `str`
        The channel name to match.
    
    Returns
    -------
    priority_queue : `tuple` (`int`, ``Channel``)
    """
    priority_queue = []
    
    pattern = re_compile(re_escape(channel_name), re_ignore_case | re_unicode)
    for channel in iter_channels(guild):
        match = pattern.search(channel.name)
        if (match is not None):
            priority_queue.append((match.start, channel))
    
    priority_queue.sort(key = _channel_match_sort_key)
    
    return priority_queue


def get_channels_like(guild, channel_name):
    """
    Gets channels which match the given input value.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    channel_name : `str`
        The channel name to match.
    
    Returns
    -------
    channels : `list` of ``Channel``
    """
    return [channel for start, channel in _channel_match_priority_queue(guild, channel_name)]


def get_channel_like(guild, channel_name):
    """
    Gets the channel which matches the input value the most.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    channel_name : `str`
        The channel name to match.
    
    Returns
    -------
    channel : `None`, ``Channel``
        The matched channel.
    """
    priority_queue = _channel_match_priority_queue(guild, channel_name)
    if priority_queue:
        return priority_queue[0][1]



def built_listing_page_embed(guild, page):
    """
    Builds listing page embed for the given page index.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    page : `int`
        The selected page.
    
    Returns
    -------
    response : ``InteractionResponse``
        Response instance.
    """
    channels = get_channels(guild)
    channels.sort(key = _channel_sort_key)
    
    channel_count = len(channels)
    if channel_count == 0:
        page_count = 1
    else:
        page_count = ((channel_count - 1) // DISPLAY_PER_PAGE) + 1
    
    if page > page_count:
        page = page_count
    elif page < 1:
        page = 1
    
    embed = Embed(
        'Touhou feed channels',
    ).add_thumbnail(
        guild.icon_url,
    ).add_footer(
        f'Page {page} / {page_count}',
    )
    
    channels = channels[(page - 1) * DISPLAY_PER_PAGE : page * DISPLAY_PER_PAGE]
    
    for channel in channels:
        try:
            feeder = FEEDERS[channel.id]
        except KeyError:
            character_name = 'unknown'
            solo = False
            style = STYLE_RED
        else:
            character_name = join_names_of_touhou_characters(feeder.handler_key.characters, '\n')
            solo = feeder.handler_key.solo
            style = STYLE_GREEN
        
        delta = elapsed_time(RelativeDelta(seconds = get_feed_interval(channel)))
        
        embed.add_field(
            f'\u200b',
            f'{channel.mention}'
        ).add_field(
            'Character',
            (
                f'```ansi\n'
                f'{STYLE_RESET}{style}{character_name}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Interval',
            (
                f'```\n'
                f'{delta}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Solo',
            (
                f'```\n'
                f'{"true" if solo else "false"}'
                f'```'
            ),
            inline = True,
        )
    
    
    if page <= 1:
        button_previous_page = BUTTON_PREVIOUS_DISABLED
    else:
        button_previous_page = Button(
            emoji = EMOJI_PAGE_PREVIOUS,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page - 1}',
        )
    
    if page >= page_count:
        button_next_page = BUTTON_NEXT_DISABLED
    else:
        button_next_page = Button(
            emoji = EMOJI_PAGE_NEXT,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page + 1}',
        )
    
    return InteractionResponse(
        embed = embed,
        components = Row(button_previous_page, button_next_page),
    )


TOUHOU_FEED_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'touhou-feed',
    description = 'Touhou feed control.',
    is_global = True,
    required_permissions = REQUIRED_PERMISSIONS,
)


@TOUHOU_FEED_COMMANDS.interactions
async def list_channels(
    event,
    page: P('int', 'Select a page', min_value = 1, max_value = 100) = 1,
):
    """Lists the touhou feed channels."""
    guild = event.guild
    if (guild is None):
        abort('Guild only command.')
    
    if not event.user_permissions & REQUIRED_PERMISSIONS:
        abort(f'Insufficient permissions.')
    
    return built_listing_page_embed(guild, page)


@SLASH_CLIENT.interactions(custom_id = [CUSTOM_ID_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_NEXT_DISABLED])
async def disabled_page_move():
    pass


@SLASH_CLIENT.interactions(custom_id = re_compile(re_escape(CUSTOM_ID_PAGE_BASE) + '(\d+)'))
async def page_move(event, page):
    guild = event.guild
    if (guild is not None) and (event.user_permissions & REQUIRED_PERMISSIONS):
        return built_listing_page_embed(guild, int(page))


@TOUHOU_FEED_COMMANDS.interactions
async def set_interval(
    client,
    event,
    channel_name: P('str', 'Select the channel', 'channel', min_length = 2, max_length = 100),
    hours: P('int', 'Interval (hours)', min_value = 0, max_value = 24) = 0,
    minutes: P('int', 'Interval (minutes)', min_value = 0, max_value = 59) = 0,
    seconds: P('int', 'Interval (seconds)', min_value = 0, max_value = 59) = 0,
):
    """Enables you to set interval by modifying channel slowmode."""
    guild = event.guild
    if (guild is None):
        abort('Guild only command.')
    
    if not event.user_permissions & REQUIRED_PERMISSIONS:
        abort(f'Insufficient permissions.')
    
    channel = get_channel_like(guild, channel_name)
    if channel is None:
        abort(f'Unknown channel: {channel_name}')
    
    yield
    
    old_slowmode = channel.slowmode
    
    interval = seconds + minutes * 60 + hours * 3600
    if interval == 0:
        interval = DEFAULT_INTERVAL
        new_slowmode = 0
    else:
        if interval > MAX_INTERVAL:
            interval = MAX_INTERVAL
        elif interval < MIN_INTERVAL:
            interval = MIN_INTERVAL
        
        new_slowmode = interval // INTERVAL_MULTIPLIER
    
    await client.channel_edit(channel, slowmode = new_slowmode)
    
    yield Embed(
        'Channel slowmode edited',
        channel.mention,
    ).add_field(
        f'\u200b',
        'From',
    ).add_field(
        'Interval',
        (
            f'```\n'
            f'{elapsed_time(RelativeDelta(seconds = slowmode_to_interval(old_slowmode)))}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Slowmode',
        (
            f'```\n'
            f'{elapsed_time(RelativeDelta(seconds = old_slowmode))}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        f'\u200b',
        'To',
    ).add_field(
        'Interval',
        (
            f'```\n'
            f'{elapsed_time(RelativeDelta(seconds = interval))}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Slowmode',
        (
            f'```\n'
            f'{elapsed_time(RelativeDelta(seconds = new_slowmode))}\n'
            f'```'
        ),
        inline = True,
    )


@set_interval.autocomplete('channel')
async def auto_complete_channel_name(event, value):
    """
    Auto completes the `channel` parameter of the `touhou-feed set-interval` command.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event instance.
    value : `None`, `str`
        The value the user typed.
    
    Returns
    -------
    channel_names : `None`, `list` of `str`
    """
    guild = event.guild
    if guild is None:
        return None
    
    if value is None:
        channels = get_channels(guild)
        channels.sort(key = _channel_sort_key)
    else:
        channels = get_channels_like(guild, value)
    
    return [channel.name for channel in channels]


def create_about_main(client, event):
    """
    Creates an about response for the "main" topic.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    client_name = client.name_at(event.guild_id)
    color = client.color_at(event.guild_id)
    
    embed = Embed(
        f'{client_name} posts images',
        (
            f'{client_name} helps you to have `touhou-feed` in your forum threads.\n'
            f'\n'
            f'To get started create a forum channel with a `touhou-feed` tag in it.\n'
            f'By assigning `touhou-feed` tag to a channel {client_name} will know, she should send images there.\n'
            f'\n'
            f'To define which character\'s images should be sent, name the channel to the character\'s name '
            f'(like `koishi`) or assign a tag to it .\n'
            f'\n'
            f'To tell {client_name} that you want one character on a image, assign an additional `solo` tag to the '
            f'channel.'
        ),
        color = color,
    )
    
    return InteractionResponse(
        embed = embed,
        components = COMPONENTS_ABOUT_MAIN,
    )


def create_about_examples(client, event):
    """
    Creates an about response for the "examples" topic.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    color = client.color_at(event.guild_id)
    
    embed = Embed(
        'Touhou-feed examples',
        color = color,
    ).add_field(
        'Komeiji sisters',
        'This setup will post the komeiji sisters.',
    ).add_field(
        'Channel name',
        (
            f'```\n'
            f'N/A*\n'
            f'```\n'
            f'*anything allowed'
        ),
        inline = True,
    ).add_field(
        'Tags',
        (
            f'```\n'
            f'touhou-feed\n'
            f'koishi\n'
            f'satori\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Mokou',
        'This setup will post Mokou solo pictures (They are all hot).'
    ).add_field(
        'Channel name',
        (
            f'```\n'
            f'Mokou\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Tags',
        (
            f'```\n'
            f'\n'
            f'touhou-feed\n'
            f'solo\n'
            f'```'
        ),
        inline = True,
    )
    
    return InteractionResponse(
        embed = embed,
        components = COMPONENTS_ABOUT_EXAMPLES,
    )


def create_about_interval(client, event):
    """
    Creates an about response for the "interval" topic.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    color = client.color_at(event.guild_id)
    
    embed = Embed(
        'Touhou-feed interval',
        (
            f'The feed interval is calculated from the thread\'s slowmode.\n'
            f'\n'
            f'If a channel has no slowmode, the default interval is **{DEFAULT_INTERVAL}.**\n'
            f'\n'
            f'If the channel has slowmode, it is multiplied by **{INTERVAL_MULTIPLIER}**. '
            f'This is to prevent complete blockage of the channel, and allow other users to post as well.\n'
            f'\n'
            f'Minimum interval is **{MIN_DELTA}** and max is **{MAX_DELTA}**.'
        ),
        color = color,
    )
    
    
    return InteractionResponse(
        embed = embed,
        components = COMPONENTS_ABOUT_INTERVAL,
    )


ABOUT_TOPIC_MAIN = 'about_main'
ABOUT_TOPIC_EXAMPLES = 'about_examples'
ABOUT_TOPIC_INTERVAL = 'about_interval'

ABOUT_FIELDS = {
    'about': ABOUT_TOPIC_MAIN,
    'examples': ABOUT_TOPIC_EXAMPLES,
    'interval': ABOUT_TOPIC_INTERVAL,
}

ABOUT_BUILDERS = {
    ABOUT_TOPIC_MAIN: create_about_main,
    ABOUT_TOPIC_EXAMPLES: create_about_examples,
    ABOUT_TOPIC_INTERVAL: create_about_interval,
}

@TOUHOU_FEED_COMMANDS.interactions
async def about(
    client,
    event,
    topic : (ABOUT_FIELDS, 'Select a topic to show') = ABOUT_TOPIC_MAIN,
):
    """Need to setup up touhou feed?"""
    return ABOUT_BUILDERS[topic](client, event)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_ABOUT_MAIN)
async def response_about_main(client, event):
    """
    Handles `about.main` component click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.user is event.message.interaction.user:
        return create_about_main(client, event)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_ABOUT_EXAMPLES)
async def response_about_examples(client, event):
    """
    Handles `about.examples` component click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.user is event.message.interaction.user:
        return create_about_examples(client, event)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_ABOUT_INTERVAL)
async def response_about_interval(client, event):
    """
    Handles `about.interval` component click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.user is event.message.interaction.user:
        return create_about_interval(client, event)
