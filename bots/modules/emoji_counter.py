from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from math import ceil

from hata import Client, parse_custom_emojis, Embed, EMOJIS, STICKERS
from hata.ext.slash import set_permission, abort

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func as alchemy_function, and_, distinct
from sqlalchemy.sql import select, desc

from bot_utils.models import DB_ENGINE, emoji_counter_model, EMOJI_COUNTER_TABLE, sticker_counter_model, \
    STICKER_COUNTER_TABLE
from bot_utils.shared import GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__EMOJI_MANAGER

Satori: Client
SLASH_CLIENT: Client

EMOJI_ACTION_TYPE_MESSAGE_CREATE= 1
EMOJI_ACTION_TYPE_REACTION = 2

RELATIVE_MONTH = relativedelta(months=1)

MONTH = timedelta(days=367, hours=6)/12

@Satori.events
async def message_create(client, message):
    if message.channel.guild is not GUILD__NEKO_DUNGEON:
        return
    
    user = message.author
    if user.is_bot:
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
    if message.channel.guild is not GUILD__NEKO_DUNGEON:
        return
    
    user = message.author
    if user.is_bot:
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
        custom_emojis = new_custom_emojis-old_custom_emojis
    
    timestamp = message.edited_at
    if timestamp is None:
        timestamp = message.created_at
    
    await upload_emojis(custom_emojis, user.id, timestamp)



async def upload_emojis(emojis, user_id, timestamp):
    data = None
    
    for emoji in emojis:
        if emoji.guild is not GUILD__NEKO_DUNGEON:
            continue
        
        if data is None:
            data = []
        
        data.append({
            'user_id': user_id,
            'emoji_id': emoji.id,
            'timestamp': timestamp,
            'action_type': EMOJI_ACTION_TYPE_MESSAGE_CREATE,
        })
    
    if (data is not None):
        async with DB_ENGINE.connect() as connector:
            await connector.execute(insert(EMOJI_COUNTER_TABLE, data))


async def upload_stickers(stickers, user_id, timestamp):
    data = None
    
    for sticker in stickers:
        if sticker.guild_id != GUILD__NEKO_DUNGEON.id:
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
    if emoji.guild is not GUILD__NEKO_DUNGEON:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(EMOJI_COUNTER_TABLE.delete(). \
            where(emoji_counter_model.emoji_id == emoji.id)
        )

@Satori.events
async def sticker_delete(client, sticker):
    if sticker.guild is not GUILD__NEKO_DUNGEON:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(STICKER_COUNTER_TABLE.delete(). \
            where(sticker_counter_model.sticker_id == sticker.id)
        )


@Satori.events
async def reaction_add(client, event):
    user = event.user
    if user.is_bot:
        return
    
    emoji = event.emoji
    if emoji.guild is not GUILD__NEKO_DUNGEON:
        return
    
    user_id = user.id
    timestamp = datetime.utcnow()
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(EMOJI_COUNTER_TABLE.insert().values(
            user_id         = user_id,
            emoji_id        = emoji.id,
            timestamp       = timestamp,
            action_type     = EMOJI_ACTION_TYPE_REACTION,
        ))


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def emoji_top_list(event,
        user: ('user', 'By who?') = None,
        count: (range(10, 91, 10), 'The maximal amount of emojis to show') = 30,
        months: (range(1, 13), 'The months to get') = 1,
            ):
    """List the most used emojis at ND by you or by the selected user."""
    if user is None:
        user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([
                emoji_counter_model.emoji_id,
                alchemy_function.count(emoji_counter_model.emoji_id).label('total'),
            ]). \
            where(and_(
                emoji_counter_model.user_id == user.id,
                emoji_counter_model.timestamp > datetime.utcnow()-RELATIVE_MONTH*months,
            )). \
            limit(count). \
            group_by(emoji_counter_model.emoji_id). \
            order_by(desc('total'))
        )
        
        results = await response.fetchall()
    
    embed = Embed(
        f'Most used emojis by {user.full_name}',
        color = user.color_at(GUILD__NEKO_DUNGEON),
    ).add_thumbnail(user.avatar_url)
    
    if results:
        description_parts = []
        start = 1
        index = 0
        
        for emoji_id, count in results:
            try:
                emoji = EMOJIS[emoji_id]
            except KeyError:
                continue
            
            index += 1
            
            description_parts.append(f'{index}.: {emoji.as_emoji} x **{count}**')
            if not index%10:
                description = '\n'.join(description_parts)
                description_parts.clear()
                embed.add_field(f'{start} - {index}', description, inline=True)
                
                start = index+1
        
        if description_parts:
            description = '\n'.join(description_parts)
            embed.add_field(f'{start} - {index}', description, inline=True)
    
    else:
        embed.description = '*no recorded data*'
    
    return embed


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def sticker_top_list(event,
        user: ('user', 'By who?') = None,
        months: (range(1, 13), 'The months to get') = 1,
            ):
    """List the most used stickers at ND by you or by the selected user."""
    if user is None:
        user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([
                sticker_counter_model.sticker_id,
                alchemy_function.count(sticker_counter_model.sticker_id).label('total'),
            ]). \
            where(and_(
                sticker_counter_model.user_id == user.id,
                sticker_counter_model.timestamp > datetime.utcnow()-RELATIVE_MONTH*months,
            )). \
            group_by(sticker_counter_model.sticker_id). \
            order_by(desc('total'))
        )
        
        results = await response.fetchall()
    
    if results:
        description_parts = []
        
        for index, (sticker_id, count) in enumerate(results, 1):
            try:
                sticker = STICKERS[sticker_id]
            except KeyError:
                continue
            
            index += 1
            
            description_parts.append(f'{index}.: {sticker.name} x **{count}**')
        
        description = '\n'.join(description_parts)
    
    else:
        description = '*no recorded data*'
    
    embed = Embed(
        f'Most used stickers by {user.full_name}',
        description,
        color = user.color_at(GUILD__NEKO_DUNGEON),
    ).add_thumbnail(user.avatar_url)
    
    return embed


