__all__ = ('query_expression_in_guild_most_used', 'query_expression_of_guild_most_used',)

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs
from sqlalchemy import and_, case, func as alchemy_function
from sqlalchemy.sql import desc, select

from ...bot_utils.models import DB_ENGINE, expression_counter_model

from .constants import (
    ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION, ENTITY_FILTER_RULE_EMOJI_ANIMATED,
    ENTITY_FILTER_RULE_EMOJI_STATIC, RELATIVE_MONTH
)
from .statistic_caching_and_synchronization import QueryCacherAndSynchronizer


if (DB_ENGINE is None):
    from .constants import ENTRY_CACHE
    SORT_KEY_GETTER = lambda item: item[1]


async def _query_expression_user_top(user_id, action_types, months):
    """
    Queries the expressions that user uses the most.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    months : `int`
        The amount of months to query for.
    
    Returns
    -------
    entries : `list<(int, int)>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    expression_counter_model.entity_id,
                    alchemy_function.count().label('total'),
                ]
            ).where(
                and_(
                    expression_counter_model.action_type.in_(action_types),
                    expression_counter_model.user_id == user_id,
                    expression_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months,
                )
            ).having(
                alchemy_function.count(expression_counter_model.entity_id) > 0
            ).group_by(
                expression_counter_model.entity_id,
            ).order_by(
                desc('total'),
            ).limit(
                1000,
            )
        )
        
        entries = await response.fetchall()
    
    return [(entity_id, total) for entity_id, total in entries]


if (DB_ENGINE is None):
    @copy_docs(_query_expression_user_top)
    async def _query_expression_user_top(user_id, action_types, months):
        timestamp = DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months
        relations = {}
        
        for element in ENTRY_CACHE:
            if not ((element[2] in action_types) and (element[3] == user_id) and (element[7] > timestamp)):
                continue
            
            element_entity_id = element[1]
            relations[element_entity_id] = relations.get(element_entity_id, 0) + 1
        
        
        return sorted(relations.items(), key = SORT_KEY_GETTER, reverse = True)


async def _query_expression_entity_top(entity_id, action_types, months):
    """
    Queries the users who use the expression the most.
    
    Parameters
    ----------
    entity_id : `int`
        The entity's identifier.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    months : `int`
        The amount of months to query for.
    
    Returns
    -------
    entries : `list<(int, int)>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    expression_counter_model.user_id,
                    alchemy_function.count().label('total'),
                ]
            ).where(
                and_(
                    expression_counter_model.action_type.in_(action_types),
                    expression_counter_model.entity_id == entity_id,
                    expression_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months,
                )
            ).having(
                alchemy_function.count(expression_counter_model.user_id) > 0
            ).group_by(
                expression_counter_model.user_id,
            ).order_by(
                desc('total'),
            ).limit(
                1000,
            )
        )
        
        entries = await response.fetchall()
    
    return [(entity_id, total) for entity_id, total in entries]


if (DB_ENGINE is None):
    @copy_docs(_query_expression_entity_top)
    async def _query_expression_entity_top(entity_id, action_types, months):
        timestamp = DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months
        relations = {}
        
        for element in ENTRY_CACHE:
            element_entity_id = element[1]
            if not ((element[2] in action_types) and (element_entity_id == entity_id) and (element[7] > timestamp)):
                continue
            
            relations[element_entity_id] = relations.get(element_entity_id, 0) + 1
        
        
        return sorted(relations.items(), key = SORT_KEY_GETTER, reverse = True)


async def query_expression_of_guild_most_used(
    guild, action_types, entity_filter_rule, months, page_index, page_size, order_decreasing
):
    """
    Queries how much each expression is used of the given guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to query for.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    page_index : `int`
        The page's index to request.
    
    page_size : `int`
        The page's size.
    
    order_decreasing : `bool`
        Whether should use decreasing order.
    
    Returns
    -------
    entry_page_and_page_count : `(list<(int, int, int)>, int)`
    """
    entries_processed = await _query_expression_of_guild_most_used(guild, action_types, entity_filter_rule, months)
    entries_count = len(entries_processed)
    page_count = (entries_count + page_size - 1) // page_size
    
    if (page_index < 0) or (page_index >= page_count):
        return [], page_count
    
    index_page_start = page_index * page_size
    index_page_end = min(index_page_start + page_size, entries_count)
    
    if order_decreasing:
        step = +1
    else:
        index_page_start = entries_count - index_page_start - 1
        index_page_end = entries_count - index_page_end
        if index_page_end:
            index_page_end -= 1
        else:
            index_page_end = None
        step = -1
    
    return entries_processed[index_page_start : index_page_end : step], page_count


def _get_of_guild_entity_ids(guild, action_types, entity_filter_rule):
    """
    Helper function to filter the entity identifiers of the guild for th given actions & filtering rule.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to query for.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    Returns
    -------
    entity_ids : `list<int>`
    """
    if (ACTION_TYPE_EMOJI_CONTENT in action_types) or (ACTION_TYPE_EMOJI_REACTION in action_types):
        if entity_filter_rule == ENTITY_FILTER_RULE_EMOJI_STATIC:
            entity_ids = sorted(emoji.id for emoji in guild.emojis.values() if (not emoji.animated))
        
        elif entity_filter_rule == ENTITY_FILTER_RULE_EMOJI_ANIMATED:
            entity_ids = sorted(emoji.id for emoji in guild.emojis.values() if emoji.animated)
        
        else:
            entity_ids = sorted(guild.emojis.keys())
    
    # elif (ACTION_TYPE_STICKER in action_types):
    else:
        entity_ids = sorted(guild.stickers.keys())
    
    return entity_ids


async def _query_expression_of_guild_most_used(guild, action_types, entity_filter_rule, months):
    """
    Queries how much each expression is used of the given guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to query for.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    months : `int`
        The amount of months to query for.
    
    Returns
    -------
    entries : `list<(int, int, int)>`
    """
    entity_ids =  _get_of_guild_entity_ids(guild, action_types, entity_filter_rule)
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    expression_counter_model.entity_id,
                    alchemy_function.count().label('total'),
                    alchemy_function.sum(case(
                        [
                            (expression_counter_model.guild_id == guild.id, 1),
                        ],
                        else_ = 0,
                    )).label('local'),
                ]
            ).where(
                and_(
                    expression_counter_model.action_type.in_(action_types),
                    expression_counter_model.entity_id.in_(entity_ids),
                    expression_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months,
                )
            ).group_by(
                expression_counter_model.entity_id,
            ).order_by(
                desc('total'),
            )
        )
        
        entries = await response.fetchall()
    
    entries_processed = []
    entry_ids_mentioned = set()
    
    for entity_id, total, local in entries:
        entries_processed.append((entity_id, total, local))
        entry_ids_mentioned.add(entity_id)
    
    for entity_id in entity_ids:
        if entity_id not in entry_ids_mentioned:
            entries_processed.append((entity_id, 0, 0))
    
    return entries_processed



if (DB_ENGINE is None):
    @copy_docs(_query_expression_of_guild_most_used)
    async def _query_expression_of_guild_most_used(guild, action_types, entity_filter_rule, months):
        entity_ids =  _get_of_guild_entity_ids(guild, action_types, entity_filter_rule)
        guild_id = guild.id
        timestamp = DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months
        relations = {}
        
        for element in ENTRY_CACHE:
            element_entity_id = element[1]
            if not ((element[2] in action_types) and (element_entity_id in entity_ids) and (element[7] > timestamp)):
                continue
            
            total, local = relations.get(element_entity_id, (0, 0))
            total += 1
            local += element[6] == guild_id
            relations[element_entity_id] = (total, local)
        
        
        entries_processed = sorted(
            ((key, value[0], value[1]) for key, value in relations.items()),
            key = SORT_KEY_GETTER,
            reverse = True,
        )
        entry_ids_mentioned = {entry[0] for entry in entries_processed}
        
        for entity_id in entity_ids:
            if entity_id not in entry_ids_mentioned:
                entries_processed.append((entity_id, 0, 0))
        
        return entries_processed


async def query_expression_in_guild_most_used(guild, action_types, months, page_index, page_size, order_decreasing):
    """
    Queries how much each expression is used in the given guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to query for.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    months : `int`
        The amount of months to query for.
    
    page_index : `int`
        The page's index to request.
    
    page_size : `int`
        The page's size.
    
    order_decreasing : `bool`
        Whether should use decreasing order.
    
    Returns
    -------
    entry_page_and_page_count : `(list<(int, int, int)>, int)`
    """
    entries_processed = await _query_expression_in_guild_most_used(guild, action_types, months)
    entries_count = len(entries_processed)
    page_count = (entries_count + page_size - 1) // page_size
    
    if (page_index < 0) or (page_index >= page_count):
        return [], page_count
    
    index_page_start = page_index * page_size
    index_page_end = min(index_page_start + page_size, entries_count)
    
    if order_decreasing:
        step = +1
    else:
        index_page_start = entries_count - index_page_start - 1
        index_page_end = entries_count - index_page_end
        if index_page_end:
            index_page_end -= 1
        else:
            index_page_end = None
        step = -1
    
    return entries_processed[index_page_start : index_page_end : step], page_count


async def _query_expression_in_guild_most_used(guild, action_types, months):
    """
    Queries how much each expression is used in the given guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to query for.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    months : `int`
        The amount of months to query for.
    
    Returns
    -------
    entries : `list<(int, int)>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    expression_counter_model.entity_id,
                    alchemy_function.count(expression_counter_model.entity_id).label('total'),
                ]
            ).where(
                and_(
                    expression_counter_model.action_type.in_(action_types),
                    expression_counter_model.guild_id == guild.id,
                    expression_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months,
                )
            ).having(
                alchemy_function.count(expression_counter_model.entity_id) > 0
            ).group_by(
                expression_counter_model.entity_id,
            ).order_by(
                desc('total'),
            ).limit(
                1000,
            )
        )
        
        entries = await response.fetchall()
    
    return [(entity_id, total) for entity_id, total in entries]


if (DB_ENGINE is None):
    @copy_docs(_query_expression_in_guild_most_used)
    async def _query_expression_in_guild_most_used(guild, action_types, months):
        timestamp = DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months
        guild_id = guild.id
        relations = {}
        
        for element in ENTRY_CACHE:
            if not ((element[2] in action_types) and (element[6] == guild_id) and (element[7] > timestamp)):
                continue
            
            element_entity_id = element[1]
            relations[element_entity_id] = relations.get(element_entity_id, 0) + 1
        
        
        return sorted(relations.items(), key = SORT_KEY_GETTER, reverse = True)


_query_expression_user_top = QueryCacherAndSynchronizer(_query_expression_user_top)
_query_expression_entity_top = QueryCacherAndSynchronizer(_query_expression_entity_top)
_query_expression_of_guild_most_used = QueryCacherAndSynchronizer(_query_expression_of_guild_most_used)
_query_expression_in_guild_most_used = QueryCacherAndSynchronizer(_query_expression_in_guild_most_used)
