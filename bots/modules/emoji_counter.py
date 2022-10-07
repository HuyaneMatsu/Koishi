__all__ = ()

from datetime import datetime, timedelta
from math import log, floor
from dateutil.relativedelta import relativedelta
from hata import Client, parse_custom_emojis, Embed, EMOJIS, parse_emoji, USERS
from hata.ext.slash import abort
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func as alchemy_function, and_
from sqlalchemy.sql import select, desc

from bot_utils.models import DB_ENGINE, emoji_counter_model, EMOJI_COUNTER_TABLE, sticker_counter_model, \
    STICKER_COUNTER_TABLE
from bot_utils.constants import GUILD__SUPPORT, ROLE__SUPPORT__EMOJI_MANAGER

Satori: Client
SLASH_CLIENT: Client

EMOJI_ACTION_TYPE_MESSAGE_CONTENT = 1
EMOJI_ACTION_TYPE_REACTION = 2

RELATIVE_MONTH = relativedelta(months=1)

MONTH = timedelta(days=367, hours=6) / 12

MOST_USED_PER_PAGE = 90

@Satori.events
async def message_create(client, message):
    if message.guild is not GUILD__SUPPORT:
        return
    
    user = message.author
    if user.bot:
        return
    
    content = message.content
    if content:
        custom_emojis = parse_custom_emojis(content)
        if custom_emojis:
            await upload_emojis(custom_emojis, user.id, message.created_at)
    
    stickers = message.stickers
    if (stickers is not None):
         await upload_stickers(stickers, user.id, message.created_at)


@Satori.events
async def message_edit(client, message, old_attributes):
    if (old_attributes is None):
        # The was not cached, we cannot calculate difference.
        return
    
    if message.guild is not GUILD__SUPPORT:
        return
    
    user = message.author
    if user.bot:
        return
    
    try:
        old_content = old_attributes['content']
    except KeyError:
        return
    
    new_content = message.content
    if not new_content:
        return
    
    new_custom_emojis = parse_custom_emojis(new_content)
    if not new_custom_emojis:
        return
    
    if old_content:
        old_custom_emojis = parse_custom_emojis(old_content)
        if not old_custom_emojis:
            old_custom_emojis = None
    else:
        old_custom_emojis = None
    
    if (old_custom_emojis is None):
        custom_emojis = new_custom_emojis
    else:
        custom_emojis = new_custom_emojis - old_custom_emojis
    
    timestamp = message.edited_at
    if timestamp is None:
        timestamp = message.created_at
    
    await upload_emojis(custom_emojis, user.id, timestamp)



async def upload_emojis(emojis, user_id, timestamp):
    data = None
    
    for emoji in emojis:
        if emoji.guild is not GUILD__SUPPORT:
            continue
        
        if data is None:
            data = []
        
        data.append({
            'user_id': user_id,
            'emoji_id': emoji.id,
            'timestamp': timestamp,
            'action_type': EMOJI_ACTION_TYPE_MESSAGE_CONTENT,
        })
    
    if (data is not None):
        async with DB_ENGINE.connect() as connector:
            await connector.execute(insert(EMOJI_COUNTER_TABLE, data))


async def upload_stickers(stickers, user_id, timestamp):
    data = None
    
    for sticker in stickers:
        if sticker.guild_id != GUILD__SUPPORT.id:
            continue
        
        if data is None:
            data = []
        
        data.append({
            'user_id': user_id,
            'sticker_id': sticker.id,
            'timestamp': timestamp,
        })
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(insert(STICKER_COUNTER_TABLE, data))


@Satori.events
async def emoji_delete(client, emoji):
    if emoji.guild is not GUILD__SUPPORT:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EMOJI_COUNTER_TABLE.delete().where(
                emoji_counter_model.emoji_id == emoji.id,
            )
        )

@Satori.events
async def sticker_delete(client, sticker):
    if sticker.guild is not GUILD__SUPPORT:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            STICKER_COUNTER_TABLE.delete().where(
                sticker_counter_model.sticker_id == sticker.id,
            )
        )


