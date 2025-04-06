import vampytest
from hata import InteractionEvent, User

from ....bot_utils.daily import ConditionName

from ..rendering import render_condition_head_name_into


def _iter_options():
    name = 'brain'
    
    yield (
        ConditionName(name),
        InteractionEvent.precreate(
            202412020011,
            user = User.precreate(202412020012, name = name),
        ),
        f'**Called as `{name}`:**\n',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_condition_head_name_into(condition, interaction_event):
    """
    Tests whether ``render_condition_head_name_into`` works as intended.
    
    Parameters
    ----------
    condition : ``ConditionName``
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    into = render_condition_head_name_into([], condition, interaction_event)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
