__all__ = ('CommonFields',)

from datetime import datetime

from bot_utils.models import DB_ENGINE, USER_COMMON_TABLE, user_common_model
from bot_utils.model_linker import ModelLink, Field


class CommonFields(ModelLink, model=user_common_model, table=USER_COMMON_TABLE, engine=DB_ENGINE):
    __slots__ = ()
    
    def __new__(cls, user):
        self = ModelLink.__new__(cls, user)
        self.user_id = user.id
        return self
    
    user_id = Field(user_common_model.user_id, 0, query_key = 'user_id')
    entry_id = Field(user_common_model.id, 0, primary_key = True)
    
    total_love = Field(user_common_model.total_love, 0)
    total_allocated = Field(user_common_model.total_allocated, 0)
    
    daily_next = Field(user_common_model.daily_next, datetime.utcnow)
    daily_streak = Field(user_common_model.daily_streak, 0)
    
    count_daily_self = Field(user_common_model.count_daily_self, 0)
    count_daily_by_waifu = Field(user_common_model.count_daily_by_waifu, 0)
    count_daily_for_waifu = Field(user_common_model.count_daily_for_waifu, 0)
    count_top_gg_vote = Field(user_common_model.count_top_gg_vote, 0)
    
    waifu_cost = Field(user_common_model.waifu_cost, 0)
    waifu_divorces = Field(user_common_model.waifu_divorces, 0)
    waifu_slots = Field(user_common_model.waifu_slots, 0)
    waifu_owner_id = Field(user_common_model.waifu_owner_id, 0)
    
    notify_proposal = Field(user_common_model.notify_proposal, 0)
    notify_daily = Field(user_common_model.notify_daily, 0)
    top_gg_last_vote = Field(user_common_model.top_gg_last_vote, datetime.utcnow)
