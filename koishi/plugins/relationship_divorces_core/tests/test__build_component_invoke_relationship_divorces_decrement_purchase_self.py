import vampytest

from hata import Component
from hata.ext.slash import Button

from ..component_builders import build_component_invoke_relationship_divorces_decrement_purchase_self


def _iter_options():
    yield (
        Button(
            'Burn the divorce papers!',
            custom_id = 'user_balance.relationship_divorces.decrement.invoke.self'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_invoke_relationship_divorces_decrement_purchase_self():
    """
    tests whether ``build_component_invoke_relationship_divorces_decrement_purchase_self`` works as intended.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_invoke_relationship_divorces_decrement_purchase_self()
    vampytest.assert_instance(output, Component)
    return output
