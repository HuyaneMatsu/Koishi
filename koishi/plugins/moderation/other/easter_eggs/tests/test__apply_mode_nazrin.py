import vampytest
from hata import Embed

from ..nazrin import apply_mode_nazrin


def test__apply_mode_nazrin():
    """
    Tests whether ``apply_mode_nazrin`` works as intended.
    """
    embed = Embed()
    apply_mode_nazrin(embed)
    
    vampytest.assert_is_not(embed.color, None)
    vampytest.assert_is_not(embed.image, None)
