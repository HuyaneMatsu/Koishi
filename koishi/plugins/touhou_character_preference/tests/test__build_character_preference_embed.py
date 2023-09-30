import vampytest
from hata import Embed, User

from ...touhou_character_preference import CharacterPreference

from ..builders import build_character_preference_embed


def test__build_character_preference_embed():
    """
    Tests whether ``build_character_preference_embed`` works as intended.
    """
    user = User.precreate(202309170060)
    
    character_preferences = [
        CharacterPreference(0, 'komeiji_koishi'),
        CharacterPreference(0, 'komeiji_satori'),
    ]
    
    expected_output = Embed(
        'Character preferences',
        (
            '```\n'
            'Komeiji Koishi\n'
            'Komeiji Satori\n'
            '```'
        ),
    ).add_thumbnail(
        user.avatar_url,
    )
    
    output = build_character_preference_embed(user, character_preferences)
    vampytest.assert_instance(output, Embed)
    vampytest.assert_eq(output, expected_output)
