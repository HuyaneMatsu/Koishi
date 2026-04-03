import vampytest

from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..character_preference import CharacterPreference
from ..helpers import should_remove_touhou_character_preference


def _iter_options():
    character_preference_0 = CharacterPreference(202309170000, KOMEIJI_KOISHI.system_name)
    character_preference_1 = CharacterPreference(202309170001, KOMEIJI_SATORI.system_name)
    
    yield (
        None,
        KOMEIJI_KOISHI,
        None,
    )
    
    yield (
        [
            character_preference_0,
        ],
        KOMEIJI_KOISHI,
        character_preference_0,
    )
    
    yield (
        [
            character_preference_0,
            character_preference_1,
        ],
        KOMEIJI_KOISHI,
        character_preference_0,
    )

    yield (
        [
            character_preference_1,
        ],
        KOMEIJI_KOISHI,
        None,
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__should_remove_touhou_character_preference(character_preferences, character):
    """
    Tests whether ``should_remove_touhou_character_preference`` works as intended.
    
    Parameters
    ----------
    character_preferences : `None | list<CharacterPreference>`
        The user's actual character preferences.
    character : ``TouhouCharacter``
        Touhou character to remove as a preference.
    
    Returns
    -------
    should_remove : `None | CharacterPreference`
    """
    return should_remove_touhou_character_preference(character_preferences, character)
