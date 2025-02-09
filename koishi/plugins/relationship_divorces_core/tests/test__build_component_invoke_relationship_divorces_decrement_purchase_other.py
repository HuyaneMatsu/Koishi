import vampytest

from hata import Component
from hata.ext.slash import Button

from ..component_builders import build_component_invoke_relationship_divorces_decrement_purchase_other


def _iter_options():
    user_id = 202502060000
    
    yield (
        user_id,
        Button(
            'Burn the divorce papers!',
            custom_id = 'user_balance.relationship_divorces.decrement.invoke.other.2f261037e0'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_invoke_relationship_divorces_decrement_purchase_other(user_id):
    """
    tests whether ``build_component_invoke_relationship_divorces_decrement_purchase_other`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_invoke_relationship_divorces_decrement_purchase_other(user_id)
    vampytest.assert_instance(output, Component)
    return output
