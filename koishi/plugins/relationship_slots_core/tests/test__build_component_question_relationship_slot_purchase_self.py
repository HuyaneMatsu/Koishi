import vampytest

from hata import Component, create_button, create_row

from ..component_builders import build_component_question_relationship_slot_purchase_self
from ..constants import EMOJI_NO, EMOJI_YES


def _iter_options():
    source_user_id = 202508290000
    
    yield (
        source_user_id,
        create_row(
            create_button(
                'Yes',
                EMOJI_YES,
                custom_id = f'user_balance.relationship_slots.increment.confirm.self.{source_user_id:x}',
            ),
            create_button(
                'No',
                EMOJI_NO,
                custom_id = f'user_balance.relationship_slots.increment.cancel.self.{source_user_id:x}',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_question_relationship_slot_purchase_self(source_user_id):
    """
    Tests whether ``build_component_question_relationship_slot_purchase_self`` works as intended.
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_question_relationship_slot_purchase_self(source_user_id)
    vampytest.assert_instance(output, Component)
    return output
