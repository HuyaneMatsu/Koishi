import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__KOISHI_HELP

from ..embed_builders import build_embed_rules_all


def _iter_options():
    yield (
        Embed(
            'Rules of Koishi Wonderland:',
            color = COLOR__KOISHI_HELP,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_rules_all():
    """
    Tests whether ``build_embed_rules_all`` works as intended.
    
    Returns
    -------
    output : ``Embed``
        The embed to match.
    """
    output = build_embed_rules_all()
    vampytest.assert_instance(output, Embed)
    
    # We omit the description after checking its set.
    vampytest.assert_instance(output.description, str)
    output.description = None
    
    return output
