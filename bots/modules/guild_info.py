from hata import Embed, Client, elapsed_time, ICON_TYPE_NONE, DATETIME_FORMAT_CODE, BUILTIN_EMOJIS, CHANNEL_TYPES
from hata.ext.slash import abort


SLASH_CLIENT: Client


EMOJI_HEART_GIFT = BUILTIN_EMOJIS['gift_heart']


CHANNEL_TYPES_AND_NAMES = (
    (CHANNEL_TYPES.guild_text, 'Text'),
    (CHANNEL_TYPES.guild_announcements, 'Announcements'),
    (CHANNEL_TYPES.guild_voice, 'Voice'),
    (CHANNEL_TYPES.guild_stage, 'Stage'),
    (CHANNEL_TYPES.guild_category, 'Category'),
    (CHANNEL_TYPES.guild_forum, 'Forum'),
)


async def add_guild_generic_field(client, guild, embed, even_if_empty):
    await add_guild_info_field(client, guild, embed, False)
    await add_guild_counts_field(client, guild, embed, False)
    await add_guild_emojis_field(client, guild, embed, False)
    await add_guild_stickers_field(client, guild, embed, False)


async def add_guild_info_field(client, guild, embed, even_if_empty):
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
    approximate_user_count = guild.approximate_user_count
    if approximate_user_count == 0:
        await client.guild_get(guild)
        approximate_user_count = guild.approximate_user_count
    
    sections_parts = [
        '**Users: ', str(approximate_user_count), '**\n'
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
    sticker_count = len(guild.stickers)
    if sticker_count:
        sections_parts = [
            '**Total: ', str(sticker_count), '** [', str(guild.sticker_limit - sticker_count), ' free]\n'
            '**Static stickers: '
        ]
        
        static_count, animated_count, lottie_count = guild.sticker_count
        
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


DEFAULT_GUILD_FILED = 'generic'

GUILD_FIELDS = {
    DEFAULT_GUILD_FILED : add_guild_generic_field  ,
    'info'              : add_guild_info_field     ,
    'counts'            : add_guild_counts_field   ,
    'emojis'            : add_guild_emojis_field   ,
    'stickers'          : add_guild_stickers_field ,
    'boosters'          : add_guild_boosters_field ,
}

@SLASH_CLIENT.interactions(name='guild', is_global=True)
async def guild_info(client, event,
    field: (list(GUILD_FIELDS.keys()), 'Which fields should I show?') = DEFAULT_GUILD_FILED,
):
    """Shows some information about the guild."""
    guild = event.guild
    if (guild is None) or guild.partial:
        abort('I must be in the guild to execute this command.')
    
    embed = Embed(
        guild.name,
        color = (guild.icon_hash & 0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id >> 22) & 0xFFFFFF),
    ).add_thumbnail(
        guild.icon_url_as(size=128),
    )
    
    await GUILD_FIELDS[field](client, guild, embed, True)
    
    return embed
