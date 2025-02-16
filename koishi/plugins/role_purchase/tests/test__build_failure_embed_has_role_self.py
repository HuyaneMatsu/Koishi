import vampytest
from hata import Embed, Role

from ..embed_builders import build_failure_embed_has_role_self


def _iter_options():
    role_id = 202502130005
    guild_id = 202502130006
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    yield (
        role,
        Embed(
            'Suffering from success',
            'You already have the Nyan role.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_has_role_self(role):
    """
    Tests whether ``build_failure_embed_has_role_self`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to check for.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_has_role_self(role)
    vampytest.assert_instance(output, Embed)
    return output
