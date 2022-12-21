__all__ = ()
from hata import BUILTIN_EMOJIS, ChannelType, DATETIME_FORMAT_CODE, elapsed_time


EMOJI_HEART_GIFT = BUILTIN_EMOJIS['gift_heart']

CHANNEL_TYPES_AND_NAMES = (
    (ChannelType.guild_text, 'Text'),
    (ChannelType.guild_announcements, 'Announcements'),
    (ChannelType.guild_voice, 'Voice'),
    (ChannelType.guild_stage, 'Stage'),
    (ChannelType.guild_category, 'Category'),
    (ChannelType.guild_forum, 'Forum'),
)


async def add_guild_all_field(client, guild, embed, even_if_empty):
    """
    Adds every field to the given embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild in context.
    embed : ``Embed``
        The embed to extend.
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    """
    await add_guild_info_field(client, guild, embed, False)
    await add_guild_counts_field(client, guild, embed, False)
    await add_guild_emojis_field(client, guild, embed, False)
    await add_guild_stickers_field(client, guild, embed, False)
    await add_guild_boosters_field(client, guild, embed, False)


async def add_guild_info_field(client, guild, embed, even_if_empty):
    """
    Adds generic guild info field to the given embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild in context.
    embed : ``Embed``
        The embed to extend.
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    """
    created_at = guild.created_at
    sections_parts = [
        '**Created**: ', created_at.__format__(DATETIME_FORMAT_CODE), ' [*', elapsed_time(created_at), ' ago*]'
    ]
    
    features = guild.features
    if features:
        sections_parts.append('\n**Features**: ')
        for feature in features:
            sections_parts.append(feature.name)
            sections_parts.append(', ')
        
        del sections_parts[-1]
    
    embed.add_field('Guild information', ''.join(sections_parts))


async def add_guild_counts_field(client, guild, embed, even_if_empty):
    """
    Adds generic guild counts field to the given embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild in context.
    embed : ``Embed``
        The embed to extend.
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    """
    # approximate_user_count = guild.approximate_user_count
    # if approximate_user_count == 0:
    #     await client.guild_get(guild)
    #     approximate_user_count = guild.approximate_user_count
    
    sections_parts = [
        '**Users: ', str(guild.user_count), '**\n'
        '**Roles: ', str(len(guild.roles)), '**'
    ]
    
    channel_counts_by_type = {}
    
    for channel in guild.channels.values():
        channel_type = channel.type
        channel_counts_by_type[channel_type] = channel_counts_by_type.get(channel_type, 0) + 1
    
    
    for channel_type, channel_name in CHANNEL_TYPES_AND_NAMES:
        try:
            channel_count = channel_counts_by_type[channel_type]
        except KeyError:
            continue
        
        sections_parts.append('\n**')
        sections_parts.append(channel_name)
        sections_parts.append(' channels: ')
        sections_parts.append(str(channel_count))
        sections_parts.append('**')
    
    embed.add_field('Counts', ''.join(sections_parts))


async def add_guild_emojis_field(client, guild, embed, even_if_empty):
    """
    Adds emojis field to the given embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild in context.
    embed : ``Embed``
        The embed to extend.
    even_if_empty : `bool`
        Whether the field should be added even if there are no emojis.
    """
    emoji_count = len(guild.emojis)
    if emoji_count:
        sections_parts = [
            '**Total: ', str(emoji_count), '**\n'
            '**Static emojis: '
        ]
        
        normal_static, normal_animated, managed_static, managed_animated = guild.emoji_counts
        emoji_limit = guild.emoji_limit
        sections_parts.append(str(normal_static))
        sections_parts.append('** [')
        sections_parts.append(str(emoji_limit - normal_static))
        sections_parts.append(
            ' free]\n'
            '**Animated emojis: '
        )
        sections_parts.append(str(normal_animated))
        sections_parts.append('** [')
        sections_parts.append(str(emoji_limit - normal_animated))
        sections_parts.append(' free]')
        
        managed_total = managed_static + managed_animated
        if managed_total:
            sections_parts.append('\n**Managed: ')
            sections_parts.append(str(managed_total))
            sections_parts.append('** [')
            sections_parts.append(str(managed_static))
            sections_parts.append(' static, ')
            sections_parts.append(str(managed_animated))
            sections_parts.append(' animated]')
        
        embed.add_field('Emojis', ''.join(sections_parts))
    
    elif even_if_empty:
        embed.add_field('Emojis', '*The guild has no emojis*')


async def add_guild_stickers_field(client, guild, embed, even_if_empty):
    """
    Adds stickers field to the given embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild in context.
    embed : ``Embed``
        The embed to extend.
    even_if_empty : `bool`
        Whether the field should be added even if there are no stickers.
    """
    sticker_count = len(guild.stickers)
    if sticker_count:
        sections_parts = [
            '**Total: ', str(sticker_count), '** [', str(guild.sticker_limit - sticker_count), ' free]\n'
            '**Static stickers: '
        ]
        
        static_count, animated_count, lottie_count = guild.sticker_counts
        
        sections_parts.append(str(static_count))
        sections_parts.append(
            '**\n'
            '**Animated stickers: '
        )
        sections_parts.append(str(animated_count))
        sections_parts.append('**')
        
        if lottie_count:
            sections_parts.append('\n**Lottie stickers:')
            sections_parts.append(str(lottie_count))
            sections_parts.append('**')

        embed.add_field('Stickers', ''.join(sections_parts))
    
    elif even_if_empty:
        embed.add_field('Stickers', '*The guild has no stickers*')


async def add_guild_boosters_field(client, guild, embed, even_if_empty):
    """
    Adds guild boosters field to the given embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild in context.
    embed : ``Embed``
        The embed to extend.
    even_if_empty : `bool`
        Whether the field should be added even if there are no boosters.
    """
    boost_count = guild.boost_count
    if boost_count:
        
        boosters = guild.boosters
        count = len(boosters)
        
        embed.add_field(
            f'Most awesome people of the guild',
            f'{boost_count} boosts {EMOJI_HEART_GIFT} | {count} people {EMOJI_HEART_GIFT}'
        )
        
        for user in boosters[:21]:
            embed.add_field(user.full_name,
                f'since: {elapsed_time(user.get_guild_profile_for(guild).boosts_since)}')
        
        embed.add_footer('The displayed users might be just a subset of the reality')
    
    elif even_if_empty:
        embed.add_field(
            f'Most awesome people of the guild',
            '*The guild has no chicken nuggets.*',
        )
