import vampytest

from hata import Component, create_button, create_row

from ..component_builders import build_component_question_relationship_slot_purchase_other
from ..constants import EMOJI_NO, EMOJI_YES


def _iter_options():
    user_id = 202501260010
    
    yield (
        user_id,
        create_row(
            create_button(
                'Yes',
                EMOJI_YES,
                custom_id = 'user_balance.relationship_slots.increment.confirm.other.2f260402ea',
            ),
            create_button(
                'No',
                EMOJI_NO,
                custom_id = 'user_balance.relationship_slots.increment.cancel.other.2f260402ea',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_question_relationship_slot_purchase_other(user_id):
    """
    tests whether ``build_component_question_relationship_slot_purchase_other`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_question_relationship_slot_purchase_other(user_id)
    vampytest.assert_instance(output, Component)
    return output