EMOJI_LIST = SLASH_CLIENT.interactions(
    set_permission(
        GUILD__NEKO_DUNGEON,
        ROLE__NEKO_DUNGEON__EMOJI_MANAGER,
        True
    )(None),
    name = 'emoji-list',
    description = 'Emoji list commands.',
    guild = GUILD__NEKO_DUNGEON,
    allow_by_default = False,
)

@EMOJI_LIST.interactions
async def sync_emojis(event):
    """Syncs emoji list emojis."""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__EMOJI_MANAGER):
        abort(f'You must have {ROLE__NEKO_DUNGEON__EMOJI_MANAGER:m} role to invoke this command.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([emoji_counter_model.emoji_id]).distinct(emoji_counter_model.emoji_id),
        )
        
        results = await response.fetchall()
        
        emoji_ids = [result[0] for result in results]
        guild_emojis = GUILD__NEKO_DUNGEON.emojis
        
        emoji_ids_to_remove = [emoji_id for emoji_id in emoji_ids if (emoji_id not in guild_emojis)]
        
        if emoji_ids_to_remove:
            await connector.execute(
                EMOJI_COUNTER_TABLE.delete().where(
                    emoji_counter_model.emoji_id.in_(emoji_ids_to_remove)
                )
            )
    
    return f'Unused emoji entries removed: {len(emoji_ids_to_remove)}'


@EMOJI_LIST.interactions
async def sync_users(event):
    """Syncs emoji list users."""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__EMOJI_MANAGER):
        abort(f'You must have {ROLE__NEKO_DUNGEON__EMOJI_MANAGER:m} role to invoke this command.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([emoji_counter_model.user_id]).distinct(emoji_counter_model.user_id),
        )
        
        results = await response.fetchall()
        
        user_ids = [result[0] for result in results]
        guild_users = GUILD__NEKO_DUNGEON.users
        
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


@EMOJI_LIST.interactions
async def user_based_statistic(client, event,
        months: (range(1, 13), 'The months to get') = 1,
            ):
    
    low_date_limit = datetime.utcnow()-RELATIVE_MONTH*months
    
    async with DB_ENGINE.connect() as connector:
        
        response = await connector.execute(
            select([
                emoji_counter_model.emoji_id,
                alchemy_function.count(emoji_counter_model.user_id),
            ]). \
            where(and_(
                emoji_counter_model.timestamp > low_date_limit,
            )). \
            group_by(emoji_counter_model.emoji_id)
        )
        
        results = await response.fetchall()
    
    date_difference = MONTH*months
    
    items = []
    
    guild_emojis = set(GUILD__NEKO_DUNGEON.emojis.values())
    for emoji_id, count in results:
        try:
            emoji = EMOJIS[emoji_id]
        except KeyError:
            continue
        
        guild_emojis.discard(emoji)
        
        emoji_created_at = emoji.created_at
        if emoji_created_at > low_date_limit:
            count = ceil((1.0-((emoji_created_at-low_date_limit))/date_difference)*count)
        
        items.append((emoji, count))
    
    for emoji in guild_emojis:
        items.append((emoji, 0))
    
    items.sort(key=item_sort_key)
    del items[50:]
    
    description_parts = []
    for index, (emoji, count) in enumerate(items, 1):
        description_parts.append(f'{index}.: {emoji.as_emoji} x **{count}**')
    
    description = '\n'.join(description_parts)
    
    return Embed('Most not used emojis:', description)
