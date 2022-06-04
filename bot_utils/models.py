from config import DATABASE_NAME
from datetime import datetime

if DATABASE_NAME is None:
    user_common_model = None
    USER_COMMON_TABLE = None
    
    waifu_list_model = None
    WAIFU_LIST_TABLE = None
    
    waifu_proposal_model = None
    WAIFU_PROPOSAL_TABLE = None
    
    auto_react_role_model = None
    AUTO_REACT_ROLE_TABLE = None
    
    emoji_counter_model = None
    EMOJI_COUNTER_TABLE = None
    
    ds_v2_model = None
    DS_V2_TABLE = None
    
    ds_v2_result_model = None
    DS_V2_RESULT_TABLE = None
    
    sticker_counter_model = None
    STICKER_COUNTER_TABLE = None
    
    DB_ENGINE = None
    
    get_create_common_user_expression = None
    
    waifu_stats_model = None
    WAIFU_STATS_TABLE = None
    
else:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer as Int32, BIGINT as Int64, LargeBinary as Binary, create_engine, DateTime, \
        String, Boolean, Unicode, SmallInteger as Int16
    from sqlalchemy.sql.expression import func
    
    BASE = declarative_base()
    
    class user_common_model(BASE):
        __tablename__   = 'CURRENCY'
        # Generic
        id              = Column(Int64, primary_key=True)
        user_id         = Column(Int64, unique=True)
        
        # Love
        total_love      = Column(Int64, default=0)
        total_allocated = Column(Int64, default=0)
        
        # Daily
        daily_next      = Column(DateTime, default=func.utc_timestamp())
        daily_streak    = Column(Int32, default=0)
        
        # Counters
        count_daily_self = Column(Int32, default=0)
        count_daily_by_waifu = Column(Int32, default=0)
        count_daily_for_waifu = Column(Int32, default=0)
        count_top_gg_vote = Column(Int32, default=0)
        
        # Waifu
        waifu_cost      = Column(Int64, default=0)
        waifu_divorces  = Column(Int32, default=0)
        waifu_slots     = Column(Int32, default=1)
        
        # notification settings
        notify_proposal = Column(Boolean, default=True)
        notify_daily = Column(Boolean, default=True)
        
        # Notify voters that they can vote on top.gg if they can. We base this on a top.gg vote timer and whether they
        # voted before
        top_gg_last_vote = Column(DateTime, default=func.utc_timestamp())
        
    
    USER_COMMON_TABLE = user_common_model.__table__
    
    class waifu_list_model(BASE):
        __tablename__   = 'WAIFU_LIST'
        id              = Column(Int64, primary_key=True)
        user_id         = Column(Int64)
        waifu_id        = Column(Int64)
    
    WAIFU_LIST_TABLE = waifu_list_model.__table__
    
    
    class waifu_proposal_model(BASE):
        __tablename__   = 'WAIFU_PROPOSAL'
        id              = Column(Int64, primary_key=True)
        source_id       = Column(Int64)
        target_id       = Column(Int64)
        investment      = Column(Int64)
    
    WAIFU_PROPOSAL_TABLE = waifu_proposal_model.__table__
    
    
    class auto_react_role_model(BASE):
        __tablename__   = 'AUTO_REACT_ROLE'
        id              = Column(Int64, primary_key=True)
        message_id      = Column(Int64, unique=True)
        channel_id      = Column(Int64)
        data            = Column(Binary(320))
        behaviour       = Column(Int32)
        client_id       = Column(Int64)
    
    AUTO_REACT_ROLE_TABLE = auto_react_role_model.__table__
    
    
    class item_model(BASE):
        __tablename__   = 'ITEM'
        id              = Column(Int64, primary_key=True)
        user_id         = Column(Int64)
        amount          = Column(Int64, default=0)
        type            = Column(Int32, default=0)
    
    ITEM_TABLE = item_model.__table__
    
    
    class emoji_counter_model(BASE):
        __tablename__   = 'EMOJI_COUNTER'
        id              = Column(Int64, primary_key=True)
        user_id         = Column(Int64)
        emoji_id        = Column(Int64)
        timestamp       = Column(DateTime)
        action_type     = Column(Int32)
    
    EMOJI_COUNTER_TABLE = emoji_counter_model.__table__
    
    
    class sticker_counter_model(BASE):
        __tablename__   = 'STICKER_COUNTER'
        id              = Column(Int64, primary_key=True)
        user_id         = Column(Int64)
        sticker_id      = Column(Int64)
        timestamp       = Column(DateTime)
    
    STICKER_COUNTER_TABLE = sticker_counter_model.__table__
    
    
    class ds_v2_model(BASE):
        __tablename__   = 'DS_V2'
        id              = Column(Int64, primary_key=True)
        user_id         = Column(Int64, unique=True)
        game_state      = Column(Binary(), nullable=True)
        selected_stage_id = Column(Int32)
    
    DS_V2_TABLE = ds_v2_model.__table__
    
    
    class ds_v2_result_model(BASE):
        __tablename__   = 'DS_V2_RESULT'
        id              = Column(Int64, primary_key=True)
        user_id         = Column(Int64)
        stage_id        = Column(Int64)
        best            = Column(Int32)
    
    DS_V2_RESULT_TABLE = ds_v2_result_model.__table__
    
    
    class todo_model(BASE):
        __tablename__ = 'TODO'
        id = Column(Int64, primary_key=True)
        name = Column(Unicode)
        description = Column(Unicode)
        created_at = Column(DateTime)
        creator_id = Column(Int64)
    
    TODO_TABLE = todo_model.__table__
    
    
    class waifu_stats_model(BASE):
        __tablename__ = 'WAIFU_STATS'
        
        id = Column(Int64, primary_key=True)
        user_id = Column(Int64, unique=True)
        
        stat_housewife = Column(Int32)
        stat_cuteness = Column(Int32)
        stat_bedroom = Column(Int32)
        stat_charm = Column(Int32)
        stat_loyalty = Column(Int32)
        
        level = Column(Int32)
        experience = Column(Int32)
        
        raw_species = Column(Binary(), nullable=True)
        raw_weapon = Column(Binary(), nullable=True)
        raw_costume = Column(Binary(), nullable=True)
    
    
    WAIFU_STATS_TABLE = waifu_stats_model.__table__
    
    
    DB_ENGINE = create_engine(DATABASE_NAME)
    DB_ENGINE.dispose()
    #BASE.metadata.create_all(DB_ENGINE)
    
    def get_create_common_user_expression(
        user_id,
        total_love = 0,
        daily_next = None,
        daily_streak = 0,
        total_allocated = 0,
        waifu_cost = 0,
        waifu_divorces = 0,
        waifu_slots = 1,
        notify_proposal = True,
        notify_daily = True,
        count_daily_self = 0,
        count_daily_by_waifu = 0,
        count_daily_for_waifu = 0,
        count_top_gg_vote = 0,
        top_gg_last_vote = None,
    ):
        now = None
        
        if daily_next is None:
            if now is None:
                now = datetime.utcnow()

            daily_next = now
        
        if top_gg_last_vote is None:
            if now is None:
                now = datetime.utcnow()
            
            top_gg_last_vote = now
        
        return USER_COMMON_TABLE.insert().values(
            user_id         = user_id,
            total_love      = total_love,
            daily_next      = daily_next,
            daily_streak    = daily_streak,
            total_allocated = total_allocated,
            waifu_cost      = waifu_cost,
            waifu_divorces  = waifu_divorces,
            waifu_slots     = waifu_slots,
            notify_proposal = notify_proposal,
            notify_daily = notify_daily,
            count_daily_self = count_daily_self,
            count_daily_by_waifu = count_daily_by_waifu,
            count_daily_for_waifu = count_daily_for_waifu,
            count_top_gg_vote = count_top_gg_vote,
            top_gg_last_vote = top_gg_last_vote,
        )
