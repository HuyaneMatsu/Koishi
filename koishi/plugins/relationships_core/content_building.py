__all__ = ('get_relationship_request_type_concept',)

from .constants import ACTION_NAME_UNKNOWN, ACTION_NAME_UNKNOWN_CAPITALISED
from .relationship_types import (
    RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_UNSET,
    RELATIONSHIP_TYPE_WAIFU
)


def get_relationship_request_type_concept(relationship_type, capitalised):
    """
    Helper function to get relationship request type concept name.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    capitalised : `bool`
        Whether to return a capitalised version,
    
    Returns
    -------
    concept : `str`
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'Marriage proposal' if capitalised else 'marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'Blood-pact request' if capitalised else 'blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'Adoption agreement' if capitalised else 'adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MISTRESS:
        concept = 'Employment contract' if capitalised else 'employment contract'
    elif relationship_type == RELATIONSHIP_TYPE_UNSET:
        concept = 'Unset'
    else:
        concept = ACTION_NAME_UNKNOWN_CAPITALISED if capitalised else ACTION_NAME_UNKNOWN
    
    return concept
