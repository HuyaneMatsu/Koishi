from datetime import datetime, timedelta

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

MOON_DAY = timedelta(days=28)


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
    
    emojis = []
    for emoji in custom_emojis:
        if emoji.guild is GUILD__NEKO_DUNGEON:
            emojis.append(emoji)
    
    if not emojis:
        return
    
    user_id = user.id
    timestamp = message.created_at
    
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
        user:('user', 'By who?', 'by')=None,
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
                emoji_counter_model.timestamp > datetime.utcnow()-MOON_DAY,
            )). \
            limit(30). \
            group_by(emoji_counter_model.emoji_id). \
            order_by(desc('total'))
        )
        
        results = await response.fetchall()
    
    embed = Embed(
            f'Most used emojis by {user.full_name}',
            color = user.color_at(GUILD__NEKO_DUNGEON),
        ). \
        add_thumbnail(user.avatar_url)
    
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



