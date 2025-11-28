__all__ = ()

from hata import BUILTIN_EMOJIS, ChannelType, DATETIME_FORMAT_CODE, GuildFeature, elapsed_time


EMOJI_HEART_GIFT = BUILTIN_EMOJIS['gift_heart']

CHANNEL_TYPES_AND_NAMES = (
    (ChannelType.guild_text, 'Text'),
    (ChannelType.guild_announcements, 'Announcements'),
    (ChannelType.guild_voice, 'Voice'),
    (ChannelType.guild_stage, 'Stage'),
    (ChannelType.guild_category, 'Category'),
    (ChannelType.guild_forum, 'Forum'),
)

GUILD_BADGE_FEATURES_AND_NAMES = (
    (GuildFeature.badge, 'base'),
    (GuildFeature.badge_pack_flex, 'flex'),
    (GuildFeature.badge_pack_pets, 'pets'),
)

GUILD_OTHER_FEATURES_AND_NAMES = (
    (GuildFeature.role_colors_enhanced, 'unpleasant role gradients'),
)


def produce_guild_info_description(guild, even_if_empty):
    """
    Adds generic guild info field to the given embed.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    """
    created_at = guild.created_at
    yield (
        '## Guild information\n'
        '**Created**: '
    )
    yield format(created_at, DATETIME_FORMAT_CODE)
    yield ' [*'
    yield elapsed_time(created_at)
    yield ' ago*]'
    
    features = guild.features
    if (features is not None):
        features_boost = []
        features_other = []
        for feature in features:
            if feature.flags.boost:
                container = features_boost
            else:
                container = features_other
            
            container.append(feature)
            continue
        
        for features_filtered, name in (
            (features_boost, 'Boost'),
            (features_other, 'Other'),
        ):
            if not features_filtered:
                continue
            
            yield '\n**'
            yield name
            yield ' features**: '
            
            index = 0
            limit = len(features_filtered)
            
            while True:
                feature = features_filtered[index]
                index += 1
                
                yield feature.name
                if index == limit:
                    break
                
                yield ', '
                continue


def produce_guild_counts_description(guild, even_if_empty):
    """
    Produces guild counts description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    
    Yields
    ------
    part : `str`
    """
    yield (
        '## Counts\n'
        '**Users: '
    )
    yield str(guild.user_count)
    yield '**\n**Roles: '
    yield str(len(guild.roles))
    yield '**'
    
    channel_counts_by_type = {}
    
    for channel in guild.channels.values():
        channel_type = channel.type
        channel_counts_by_type[channel_type] = channel_counts_by_type.get(channel_type, 0) + 1
    
    for channel_type, channel_name in CHANNEL_TYPES_AND_NAMES:
        try:
            channel_count = channel_counts_by_type[channel_type]
        except KeyError:
            continue
        
        yield '\n**'
        yield channel_name
        yield ' channels: '
        yield str(channel_count)
        yield '**'


def produce_guild_emojis_description(guild, even_if_empty):
    """
    Guilds guild emojis description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether to produce anything even if there is nothing to produce.
    
    Yields
    ------
    part : `str`
    """
    emoji_count = len(guild.emojis)
    if not emoji_count:
        if even_if_empty:
            yield '## Emojis\n*The guild has no emojis*'
        return
    
    yield '## Emojis\n**Total: '
    yield str(emoji_count)
    yield '**\n**Static emojis: '
    
    emoji_counts = guild.emoji_counts
    normal_static = emoji_counts.normal_static
    normal_animated = emoji_counts.normal_animated
    managed_static = emoji_counts.managed_static
    managed_animated = emoji_counts.managed_animated
    
    emoji_limit = guild.emoji_limit
    yield str(normal_static)
    yield '** ['
    yield str(emoji_limit - normal_static)
    yield ' free]\n**Animated emojis: '
    yield str(normal_animated)
    yield '** ['
    yield str(emoji_limit - normal_animated)
    yield ' free]'
    
    managed_total = managed_static + managed_animated
    if managed_total:
        yield '\n**Managed: '
        yield str(managed_total)
        yield '** ['
        yield str(managed_static)
        yield ' static, '
        yield str(managed_animated)
        yield ' animated]'


def produce_guild_stickers_description(guild, even_if_empty):
    """
    Produces guild stickers description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if there are no stickers.
    
    Yields
    ------
    part : `str`
    """
    sticker_count = len(guild.stickers)
    if not sticker_count:
        if even_if_empty:
            yield '## Stickers\n*The guild has no stickers*'
        return
    
    yield (
        '## Stickers\n'
        '**Total: '
    )
    
    yield str(sticker_count)
    yield '** ['
    yield str(guild.sticker_limit - sticker_count)
    yield ' free]\n**Static stickers: '
    
    sticker_counts = guild.sticker_counts
    static_count = sticker_counts.static
    animated_count = sticker_counts.animated
    lottie_count = sticker_counts.lottie
    
    yield str(static_count)
    yield (
        '**\n'
        '**Animated stickers: '
    )
    yield str(animated_count)
    yield '**'
    
    if lottie_count:
        yield '\n**Lottie stickers: '
        yield str(lottie_count)
        yield '**'


