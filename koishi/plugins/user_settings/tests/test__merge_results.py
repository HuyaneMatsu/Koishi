__all__ = ()

import vampytest

from ..user_settings import UserSettings
from ..helpers import merge_results


def _iter_options():
    user_id_0 = 202309220040
    user_id_1 = 202309220041
    user_id_2 = 202309220042
    user_id_3 = 202309220043
    
    user_settings_0 = UserSettings(user_id_0, notification_daily_by_waifu = False)
    user_settings_1 = UserSettings(user_id_1, notification_daily_by_waifu = False)
    user_settings_2 = UserSettings(user_id_2, notification_proposal = False)
    user_settings_3 = UserSettings(user_id_3, notification_daily_by_waifu = False, notification_proposal = False)
    
    yield None, None, None
    yield [user_settings_0], None, [user_settings_0]
    yield None, [user_settings_0], [user_settings_0]
    yield [user_settings_0], [user_settings_1], [user_settings_0, user_settings_1]
    
    yield (
        [user_settings_0, user_settings_1],
        [user_settings_2, user_settings_3],
        [user_settings_0, user_settings_1, user_settings_2, user_settings_3],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_results(results_0, results_1):
    """
    Tests whether ``merge_results`` works as intended.
    
    Parameters
    ----------
    results_0 : `None | list<UserSettings>`
        Results to merge.
    results_1 : `None | list<UserSettings>`
        Results to merge.
    
    Returns
    -------
    results : `None | list<UserSettings>`
    """
    if (results_0 is not None):
        results_0 = results_0.copy()
    
    if (results_1 is not None):
        results_1 = results_1.copy()
    
    return merge_results(results_0, results_1)
