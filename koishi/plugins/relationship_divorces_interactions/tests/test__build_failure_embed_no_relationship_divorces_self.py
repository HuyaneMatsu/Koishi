import vampytest
from hata import Embed

from ..embed_builders import build_failure_embed_no_relationship_divorces_self


def _iter_options():
    yield (
        Embed(
            'Suffering from success',
            'You have no divorces.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_no_relationship_divorces_self():
    """
    Tests whether ``build_failure_embed_no_relationship_divorces_self`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_no_relationship_divorces_self()
    vampytest.assert_instance(output, Embed)
    return output
