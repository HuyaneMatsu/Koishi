import vampytest
from hata import InteractionEvent, User

from ....bot_utils.daily import ConditionName

from ..rendering import produce_condition_head_name


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
def test__produce_condition_head_name(condition, interaction_event):
    """
    Tests whether ``produce_condition_head_name`` works as intended.
    
    Parameters
    ----------
    condition : ``ConditionName``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    return ''.join(produce_condition_head_name(condition, interaction_event))
