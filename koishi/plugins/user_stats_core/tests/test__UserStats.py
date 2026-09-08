from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..user_stats import (
    USER_STATS_MODIFICATION_FLAG_CREDIBILITY, USER_STATS_MODIFICATION_FLAG_ITEM_ID_COSTUME,
    USER_STATS_MODIFICATION_FLAG_ITEM_ID_HEAD, USER_STATS_MODIFICATION_FLAG_ITEM_ID_SPECIES,
    USER_STATS_MODIFICATION_FLAG_ITEM_ID_WEAPON, USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL,
    USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL_NOTIFICATION_AT, USER_STATS_MODIFICATION_FLAG_STAT_BEDROOM,
    USER_STATS_MODIFICATION_FLAG_STAT_CHARM, USER_STATS_MODIFICATION_FLAG_STAT_CUTENESS,
    USER_STATS_MODIFICATION_FLAG_STAT_HOUSEWIFE, USER_STATS_MODIFICATION_FLAG_STAT_LOYALTY, UserStats,
    user_stats_calculate, user_stats_collect_modifications, user_stats_create, user_stats_create_from_entry,
    user_stats_modify_credibility_by, user_stats_modify_stat_bedroom_by, user_stats_modify_stat_charm_by,
    user_stats_modify_stat_cuteness_by, user_stats_modify_stat_housewife_by, user_stats_modify_stat_loyalty_by,
    user_stats_set_item_id_costume, user_stats_set_item_id_head, user_stats_set_item_id_species,
    user_stats_set_item_id_weapon, user_stats_set_recovering_until, user_stats_set_recovering_until_notification_at
)
from ..user_stats_calculated import UserStatsCalculated


def assert_user_stats_fields_set(user_stats):
    """
    Asserts whether every fields are set of the user_stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        UserStats to test.
    """
    vampytest.assert_instance(user_stats, UserStats)
    vampytest.assert_instance(user_stats._cache_user_stats_calculated, UserStatsCalculated, nullable = True)
    vampytest.assert_instance(user_stats.entry_id, int)
    vampytest.assert_instance(user_stats.credibility, int)
    vampytest.assert_instance(user_stats.item_id_costume, int)
    vampytest.assert_instance(user_stats.item_id_head, int)
    vampytest.assert_instance(user_stats.item_id_species, int)
    vampytest.assert_instance(user_stats.item_id_weapon, int)
    vampytest.assert_instance(user_stats.modification_flags, int)
    vampytest.assert_instance(user_stats.recovering_until, DateTime, nullable = True)
    vampytest.assert_instance(user_stats.recovering_until_notification_at, DateTime, nullable = True)
    vampytest.assert_instance(user_stats.stat_bedroom, int)
    vampytest.assert_instance(user_stats.stat_charm, int)
    vampytest.assert_instance(user_stats.stat_cuteness, int)
    vampytest.assert_instance(user_stats.stat_housewife, int)
    vampytest.assert_instance(user_stats.stat_loyalty, int)
    vampytest.assert_instance(user_stats.user_id, int)


def test__UserStats__repr():
    """
    Tests whether ``user_stats.__repr__`` works as intended.
    """
    user_id = 20250310009
    entry_id = 19999
    
    user_stats = user_stats_create(user_id)
    
    user_stats.entry_id = entry_id
    
    output = repr(user_stats)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(UserStats.__name__, output)
    vampytest.assert_in(f'entry_id = {entry_id!r}', output)
    vampytest.assert_in(f'user_id = {user_id!r}', output)


def test__user_stats_create():
    """
    Tests whether ``user_stats_create`` works as intended.
    """
    user_id = 20250310008
    
    user_stats = user_stats_create(user_id)
    assert_user_stats_fields_set(user_stats)


