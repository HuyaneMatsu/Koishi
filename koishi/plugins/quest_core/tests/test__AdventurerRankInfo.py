import vampytest

from ..adventurer_rank_info import AdventurerRankInfo, adventure_rank_info_create


def test__adventure_rank_info_create():
    level = 1
    quest_limit = 1
    
    adventurer_rank_info = adventure_rank_info_create(level, quest_limit)
    
    vampytest.assert_eq(adventurer_rank_info.level, level)
    vampytest.assert_eq(adventurer_rank_info.quest_limit, quest_limit)
    
    vampytest.assert_instance(adventurer_rank_info, AdventurerRankInfo)
    vampytest.assert_instance(adventurer_rank_info.level, int)
    vampytest.assert_instance(adventurer_rank_info.quest_limit, int)
