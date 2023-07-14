__all__ = (
    'TOUHOU_FEED_ABOUT_BUILDERS', 'TOUHOU_FEED_ABOUT_FIELDS', 'TOUHOU_FEED_ABOUT_TOPIC_MAIN',
    'build_touhou_feed_listing_response'
)

from itertools import chain
from re import I as re_ignore_case, U as re_unicode, compile as re_compile, escape as re_escape

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import AnsiForegroundColor, BUILTIN_EMOJIS, Embed, create_ansi_format_code, elapsed_time
from hata.ext.slash import Button, InteractionResponse, Row

from .constants import DEFAULT_INTERVAL, FEEDERS, MAX_INTERVAL, MIN_INTERVAL
from .logic import get_interval_only, join_names_of_touhou_characters, parse_channel_tags, should_auto_post_in_channel


STYLE_RESET = create_ansi_format_code()
STYLE_RED = create_ansi_format_code(foreground_color = AnsiForegroundColor.red)
STYLE_GREEN = create_ansi_format_code(foreground_color = AnsiForegroundColor.green)
STYLE_BLUE = create_ansi_format_code(foreground_color = AnsiForegroundColor.blue)

MIN_DELTA = elapsed_time(RelativeDelta(seconds = MIN_INTERVAL))
MAX_DELTA = elapsed_time(RelativeDelta(seconds = MAX_INTERVAL))
DEFAULT_DELTA = elapsed_time(RelativeDelta(seconds = DEFAULT_INTERVAL))

EMOJI_PAGE_PREVIOUS = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_NEXT = BUILTIN_EMOJIS['arrow_right']
EMOJI_REFRESH = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']

CUSTOM_ID_CLOSE = 'auto_post.close'

CUSTOM_ID_PAGE_BASE = 'auto_post.page.'
CUSTOM_ID_REFRESH_BASE = 'auto_post.refresh.'

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

BUTTON_REFRESH_BASE = Button(
    'Refresh',
    EMOJI_REFRESH,
)
    
BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
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
    BUTTON_CLOSE,
)

COMPONENTS_ABOUT_EXAMPLES = Row(
    BUTTON_ABOUT_MAIN,
    BUTTON_ABOUT_EXAMPLES.copy_with(enabled = False),
    BUTTON_ABOUT_INTERVAL,
    BUTTON_CLOSE,
)

COMPONENTS_ABOUT_INTERVAL = Row(
    BUTTON_ABOUT_MAIN,
    BUTTON_ABOUT_EXAMPLES,
    BUTTON_ABOUT_INTERVAL.copy_with(enabled = False),
    BUTTON_CLOSE,
)

