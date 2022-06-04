__all__ = ('WaifuType', )

from bot_utils.models import DB_ENGINE, WAIFU_STATS_TABLE, waifu_stats_model
from bot_utils.model_linker import ModelLink, Field


class WaifuType(ModelLink, model=waifu_stats_model, table=WAIFU_STATS_TABLE, engine=DB_ENGINE):
    __slots__ = ()
    
    def __new__(cls, user):
        self = WaifuType.__new__(cls, user)
        self.user_id = user.id
        return self
    
    user_id = Field(waifu_stats_model.user_id, 0, query_key='user_id')
    entry_id = Field(waifu_stats_model.id, 0, primary_key=True)
    
    stat_housewife = Field(waifu_stats_model.stat_housewife, 0)
    stat_cuteness = Field(waifu_stats_model.stat_cuteness, 0)
    stat_bedroom = Field(waifu_stats_model.stat_bedroom, 0)
    stat_charm = Field(waifu_stats_model.stat_charm, 0)
    stat_loyalty = Field(waifu_stats_model.stat_loyalty, 0)
    
    level = Field(waifu_stats_model.level, 0)
    experience = Field(waifu_stats_model.experience, 0)
    
    raw_species = Field(waifu_stats_model.raw_species, 0)
    raw_weapon = Field(waifu_stats_model.raw_weapon, 0)
    raw_costume = Field(waifu_stats_model.raw_costume, 0)