def test__user_stats_create_from_entry():
    """
    Tests whether ``user_stats_create_from_entry`` works as intended.
    """
    user_id = 20250310013
    
    stat_housewife = 11
    stat_cuteness = 12
    stat_bedroom = 13
    stat_charm = 14
    stat_loyalty = 15
    
    credibility = 12222
    recovering_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    recovering_until_notification_at = DateTime(2016, 5, 14, 1, 0, 0, tzinfo = TimeZone.utc)
    
    item_id_costume = 2
    item_id_head = 3
    item_id_species = 4
    item_id_weapon = 5
    
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
        'recovering_until': recovering_until.replace(tzinfo = None),
        'recovering_until_notification_at': recovering_until_notification_at.replace(tzinfo = None),
        
        'item_id_costume': item_id_costume,
        'item_id_head': item_id_head,
        'item_id_species': item_id_species,
        'item_id_weapon': item_id_weapon,
    }
    
    user_stats = user_stats_create_from_entry(entry)
    assert_user_stats_fields_set(user_stats)
    
    vampytest.assert_eq(user_stats.entry_id, entry_id)
    vampytest.assert_eq(user_stats.user_id, user_id)
    
    vampytest.assert_eq(user_stats.stat_housewife, stat_housewife)
    vampytest.assert_eq(user_stats.stat_cuteness, stat_cuteness)
    vampytest.assert_eq(user_stats.stat_bedroom, stat_bedroom)
    vampytest.assert_eq(user_stats.stat_charm, stat_charm)
    vampytest.assert_eq(user_stats.stat_loyalty, stat_loyalty)
    
    vampytest.assert_eq(user_stats.credibility, credibility)
    vampytest.assert_eq(user_stats.recovering_until, recovering_until)
    vampytest.assert_eq(user_stats.recovering_until_notification_at, recovering_until_notification_at)
    
    vampytest.assert_eq(user_stats.item_id_costume, item_id_costume)
    vampytest.assert_eq(user_stats.item_id_head, item_id_head)
    vampytest.assert_eq(user_stats.item_id_species, item_id_species)
    vampytest.assert_eq(user_stats.item_id_weapon, item_id_weapon)


def test__user_stats_calculate():
    """
    Tests whether ``user_stats_calculate`` works as intended.
    """
    user_id = 202503230002
    
    user_stats = user_stats_create(user_id)
    assert_user_stats_fields_set(user_stats)
    
    user_stats_calculated = user_stats_calculate(user_stats)
    vampytest.assert_instance(user_stats_calculated, UserStatsCalculated)
    vampytest.assert_is(user_stats._cache_user_stats_calculated, user_stats_calculated)


def test__user_stats_modify_stat_housewife_by():
    """
    Tests whether ``user_stats_modify_stat_housewife_by`` works as intended.
    """
    current = 10
    amount = 2
    
    user_stats = user_stats_create(202511290000)
    user_stats.stat_housewife = current
    user_stats_modify_stat_housewife_by(user_stats, amount)
    
    vampytest.assert_eq(user_stats.stat_housewife, current + amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_HOUSEWIFE)



def test__user_stats_modify_stat_cuteness_by():
    """
    Tests whether ``user_stats_modify_stat_cuteness_by`` works as intended.
    """
    current = 10
    amount = 2
    
    user_stats = user_stats_create(202511290001)
    user_stats.stat_cuteness = current
    user_stats_modify_stat_cuteness_by(user_stats, amount)
    
    vampytest.assert_eq(user_stats.stat_cuteness, current + amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_CUTENESS)


def test__user_stats_modify_stat_bedroom_by():
    """
    Tests whether ``user_stats_modify_stat_bedroom_by`` works as intended.
    """
    current = 10
    amount = 2
    
    user_stats = user_stats_create(202511290002)
    user_stats.stat_bedroom = current
    user_stats_modify_stat_bedroom_by(user_stats, amount)
    
    vampytest.assert_eq(user_stats.stat_bedroom, current + amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_BEDROOM)


def test__user_stats_modify_stat_charm_by():
    """
    Tests whether ``user_stats_modify_stat_charm_by`` works as intended.
    """
    current = 10
    amount = 2
    
    user_stats = user_stats_create(202511290003)
    user_stats.stat_charm = current
    user_stats_modify_stat_charm_by(user_stats, amount)
    
    vampytest.assert_eq(user_stats.stat_charm, current + amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_CHARM)


