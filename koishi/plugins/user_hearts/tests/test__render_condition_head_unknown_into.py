import vampytest
from hata import InteractionEvent, User

from ....bot_utils.daily import ConditionBase

from ..rendering import render_condition_head_unknown_into


def _iter_options():
    yield (
        ConditionBase(),
        InteractionEvent.precreate(
            202412020013,
            user = User.precreate(202412020014),
        ),
        f'**Unknown:**\n',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_condition_head_unknown_into(condition, interaction_event):
    """
    Tests whether ``render_condition_head_unknown_into`` works as intended.
    
    Parameters
    ----------
    condition : ``ConditionBase``
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    into = render_condition_head_unknown_into([], condition, interaction_event)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
