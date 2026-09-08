__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from struct import Struct

from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE, adventure_model
from sqlalchemy import (
    BIGINT as Int64, Column, DateTime as DateTimeRowType, Integer as Int32, LargeBinary as Binary
)

from sqlalchemy.ext.declarative import declarative_base


ADVENTURE_ACTION_STRUCT = Struct('<IQIIQQ')


def _get_adventure_model_old():
    """
    Gets old adventure model.
    
    Returns
    -------
    adventure_model_old : ``DeclarativeMeta``
    """
    class adventure_model_old(declarative_base()):
        __tablename__   = 'ADVENTURES'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64, nullable = False)
        
        location_id     = Column(Int32, nullable = False)
        target_id       = Column(Int32, nullable = False)
        return_id       = Column(Int32, nullable = False)
        auto_cancellation_id = Column(Int32, nullable = False)
        state           = Column(Int32, nullable = False)
        
        initial_duration = Column(Int64, nullable = False)
        created_at      = Column(DateTimeRowType, nullable = False)
        updated_at      = Column(DateTimeRowType, nullable = False)
        action_count    = Column(Int32, nullable = False)
        seed            = Column(Int64, nullable = False)
        
        health_initial = Column(Int64, nullable = False)
        health_exhausted = Column(Int64, nullable = False)
        energy_initial = Column(Int64, nullable = False)
        energy_exhausted = Column(Int64, nullable = False)
    
    return adventure_model_old


def _get_adventure_action_model_old():
    """
    Gets old adventure action model.
    
    Returns
    -------
    adventure_action_model : ``DeclarativeMeta``
    """
    class adventure_action_model_old(declarative_base()):
        __tablename__   = 'ADVENTURE_ACTIONS'
        id              = Column(Int64, primary_key = True)
        adventure_entry_id = Column(Int64, nullable = False)
        action_id       = Column(Int32, nullable = False)
        created_at      = Column(DateTimeRowType, nullable = False)
        
        battle_data     = Column(Binary(), nullable = True)
        loot_data       = Column(Binary(), nullable = True)
        
        health_exhausted = Column(Int64, nullable = False)
        energy_exhausted = Column(Int64, nullable = False)
    
    return adventure_action_model_old


def _db_date_time_to_unix_time_seconds(date_time):
    """
    Converts a date-time received from the data base to a unix time in nano seconds.
    
    Parameters
    -----------
    date_time : `DateTime`
        Date time to convert.
    
    Returns
    -------
    unix_time_seconds : `int`
    """
    return int(date_time.replace(tzinfo = TimeZone.utc).timestamp())


def execute_migration():
    """
    Executes the migration.
    """
    adventure_model_old = _get_adventure_model_old()
    adventure_action_model_old = _get_adventure_action_model_old()
    
    with DB_ENGINE.connect() as connector:
        adventure_listing_response = connector.execute(
            select(
                [
                    adventure_model_old.id,
                    adventure_model_old.user_id,
                    adventure_model_old.location_id,
                    adventure_model_old.target_id,
                    adventure_model_old.return_id,
                    adventure_model_old.auto_cancellation_id,
                    adventure_model_old.state,
                    adventure_model_old.initial_duration,
                    adventure_model_old.created_at,
                    adventure_model_old.updated_at,
                    adventure_model_old.seed,
                    adventure_model_old.health_initial,
                    adventure_model_old.health_exhausted,
                    adventure_model_old.energy_initial,
                    adventure_model_old.energy_exhausted,
                ]
            )
        )
        
        while True:
            adventure_entry = adventure_listing_response.fetchone()
            if adventure_entry is None:
                break
            
            (
                adventure_entry_id,
                user_id,
                location_id,
                target_id,
                return_id,
                auto_cancellation_id,
                state,
                initial_duration_seconds,
                created_at_date_time,
                updated_at_date_time,
                seed,
                health_initial,
                health_exhausted,
                energy_initial,
                energy_exhausted,
            ) = adventure_entry
            
            created_at_unix_time_seconds = _db_date_time_to_unix_time_seconds(created_at_date_time)
            updated_at_unix_time_seconds = _db_date_time_to_unix_time_seconds(updated_at_date_time)
            
            adventure_action_listing_response = connector.execute(
                select(
                    [
                        adventure_action_model_old.action_id,
                        adventure_action_model_old.created_at,
                        adventure_action_model_old.battle_data,
                        adventure_action_model_old.loot_data,
                        adventure_action_model_old.health_exhausted,
                        adventure_action_model_old.energy_exhausted,
                    ]
                ).where(
                    adventure_action_model_old.adventure_entry_id == adventure_entry_id
                )
            )
                
            adventure_action_entries = adventure_action_listing_response.fetchall()
            if (not adventure_action_entries):
                action_listing_data = None
            else:
                action_listing_data_parts = []
                
                for (
                    action_action_id,
                    action_created_at,
                    action_battle_data,
                    action_loot_data,
                    action_health_exhausted,
                    action_energy_exhausted,
                ) in adventure_action_entries:
                    action_listing_data_parts.append(ADVENTURE_ACTION_STRUCT.pack(
                        action_action_id,
                        _db_date_time_to_unix_time_seconds(action_created_at),
                        (0 if action_battle_data is None else len(action_battle_data)),
                        (0 if action_loot_data is None else len(action_loot_data)),
                        action_health_exhausted,
                        action_energy_exhausted,
                    ))
                    
                    if (action_battle_data is not None):
                        action_listing_data_parts.append(action_battle_data)
                    
                    if (action_loot_data is not None):
                        action_listing_data_parts.append(action_loot_data)
                
                action_listing_data = b''.join(action_listing_data_parts)
                action_listing_data_parts = None
            
            connector.execute(
                adventure_model.__table__.insert().values(
                    user_id = user_id,
                    location_id = location_id,
                    target_id = target_id,
                    return_id = return_id,
                    auto_cancellation_id = auto_cancellation_id,
                    state = state,
                    initial_duration_seconds = initial_duration_seconds,
                    created_at = created_at_unix_time_seconds,
                    updated_at = updated_at_unix_time_seconds,
                    action_listing_data = action_listing_data,
                    seed = seed,
                    health_initial = health_initial,
                    health_exhausted = health_exhausted,
                    energy_initial = energy_initial,
                    energy_exhausted = energy_exhausted,
                )
            )