def test__user_stats_modify_stat_loyalty_by():
    """
    Tests whether ``user_stats_modify_stat_loyalty_by`` works as intended.
    """
    current = 10
    amount = 2
    
    user_stats = user_stats_create(202511290004)
    user_stats.stat_loyalty = current
    user_stats_modify_stat_loyalty_by(user_stats, amount)
    
    vampytest.assert_eq(user_stats.stat_loyalty, current + amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_LOYALTY)


def test__user_stats_set_recovering_until():
    """
    Tests whether ``user_stats_set_recovering_until`` works as intended.
    """
    current = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    amount = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    user_stats = user_stats_create(202511290005)
    user_stats.recovering_until = current
    user_stats_set_recovering_until(user_stats, amount)
    
    vampytest.assert_eq(user_stats.recovering_until, amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL)


def test__user_stats_set_set_recovering_until_notification_at():
    """
    Tests whether ``user_stats_set_set_recovering_until_notification_at`` works as intended.
    """
    current = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    amount = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    user_stats = user_stats_create(202511290005)
    user_stats.recovering_until_notification_at = current
    user_stats_set_recovering_until_notification_at(user_stats, amount)
    
    vampytest.assert_eq(user_stats.recovering_until_notification_at, amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL_NOTIFICATION_AT)


def test__user_stats_modify_credibility_by():
    """
    Tests whether ``user_stats_modify_credibility_by`` works as intended.
    """
    current = 10
    amount = 2
    
    user_stats = user_stats_create(202511290006)
    user_stats.credibility = current
    user_stats_modify_credibility_by(user_stats, amount)
    
    vampytest.assert_eq(user_stats.credibility, current + amount)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_CREDIBILITY)


def test__user_stats_set_item_id_costume():
    """
    Tests whether ``user_stats_set_item_id_costume`` works as intended.
    """
    current = 10
    item_id = 12
    
    user_stats = user_stats_create(202511290007)
    user_stats.item_id_costume = current
    user_stats_set_item_id_costume(user_stats, item_id)
    
    vampytest.assert_eq(user_stats.item_id_costume, item_id)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_COSTUME)


def test__user_stats_set_item_id_head():
    """
    Tests whether ``user_stats_set_item_id_head`` works as intended.
    """
    current = 10
    item_id = 12
    
    user_stats = user_stats_create(202511290008)
    user_stats.item_id_head = current
    user_stats_set_item_id_head(user_stats, item_id)
    
    vampytest.assert_eq(user_stats.item_id_head, item_id)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_HEAD)


def test__user_stats_set_item_id_species():
    """
    Tests whether ``user_stats_set_item_id_species`` works as intended.
    """
    current = 10
    item_id = 12
    
    user_stats = user_stats_create(202511290009)
    user_stats.item_id_species = current
    user_stats_set_item_id_species(user_stats, item_id)
    
    vampytest.assert_eq(user_stats.item_id_species, item_id)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_SPECIES)


def test__user_stats_set_item_id_weapon():
    """
    Tests whether ``user_stats_set_item_id_weapon`` works as intended.
    """
    current = 10
    item_id = 12
    
    user_stats = user_stats_create(202511290010)
    user_stats.item_id_weapon = current
    user_stats_set_item_id_weapon(user_stats, item_id)
    
    vampytest.assert_eq(user_stats.item_id_weapon, item_id)
    vampytest.assert_true(user_stats.modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_WEAPON)


def test__user_stats_collect_modifications():
    """
    Tests whether ``user_stats_collect_modifications`` works as intended.
    """
    user_stats = user_stats_create(202609040000)
    
    user_stats_set_item_id_costume(user_stats, 12)
    user_stats_set_item_id_weapon(user_stats, 23)
    
    output = user_stats_collect_modifications(user_stats)
    
    vampytest.assert_eq(
        output,
        {
            'item_id_costume': 12,
            'item_id_weapon': 23,
        },
    )
    vampytest.assert_eq(user_stats.modification_flags, 0)
