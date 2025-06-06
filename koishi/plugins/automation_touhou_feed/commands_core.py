__all__ = (
    'TOUHOU_FEED_ABOUT_BUILDERS', 'TOUHOU_FEED_ABOUT_FIELDS', 'TOUHOU_FEED_ABOUT_TOPIC_MAIN',
    'build_touhou_feed_listing_response'
)
from itertools import chain
from re import I as re_ignore_case, U as re_unicode, compile as re_compile, escape as re_escape

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import Embed, create_button, create_row, elapsed_time
from hata.ext.slash import InteractionResponse

from .constants import (
    BUTTON_CLOSE, BUTTON_NEXT_DISABLED, BUTTON_PREVIOUS_DISABLED, BUTTON_REFRESH_BASE, COMPONENTS_ABOUT_EXAMPLES,
    COMPONENTS_ABOUT_INTERVAL, COMPONENTS_ABOUT_MAIN, CUSTOM_ID_PAGE_BASE, CUSTOM_ID_REFRESH_BASE, DEFAULT_DELTA,
    DISPLAY_PER_PAGE, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, FEEDERS, MAX_DELTA, MIN_DELTA, STYLE_BLUE, STYLE_GREEN,
    STYLE_RED, STYLE_RESET
)
from .logic import (
    get_interval_only, join_names_of_touhou_characters, parse_channel_tags, should_touhou_feed_in_channel
)


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
    for channel in chain(guild.iter_channels(), guild.iter_threads()):
        if should_touhou_feed_in_channel(client, channel):
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
    channel : ``None | Channel``
        The matched channel.
    """
    priority_queue = _channel_match_priority_queue(client, guild, channel_name)
    if priority_queue:
        return priority_queue[0][1]


def render_handler_keys_into(into, handler_keys, truncate_after):
    """
    Joins the given handler keys together into one string.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    handler_keys : `tuple<TouhouHandlerKey>`
        The handler keys to render.
    
    truncate_after : `int`
        The amount of characters to truncate after.
    
    Returns
    -------
    into : `list<str>`
    """
    truncate_after -= len(STYLE_GREEN)
    into.append(STYLE_GREEN)
    handler_key_index = 0
    handler_key_count = len(handler_keys)
    
    while True:
        handler_key = handler_keys[handler_key_index]
        
        joined_character_names = join_names_of_touhou_characters(handler_key.characters, ' + ')
        
        # Get line length # always add line break at the end.
        line_length = len(joined_character_names) + 1
        if handler_key.solo:
            line_length += 7
        
        truncate_after -= line_length
        if truncate_after < 0:
            into.append(STYLE_BLUE)
            into.append('... + ')
            into.append(str(handler_key_count - handler_key_index))
            break
        
        # add line
        into.append(joined_character_names)
        if handler_key.solo:
            into.append(' (solo)')
        
        handler_key_index += 1
        if handler_key_index >= handler_key_count:
            break
        
        into.append('\n')
        continue
    
    return into


def build_characters_section_description(handler_keys):
    """
    Renders `characters` section description.
    
    Parameters
    ----------
    handler_keys : `None | tuple<TouhouHandlerKey>`
        The handler keys to render.
    
    Returns
    -------
    section_description : `str`
    """
    into = ['```ansi\n', STYLE_RESET]
    while True:
        if handler_keys is None:
            into.append(STYLE_RED)
            into.append('unknown')
            break
        
        if handler_keys[0].characters is None:
            into.append(STYLE_BLUE)
            into.append('*all*')
            if handler_keys[0].solo:
                into.append(' (solo)')
            break
        
        into = render_handler_keys_into(into, handler_keys, 990)
        break
    
    into.append('\n```')
    return ''.join(into)


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
        
        delta = elapsed_time(RelativeDelta(seconds = interval))
        
        embed.add_field(
            f'\u200b',
            f'{channel.mention}'
        ).add_field(
            'Character',
            build_characters_section_description(handler_keys),
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
        button_previous_page = create_button(
            emoji = EMOJI_PAGE_PREVIOUS,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page - 1}',
        )
    
    if page >= page_count:
        button_next_page = BUTTON_NEXT_DISABLED
    else:
        button_next_page = create_button(
            emoji = EMOJI_PAGE_NEXT,
            custom_id = f'{CUSTOM_ID_PAGE_BASE}{page + 1}',
        )
    
    return InteractionResponse(
        embed = embed,
        components = create_row(
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


