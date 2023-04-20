__all__ = ()

from itertools import chain

from hata import Embed, parse_all_emojis
from hata.ext.slash import abort


def collect_channels_with_emojis(client, guild):
    """
    Parameters
    ----------
    client : ``Client``
        The respective client to check permissions with.
    guild : ``Guild``
        The guild to look up.
    
    Returns
    -------
    group_0, groups : `None` | (``Channel``, `list` of ``Emoji``), \
        `dict` of (``channel``, (``Channel``, `list` of ``Emoji``)) items
    """
    emojis_to_channels = collect_emojis_to_channels(client, guild)
    channels_to_emojis = filter_emojis_to_channels(emojis_to_channels)
    return group_and_channels_to_emojis(channels_to_emojis)


def collect_emojis_to_channels(client, guild):
    """
    Collects the emojis and their related channels of the guild where the client has the required permissions.
    
    Parameters
    ----------
    client : ``Client``
        The respective client to check permissions with.
    guild : ``Guild``
        The guild to look up.
    
    Returns
    -------
    emojis_to_channels : `dict` of (``Emoji``, `set` of ``Channel``) items
    """
    emojis_to_channels = {}
    
    for channel in chain(guild.channels.values(), guild.threads.values()):
        if not channel.is_in_group_guild_textual():
            continue
        
        if not channel.cached_permissions_for(client).can_manage_webhooks:
            continue
        
        channel_name_emojis = parse_all_emojis(channel.name)
        topic = channel.topic
        if (topic is None):
            channel_emojis = channel_name_emojis
        else:
            channel_emojis = channel_name_emojis | parse_all_emojis(topic)
        
        for emoji in channel_emojis:
            if emoji.is_unicode_emoji():
                try:
                    channels = emojis_to_channels[emoji]
                except KeyError:
                    channels = set()
                    emojis_to_channels[emoji] = channels
                
                channels.add(channel)
    
    return emojis_to_channels


def filter_emojis_to_channels(emojis_to_channels):
    """
    Filters the given emojis to channels relation mapping.
    
    Parameters
    ----------
    emojis_to_channels : `dict` of (``Emoji``, `set` of ``Channel``) items
        Emojis to channels relations.
    
    Returns
    -------
    channels_to_emojis : `dict` of (``Channel``, `list` of ``Emoji``) items
        Channels to emojis relations.
    """
    channels_to_emojis = {}
    
    for emoji, channels in emojis_to_channels.items():
        if len(channels) != 1:
            continue
            
        channel = channels.pop()
        try:
            emojis = channels_to_emojis[channel]
        except KeyError:
            emojis = []
            channels_to_emojis[channel] = emojis
        
        emojis.append(emoji)
    
    return channels_to_emojis


def group_and_channels_to_emojis(channels_to_emojis):
    """
    Groups up the channels by category.
    
    Parameters
    ----------
    channels_to_emojis : `dict` of (``Channel``, `list` of ``Emoji``) items
        Channels to emojis relations.
    
    Returns
    -------
    group_0, groups : `None` | (``Channel``, `list` of ``Emoji``), \
        `dict` of (``channel``, (``Channel``, `list` of ``Emoji``)) items
    """
    group_0 = None
    groups_channels_to_emojis = {}
    
    for channel, emojis in channels_to_emojis.items():
        parent = channel.parent
        if parent is None:
            group_0 = (channel, emojis)
            continue
        
        try:
            group = groups_channels_to_emojis[parent]
        except KeyError:
            group = []
            groups_channels_to_emojis[parent] = group
        
        group.append((channel, emojis))
    
    if (group_0 is not None):
        group_0[1].sort(key = _emojis_sort_key)
    
    for channels_and_emojis in groups_channels_to_emojis.values():
        sort_channels_and_emojis(channels_and_emojis)
    
    groups = sorted(groups_channels_to_emojis.items(), key = _group_sort_key)
    return group_0, groups


def _group_sort_key(item):
    """
    Sort key used for sorting groups.
    
    Parameters
    ----------
    item : `tuple` (``Channel``, `list` of `tuple` (``Channel``, `list` of ``Emoji``))
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
    item : `tuple` (``Channel``, `list` of ``Emoji``)
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
    sort_key : `tuple` (`str`, `int`)
    """
    return emoji.name, emoji.id


def sort_channels_and_emojis(channels_and_emojis):
    """
    Sorts the given channels and emojis group.
    
    Parameters
    ----------
    channels_and_emojis : `list` of `tuple` (``Channel``, `list` of ``Emoji``)
        The item to get it's sort key of.
    """
    channels_and_emojis.sort(key = _channels_and_emojis_sort_key)
    
    for item in channels_and_emojis:
        item[1].sort(key = _emojis_sort_key)


def build_description(sorted_channels_and_emojis):
    """
    Builds description of the given channels and their respective emojis combination.
    
    Parameters
    ----------
    sorted_channels_and_emojis : `tuple` (``Channel``, `list` of ``Emoji``)
        
    
    Returns
    -------
    description : `str`
    """
    # limit the amount of channels to show
    description_parts = []
    
    channel_index = 0
    channel_limit = len(sorted_channels_and_emojis)
    if channel_limit > 20:
        channel_limit = 20
    
    while True:
        channel, emojis = sorted_channels_and_emojis[channel_index]
        
        description_parts.append(channel.mention)
        description_parts.append(' : ')
        
        emoji_index = 0
        emoji_limit = len(emojis)
        if emoji_limit > 10:
            emoji_limit = 10
        
        while True:
            emoji = emojis[emoji_index]
            
            description_parts.append(emoji.as_emoji)
            description_parts.append(' \:')
            description_parts.append(emoji.name.replace('_', '\_'))
            description_parts.append('\:')
            
            emoji_index += 1
            if emoji_index == emoji_limit:
                break
            
            description_parts.append(' | ')
            continue
        
        channel_index += 1
        if channel_index == channel_limit:
            break
        
        description_parts.append('\n')
        continue
    
    return ''.join(description_parts)


async def copy_message_list_channels(client, event):
    """Lists the copy-message target channels."""
    guild = event.guild
    if guild is None:
        return abort('guild out of cache')
    
    group_0, groups = collect_channels_with_emojis(client, guild)
    
    embed = Embed(
        f'{guild.name}\'s copy-message channels',
    ).add_thumbnail(
        guild.icon_url,
    )
    
    if (group_0 is None) and (not groups):
        embed.description = '*no match*'
    else:
        if (group_0 is not None):
            embed.description = build_description(group_0)
        
        if groups:
            del groups[25:]
            
            for parent, sorted_channels_and_emojis in groups:
                embed.add_field(
                    parent.name,
                    build_description(sorted_channels_and_emojis),
                )
    
    return embed
