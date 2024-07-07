import vampytest
from hata import Embed

from ..orin import apply_mode_orin


def test__apply_mode_orin():
    """
    Tests whether ``apply_mode_orin`` works as intended.
    """
    embed = Embed()
    apply_mode_orin(embed)
    
    vampytest.assert_is_not(embed.color, None)
    vampytest.assert_is_not(embed.image, None)
