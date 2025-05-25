import vampytest

from hata import Component, create_button, create_row

from ..component_builders import build_component_relationship_proposal_actions


def _iter_options():
    source_user_id = 202502070000
    target_user_id = 202502070001
    
    yield (
        source_user_id,
        target_user_id,
        create_row(
            create_button(
                'Accept <3',
                custom_id = 'relationship_proposal.accept.2f26105ef0.2f26105ef1',
            ),
            create_button(
                'Reject </3',
                custom_id = 'relationship_proposal.reject.2f26105ef0.2f26105ef1',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_relationship_proposal_actions(source_user_id, target_user_id):
    """
    tests whether ``build_component_relationship_proposal_actions`` works as intended.
    
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
    output = build_component_relationship_proposal_actions(source_user_id, target_user_id)
    vampytest.assert_instance(output, Component)
    return output