@Satori.events
async def reaction_add(client, event):
    user = event.user
    if user.bot:
        return
    
    emoji = event.emoji
    if emoji.guild is not GUILD__SUPPORT:
        return
    
    user_id = user.id
    timestamp = datetime.utcnow()
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EMOJI_COUNTER_TABLE.insert().values(
                user_id = user_id,
                emoji_id = emoji.id,
                timestamp = timestamp,
                action_type = EMOJI_ACTION_TYPE_REACTION,
            )
        )


ORDER_DECREASING = 1
ORDER_INCREASING = 0
ORDERS = [
    ('decreasing', ORDER_DECREASING),
    ('increasing', ORDER_INCREASING),
    
]

EMOJI_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'emoji',
    description = 'Emoji counter commands.',
    guild = GUILD__SUPPORT,
)


EMOJI_COMMAND_ACTION_TYPE_ALL = 0

EMOJI_COMMAND_ACTION_TYPES = [
    ('all', EMOJI_COMMAND_ACTION_TYPE_ALL),
    ('emoji', EMOJI_ACTION_TYPE_MESSAGE_CONTENT),
    ('reaction', EMOJI_ACTION_TYPE_REACTION),
]


def get_adjust_length(index, page_size, limit):
    end = index + page_size
    if end > limit:
        end = limit
    
    return 1 + floor(log(end, 10))


def add_emoji_into(into, emoji, index, count, adjust_length):
    into.append('`')
    index_string = str(index)
    into.append(index_string)
    into.append(' ' * (adjust_length - len(index_string)))
    into.append('.` ')
    into.append(emoji.as_emoji)
    
    into.append(' `x ')
    into.append(str(count))
    into.append('`')


@EMOJI_COMMANDS.interactions
async def user_top(event,
    user: ('user', 'By who?') = None,
    count: (range(10, 91, 10), 'The maximal amount of emojis to show') = 30,
    months: (range(1, 13), 'The months to get') = 1,
    action_type: (EMOJI_COMMAND_ACTION_TYPES, ('Choose emoji action type')) = EMOJI_COMMAND_ACTION_TYPE_ALL,
):
    """List the most used emojis at ND by you or by the selected user."""
    if user is None:
        user = event.user
    
    async with DB_ENGINE.connect() as connector:
        statement = (
            select(
                [
                    emoji_counter_model.emoji_id,
                    alchemy_function.count(emoji_counter_model.emoji_id).label('total'),
                ]
            ).where(
                and_(
                    emoji_counter_model.user_id == user.id,
                    emoji_counter_model.timestamp > datetime.utcnow() - RELATIVE_MONTH * months,
                )
            ).limit(
                count,
            ).group_by(
                emoji_counter_model.emoji_id,
            ).order_by(
                desc('total'),
            )
        )
        
        if (action_type != EMOJI_COMMAND_ACTION_TYPE_ALL):
            statement = statement.where(emoji_counter_model.action_type==action_type)
        
        response = await connector.execute(statement)
        results = await response.fetchall()
    
    embed = Embed(
        f'Most used emojis by {user.full_name}',
        color = user.color_at(GUILD__SUPPORT),
    ).add_thumbnail(
        user.avatar_url,
    )
    
    _populate_embed_with_fields(embed, results, EMOJI_MOST_USED_TYPE_ALL, True, 1, count)
    
    return embed


