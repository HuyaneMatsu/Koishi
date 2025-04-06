import vampytest

from ...item_core import Item

from ..constants import STATS_CACHE
from ..stats import Stats
from ..stats_calculated import StatsCalculated


def _assert_fields_set(stats_calculated):
    """
    Tests whether teh given stats calculated has all of its fields set.
    
    Parameters
    ----------
    stats_calculated : ``StatsCalculated``
        The instance to check its fields.
    """
    vampytest.assert_instance(stats_calculated, StatsCalculated)
    vampytest.assert_instance(stats_calculated.extra_fishing, int)
    vampytest.assert_instance(stats_calculated.extra_inventory, int)
    vampytest.assert_instance(stats_calculated.item_costume, Item, nullable = True)
    vampytest.assert_instance(stats_calculated.item_head, Item, nullable = True)
    vampytest.assert_instance(stats_calculated.item_species, Item, nullable = True)
    vampytest.assert_instance(stats_calculated.item_weapon, Item, nullable = True)
    vampytest.assert_instance(stats_calculated.stat_bedroom, int)
    vampytest.assert_instance(stats_calculated.stat_charm, int)
    vampytest.assert_instance(stats_calculated.stat_cuteness, int)
    vampytest.assert_instance(stats_calculated.stat_housewife, int)
    vampytest.assert_instance(stats_calculated.stat_loyalty, int)


def test__StatsCalculated__new():
    """
    Tests whether ``StatsCalculated.__new__`` works as intended.
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
        
        stats = Stats.from_entry(entry)
        
        stats_calculated = StatsCalculated(stats)
        _assert_fields_set(stats_calculated)
        
        vampytest.assert_eq(stats_calculated.extra_fishing, 23)
        vampytest.assert_eq(stats_calculated.extra_inventory, 56250)
        vampytest.assert_is(stats_calculated.item_costume, None)
        vampytest.assert_is(stats_calculated.item_head, None)
        vampytest.assert_is(stats_calculated.item_species, None)
        vampytest.assert_is(stats_calculated.item_weapon, None)
        vampytest.assert_eq(stats_calculated.stat_bedroom, stat_bedroom)
        vampytest.assert_eq(stats_calculated.stat_charm, stat_charm)
        vampytest.assert_eq(stats_calculated.stat_cuteness, stat_cuteness)
        vampytest.assert_eq(stats_calculated.stat_housewife, stat_housewife)
        vampytest.assert_eq(stats_calculated.stat_loyalty, stat_loyalty)
        
    finally:
        STATS_CACHE.clear()


def test__StatsCalculated__repr():
    """
    Tests whether ``StatsCalculated.__repr__`` works as intended.
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
        
        stats = Stats.from_entry(entry)
        
        stats_calculated = StatsCalculated(stats)
        output = repr(stats_calculated)
        vampytest.assert_instance(output, str)
        
    finally:
        STATS_CACHE.clear()