def _produce_limit_vs_granted(title, limit, granted, unit):
    """
    Produces a limit vs specially granted limit description part.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    title : `str`
        The field's title.
    
    limit : `int`
        Limit based on boost level.
    
    granted : `int`
        Specially granted limit.
    
    unit : `None | str`
        Unit to use.
    
    Yields
    ------
    part : `str`
    """
    yield '**'
    yield title
    yield ': '
    
    yield str(max(limit, granted))
    
    if (unit is not None):
        yield ' '
        yield unit
    
    yield '**'
    
    if granted > limit:
        yield ' ['
        yield str(limit)
        
        if (unit is not None):
            yield ' '
            yield unit
        
        yield ']'


def produce_guild_boost_perks_description(guild, even_if_empty):
    """
    Produces guild boost perks description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if there are no stickers.
    
    Yields
    ------
    part : `str`
    """
    yield (
        '## Boost perks\n'
        '**Boost level: '
    )
    yield str(guild.boost_level)
    yield '**\n**Badges:** '
    
    badge_name_produced = False
    for guild_feature, name in GUILD_BADGE_FEATURES_AND_NAMES:
        if not guild.has_feature(guild_feature):
            continue
        
        if badge_name_produced:
            yield ', '
        else:
            badge_name_produced = True
        
        yield name
        continue
    
    if not badge_name_produced:
        yield '*none*'
    
    yield '\n**Others:** '
    
    other_name_produced = False
    for guild_feature, name in GUILD_OTHER_FEATURES_AND_NAMES:
        if not guild.has_feature(guild_feature):
            continue
        
        if other_name_produced:
            yield ', '
        else:
            other_name_produced = True
        
        yield name
        continue
    
    if not other_name_produced:
        yield '*none*'
    
    boost_perks = guild.boost_perks
    yield '\n\n**Attachment size limit: '
    yield str(boost_perks.attachment_size_limit >> 20)
    yield 'MB**\n'
    
    yield from _produce_limit_vs_granted(
        'Bitrate limit',
        (boost_perks.bitrate_limit // 1000),
        (128 if guild.has_feature(GuildFeature.vip_voice_regions) else 0),
        'kbps',
    )
    
    yield '\n**Concurrent activities: '
    concurrent_activities = boost_perks.concurrent_activities
    yield (str(concurrent_activities) if concurrent_activities else 'unlimited')
    yield '**\n'
    
    yield from _produce_limit_vs_granted(
        'Emoji limit',
        boost_perks.emoji_limit,
        (200 if guild.has_feature(GuildFeature.more_emoji) else 0),
        None,
    )
    
    yield '\n'
    
    yield from _produce_limit_vs_granted(
        'Sticker limit',
        boost_perks.sticker_limit,
        (30 if guild.has_feature(GuildFeature.more_sticker) else 0),
        None,
    )
    
    yield '\n'
    
    yield from _produce_limit_vs_granted(
        'Soundboard sound limit',
        boost_perks.soundboard_sound_limit,
        (36 if guild.has_feature(GuildFeature.more_soundboard_sound) else 0),
        None,
    )
    
    yield '\n**Granted features:** '
    
    features = boost_perks.features
    if (features is None):
        yield '*none*'
    
    else:
        feature_produced = False
        for feature in features:
            if feature_produced:
                yield ', '
            else:
                feature_produced = True
            
            yield feature.name
            continue
    
    yield '\n**Screen share frame limit: '
    yield str(boost_perks.screen_share_frame_rate)
    yield '**\n**Screen share resolution: '
    yield boost_perks.screen_share_resolution
    yield '**\n**Stage channel viewer limit: '
    yield str(boost_perks.stage_channel_viewer_limit)
    yield '**'


def produce_guild_boosters_description(guild, even_if_empty):
    """
    Produces guild boosters description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if there are no boosters.
    
    Yields
    ------
    part : `str`
    """
    boost_count = guild.boost_count
    if not boost_count:
        if even_if_empty:
            yield '## Most awesome people of the guild\n*The guild has no chicken nuggets.*'
        return
    
    boosters = guild.boosters
    count = 0 if boosters is None else len(boosters)
    
    yield '## Most awesome people of the guild\n'
    yield EMOJI_HEART_GIFT.as_emoji
    yield ' '
    yield str(boost_count)
    yield ' boosts | '
    yield str(count)
    yield ' people '
    yield EMOJI_HEART_GIFT.as_emoji
    
    if count:
        yield '\n'
        for user in boosters[:20]:
            yield '\n- **'
            yield user.name_at(guild)
            yield '**, since: '
            yield elapsed_time(user.get_guild_profile_for(guild).boosts_since)
    
    yield '\n\n-# The displayed users might be just a subset of the reality'
