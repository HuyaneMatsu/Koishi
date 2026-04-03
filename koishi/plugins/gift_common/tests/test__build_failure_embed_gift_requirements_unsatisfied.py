import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, ROLE__SUPPORT__ELEVATED

from ..embed_builders import build_failure_embed_gift_requirements_unsatisfied


def _iter_options():
    yield (
        Embed(
            'Cannot gift to user',
            (
                f'You must be either related the targeted user, '
                f'or have {ROLE__SUPPORT__ELEVATED.name} role in my support guild to target anyone.'
            ),
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_gift_requirements_unsatisfied():
    """
    Tests whether ``build_failure_embed_gift_requirements_unsatisfied`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_gift_requirements_unsatisfied()
    vampytest.assert_instance(output, Embed)
    return output
