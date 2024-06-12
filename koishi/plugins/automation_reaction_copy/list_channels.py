__all__ = ('build_reaction_copy_list_channels_response',)

from itertools import chain, islice

from hata import Embed, Emoji, escape_markdown, parse_all_emojis
from hata.ext.slash import InteractionResponse

from .constants import COMPONENTS, MASK_PARSE_NAME_ALL, MASK_PARSE_TOPIC_ALL, MASK_PARSE_TOPIC_UNICODE
from .flag_naming import get_reaction_copy_flag_parse_names


def collect_channels_with_emojis(guild, flags):
    """
    Collects channels with emojis, filters them and groups them by category.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to look up.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    without_category : `None, list<(Channel, list<Emoji>)>`
    by_category : `list<(Channel, list<(Channel, list<Emoji>)>)>`
    """
    emojis_to_channels = collect_emojis_to_channels(guild, flags)
    channels_to_emojis = filter_emojis_to_channels(emojis_to_channels)
    return group_channels_to_emojis(channels_to_emojis)


def get_first_client(channel):
    """
    Returns the first client who has sufficient permissions to send a message to the given channel.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to check.
    
    Returns
    -------
    client : `None | Client`
    """
    for client in channel.clients:
        if channel.cached_permissions_for(client).can_manage_webhooks:
            return client


def collect_emojis_to_channels(guild, flags):
    """
    Collects the emojis and their related channels of the guild where the client has the required permissions.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to look up.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    emojis_to_channels : `dict<Emoji, list<Channel>>`
    """
    emojis_to_channels = {}
    
    for channel in chain(guild.channels.values(), guild.threads.values()):
        if not channel.is_in_group_guild_textual():
            continue
        
        for emoji in collect_channel_emojis(channel, flags):
            try:
                channels = emojis_to_channels[emoji]
            except KeyError:
                channels = []
                emojis_to_channels[emoji] = channels
            
            channels.append(channel)
    
    return emojis_to_channels


_condition_allow_unicode = Emoji.is_unicode_emoji
_condition_allow_custom = Emoji.is_custom_emoji
_condition_allow_all = lambda emoji: True


def collect_channel_emojis(channel, flags):
    """
    Collects all the emojis on the channel.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to collect the emojis of.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    emojis : `set<Emoji>˙
    """
    emojis = set()
    
    if flags & MASK_PARSE_NAME_ALL:
        # we allow only unicode for `.name`
        condition = _condition_allow_unicode
        
        for emoji in parse_all_emojis(channel.name):
            if condition(emoji):
                emojis.add(emoji)
    
    
    if flags & MASK_PARSE_TOPIC_ALL:
        topic = channel.topic
        if (topic is not None):
            # we allow both unicode & custom for `.topic`
            if flags & MASK_PARSE_TOPIC_ALL == MASK_PARSE_TOPIC_ALL:
                condition = _condition_allow_all
            elif flags & MASK_PARSE_TOPIC_UNICODE:
                condition = _condition_allow_unicode
            else:
                condition = _condition_allow_custom
            
            for emoji in parse_all_emojis(topic):
                if condition(emoji):
                    emojis.add(emoji)
    
    return emojis


def filter_emojis_to_channels(emojis_to_channels):
    """
    Filters the given emojis to channels relation mapping.
    Ignores duplicate emojis and creates a `channel - emojis` relation`.
    
    Parameters
    ----------
    emojis_to_channels : `dict<Emoji, list<Channel>˙
        Emojis to channels relations.
    
    Returns
    -------
    channels_to_emojis : `dict<Channel, list<Emoji>˙
        Channels to emojis relations.
    """
    channels_to_emojis = {}
    
    for emoji, channels in emojis_to_channels.items():
        if len(channels) != 1:
            continue
            
        channel = channels[0]
        try:
            emojis = channels_to_emojis[channel]
        except KeyError:
            emojis = []
            channels_to_emojis[channel] = emojis
        
        emojis.append(emoji)
    
    return channels_to_emojis


