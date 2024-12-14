import vampytest
from hata import Embed, User

from ....bot_utils.constants import COLOR__GAMBLING

from ..embed_builders import build_embed_not_related


def _iter_options():
    yield (
        User.precreate(202412110000, name = 'Remilia'),
        0,
        Embed(
            'Savage',
            'Remilia is not related to you.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_not_related(target_user, guild_id):
    """
    Tests whether ``build_embed_not_related`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_embed_not_related(target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
