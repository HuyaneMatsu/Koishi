import vampytest

from ...item_core import Item

from ..constants import STATS_CACHE
from ..user_stats import UserStats
from ..user_stats_calculated import UserStatsCalculated


def _assert_fields_set(user_stats_calculated):
    """
    Tests whether teh given stats calculated has all of its fields set.
    
    Parameters
    ----------
    user_stats_calculated : ``UserStatsCalculated``
        The instance to check its fields.
    """
    vampytest.assert_instance(user_stats_calculated, UserStatsCalculated)
    vampytest.assert_instance(user_stats_calculated.extra_fishing, int)
    vampytest.assert_instance(user_stats_calculated.extra_inventory, int)
    vampytest.assert_instance(user_stats_calculated.item_costume, Item, nullable = True)
    vampytest.assert_instance(user_stats_calculated.item_head, Item, nullable = True)
    vampytest.assert_instance(user_stats_calculated.item_species, Item, nullable = True)
    vampytest.assert_instance(user_stats_calculated.item_weapon, Item, nullable = True)
    vampytest.assert_instance(user_stats_calculated.stat_bedroom, int)
    vampytest.assert_instance(user_stats_calculated.stat_charm, int)
    vampytest.assert_instance(user_stats_calculated.stat_cuteness, int)
    vampytest.assert_instance(user_stats_calculated.stat_housewife, int)
    vampytest.assert_instance(user_stats_calculated.stat_loyalty, int)


def test__UserStatsCalculated__new():
    """
    Tests whether ``UserStatsCalculated.__new__`` works as intended.
    """
    user_id = 202503230000
    
    stat_housewife = 11
    stat_cuteness = 12
    stat_bedroom = 13
    stat_charm = 14
    stat_loyalty = 15
    
    credibility = 12222
    
    item_id_costume = 0
    item_id_head = 0
    item_id_species = 0
    item_id_weapon = 0
    
    entry_id = 3501
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        
        'stat_housewife': stat_housewife,
        'stat_cuteness': stat_cuteness,
        'stat_bedroom': stat_bedroom,
        'stat_charm': stat_charm,
        'stat_loyalty': stat_loyalty,
        
        'credibility': credibility,
        
        'item_id_costume': item_id_costume,
        'item_id_head': item_id_head,
        'item_id_species': item_id_species,
        'item_id_weapon': item_id_weapon,
    }
    
    try:
        
        stats = UserStats.from_entry(entry)
        
        user_stats_calculated = UserStatsCalculated(stats)
        _assert_fields_set(user_stats_calculated)
        
        vampytest.assert_eq(user_stats_calculated.extra_fishing, 23)
        vampytest.assert_eq(user_stats_calculated.extra_inventory, 56250)
        vampytest.assert_is(user_stats_calculated.item_costume, None)
        vampytest.assert_is(user_stats_calculated.item_head, None)
        vampytest.assert_is(user_stats_calculated.item_species, None)
        vampytest.assert_is(user_stats_calculated.item_weapon, None)
        vampytest.assert_eq(user_stats_calculated.stat_bedroom, stat_bedroom)
        vampytest.assert_eq(user_stats_calculated.stat_charm, stat_charm)
        vampytest.assert_eq(user_stats_calculated.stat_cuteness, stat_cuteness)
        vampytest.assert_eq(user_stats_calculated.stat_housewife, stat_housewife)
        vampytest.assert_eq(user_stats_calculated.stat_loyalty, stat_loyalty)
        
    finally:
        STATS_CACHE.clear()


def test__UserStatsCalculated__repr():
    """
    Tests whether ``UserStatsCalculated.__repr__`` works as intended.
    """
    user_id = 202503230001
    
    stat_housewife = 11
    stat_cuteness = 12
    stat_bedroom = 13
    stat_charm = 14
    stat_loyalty = 15
    
    credibility = 12222
    
    item_id_costume = 0
    item_id_head = 0
    item_id_species = 0
    item_id_weapon = 0
    
    entry_id = 3501
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        
        'stat_housewife': stat_housewife,
        'stat_cuteness': stat_cuteness,
        'stat_bedroom': stat_bedroom,
        'stat_charm': stat_charm,
        'stat_loyalty': stat_loyalty,
        
        'credibility': credibility,
        
        'item_id_costume': item_id_costume,
        'item_id_head': item_id_head,
        'item_id_species': item_id_species,
        'item_id_weapon': item_id_weapon,
    }
    
    try:
        
        stats = UserStats.from_entry(entry)
        
        user_stats_calculated = UserStatsCalculated(stats)
        output = repr(user_stats_calculated)
        vampytest.assert_instance(output, str)
        
    finally:
        STATS_CACHE.clear()
