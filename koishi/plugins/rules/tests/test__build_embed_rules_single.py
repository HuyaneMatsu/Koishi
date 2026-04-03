import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__KOISHI_HELP

from ..embed_builders import build_embed_rules_single


def _iter_options():
    yield (
        -1,
        Embed(
            'Rule -1 of Koishi Wonderland:',
            'There is no such a rule.',
            color = COLOR__KOISHI_HELP,
        ),
    )
    
    yield (
        0,
        Embed(
            'Rule 0 of Koishi Wonderland:',
            (
                '**0\\. Behaviour**\n'
                'Listen to staff and follow their instructions.'
            ),
            color = COLOR__KOISHI_HELP,
        ),
    )
    
    yield (
        90000,
        Embed(
            'Rule 90000 of Koishi Wonderland:',
            'There is no such a rule.',
            color = COLOR__KOISHI_HELP,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_rules_single(rule_index):
    """
    Tests whether ``build_embed_rules_single`` works as intended.
    
    Parameters
    ----------
    rule_index : `int`
        The index of the rule.
    
    Returns
    -------
    output : ``Embed``
        The embed to match.
    """
    output = build_embed_rules_single(rule_index)
    vampytest.assert_instance(output, Embed)
    
    return output
