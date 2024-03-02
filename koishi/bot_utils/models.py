from config import DATABASE_NAME
from datetime import datetime as DateTime
from warnings import warn

utc_now = DateTime.utcnow

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

todo_model = None
TODO_TABLE = None

item_model = None
ITEM_TABLE = None

automation_configuration_model = None
AUTOMATION_CONFIGURATION_TABLE = None

character_preference_model = None
CHARACTER_PREFERENCE_TABLE = None

notification_settings_model = None
NOTIFICATION_SETTINGS_TABLE = None

blacklist_model = None
BLACKLIST_TABLE = None


if (DATABASE_NAME is not None):
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer as Int32, BIGINT as Int64, LargeBinary as Binary, create_engine, DateTime, \
        String, Boolean, Unicode, SmallInteger as Int16
    from sqlalchemy.sql.expression import func
    
    try:
        DB_ENGINE = create_engine(DATABASE_NAME)
    except ImportError as err:
        warn(
            f'Could not create database engine: {err!r}.',
            RuntimeWarning,
        )
        DB_ENGINE = None
        
    
if (DB_ENGINE is not None):
    BASE = declarative_base()
    
    class user_common_model(BASE):
        __tablename__   = 'CURRENCY'
        # Generic
        id              = Column(Int64, primary_key = True, nullable = False)
        user_id         = Column(Int64, unique = True, nullable = False)
        
        # Love
        total_love      = Column(Int64, default = 0, nullable = False)
        total_allocated = Column(Int64, default = 0, nullable = False)
        
        # Daily
        daily_next      = Column(DateTime, default = func.utc_timestamp(), nullable = False)
        daily_streak    = Column(Int32, default = 0, nullable = False)
        daily_reminded  = Column(Boolean, default = False, nullable = False)
        
        # Counters
        count_daily_self = Column(Int32, default = 0, nullable = False)
        count_daily_by_waifu = Column(Int32, default = 0, nullable = False)
        count_daily_for_waifu = Column(Int32, default = 0, nullable = False)
        count_top_gg_vote = Column(Int32, default = 0, nullable = False)
        
        # Waifu
        waifu_cost      = Column(Int64, default = 0, nullable = False)
        waifu_divorces  = Column(Int32, default = 0, nullable = False)
        waifu_slots     = Column(Int32, default = 1, nullable = False)
        waifu_owner_id  = Column(Int64, default = 0, nullable = False)
        
        # Notify voters that they can vote on top.gg if they can. We base this on a top.gg vote timer and whether they
        # voted before
        top_gg_last_vote = Column(DateTime, default = func.utc_timestamp(), nullable = False)
    
    
    USER_COMMON_TABLE = user_common_model.__table__
    
    class waifu_list_model(BASE):
        __tablename__   = 'WAIFU_LIST'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64)
        waifu_id        = Column(Int64)
    
    WAIFU_LIST_TABLE = waifu_list_model.__table__
    
    
    class waifu_proposal_model(BASE):
        __tablename__   = 'WAIFU_PROPOSAL'
        id              = Column(Int64, primary_key = True)
        source_id       = Column(Int64)
        target_id       = Column(Int64)
        investment      = Column(Int64)
    
    WAIFU_PROPOSAL_TABLE = waifu_proposal_model.__table__
    
    
    class auto_react_role_model(BASE):
        __tablename__   = 'AUTO_REACT_ROLE'
        id              = Column(Int64, primary_key = True)
        message_id      = Column(Int64, unique = True)
        channel_id      = Column(Int64)
        data            = Column(Binary(320))
        behaviour       = Column(Int32)
        client_id       = Column(Int64)
    
    AUTO_REACT_ROLE_TABLE = auto_react_role_model.__table__
    
    
    class item_model(BASE):
        __tablename__   = 'ITEM'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64)
        amount          = Column(Int64, default = 0)
        type            = Column(Int32, default = 0)
    
    ITEM_TABLE = item_model.__table__
    
    
    class emoji_counter_model(BASE):
        __tablename__   = 'EMOJI_COUNTER'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64)
        emoji_id        = Column(Int64)
        timestamp       = Column(DateTime)
        action_type     = Column(Int32)
    
    EMOJI_COUNTER_TABLE = emoji_counter_model.__table__
    
    
    class sticker_counter_model(BASE):
        __tablename__   = 'STICKER_COUNTER'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64)
        sticker_id      = Column(Int64)
        timestamp       = Column(DateTime)
    
    STICKER_COUNTER_TABLE = sticker_counter_model.__table__
    
    
    class ds_v2_model(BASE):
        __tablename__   = 'DS_V2'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64, unique = True)
        game_state      = Column(Binary(), nullable = True)
        selected_stage_id = Column(Int32)
    
    DS_V2_TABLE = ds_v2_model.__table__
    
    
    class ds_v2_result_model(BASE):
        __tablename__   = 'DS_V2_RESULT'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64)
        stage_id        = Column(Int64)
        best            = Column(Int32)
    
    DS_V2_RESULT_TABLE = ds_v2_result_model.__table__
    
    
    class todo_model(BASE):
        __tablename__ = 'TODO'
        id = Column(Int64, primary_key = True)
        name = Column(Unicode)
        description = Column(Unicode)
        created_at = Column(DateTime)
        creator_id = Column(Int64)
    
    TODO_TABLE = todo_model.__table__
    
    
    class waifu_stats_model(BASE):
        __tablename__ = 'WAIFU_STATS'
        
        id = Column(Int64, primary_key = True)
        user_id = Column(Int64, unique = True)
        
        stat_housewife = Column(Int32)
        stat_cuteness = Column(Int32)
        stat_bedroom = Column(Int32)
        stat_charm = Column(Int32)
        stat_loyalty = Column(Int32)
        
        level = Column(Int32)
        experience = Column(Int32)
        
        raw_species = Column(Binary(), nullable = True)
        raw_weapon = Column(Binary(), nullable = True)
        raw_costume = Column(Binary(), nullable = True)
    
    
    WAIFU_STATS_TABLE = waifu_stats_model.__table__
    
        
    class automation_configuration_model(BASE):
        __tablename__ = 'AUTOMATION_CONFIGURATION'
        
        id = Column(Int64, nullable = False, primary_key = True)
        guild_id = Column(Int64, unique = True, nullable = False)
        
        # Logging
        log_emoji_channel_id = Column(Int64, nullable = False)
        log_mention_channel_id = Column(Int64, nullable = False)
        log_sticker_channel_id = Column(Int64, nullable = False)
        log_user_channel_id = Column(Int64, nullable = False)
        
        # Satori
        log_satori_auto_start = Column(Boolean, default = False, nullable = False)
        log_satori_channel_id = Column(Int64, nullable = False)
        
        # Reaction copy
        reaction_copy_enabled = Column(Boolean, default = False, nullable = False)
        reaction_copy_role_id = Column(Int64, nullable = False)
        
        # Touhou feed
        touhou_feed_enabled = Column(Boolean, default = False, nullable = False)
        
        # Welcome
        welcome_channel_id = Column(Int64, nullable = False)
        welcome_reply_buttons_enabled = Column(Boolean, default = False, nullable = False)
        welcome_style_name = Column(String, default = None, nullable = True)
        
        # Community message moderation
        community_message_moderation_availability_duration = Column(Int64, default = 0, nullable = False)
        community_message_moderation_down_vote_emoji_id = Column(Int64, default = 0, nullable = False)
        community_message_moderation_enabled = Column(Boolean, default = False, nullable = False)
        community_message_moderation_up_vote_emoji_id = Column(Int64, default = 0, nullable = False)
        community_message_moderation_vote_threshold = Column(Int64, default = 0, nullable = False)
        community_message_moderation_log_enabled = Column(Boolean, default = False, nullable = False)
        community_message_moderation_log_channel_id = Column(Int64, default = 0, nullable = False)
    
    
    AUTOMATION_CONFIGURATION_TABLE = automation_configuration_model.__table__
    
    
    class character_preference_model(BASE):
        __tablename__ = 'CHARACTER_PREFERENCE'
        id = Column(Int64, nullable = False, primary_key = True)
        user_id = Column(Int64, nullable = False)
        system_name = Column(String, nullable = True)
    
    CHARACTER_PREFERENCE_TABLE = character_preference_model.__table__
    
    
    class notification_settings_model(BASE):
        __tablename__ = 'NOTIFICATION_SETTINGS'
        id = Column(Int64, nullable = False, primary_key = True)
        user_id = Column(Int64, nullable = False)
        daily_by_waifu = Column(Boolean, default = True, nullable = False)
        proposal = Column(Boolean, default = True, nullable = False)
        daily_reminder = Column(Boolean, default = True, nullable = False)
        notifier_client_id = Column(Int64, default = 0, nullable = False)
    
    NOTIFICATION_SETTINGS_TABLE = notification_settings_model.__table__
    
    
    class blacklist_model(BASE):
        __tablename__   = 'BLACKLIST'
        
        id              = Column(Int64, nullable = False, primary_key = True)
        user_id         = Column(Int64, nullable = False)
    
    BLACKLIST_TABLE = blacklist_model.__table__
    
    
    DB_ENGINE.dispose()
    # BASE.metadata.create_all(DB_ENGINE)
    
    def get_create_common_user_expression(
        user_id,
        total_love = 0,
        daily_next = None,
        daily_streak = 0,
        daily_reminded = False,
        total_allocated = 0,
        waifu_cost = 0,
        waifu_divorces = 0,
        waifu_slots = 1,
        count_daily_self = 0,
        count_daily_by_waifu = 0,
        count_daily_for_waifu = 0,
        count_top_gg_vote = 0,
        top_gg_last_vote = None,
        waifu_owner_id = 0,
    ):
        now = None
        
        if daily_next is None:
            if now is None:
                now = utc_now()

            daily_next = now
        
        if top_gg_last_vote is None:
            if now is None:
                now = utc_now()
            
            top_gg_last_vote = now
        
        return USER_COMMON_TABLE.insert().values(
            user_id         = user_id,
            total_love      = total_love,
            daily_next      = daily_next,
            daily_streak    = daily_streak,
            daily_reminded  = daily_reminded,
            total_allocated = total_allocated,
            waifu_cost      = waifu_cost,
            waifu_divorces  = waifu_divorces,
            waifu_slots     = waifu_slots,
            count_daily_self = count_daily_self,
            count_daily_by_waifu = count_daily_by_waifu,
            count_daily_for_waifu = count_daily_for_waifu,
            count_top_gg_vote = count_top_gg_vote,
            top_gg_last_vote = top_gg_last_vote,
            waifu_owner_id = waifu_owner_id,
        )