@EMOJI_COMMANDS.interactions
async def emoji_top(
    raw_emoji: ('str', 'Pick an emoji', 'emoji'),
    months: (range(1, 13), 'The months to get') = 1,
    action_type: (EMOJI_COMMAND_ACTION_TYPES, ('Choose emoji action type')) = EMOJI_COMMAND_ACTION_TYPE_ALL,
):
    """List the users using the given emoji the most."""
    emoji = parse_emoji(raw_emoji)
    if emoji is None:
        emoji = GUILD__SUPPORT.get_emoji_like(raw_emoji)
        if emoji is None:
            abort(f'`{raw_emoji}` is not an emoji.')
    else:
        if emoji.is_unicode_emoji():
            abort(f'{emoji} is an unicode emoji. Please give custom.')
        
        if emoji.guild is not GUILD__SUPPORT:
            abort(f'{emoji} is bound to an other guild.')
    
    async with DB_ENGINE.connect() as connector:
        statement = (
            select(
                [
                    emoji_counter_model.user_id,
                    alchemy_function.count(emoji_counter_model.user_id).label('total'),
                ],
            ).where(
                and_(
                    emoji_counter_model.emoji_id == emoji.id,
                    emoji_counter_model.timestamp > datetime.utcnow() - RELATIVE_MONTH * months,
                ),
            ).limit(
                30,
            ).group_by(
                emoji_counter_model.user_id,
            ).order_by(
                desc('total'),
            )
        )
        
        if (action_type != EMOJI_COMMAND_ACTION_TYPE_ALL):
            statement = statement.where(emoji_counter_model.action_type==action_type)
        
        response = await connector.execute(statement)
        results = await response.fetchall()
    
    
    if results:
        index = 0
        limit = len(results)
        description_parts = []
        
        while True:
            user_id, count = results[index]
            
            index += 1
            
            try:
                user = USERS[user_id]
            except KeyError:
                continue
            
            guild_profile = user.get_guild_profile_for(GUILD__SUPPORT)
            if (guild_profile is None):
                nick = None
            else:
                nick = guild_profile.nick
            
            description_parts.append(str(index))
            description_parts.append('.: **')
            description_parts.append(str(count))
            description_parts.append('** x ')
            description_parts.append(user.full_name)
            if (nick is not None):
                description_parts.append(' *[')
                description_parts.append(nick)
                description_parts.append(']*')
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
        
        description = ''.join(description_parts)
    else:
        description = '*No usages recorded*'
    
    
    return Embed(
        f'Top emoji users of {emoji.name}',
        description,
    ).add_thumbnail(
        emoji.url,
    )



EMOJI_SYNC_COMMANDS = EMOJI_COMMANDS.interactions(None,
    name = 'sync',
    description = 'Syncs emoji table. (You must have emoji-council role)',
)

@EMOJI_SYNC_COMMANDS.interactions
async def sync_emojis_(event):
    """Syncs emoji list emojis. (You must have emoji-council role)"""
    if not event.user.has_role(ROLE__SUPPORT__EMOJI_MANAGER):
        abort(f'You must have {ROLE__SUPPORT__EMOJI_MANAGER:m} role to invoke this command.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([emoji_counter_model.emoji_id]).distinct(emoji_counter_model.emoji_id),
        )
        
        results = await response.fetchall()
        
        emoji_ids = [result[0] for result in results]
        guild_emojis = GUILD__SUPPORT.emojis
        
        emoji_ids_to_remove = [emoji_id for emoji_id in emoji_ids if (emoji_id not in guild_emojis)]
        
        if emoji_ids_to_remove:
            await connector.execute(
                EMOJI_COUNTER_TABLE.delete().where(
                    emoji_counter_model.emoji_id.in_(emoji_ids_to_remove)
                )
            )
    
    return f'Unused emoji entries removed: {len(emoji_ids_to_remove)}'


@EMOJI_SYNC_COMMANDS.interactions
async def sync_users_(event):
    """Syncs emoji list users. (You must have emoji-council role)"""
    if not event.user.has_role(ROLE__SUPPORT__EMOJI_MANAGER):
        abort(f'You must have {ROLE__SUPPORT__EMOJI_MANAGER:m} role to invoke this command.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([emoji_counter_model.user_id]).distinct(emoji_counter_model.user_id),
        )
        
        results = await response.fetchall()
        
        user_ids = [result[0] for result in results]
        guild_users = GUILD__SUPPORT.users
        
        user_ids_to_remove = [user_id for user_id in user_ids if (user_id not in guild_users)]
        
        if user_ids_to_remove:
            await connector.execute(
                EMOJI_COUNTER_TABLE.delete().where(
                    emoji_counter_model.user_id.in_(user_ids_to_remove)
                )
            )
    
    return f'Unused user entries removed: {len(user_ids_to_remove)}'



def item_sort_key(item):
    return item[1]

EMOJI_MOST_USED_TYPE_ALL = 0
EMOJI_MOST_USED_TYPE_STATIC = 1
EMOJI_MOST_USED_TYPE_ANIMATED = 2

