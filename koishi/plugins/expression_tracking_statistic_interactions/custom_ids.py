__all__ = ()

from re import compile as re_compile


CUSTOM_ID_EXPRESSION_TRACKING_STATISTIC_VIEW_BUILDER = (
    lambda 
        user_id,
        mode,
        entity_id,
        action_types_packed,
        entity_filter_rule,
        months,
        page_index,
        page_size,
        order_decreasing
    : (
        f'expression_tracking.stats.{user_id:x}.{mode:x}.{entity_id:x}.{action_types_packed:x}.{entity_filter_rule:x}.'
        f'{months:x}.{page_index:x}.{page_size:x}.{order_decreasing:x}'
    )
)


CUSTOM_ID_EXPRESSION_TRACKING_STATISTIC_VIEW_RP = re_compile(
    'expression_tracking\\.stats\\.([a-z0-9]+)\\.([a-z0-9]+)\\.([a-z0-9]+)\\.([a-z0-9]+)\\.'
    '([a-z0-9]+)\\.([a-z0-9]+)\\.([a-z0-9]+)\\.([a-z0-9]+)\\.([a-z0-9]+)'
)

CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_DECREMENT_DISABLED = 'expression_tracking.disabled.0'
CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_INCREMENT_DISABLED = 'expression_tracking.disabled.1'

CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_CLOSE_BUILDER = lambda user_id : f'expression_tracking.close.{user_id:x}'
CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_CLOSE_RP = re_compile('expression_tracking\\.close\\.([a-z0-9]+)')