DISPLAY_PER_PAGE = min(25 // 3, 4)


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


def iter_channels(client, guild):
    """
    Iterates over the forum's channels.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who would auto post.
    
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    
    Yields
    ------
    channel : ``Channel``
    """
    for channel in chain(guild.channels.values(), guild.threads.values()):
        if should_auto_post_in_channel(client, channel):
            yield channel


def get_channels(client, guild):
    """
    Gets all the channels of the forum.
    
    Parameters
    ----------
    client : ``Client``
        The client who would auto post.
    
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    
    Returns
    -------
    channels : `list` of ``Channel``
    """
    return [*iter_channels(client, guild)]


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


def _channel_match_priority_queue(client, guild, channel_name):
    """
    Produces priority queue of channels which match the given input value.
    
    Parameters
    ----------
    client : ``Client``
        The client who would auto post.
    
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
    for channel in iter_channels(client, guild):
        match = pattern.search(channel.name)
        if (match is not None):
            priority_queue.append((match.start(), channel))
    
    priority_queue.sort(key = _channel_match_sort_key)
    
    return priority_queue


def get_channels_like(client, guild, channel_name):
    """
    Gets channels which match the given input value.
    
    Parameters
    ----------
    client : ``Client``
        The client who would auto post.
    
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    
    channel_name : `str`
        The channel name to match.
    
    Returns
    -------
    channels : `list` of ``Channel``
    """
    return [channel for start, channel in _channel_match_priority_queue(client, guild, channel_name)]


def get_channel_like(client, guild, channel_name):
    """
    Gets the channel which matches the input value the most.
    
    Parameters
    ----------
    client : ``Client``
        The client who would auto post.
    
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    
    channel_name : `str`
        The channel name to match.
    
    Returns
    -------
    channel : `None`, ``Channel``
        The matched channel.
    """
    priority_queue = _channel_match_priority_queue(client, guild, channel_name)
    if priority_queue:
        return priority_queue[0][1]


def join_handler_keys(handler_keys):
    """
    Joins the given handler keys together into one string.
    
    Parameters
    ----------
    handler_keys : `tuple` of ``TouhouHandlerKey``
        The handler keys to join.
    
    Returns
    -------
    joined : `str`
    """
    join_parts = []
    handler_key_index = 0
    handler_key_count = len(handler_keys)
    
    while True:
        handler_key = handler_keys[handler_key_index]
        
        join_parts.append(join_names_of_touhou_characters(handler_key.characters, ' + '))
        
        if handler_key.solo:
            join_parts.append(' (solo)')
        
        handler_key_index += 1
        if handler_key_index >= handler_key_count:
            break
        
        join_parts.append('\n')
        continue
    
    return ''.join(join_parts)


def build_touhou_feed_listing_response(client, guild, page, enabled):
    """
    Builds listing page embed for the given page index.
    
    Parameters
    ----------
    client : ``Client``
        The client who would auto post.
    
    guild : ``Guild``
        The guild's identifier which channel to iterate.
    
    page : `int`
        The selected page.
        
    enabled : `bool`
        Whether the feature is enabled in the guild.
    
    Returns
    -------
    response : ``InteractionResponse``
        Response instance.
    """
    channels = get_channels(client, guild)
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
        if enabled:
            try:
                feeder = FEEDERS[channel.id]
            except KeyError:
                handler_keys = None
                interval = get_interval_only(channel)
            else:
                handler_keys = feeder.handler_keys
                interval = feeder.interval
        else:
            handler_keys_and_interval = parse_channel_tags(channel)
            if handler_keys_and_interval is None:
                handler_keys = None
                interval = get_interval_only(channel)
            else:
                handler_keys, interval = handler_keys_and_interval
        
        if handler_keys is None:
            style = STYLE_RED
            character_name = 'unknown'
        else:
            if handler_keys[0].characters:
                character_name = join_handler_keys(handler_keys)
                style = STYLE_GREEN
            else:
                character_name = '*all*'
                if handler_keys[0].solo:
                    character_name += ' (solo)'
                
                style = STYLE_BLUE
        
        delta = elapsed_time(RelativeDelta(seconds = interval))
        
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
        ).add_field(
            'Interval',
            (
                f'```\n'
                f'{delta}\n'
                f'```'
            ),
        )
    
    if not enabled:
        embed.add_footer('!! Touhou-feed is disabled in the guild !!')
    
    
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
        components = Row(
            button_previous_page,
            button_next_page,
            BUTTON_REFRESH_BASE.copy_with(custom_id = f'{CUSTOM_ID_REFRESH_BASE}{page}'),
            BUTTON_CLOSE,
        ),
    )


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
        f'{client_name} touhou-feed',
        f'{client_name} helps you to have `touhou-feed` in your **forum threads** and **text channels**.',
        color = color,
    ).add_field(
        f'Enable the touhou-feed feature in channels',
        (
            f'• For a forum thread, add `touhou-feed` tag in it.\n'
            f'• For a text channel, put `#touhou-feed` into it\'s topic.'
        ),
    ).add_field(
        f'Define which character\'s images should be sent',
        (
            f'• Name the channel after a character.\n'
            f'• For a forum thread, assign a tag with the character\'s name to it.\n'
            f'• For a text channel, put the character\'s name into the channel\'s topic (like `#koishi`).\n'
            f'• If multiple tags (like `#satori` & `#koishi`) are present in one channel then one of them '
            f'will be randomly chosen each time (so either Satori or Koishi).\n'
            f'If no character is specified {client_name} will select one of them each time randomly.'
        ),
    ).add_field(
        f'Tell {client_name} that you want only one character on a image',
        (
            f'• For a forum thread, assign an additional `solo` tag.\n'
            f'• For a text channel, put `#solo` into it\'s topic.\n'
            f'This will apply a solo modifier for each defined character.'
        ),
    ).add_field(
        'Combined tags using the `+` sign',
        (
            f'• To apply solo tag only to 1 character you may do `#character+solo` (like `#koishi+solo`)\n'
            f'• To receive a combination of characters at once, use `#character+character` syntax '
            f'(like `#koishi+satori`).\n'
            f'• If multiple group tags (like `#satori+koishi` & `#kokoro+solo`) are present then one group will be '
            f'selected randomly every time (so either Satori and Koishi together **or** Kokoro alone).'
        ),
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
        'This setup will send komeiji sisters.',
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
            f'koishi+satori\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Mokou',
        'This setup will send Mokou solo pictures (They are all hot).'
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
    ).add_field(
        'Cuties',
        'This setup will send a Koishi, Flandre and Kokoro pictures with 2 hour interval.'
    ).add_field(
        'Channel name',
        (
            f'```\n'
            f'N/A\n'
            f'```'
            f'*anything allowed'
        ),
        inline = True,
    ).add_field(
        'Tags',
        (
            f'```\n'
            f'\n'
            f'touhou-feed\n'
            f'koishi\n'
            f'flandre\n'
            f'kokoro\n'
            f'interval:2h\n'
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
            f'The feed interval is determined based on tags.\n'
            f'\n'
            f'If a channel has no interval determining tag, then **{DEFAULT_DELTA}** is used.\n'
            f'\n'
            f'To determine feed interval of a channel use the `#interval:` tag with the intervallum following it after.\n'
            f'\n'
            f'**Examples:**'
            f'```'
            f'#interval:12h -> 12 hours\n'
            f'#interval:6h30m -> 6 hours and 30 minutes\n'
            f'#interval:16s14h2m -> 14 hours, 2 minutes and 16 seconds\n'
            f'```\n'
            f'\n'
            f'Minimum interval is **{MIN_DELTA}** and maximum is **{MAX_DELTA}**.'
        ),
        color = color,
    )
    
    
    return InteractionResponse(
        embed = embed,
        components = COMPONENTS_ABOUT_INTERVAL,
    )


TOUHOU_FEED_ABOUT_TOPIC_MAIN = 'about_main'
TOUHOU_FEED_ABOUT_TOPIC_EXAMPLES = 'about_examples'
TOUHOU_FEED_ABOUT_TOPIC_INTERVAL = 'about_interval'

TOUHOU_FEED_ABOUT_FIELDS = {
    'about': TOUHOU_FEED_ABOUT_TOPIC_MAIN,
    'examples': TOUHOU_FEED_ABOUT_TOPIC_EXAMPLES,
    'interval': TOUHOU_FEED_ABOUT_TOPIC_INTERVAL,
}

TOUHOU_FEED_ABOUT_BUILDERS = {
    TOUHOU_FEED_ABOUT_TOPIC_MAIN: create_about_main,
    TOUHOU_FEED_ABOUT_TOPIC_EXAMPLES: create_about_examples,
    TOUHOU_FEED_ABOUT_TOPIC_INTERVAL: create_about_interval,
}


