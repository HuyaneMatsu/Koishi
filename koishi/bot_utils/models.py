from config import DATABASE_NAME
from warnings import warn

user_balance_model = None
USER_BALANCE_TABLE = None

automation_reaction_role_model = None
AUTOMATION_REACTION_ROLE_TABLE = None

emoji_counter_model = None
EMOJI_COUNTER_TABLE = None

ds_v2_model = None
DS_V2_TABLE = None

ds_v2_result_model = None
DS_V2_RESULT_TABLE = None

sticker_counter_model = None
STICKER_COUNTER_TABLE = None

DB_ENGINE = None

stats_model = None
STATS_TABLE = None

todo_model = None
TODO_TABLE = None

automation_configuration_model = None
AUTOMATION_CONFIGURATION_TABLE = None

character_preference_model = None
CHARACTER_PREFERENCE_TABLE = None

user_settings_model = None
USER_SETTINGS_TABLE = None

blacklist_model = None
BLACKLIST_TABLE = None

external_events_model = None
EXTERNAL_EVENTS_TABLE = None

relationship_request_model = None
RELATIONSHIP_REQUEST_TABLE = None

relationship_model = None
RELATIONSHIP_TABLE = None

expression_counter_model = None
EXPRESSION_COUNTER_TABLE = None

item_model = None
ITEM_TABLE = None

guild_stats_model = None
GUILD_STATS_TABLE = None

linked_quest_model = None
LINKED_QUEST_TABLE = None

adventure_action_model = None
ADVENTURE_ACTION_TABLE = None

adventure_model = None
ADVENTURE_TABLE = None

if (DATABASE_NAME is not None):
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer as Int32, BIGINT as Int64, LargeBinary as Binary, create_engine, DateTime, \
        String, Boolean, Unicode, SmallInteger as Int16
    from sqlalchemy.sql.expression import func
        
    try:
        DB_ENGINE = create_engine(DATABASE_NAME, max_overflow = -1, pool_size = 50)
    except ImportError as err:
        warn(
            f'Could not create database engine: {err!r}.',
            RuntimeWarning,
        )
        DB_ENGINE = None