EMOJI_MOST_USED_TYPES = [
    ('all', EMOJI_MOST_USED_TYPE_ALL),
    ('static', EMOJI_MOST_USED_TYPE_STATIC),
    ('animated', EMOJI_MOST_USED_TYPE_ANIMATED),
]

def filter_all(emoji):
    return True

def filter_static(emoji):
    return not emoji.animated

def filter_animated(emoji):
    return emoji.animated


EMOJI_MOST_USED_FILTERS = {
    EMOJI_MOST_USED_TYPE_ALL: filter_all,
    EMOJI_MOST_USED_TYPE_STATIC: filter_static,
    EMOJI_MOST_USED_TYPE_ANIMATED: filter_animated,
}


def _populate_embed_with_fields(embed, query_result, type_, order, page, page_size):
    emoji_filter = EMOJI_MOST_USED_FILTERS[type_]
    
    guild_emojis = set(emoji for emoji in GUILD__SUPPORT.emojis.values() if emoji_filter(emoji))
    is_new_limit = datetime.utcnow() - MONTH
    
    items = []
    
    for emoji_id, count in query_result:
        try:
            emoji = EMOJIS[emoji_id]
        except KeyError:
            continue
        
        if not emoji_filter(emoji):
            continue
        
        guild_emojis.discard(emoji)
        
        is_new = (emoji.created_at >= is_new_limit)
        items.append((emoji, count, is_new))
    
    for emoji in guild_emojis:
        is_new = (emoji.created_at >= is_new_limit)
        items.append((emoji, 0, is_new))
    
    items.sort(key=item_sort_key, reverse=order)
    
    page_shift = (page - 1) * page_size
    index = page_shift
    limit = min(len(items), index + page_size)
    
    embed.add_footer(
        f'Page {page} / {(len(items) // page_size) + 1}',
    )
    
    if index >= limit:
        embed.add_field('\u200B', '*Page out of range or no recorded data*')
        return
    
    adjust_length = get_adjust_length(index, 10, limit)
    description_parts = []
    
    while True:
        emoji, count, is_new = items[index]
        index += 1
        
        add_emoji_into(description_parts, emoji, index, count, adjust_length)
        if is_new:
            description_parts.append(' *[New!]*')

        if (not index % 10) or (index == limit):
            description = ''.join(description_parts)
            description_parts.clear()
            embed.add_field('\u200B', description, inline=True)
            
            if (index == limit):
                break
            
            adjust_length = get_adjust_length(index, 10, limit)
            continue
        
        description_parts.append('\n')
        continue


@EMOJI_COMMANDS.interactions
async def most_used(
    months: (range(1, 13), 'The months to get') = 1,
    page: ('int', 'Select a page') = 1,
    type_: (EMOJI_MOST_USED_TYPES, 'Choose emoji type to filter on') = EMOJI_MOST_USED_TYPE_ALL,
    action_type: (EMOJI_COMMAND_ACTION_TYPES, ('Choose emoji action type')) = EMOJI_COMMAND_ACTION_TYPE_ALL,
    order: (ORDERS, 'Ordering?') = ORDER_DECREASING,
):
    """Shows the most used emojis."""
    
    if page < 1:
        abort('Page value can be only positive')
    
    low_date_limit = datetime.utcnow() - RELATIVE_MONTH * months
    
    async with DB_ENGINE.connect() as connector:
        
        statement = (
            select(
                [
                    emoji_counter_model.emoji_id,
                    alchemy_function.count(emoji_counter_model.user_id).label('total'),
                ],
            ).where(
                emoji_counter_model.timestamp > low_date_limit,
            ).group_by(
                emoji_counter_model.emoji_id,
            )
        )
        
        if (action_type != EMOJI_COMMAND_ACTION_TYPE_ALL):
            statement = statement.where(emoji_counter_model.action_type==action_type)
        
        response = await connector.execute(statement)
        results = await response.fetchall()
    
    embed = Embed(
        'Most used emojis:',
    )
    
    _populate_embed_with_fields(embed, results, type_, order, page, MOST_USED_PER_PAGE)
    
    return embed
