import vampytest

from hata import Component, create_button, create_row

from ..component_builders import build_component_question_relationship_slot_purchase_self
from ..constants import EMOJI_NO, EMOJI_YES


def _iter_options():
    yield (
        create_row(
            create_button(
                'Yes',
                EMOJI_YES,
                custom_id = 'user_balance.relationship_slots.increment.confirm.self',
            ),
            create_button(
                'No',
                EMOJI_NO,
                custom_id = 'user_balance.relationship_slots.increment.cancel.self',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_question_relationship_slot_purchase_self():
    """
    tests whether ``build_component_question_relationship_slot_purchase_self`` works as intended.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_question_relationship_slot_purchase_self()
    vampytest.assert_instance(output, Component)
    return output