if (DB_ENGINE is not None):
    BASE = declarative_base()
    
    class user_balance_model(BASE):
        __tablename__   = 'CURRENCY'
        # Generic
        id = Column(Int64, primary_key = True, nullable = False)
        user_id = Column(Int64, unique = True, nullable = False)
        
        # Balance
        balance = Column(Int64, default = 0, nullable = False)
        allocated = Column(Int64, default = 0, nullable = False)
        
        # Streak
        streak = Column(Int32, default = 0, nullable = False)
        daily_can_claim_at = Column(DateTime, default = func.utc_timestamp(), nullable = False)
        daily_reminded  = Column(Boolean, default = False, nullable = False)
        top_gg_voted_at = Column(DateTime, default = func.utc_timestamp(), nullable = False)
        
        # Counters
        count_daily_self = Column(Int32, default = 0, nullable = False)
        count_daily_by_related = Column(Int32, default = 0, nullable = False)
        count_daily_for_related = Column(Int32, default = 0, nullable = False)
        count_top_gg_vote = Column(Int32, default = 0, nullable = False)
        
        # Relationships
        relationship_value = Column(Int64, default = 0, nullable = False)
        relationship_divorces = Column(Int32, default = 0, nullable = False)
        relationship_slots = Column(Int32, default = 1, nullable = False)
    
    
    USER_BALANCE_TABLE = user_balance_model.__table__
    
    
    class automation_reaction_role_model(BASE):
        __tablename__   = 'AUTOMATION_REACTION_ROLE'
        id              = Column(Int64, primary_key = True)
        
        guild_id        = Column(Int64, nullable = False)
        message_id      = Column(Int64, nullable = False, unique = True)
        channel_id      = Column(Int64, nullable = True)
        
        flags           = Column(Int64)
        data            = Column(Binary(), nullable = True)
        data_version    = Column(Int16, nullable = False)
    
    AUTOMATION_REACTION_ROLE_TABLE = automation_reaction_role_model.__table__
    
    
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
    
    
    class stats_model(BASE):
        __tablename__ = 'WAIFU_STATS'
        
        id = Column(Int64, primary_key = True)
        user_id = Column(Int64, unique = True)
        
        stat_housewife = Column(Int32)
        stat_cuteness = Column(Int32)
        stat_bedroom = Column(Int32)
        stat_charm = Column(Int32)
        stat_loyalty = Column(Int32)
        
        credibility = Column(Int64, default = 0, nullable = False)
        recovering_until = Column(DateTime, nullable = True)
        
        item_id_costume = Column(Int32, default = 0, nullable = False)
        item_id_head = Column(Int32, default = 0, nullable = False)
        item_id_species = Column(Int32, default = 0, nullable = False)
        item_id_weapon = Column(Int32, default = 0, nullable = False)
        
    
    STATS_TABLE = stats_model.__table__
    
        
    class automation_configuration_model(BASE):
        __tablename__ = 'AUTOMATION_CONFIGURATION'
        
        id = Column(Int64, nullable = False, primary_key = True)
        guild_id = Column(Int64, unique = True, nullable = False)
        
        # Logging
        log_emoji_channel_id = Column(Int64, nullable = False)
        log_emoji_enabled = Column(Boolean, default = False, nullable = False)
        log_mention_channel_id = Column(Int64, nullable = False)
        log_mention_enabled = Column(Boolean, default = False, nullable = False)
        log_sticker_channel_id = Column(Int64, nullable = False)
        log_sticker_enabled = Column(Boolean, default = False, nullable = False)
        log_user_channel_id = Column(Int64, nullable = False)
        log_user_enabled = Column(Boolean, default = False, nullable = False)
        
        # Satori
        log_satori_auto_start = Column(Boolean, default = False, nullable = False)
        log_satori_channel_id = Column(Int64, nullable = False)
        log_satori_enabled = Column(Boolean, default = False, nullable = False)
        
        # Reaction copy
        reaction_copy_enabled = Column(Boolean, default = False, nullable = False)
        reaction_copy_flags = Column(Int64, nullable = False)
        reaction_copy_role_id = Column(Int64, nullable = False)
        
        # Touhou feed
        touhou_feed_enabled = Column(Boolean, default = False, nullable = False)
        
        # Welcome
        welcome_channel_id = Column(Int64, nullable = False)
        welcome_enabled = Column(Boolean, default = False, nullable = False)
        welcome_reply_buttons_enabled = Column(Boolean, default = False, nullable = False)
        welcome_style_name = Column(String, default = None, nullable = True)
        
        # Farewell
        farewell_channel_id = Column(Int64, nullable = False)
        farewell_enabled = Column(Boolean, default = False, nullable = False)
        farewell_style_name = Column(String, default = None, nullable = True)
        
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
    
    
    class user_settings_model(BASE):
        __tablename__ = 'USER_SETTINGS'
        id = Column(Int64, nullable = False, primary_key = True)
        user_id = Column(Int64, nullable = False)
        notification_daily_by_waifu = Column(Boolean, default = True, nullable = False)
        notification_daily_reminder = Column(Boolean, default = False, nullable = False)
        notification_gift = Column(Boolean, default = True, nullable = False)
        notification_proposal = Column(Boolean, default = True, nullable = False)
        notification_vote = Column(Boolean, default = True, nullable = False)
        preferred_client_id = Column(Int64, default = 0, nullable = False)
        preferred_image_source = Column(Int16, default = 0, nullable = False)
    
    
    USER_SETTINGS_TABLE = user_settings_model.__table__
    
    
    class blacklist_model(BASE):
        __tablename__   = 'BLACKLIST'
        
        id = Column(Int64, nullable = False, primary_key = True)
        user_id = Column(Int64, nullable = False)
    
    BLACKLIST_TABLE = blacklist_model.__table__
    
    
    class external_events_model(BASE):
        __tablename__ = 'EXTERNAL_EVENTS'
        id = Column(Int64, nullable = False, primary_key = True)
        client_id = Column(Int64, nullable = False)
        user_id = Column(Int64, nullable = False)
        event_type = Column(Int32, default = 0, nullable = False)
        event_data = Column(Binary(), nullable = True)
        guild_id = Column(Int64, nullable = False)
        trigger_after = Column(DateTime, nullable = True)
    
    
    EXTERNAL_EVENTS_TABLE = external_events_model.__table__
    
    
    class relationship_request_model(BASE):
        __tablename__   = 'RELATIONSHIP_REQUESTS'
        
        id = Column(Int64, primary_key = True, nullable = False)
        source_user_id = Column(Int64, unique = False, nullable = False)
        target_user_id = Column(Int64, unique = False, nullable = False)
        investment = Column(Int64, default = 0, nullable = False)
        relationship_type = Column(Int16, unique = False, nullable = False)
    
    
    RELATIONSHIP_REQUEST_TABLE = relationship_request_model.__table__
    
    
    class relationship_model(BASE):
        __tablename__   = 'RELATIONSHIPS'
        
        id = Column(Int64, primary_key = True, nullable = False)
        source_user_id = Column(Int64, unique = False, nullable = False)
        target_user_id = Column(Int64, unique = False, nullable = False)
        source_investment = Column(Int64, default = 0, nullable = False)
        target_investment = Column(Int64, default = 0, nullable = False)
        source_can_boost_at = Column(DateTime, nullable = False)
        target_can_boost_at = Column(DateTime, nullable = False)
        relationship_type = Column(Int16, unique = False, nullable = False)
    
    
    RELATIONSHIP_TABLE = relationship_model.__table__
    
    
    class expression_counter_model(BASE):
        __tablename__   = 'EXPRESSION_COUNTER'
        id              = Column(Int64, primary_key = True)
        
        entity_id       = Column(Int64, nullable = False)
        action_type     = Column(Int16, nullable = False)
        
        user_id         = Column(Int64, nullable = False)
        message_id      = Column(Int64, nullable = False)
        channel_id      = Column(Int64, nullable = False)
        guild_id        = Column(Int64, nullable = False)
        timestamp       = Column(DateTime, nullable = False)
    
    EXPRESSION_COUNTER_TABLE = expression_counter_model.__table__
    
    
    class item_model(BASE):
        __tablename__   = 'ITEM'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64, nullable = False)
        amount          = Column(Int64, nullable = False, default = 0)
        item_id         = Column(Int32, nullable = False)
    
    ITEM_TABLE = item_model.__table__
    
    
    class guild_stats_model(BASE):
        __tablename__ = 'GUILD_STATS'
        id            = Column(Int64, primary_key = True)
        guild_id      = Column(Int64, default = 0, nullable = False)
        credibility   = Column(Int64, default = 0, nullable = False)
    
    GUILD_STATS_TABLE = guild_stats_model.__table__
    
    
    class linked_quest_model(BASE):
        __tablename__      = 'LINKED_QUESTS'
        id                 = Column(Int64, primary_key = True)
        amount_required    = Column(Int64, default = 0, nullable = False)
        amount_submitted   = Column(Int64, default = 0, nullable = False)
        batch_id           = Column(Int64, default = 0, nullable = False)
        expires_at         = Column(DateTime, nullable = False)
        guild_id           = Column(Int64, default = 0, nullable = False)
        reward_balance     = Column(Int64, default = 0, nullable = False)
        reward_credibility = Column(Int64, default = 0, nullable = False)
        taken_at           = Column(DateTime, nullable = False)
        template_id        = Column(Int64, default = 0, nullable = False)
        user_id            = Column(Int64, default = 0, nullable = False)
        completion_state   = Column(Int16, default = 1, nullable = False)
        completion_count   = Column(Int32, default = 0, nullable = False)
    
    LINKED_QUEST_TABLE = linked_quest_model.__table__
    
    
    class adventure_action_model(BASE):
        __tablename__   = 'ADVENTURE_ACTIONS'
        id              = Column(Int64, primary_key = True)
        adventure_entry_id = Column(Int64, nullable = False)
        action_id       = Column(Int32, nullable = False)
        created_at      = Column(DateTime, nullable = False)
        
        battle_data     = Column(Binary(), nullable = True)
        loot_data       = Column(Binary(), nullable = True)
        
        health_exhausted = Column(Int64, nullable = False)
        energy_exhausted = Column(Int64, nullable = False)
    
    
    ADVENTURE_ACTION_TABLE = adventure_action_model.__table__
    
    
    class adventure_model(BASE):
        __tablename__   = 'ADVENTURES'
        id              = Column(Int64, primary_key = True)
        user_id         = Column(Int64, nullable = False)
        
        location_id     = Column(Int32, nullable = False)
        target_id       = Column(Int32, nullable = False)
        return_id       = Column(Int32, nullable = False)
        auto_cancellation_id = Column(Int32, nullable = False)
        state           = Column(Int32, nullable = False)
        
        initial_duration = Column(Int64, nullable = False)
        created_at      = Column(DateTime, nullable = False)
        updated_at      = Column(DateTime, nullable = False)
        action_count    = Column(Int32, nullable = False)
        seed            = Column(Int64, nullable = False)
        
        health_initial = Column(Int64, nullable = False)
        health_exhausted = Column(Int64, nullable = False)
        energy_initial = Column(Int64, nullable = False)
        energy_exhausted = Column(Int64, nullable = False)
    
    ADVENTURE_TABLE = adventure_model.__table__
    
    DB_ENGINE.dispose()
    # BASE.metadata.create_all(DB_ENGINE)
