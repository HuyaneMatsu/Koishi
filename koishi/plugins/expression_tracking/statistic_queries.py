__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from sqlalchemy import and_, func as alchemy_function
from sqlalchemy.sql import asc, desc, select

from ...bot_utils.models import DB_ENGINE, expression_counter_model

from .constants import RELATIVE_MONTH, ACTION_TYPE_STICKER
from .statistic_caching_and_synchronization import QueryCacherAndSynchronizer


@QueryCacherAndSynchronizer
async def query_expression_user_top(user_id, action_types, months, limit, offset):
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
    
    limit : `int`
        The amount of entities to query for.
    
    offset : `int`
        The amount to offset.
    
    Returns
    -------
    entries : `list<RowProxy<int, int>>`
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
                limit,
            ).offset(
                offset,
            )
        )
        
        return await response.fetchall()


@QueryCacherAndSynchronizer
async def query_expression_entity_top(entity_id, action_types, months, limit, offset):
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
    
    limit : `int`
        The amount of entities to query for.
    
    offset : `int`
        The amount to offset.
    
    Returns
    -------
    entries : `list<RowProxy<int, int>>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    expression_counter_model.user_id,
                    alchemy_function.count(expression_counter_model.user_id).label('total'),
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
                limit,
            ).offset(
                offset,
            )
        )
        
        return await response.fetchall()


@QueryCacherAndSynchronizer
async def query_expression_of_guild_most_used(guild, action_types, months, limit, offset, order_decreasing):
    """
    Queries how much each expression is used of the given guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to query for.
    
    action_types : `tuple<int>`
        The action types to query for.
    
    months : `int`
        The amount of months to query for.
    
    limit : `int`
        The amount of entities to query for.
    
    offset : `int`
        The amount to offset.
    
    order_decreasing : `bool`
        Whether should use decreasing order.
    
    Returns
    -------
    entries : `list<RowProxy<int, int>>`
    """
    entity_ids = [*(guild.stickers if ACTION_TYPE_STICKER else guild.emojis).keys()]
    
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
                    expression_counter_model.entity_id.in_(entity_ids),
                    expression_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months,
                )
            ).group_by(
                expression_counter_model.entity_id,
            ).order_by(
                (desc if order_decreasing else asc)('total'),
            ).limit(
                limit,
            ).offset(
                offset,
            )
        )
        
        return await response.fetchall()


@QueryCacherAndSynchronizer
async def query_expression_in_guild_most_used(guild, action_types, months, limit, offset, order_decreasing):
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
    
    limit : `int`
        The amount of entities to query for.
    
    offset : `int`
        The amount to offset.
    
    Returns
    -------
    entries : `list<RowProxy<int, int>>`
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
                (desc if order_decreasing else asc)('total'),
            ).limit(
                limit,
            ).offset(
                offset,
            )
        )
        
        return await response.fetchall()
