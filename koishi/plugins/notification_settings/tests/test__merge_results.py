__all__ = ()

import vampytest

from ..notification_settings import NotificationSettings
from ..helpers import merge_results


def _iter_options():
    user_id_0 = 202309220040
    user_id_1 = 202309220041
    user_id_2 = 202309220042
    user_id_3 = 202309220043
    
    notification_settings_0 = NotificationSettings(user_id_0, daily_by_waifu = False)
    notification_settings_1 = NotificationSettings(user_id_1, daily_by_waifu = False)
    notification_settings_2 = NotificationSettings(user_id_2, proposal = False)
    notification_settings_3 = NotificationSettings(user_id_3, daily_by_waifu = False, proposal = False)
    
    yield None, None, None
    yield [notification_settings_0], None, [notification_settings_0]
    yield None, [notification_settings_0], [notification_settings_0]
    yield [notification_settings_0], [notification_settings_1], [notification_settings_0, notification_settings_1]
    
    yield (
        [notification_settings_0, notification_settings_1],
        [notification_settings_2, notification_settings_3],
        [notification_settings_0, notification_settings_1, notification_settings_2, notification_settings_3],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_results(results_0, results_1):
    """
    Tests whether ``merge_results`` works as intended.
    
    Parameters
    ----------
    results_0 : `None | list<NotificationSettings>`
        Results to merge.
    results_1 : `None | list<NotificationSettings>`
        Results to merge.
    
    Returns
    -------
    results : `None | list<NotificationSettings>`
    """
    if (results_0 is not None):
        results_0 = results_0.copy()
    
    if (results_1 is not None):
        results_1 = results_1.copy()
    
    return merge_results(results_0, results_1)
