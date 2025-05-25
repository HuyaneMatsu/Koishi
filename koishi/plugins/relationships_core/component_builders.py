__all__ = ('build_component_relationship_divorce_question', 'build_component_relationship_proposal_actions',)

from hata import create_button, create_row

from .constants import (
    CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_BUILDER, CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_BUILDER,
    CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_BUILDER, CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_BUILDER, EMOJI_NO, EMOJI_YES
)


def build_component_relationship_proposal_actions(source_user_id, target_user_id):
    """
    Builds a component (row) to accept or reject a proposal.
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    Returns
    -------
    component : ``Component``
    """
    return create_row(
        create_button(
            'Accept <3',
            custom_id = CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_BUILDER(source_user_id, target_user_id),
        ),
        create_button(
            'Reject </3',
            custom_id = CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_BUILDER(source_user_id, target_user_id),
        ),
    )


def build_component_relationship_divorce_question(source_user_id, target_user_id):
    """
    Builds a component (row) to question the user about their divorce decision.
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    Returns
    -------
    component : ``Component``
    """
    return create_row(
        create_button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_BUILDER(source_user_id, target_user_id),
        ),
        create_button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_BUILDER(source_user_id, target_user_id),
        ),
    )
