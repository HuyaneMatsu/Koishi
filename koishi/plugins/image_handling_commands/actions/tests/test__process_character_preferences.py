import vampytest
from hata import User

from ....touhou_character_preference import CharacterPreference

from ..character_preference import process_character_preferences


def _iter_options():
    user_id_0 = 202309170070
    user_id_1 = 202309170071
    
    user_0 = User.precreate(user_id_0)
    
    yield (
        [
            CharacterPreference(user_id_0, 'komeiji_koishi'),
        ],
        user_0,
        (
            {
                'komeiji_koishi',
            },
            None,
        ),
    )

    yield (
        [
            CharacterPreference(user_id_0, 'komeiji_koishi'),
            CharacterPreference(user_id_0, 'komeiji_satori'),
        ],
        user_0,
        (
            {
                'komeiji_koishi',
                'komeiji_satori',
            },
            None,
        ),
    )

    yield (
        [
            CharacterPreference(user_id_1, 'komeiji_koishi'),
        ],
        user_0,
        (
            None,
            {
                'komeiji_koishi',
            },
        ),
    )
    
    yield (
        [
            CharacterPreference(user_id_1, 'komeiji_koishi'),
            CharacterPreference(user_id_1, 'komeiji_satori'),
        ],
        user_0,
        (
            None,
            {
                'komeiji_koishi',
                'komeiji_satori',
            },
        ),
    )

    yield (
        [
            CharacterPreference(user_id_0, 'komeiji_koishi'),
            CharacterPreference(user_id_0, 'komeiji_satori'),
            CharacterPreference(user_id_1, 'komeiji_koishi'),
            CharacterPreference(user_id_1, 'komeiji_satori'),
        ],
        user_0,
        (
            {
                'komeiji_koishi',
                'komeiji_satori',
            },
            {
                'komeiji_koishi',
                'komeiji_satori',
            },
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__process_character_preferences(character_preferences, source_user):
    """
    Tests whether ``process_character_preferences`` works as intended.
    
    Parameters
    ----------
    character_preferences : `list<CharacterPreference>`
        Character preferences to process.
    
    Returns
    -------
    source_character_system_names : `None | set<str>`
    target_character_system_names : `None | set<str>`
    """
    return process_character_preferences(character_preferences, source_user)
