import vampytest

from ..content_building import produce_modifiers_section
from ..helpers import construct_modifier_type
from ..modifier import Modifier
from ..modifier_ids import (
    MODIFIER_ID__STAT_BEDROOM, MODIFIER_ID__FISHING, MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_ID__STAT_LOYALTY
)
from ..modifier_kinds import MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT


def _iter_options():
    yield (
        (
            Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +1),
            Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +1),
            Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +1),
            Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), -20),
        ),
        (
            '- +1 Housewife capabilities\n'
            '- +1 Bedroom skills\n'
            '- +1 Loyalty\n'
            '- -20% Fishing'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_produce_modifiers_section(modifier):
    """
    Tests whether ``produce_modifiers_section`` works as intended.
    
    Parameters
    ----------
    modifier. : ``tuple<Modifier>``
        The modifiers to produce.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_modifiers_section(modifier)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
