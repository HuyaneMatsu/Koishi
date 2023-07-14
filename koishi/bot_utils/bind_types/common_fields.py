__all__ = ('CommonFields',)

from datetime import datetime as DateTime

from ...bot_utils.models import DB_ENGINE, USER_COMMON_TABLE, user_common_model
from ...bot_utils.model_linker import ModelLink, Field


class CommonFields(ModelLink, model = user_common_model, table = USER_COMMON_TABLE, engine = DB_ENGINE):
    __slots__ = ()
    
    def __new__(cls, user):
        self = ModelLink.__new__(cls, user)
        self.user_id = user.id
        return self
    
    user_id = Field(getattr(user_common_model, 'user_id', None), 0, query_key = 'user_id')
    entry_id = Field(getattr(user_common_model, 'id', None), 0, primary_key = True)
    
    total_love = Field(getattr(user_common_model, 'total_love', None), 0)
    total_allocated = Field(getattr(user_common_model, 'total_allocated', None), 0)
    
    daily_next = Field(getattr(user_common_model, 'daily_next', None), DateTime.utcnow)
    daily_streak = Field(getattr(user_common_model, 'daily_streak', None), 0)
    
    count_daily_self = Field(getattr(user_common_model, 'count_daily_self', None), 0)
    count_daily_by_waifu = Field(getattr(user_common_model, 'count_daily_by_waifu', None), 0)
    count_daily_for_waifu = Field(getattr(user_common_model, 'count_daily_for_waifu', None), 0)
    count_top_gg_vote = Field(getattr(user_common_model, 'count_top_gg_vote', None), 0)
    
    waifu_cost = Field(getattr(user_common_model, 'waifu_cost', None), 0)
    waifu_divorces = Field(getattr(user_common_model, 'waifu_divorces', None), 0)
    waifu_slots = Field(getattr(user_common_model, 'waifu_slots', None), 0)
    waifu_owner_id = Field(getattr(user_common_model, 'waifu_owner_id', None), 0)
    
    notify_proposal = Field(getattr(user_common_model, 'notify_proposal', None), 0)
    notify_daily = Field(getattr(user_common_model, 'notify_daily', None), 0)
    top_gg_last_vote = Field(getattr(user_common_model, 'top_gg_last_vote', None), DateTime.utcnow)
