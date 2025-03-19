import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import STATS_CACHE
from ..stats import Stats
from ..stats_saver import StatsSaver


def _assert_fields_set(stats_saver):
    """
    Tests whether every fields are set of the given stats request saver.
    
    Parameters
    ----------
    stats_saver : ``StatsSaver``
        The instance to check.
    """
    vampytest.assert_instance(stats_saver, StatsSaver)
    vampytest.assert_instance(stats_saver.entry_proxy, Stats)
    vampytest.assert_instance(stats_saver.ensured_for_deletion, bool)
    vampytest.assert_instance(stats_saver.modified_fields, dict, nullable = True)
    vampytest.assert_instance(stats_saver.run_task, Task, nullable = True)


def test__StatsSaver__new():
    """
    Tests whether ``StatsSaver.__new__`` works as intended.
    """
    user_id = 20250310000
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        _assert_fields_set(stats_saver)
        
        vampytest.assert_is(stats_saver.entry_proxy, stats)

    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__StatsSaver__repr():
    """
    Tests whether ``StatsSaver.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 20250310001
    
    new_stat_housewife = 2002
    
    try:
        stats = Stats(user_id)
        
        ensured_for_deletion = True
        modified_fields = {'stat_housewife': new_stat_housewife}
        
        stats_saver = StatsSaver(stats)
        stats_saver.ensured_for_deletion = ensured_for_deletion
        stats_saver.modified_fields = modified_fields
        stats_saver.run_task = Task(get_event_loop(), stats_saver.run())
        
        output = repr(stats_saver)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(StatsSaver.__name__, output)
        vampytest.assert_in(f'entry_proxy = {stats!r}', output)
        vampytest.assert_in(f'ensured_for_deletion = {ensured_for_deletion!r}', output)
        vampytest.assert_in(f'modified_fields = {modified_fields!r}', output)
        vampytest.assert_in(f'running = {True!r}', output)
    
    finally:
        STATS_CACHE.clear()


def test__StatsSaver__add_modification():
    """
    Tests whether ``StatsSaver.add_modification`` works as intended.
    """
    user_id = 20250310002
    
    new_stat_housewife = 2002
    new_stat_loyalty = 2000
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        
        vampytest.assert_eq(
            stats_saver.modified_fields,
            None,
        )
        
        stats_saver.add_modification('stat_housewife', new_stat_housewife)
        
        vampytest.assert_eq(
            stats_saver.modified_fields,
            {
                'stat_housewife': new_stat_housewife,
            }
        )
        
        stats_saver.add_modification('stat_loyalty', new_stat_loyalty)
        
        vampytest.assert_eq(
            stats_saver.modified_fields,
            {
                'stat_housewife': new_stat_housewife,
                'stat_loyalty': new_stat_loyalty,
            }
        )
    
    finally:
        STATS_CACHE.clear()


def test__StatsSaver__ensure_deletion():
    """
    Tests whether ``StatsSaver.ensure_deletion`` works as intended.
    """
    user_id = 20250310003
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        
        vampytest.assert_eq(stats_saver.ensured_for_deletion, False)
        
        stats_saver.ensure_deletion()
        
        vampytest.assert_eq(stats_saver.ensured_for_deletion, True)
    
    finally:
        STATS_CACHE.clear()


def test__StatsSaver__is_modified__not():
    """
    Tests whether ``StatsSaver.is_modified`` works as intended.
    
    Case: not modified.
    """
    user_id = 20250310004
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        
        output = stats_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        STATS_CACHE.clear()


def test__StatsSaver__is_modified__delete():
    """
    Tests whether ``StatsSaver.is_modified`` works as intended.
    
    Case: ensured for deletion.
    """
    user_id = 20250310005
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        stats_saver.ensure_deletion()
        
        output = stats_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        STATS_CACHE.clear()


def test__StatsSaver__is_modified__field():
    """
    Tests whether ``StatsSaver.is_modified`` works as intended.
    
    Case: field modified.
    """
    user_id = 20250310005
    
    new_stat_housewife = 2002
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        stats_saver.add_modification('stat_housewife', new_stat_housewife)
        
        output = stats_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__StatsSaver__begin():
    """
    Tests whether ``StatsSaver.begin`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 20250310006
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        stats.saver = stats_saver
        
        output = stats_saver.begin()
        
        vampytest.assert_instance(output, Task)
        vampytest.assert_is(stats_saver.run_task, output)
        vampytest.assert_is(stats.saver, stats_saver)
        
        # do save
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        # after save nothing should be set.
        vampytest.assert_is(stats_saver.run_task, None)
        vampytest.assert_is(stats.saver, None)
    
    finally:
        STATS_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def StatsSaver__running():
    """
    Tests whether ``StatsSaver.running`` works as intended.
    """
    user_id = 20250310007
    
    try:
        stats = Stats(user_id)
        
        stats_saver = StatsSaver(stats)
        stats.saver = stats_saver
        
        output = stats_saver.running
        vampytest.assert_eq(output, False)
        
        stats_saver.begin()
        
        output = stats_saver.running
        vampytest.assert_eq(output, True)
        
    finally:
        STATS_CACHE.clear()
