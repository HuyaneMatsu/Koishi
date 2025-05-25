import vampytest

from ..adventurer_rank_info import AdventurerRankInfo


def _assert_fields_set(adventurer_rank_info):
    """
    Tests whether the given adventurer rank info has all of its fields set.
    
    Parameters
    ----------
    adventurer_rank_info : ``AdventurerRankInfo``
        The instance to test.
    """
    vampytest.assert_instance(adventurer_rank_info, AdventurerRankInfo)
    vampytest.assert_instance(adventurer_rank_info.level, int)
    vampytest.assert_instance(adventurer_rank_info.quest_limit, int)


def test__AdventurerRankInfo__new():
    """
    Tests whether ``AdventurerRankInfo.__new__`` works as intended.
    """
    level = 1
    quest_limit = 1
    
    adventurer_rank_info = AdventurerRankInfo(level, quest_limit)
    
    vampytest.assert_eq(adventurer_rank_info.level, level)
    vampytest.assert_eq(adventurer_rank_info.quest_limit, quest_limit)


def test__AdventurerRankInfo__repr():
    """
    Tests whether ``AdventurerRankInfo.__repr__`` works as intended.
    """
    level = 1
    quest_limit = 1
    
    adventurer_rank_info = AdventurerRankInfo(level, quest_limit)
    
    output = repr(adventurer_rank_info)
    vampytest.assert_instance(output, str)
