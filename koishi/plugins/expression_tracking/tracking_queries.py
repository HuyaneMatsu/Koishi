__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs
from sqlalchemy import and_, or_
from sqlalchemy.dialects.postgresql import insert

from ...bot_utils.models import DB_ENGINE, EXPRESSION_COUNTER_TABLE, expression_counter_model

from .constants import ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION, ACTION_TYPE_STICKER


def _iter_entity_ids_and_action_types_for_message_create(emojis, stickers):
    """
    Iterates over entity id-s and their action types to be inserted on message creation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    emojis : `None | set<Emoji>`
        Emojis to insert.
    
    stickers : `None | set<Sticker>`
        Stickers to insert.
    
    Yields
    ------
    entity_id_and_action_type : `(int, int)`
    """
    if (emojis is not None):
        for emoji in emojis:
            yield emoji.id, ACTION_TYPE_EMOJI_CONTENT
    
    if (stickers is not None):
        for sticker in stickers:
            yield sticker.id, ACTION_TYPE_STICKER


async def execute_message_create(message, emojis, stickers):
    """
    Executes insertions on message creation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    emojis : `None | set<Emoji>`
        Emojis to insert.
    
    stickers : `None | set<Sticker>`
        Stickers to insert.
    """
    async with DB_ENGINE.connect() as connector:
        now = DateTime.now(TimeZone.utc)
        
        await connector.execute(insert(
            EXPRESSION_COUNTER_TABLE,
            [
                {
                    'entity_id' : entity_id,
                    'action_type' : action_type,
                    
                    'user_id' : message.author.id,
                    'message_id' : message.id,
                    'channel_id' : message.channel_id,
                    'guild_id' : message.guild_id,
                    'timestamp' : now,
                }
                for entity_id, action_type in _iter_entity_ids_and_action_types_for_message_create(emojis, stickers)
            ],
        ))


if (DB_ENGINE is None):
    @copy_docs(execute_message_create)
    async def execute_message_create(message, emojis, stickers):
        pass


async def execute_message_delete(message):
    """
    Executes deletions on a message deletion.
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                expression_counter_model.message_id == message.id
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_message_delete)
    async def execute_message_delete(message):
        pass


async def execute_message_update(message, delete_old_emojis, delete_all_old_emoji, add_new_emojis):
    """
    Executes entry deletion and entry insertions on a message update.
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    delete_old_emojis : `None | set<Emoji>`
        Emojis to delete of the message.
    
    delete_all_old_emoji : `bool`
        Whether all old emojis should be deleted of the message
    
    add_new_emojis : `None | set<Emoji>`
        Emojis to add to the message.
    """
    # No need to update stickers since tho cannot be edited.
    async with DB_ENGINE.connect() as connector:
        if delete_all_old_emoji:
            await connector.execute(
                EXPRESSION_COUNTER_TABLE.delete().where(
                    and_(
                        expression_counter_model.message_id == message.id,
                        expression_counter_model.action_type == ACTION_TYPE_EMOJI_CONTENT,
                    )
                )
            )
        
        if (delete_old_emojis is not None):
            await connector.execute(
                EXPRESSION_COUNTER_TABLE.delete().where(
                    and_(
                        expression_counter_model.message_id == message.id,
                        expression_counter_model.action_type == ACTION_TYPE_EMOJI_CONTENT,
                        expression_counter_model.entity_id.in_([emoji.id for emoji in delete_old_emojis]),
                    )
                )
            )
        
        if (add_new_emojis is not None):
            now = DateTime.now(TimeZone.utc)
            
            await connector.execute(insert(
                EXPRESSION_COUNTER_TABLE,
                [
                    {
                        'entity_id': emoji.id,
                        'action_type': ACTION_TYPE_EMOJI_CONTENT,
                        
                        'user_id': message.author.id,
                        'message_id': message.id,
                        'channel_id': message.channel_id,
                        'guild_id': message.guild_id,
                        'timestamp' : now,
                    }
                    for emoji in add_new_emojis
                ],
            ))


if (DB_ENGINE is None):
    @copy_docs(execute_message_update)
    async def execute_message_update(message, delete_old_emojis, delete_all_old_emoji, add_new_emojis):
        pass


async def execute_reaction_add(message, emoji, user):
    """
    Executes insertion on reaction addition.
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    emoji : ``Emoji`
        The reacted emoji.
    
    user : ``ClientUserBase``
        The user who reacted.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.insert().values(
                entity_id = emoji.id,
                action_type = ACTION_TYPE_EMOJI_REACTION,
                
                user_id =  user.id,
                message_id = message.id,
                channel_id = message.channel_id,
                guild_id =  message.guild_id,
                timestamp = DateTime.now(TimeZone.utc),
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_reaction_add)
    async def execute_reaction_add(message, emoji, user):
        pass


async def execute_reaction_delete(message, emoji, user):
    """
    Executes deletion on reaction deletion.
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    emoji : ``Emoji`
        The removed reacted emoji.
    
    user : ``ClientUserBase``
        The user who deleted their reaction.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                and_(
                    expression_counter_model.message_id == message.id,
                    expression_counter_model.action_type == ACTION_TYPE_EMOJI_REACTION,
                    expression_counter_model.entity_id == emoji.id,
                    expression_counter_model.user_id == user.id,
                )
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_reaction_delete)
    async def execute_reaction_delete(message, emoji, user):
        pass


async def execute_reaction_delete_emoji(message, emoji):
    """
    Executes deletion on reaction emoji deletion. (When all reactions for a single emojis are deleted.)
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    emoji : ``Emoji`
        The removed reacted emoji.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                and_(
                    expression_counter_model.message_id == message.id,
                    expression_counter_model.action_type == ACTION_TYPE_EMOJI_REACTION,
                    expression_counter_model.entity_id == emoji.id,
                )
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_reaction_delete_emoji)
    async def execute_reaction_delete_emoji(message, emoji):
        pass


async def execute_reaction_clear(message):
    """
    Executes deletion on reaction clearing. (When all reaction of a message are deleted.)
    
    This function is a coroutine.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                and_(
                    expression_counter_model.message_id == message.id,
                    expression_counter_model.action_type == ACTION_TYPE_EMOJI_REACTION,
                )
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_reaction_clear)
    async def execute_reaction_clear(message):
        pass


async def execute_emoji_delete(emoji):
    """
    Executes deletion on emoji deletion.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The deleted emoji.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                expression_counter_model.entity_id == emoji.id,
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_emoji_delete)
    async def execute_emoji_delete(emoji):
        pass


async def execute_sticker_delete(sticker):
    """
    Executes deletion on sticker deletion.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The deleted sticker.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                expression_counter_model.entity_id == sticker.id,
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_sticker_delete)
    async def execute_sticker_delete(sticker):
        pass


async def execute_channel_delete(channel):
    """
    Executes deletion on channel deletion.
    
    Parameters
    ----------
    channel : ``Channel``
        The deleted channel.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                expression_counter_model.channel_id == channel.id,
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_channel_delete)
    async def execute_channel_delete(channel):
        pass


async def execute_guild_delete(guild):
    """
    Executes deletion on guild deletion.
    
    Parameters
    ----------
    guild : ``Guild``
        The deleted guild.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXPRESSION_COUNTER_TABLE.delete().where(
                or_(
                    expression_counter_model.guild_id == guild.id,
                    expression_counter_model.entity_id.in_([*guild.emojis.keys(), *guild.stickers.keys()]),
                )
            )
        )


if (DB_ENGINE is None):
    @copy_docs(execute_guild_delete)
    async def execute_guild_delete(guild):
        pass
