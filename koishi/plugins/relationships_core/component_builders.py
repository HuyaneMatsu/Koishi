__all__ = ('build_component_relationship_divorce_question', 'build_component_relationship_proposal_actions',)

from hata.ext.slash import Button, Row

from .constants import CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_BUILDER, CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_BUILDER, \
    CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_BUILDER, CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_BUILDER, EMOJI_YES, EMOJI_NO


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
    return Row(
        Button(
            'Accept <3',
            custom_id = CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_BUILDER(source_user_id, target_user_id),
        ),
        Button(
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
    return Row(
        Button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_BUILDER(source_user_id, target_user_id),
        ),
        Button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_BUILDER(source_user_id, target_user_id),
        ),
    )
