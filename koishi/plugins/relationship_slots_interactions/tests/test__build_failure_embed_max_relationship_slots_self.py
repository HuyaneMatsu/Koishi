import vampytest
from hata import Embed

from ..embed_builders import build_failure_embed_max_relationship_slots_self


def _iter_options():
    yield (
        Embed(
            'Suffering from success',
            'You reached the maximum amount of relationship slots.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_max_relationship_slots_self():
    """
    Tests whether ``build_failure_embed_max_relationship_slots_self`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_max_relationship_slots_self()
    vampytest.assert_instance(output, Embed)
    return output
