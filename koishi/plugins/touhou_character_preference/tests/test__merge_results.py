__all__ = ()

import vampytest

from ..character_preference import CharacterPreference
from ..helpers import merge_results


def _iter_options():
    user_id_0 = 202309160040
    user_id_1 = 202309160041
    
    character_preference_0 = CharacterPreference(user_id_0, 'komeiji_koishi')
    character_preference_1 = CharacterPreference(user_id_0, 'komeiji_satori')
    character_preference_2 = CharacterPreference(user_id_1, 'kaenbyou_rin')
    character_preference_3 = CharacterPreference(user_id_1, 'reiuji_utsuho')
    
    yield None, None, None
    yield [character_preference_0], None, [character_preference_0]
    yield None, [character_preference_0], [character_preference_0]
    yield [character_preference_0], [character_preference_1], [character_preference_0, character_preference_1]
    
    yield (
        [character_preference_0, character_preference_1],
        [character_preference_2, character_preference_3],
        [character_preference_0, character_preference_1, character_preference_2, character_preference_3],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_results(results_0, results_1):
    """
    Tests whether ``merge_results`` works as intended.
    
    Parameters
    ----------
    results_0 : `None | list<CharacterPreference>`
        Results to merge.
    results_1 : `None | list<CharacterPreference>`
        Results to merge.
    
    Returns
    -------
    results : `None | list<CharacterPreference>`
    """
    if (results_0 is not None):
        results_0 = results_0.copy()
    
    if (results_1 is not None):
        results_1 = results_1.copy()
    
    return merge_results(results_0, results_1)
