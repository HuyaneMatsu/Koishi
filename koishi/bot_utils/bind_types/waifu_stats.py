__all__ = ('WaifuStats', )

from math import floor

from ...bot_utils.models import DB_ENGINE, WAIFU_STATS_TABLE, waifu_stats_model
from ...bot_utils.model_linker import ModelLink, Field


STAT_MASKS = [
    219902325437,
    219902325439,
    219902325491,
    219902325497,
    219902325523,
]


STAT_COUNT = 5  

def get_multiplier_fields(value):
    positive = [(value - 1) % STAT_COUNT, (value + 1) % STAT_COUNT]
    negative = [index for index in range(STAT_COUNT) if (index != value) and (value not in positive)]
    
    return positive, negative


def generate_multiplier_fields():
    return {index: get_multiplier_fields(index) for index in range(STAT_COUNT)}


MULTIPLIER_FIELDS = generate_multiplier_fields()
MULTIPLIER_FACTOR = 1.0 / 4.0
MAX_MULTIPLIER = 10.0 * MULTIPLIER_FACTOR


def get_default_user_stats(user_id):
    # structure:
    # 1 bit +/-
    # 41 date
    # 22 bit server info
    
    # We use only the date one, so everything we use is shifted by 22 bits
    # then we cut down the last 24 bits of the date and switch it with the first 19
    mask = ((user_id & 0x1ffffc00000000000) >> 46) | ((user_id & 0x3fffffc00000) >> 3)
    
    stats = [(mask & stat_mask) % 11 for stat_mask in STAT_MASKS]
    
    bonuses = [0.0 for x in range(STAT_COUNT)]
    
    for index in range(STAT_COUNT):
        bonus = stats[index] * MULTIPLIER_FACTOR
        positive, negative = MULTIPLIER_FIELDS[index]
        
        local_bonus = (bonus / len(positive))
        for index in positive:
            bonuses[index] += local_bonus
        
        bonus = MAX_MULTIPLIER - bonus
        
        local_bonus = (bonus / len(negative))
        for index in negative:
            bonuses[index] += local_bonus
    
    for index in range(STAT_COUNT):
        bonus = bonuses[index]
        bonus = floor(bonus)
        
        value = stats[index]
        
        value = value + bonus
        if value > 10:
            value = 10
        elif value < 0:
            value = 0
        
        stats[index] = value
    
    return stats



class WaifuStats(ModelLink, model = waifu_stats_model, table = WAIFU_STATS_TABLE, engine = DB_ENGINE):
    __slots__ = ()
    
    def __new__(cls, user):
        self = ModelLink.__new__(cls, user)
        self.user_id = user.id
        return self
    
    user_id = Field(getattr(waifu_stats_model, 'user_id', None), 0, query_key = 'user_id')
    entry_id = Field(getattr(waifu_stats_model, 'id', None), 0, primary_key = True)
    
    stat_housewife = Field(getattr(waifu_stats_model, 'stat_housewife', None), 0)
    stat_cuteness = Field(getattr(waifu_stats_model, 'stat_cuteness', None), 0)
    stat_bedroom = Field(getattr(waifu_stats_model, 'stat_bedroom', None), 0)
    stat_charm = Field(getattr(waifu_stats_model, 'stat_charm', None), 0)
    stat_loyalty = Field(getattr(waifu_stats_model, 'stat_loyalty', None), 0)
    
    level = Field(getattr(waifu_stats_model, 'level', None), 0)
    experience = Field(getattr(waifu_stats_model, 'experience', None), 0)
    
    raw_species = Field(getattr(waifu_stats_model, 'raw_species', None), b'')
    raw_weapon = Field(getattr(waifu_stats_model, 'raw_weapon', None), b'')
    raw_costume = Field(getattr(waifu_stats_model, 'raw_costume', None), b'')
    
    
    def __set_initial_values__(self):
        (
            self.stat_housewife,
            self.stat_cuteness,
            self.stat_bedroom,
            self.stat_charm,
            self.stat_loyalty,
        ) = get_default_user_stats(self.user_id)
        ModelLink.__set_initial_values__(self)
