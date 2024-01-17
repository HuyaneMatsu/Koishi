import vampytest
from hata import Embed, User

from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..builders import build_character_preference_change_embed


def _iter_options():
    user_0 = User.precreate(202309170061)
    
    yield (
        user_0,
        KOMEIJI_KOISHI,
        True,
        Embed(
            'Great success!',
            'From now on Komeiji Koishi is associate with you.',
        ).add_thumbnail(
            user_0.avatar_url,
        ),
    )
    
    user_1 = User.precreate(202309170062)
    
    yield (
        user_1,
        KOMEIJI_SATORI,
        False,
        Embed(
            'Great success!',
            'From now on wont associate Komeiji Satori with you.',
        ).add_thumbnail(
            user_1.avatar_url,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_character_preference_change_embed(user, character, added):
    """
    Tests whether ``build_character_preference_change_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's character preference were changed.
    character : ``TouhouCharacter``
        The touhou character added / removed.
    added : `bool`
        Whether the character preference was added / removed.
    
    Returns
    -------
    embed : ``Embed``
    """
    output = build_character_preference_change_embed(user, character, added)
    vampytest.assert_instance(output, Embed)
    return output


    return Embed(
        
        build_character_preference_change_description(character, added),
    ).add_thumbnail(
        user.avatar_url,
    )
