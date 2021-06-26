from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from hata import Client, parse_custom_emojis, Embed, EMOJIS

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func as alchemy_function, and_
from sqlalchemy.sql import select, desc

from bot_utils.models import DB_ENGINE, emoji_counter_model, EMOJI_COUNTER_TABLE
from bot_utils.shared import GUILD__NEKO_DUNGEON

Satori: Client
SLASH_CLIENT: Client

EMOJI_ACTION_TYPE_MESSAGE_CREATE= 1
EMOJI_ACTION_TYPE_REACTION = 2

MONTH = relativedelta(months=1)


@Satori.events
async def message_create(client, message):
    if message.channel.guild is not GUILD__NEKO_DUNGEON:
        return
    
    user = message.author
    if user.is_bot:
        return
    
    content = message.content
    if not content:
        return
    
    custom_emojis = parse_custom_emojis(content)
    if not custom_emojis:
        return
    
    await upload_emojis(custom_emojis, user.id, message.created_at)


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



async def upload_emojis(custom_emojis, user_id, timestamp):
    emojis = []
    for emoji in custom_emojis:
        if emoji.guild is GUILD__NEKO_DUNGEON:
            emojis.append(emoji)
    
    if not emojis:
        return
    
    data = []
    for emoji in custom_emojis:
        data.append({
            'user_id': user_id,
            'emoji_id': emoji.id,
            'timestamp': timestamp,
            'action_type': EMOJI_ACTION_TYPE_MESSAGE_CREATE,
        })
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(insert(EMOJI_COUNTER_TABLE, data))

@Satori.events
async def emoji_delete(client, emoji, guild):
    if guild is not GUILD__NEKO_DUNGEON:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(emoji_counter_model.delete(). \
            where(emoji_counter_model.emoji_id == emoji.id)
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
        user: ('user', 'By who?')=None,
        count: (range(10, 91, 10), 'The maximal amount of emojis to show')=30,
        months: (range(1, 13), 'The months to get')=1,
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
                emoji_counter_model.timestamp > datetime.utcnow()-MONTH*months,
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
