import vampytest

from hata import Component, create_button, create_row

from ..component_builders import build_component_question_relationship_divorces_decrement_purchase_other
from ..constants import EMOJI_NO, EMOJI_YES


def _iter_options():
    user_id = 202502060001
    
    yield (
        user_id,
        create_row(
            create_button(
                'Yes',
                EMOJI_YES,
                custom_id = 'user_balance.relationship_divorces.decrement.confirm.other.2f261037e1',
            ),
            create_button(
                'No',
                EMOJI_NO,
                custom_id = 'user_balance.relationship_divorces.decrement.cancel.other.2f261037e1',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_question_relationship_divorces_decrement_purchase_other(user_id):
    """
    tests whether ``build_component_question_relationship_divorces_decrement_purchase_other`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_question_relationship_divorces_decrement_purchase_other(user_id)
    vampytest.assert_instance(output, Component)
    return output
