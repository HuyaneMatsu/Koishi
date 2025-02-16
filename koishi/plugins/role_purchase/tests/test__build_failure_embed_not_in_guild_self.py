import vampytest
from hata import Embed, Guild, Role

from ..embed_builders import build_failure_embed_not_in_guild_self


def _iter_options():
    role_id = 202502130003
    guild_id = 202502130004
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    guild = Guild.precreate(guild_id, name = 'Hell')
    
    yield (
        role,
        [guild],
        Embed(
            'Not in guild',
            f'You must be in Hell to acquire Nyan role.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_not_in_guild_self(role, cache):
    """
    Tests whether ``build_failure_embed_not_in_guild_self`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to check for.
    
    cache : `None | list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_not_in_guild_self(role)
    vampytest.assert_instance(output, Embed)
    return output