def group_channels_to_emojis(channels_to_emojis):
    """
    Groups up the channels by category.
    
    Parameters
    ----------
    channels_to_emojis : `dict<Channel, list<Emoji>˙
        Channels to emojis relations.
    
    Returns
    -------
    without_category : `None, list<(Channel, list<Emoji>)>`
    by_category : `list<(Channel, list<(Channel, list<Emoji>)>)>`
    """
    without_category = None
    by_category = {}
    
    for channel, emojis in channels_to_emojis.items():
        parent = channel.parent
        if parent is None:
            if without_category is None:
                without_category = []
            
            without_category.append((channel, emojis))
            continue
        
        try:
            group = by_category[parent]
        except KeyError:
            group = []
            by_category[parent] = group
        
        group.append((channel, emojis))
    
    if (without_category is not None):
        sort_channels_and_emojis(without_category)
    
    for channels_and_emojis in by_category.values():
        sort_channels_and_emojis(channels_and_emojis)
    
    groups = sorted(by_category.items(), key = _group_sort_key)
    return without_category, groups


def _group_sort_key(item):
    """
    Sort key used for sorting groups.
    
    Parameters
    ----------
    item : `(Channel, list<(Channel, list<Emoji)>)`
        The item to get it's sort key of.
    
    Returns
    -------
    sort_key : ``Channel``
    """
    return item[0]


def _channels_and_emojis_sort_key(item):
    """
    Sort key used for sorting channels.
    
    Parameters
    ----------
    item : `(Channel, list<Emoji>)`
        The item to get it's sort key of.
    
    Returns
    -------
    sort_key : ``Channel``
    """
    return item[0]


def _emojis_sort_key(emoji):
    """
    Sort key used for sorting emojis.
    
    Parameters
    ----------
    emoji : ``Emoji``
    
    Returns
    -------
    sort_key : `(str, int)`
    """
    return emoji.name, emoji.id


def sort_channels_and_emojis(channels_and_emojis):
    """
    Sorts the given channels and emojis group.
    
    Parameters
    ----------
    channels_and_emojis : `list<(Channel, list<Emoji>)>`
        The item to get it's sort key of.
    """
    channels_and_emojis.sort(key = _channels_and_emojis_sort_key)
    
    for item in channels_and_emojis:
        item[1].sort(key = _emojis_sort_key)


def build_description(channels_and_emojis):
    """
    Builds description of the given channels and their respective emojis combination.
    
    Parameters
    ----------
    channels_and_emojis : `list<(Channel, list<Emoji>)>`
        The channels and the emojis that are targetable.
    
    Returns
    -------
    description : `str`
    """
    # limit the amount of channels to show
    description_parts = []
    
    channel_index = 0
    channel_limit = min(len(channels_and_emojis), 20)
    
    while True:
        channel, emojis = channels_and_emojis[channel_index]
        
        description_parts.append(channel.mention)
        description_parts.append(' : ')
        
        emoji_index = 0
        emoji_limit = min(len(emojis), 10)
        
        while True:
            emoji = emojis[emoji_index]
            
            description_parts.append(emoji.as_emoji)
            description_parts.append(' ')
            
            if emoji.is_unicode_emoji():
                description_parts.append('\\:')
                description_parts.append(emoji.name.replace('_', '\\_'))
                description_parts.append('\\:')
            else:
                description_parts.append(escape_markdown(emoji.as_emoji))
            
            emoji_index += 1
            if emoji_index == emoji_limit:
                break
            
            description_parts.append(' | ')
            continue
        
        channel_index += 1
        if channel_index == channel_limit:
            break
        
        if get_first_client(channel) is None:
            description_parts.append(' (missing permissions)')
        
        description_parts.append('\n')
        continue
    
    return ''.join(description_parts)


def build_reaction_copy_list_channels_response(guild, enabled, flags):
    """
    Lists the reaction-message target channel listing.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to build listing for.
    enabled : `bool`
        Whether the feature is enabled.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    without_category, with_category = collect_channels_with_emojis(guild, flags)
    
    embed = Embed(
        f'{guild.name}\'s reaction-copy channels',
        f'Parsing: {get_reaction_copy_flag_parse_names(flags)}.',
    ).add_thumbnail(
        guild.icon_url,
    )
    
    if (without_category is None) and (not with_category):
        embed.add_field(
            '\u200b',
            '*no match*',
        )
    
    else:
        if (without_category is not None):
            embed.add_field(
                '\u200b',
                build_description(without_category),
            )
        
        for parent, sorted_channels_and_emojis in islice(with_category, None, 25):
            embed.add_field(
                parent.name,
                build_description(sorted_channels_and_emojis),
            )
    
    
    if not enabled:
        embed.add_footer('!! Reaction-copy is disabled in the guild !!')
    
    return InteractionResponse(
        components = COMPONENTS,
        embed = embed,
    )
