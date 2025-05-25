import vampytest

from hata import Component, create_button, create_row

from ..component_builders import build_component_relationship_divorce_question
from ..constants import EMOJI_NO, EMOJI_YES


def _iter_options():
    source_user_id = 202502110000
    target_user_id = 202502110001
    
    yield (
        source_user_id,
        target_user_id,
        create_row(
            create_button(
                'Yes',
                EMOJI_YES,
                custom_id = 'relationship_divorce.confirm.2f2610fb30.2f2610fb31',
            ),
            create_button(
                'No',
                EMOJI_NO,
                custom_id = 'relationship_divorce.cancel.2f2610fb30.2f2610fb31',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_relationship_divorce_question(source_user_id, target_user_id):
    """
    tests whether ``build_component_relationship_divorce_question`` works as intended.
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_relationship_divorce_question(source_user_id, target_user_id)
    vampytest.assert_instance(output, Component)
    return output
