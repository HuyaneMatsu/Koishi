__all__ = (
    'RELATIONSHIP_TYPE_DAUGHTER', 'RELATIONSHIP_TYPE_MAID', 'RELATIONSHIP_TYPE_MAMA', 'RELATIONSHIP_TYPE_MISTRESS',
    'RELATIONSHIP_TYPE_NONE', 'RELATIONSHIP_TYPE_RELATIONSHIPS', 'RELATIONSHIP_TYPE_SISTER_BIG',
    'RELATIONSHIP_TYPE_SISTER_LIL', 'RELATIONSHIP_TYPE_SISTER_RELATIVE', 'RELATIONSHIP_TYPE_UNSET',
    'RELATIONSHIP_TYPE_WAIFU', 'determine_relative_sister', 'get_relationship_type_name'
)


RELATIONSHIP_TYPE_NONE = 0
RELATIONSHIP_TYPE_UNSET = 1
RELATIONSHIP_TYPE_WAIFU = 2
RELATIONSHIP_TYPE_SISTER_LIL = 3
RELATIONSHIP_TYPE_SISTER_BIG = 4
RELATIONSHIP_TYPE_MAMA = 5
RELATIONSHIP_TYPE_MISTRESS = 6
RELATIONSHIP_TYPE_MAID = 7
RELATIONSHIP_TYPE_DAUGHTER = 8
RELATIONSHIP_TYPE_SISTER_RELATIVE = 9

RELATIONSHIP_TYPE_NAME_DEFAULT = 'pudding'

RELATIONSHIP_TYPE_NAMES = {
    RELATIONSHIP_TYPE_NONE: RELATIONSHIP_TYPE_NAME_DEFAULT,
    RELATIONSHIP_TYPE_UNSET: 'unset',
    RELATIONSHIP_TYPE_WAIFU: 'waifu',
    RELATIONSHIP_TYPE_SISTER_LIL: 'little sister',
    RELATIONSHIP_TYPE_SISTER_BIG: 'big sister',
    RELATIONSHIP_TYPE_MAMA: 'mama',
    RELATIONSHIP_TYPE_MISTRESS: 'mistress',
    RELATIONSHIP_TYPE_MAID: 'maid',
    RELATIONSHIP_TYPE_DAUGHTER: 'daughter',
    RELATIONSHIP_TYPE_SISTER_RELATIVE: 'sister',
}

RELATIONSHIP_TYPE_RELATIONSHIPS = {
    # unset
    RELATIONSHIP_TYPE_UNSET: RELATIONSHIP_TYPE_UNSET,
    
    # acquirable
    RELATIONSHIP_TYPE_WAIFU: RELATIONSHIP_TYPE_WAIFU,
    RELATIONSHIP_TYPE_SISTER_LIL: RELATIONSHIP_TYPE_SISTER_BIG,
    RELATIONSHIP_TYPE_SISTER_BIG: RELATIONSHIP_TYPE_SISTER_LIL,
    RELATIONSHIP_TYPE_MAMA: RELATIONSHIP_TYPE_DAUGHTER,
    RELATIONSHIP_TYPE_DAUGHTER: RELATIONSHIP_TYPE_MAMA,
    RELATIONSHIP_TYPE_MISTRESS: RELATIONSHIP_TYPE_MAID,
    RELATIONSHIP_TYPE_MAID: RELATIONSHIP_TYPE_MISTRESS,
    
    # for display
    RELATIONSHIP_TYPE_SISTER_RELATIVE: RELATIONSHIP_TYPE_SISTER_RELATIVE,
}


def get_relationship_type_name(relationship_type):
    """
    Gets the relationship type's name.
    
    Parameters
    ----------
    relationship_type : `int`
        Relationship type.
    
    Returns
    -------
    relationship_type_name : `str`
    """
    return RELATIONSHIP_TYPE_NAMES.get(relationship_type, RELATIONSHIP_TYPE_NAME_DEFAULT)


RELATION_TYPE_ALLOWED_EXTENDS = (
    # shared through waifu
    (
        RELATIONSHIP_TYPE_WAIFU,
        (
            RELATIONSHIP_TYPE_SISTER_LIL,
            RELATIONSHIP_TYPE_SISTER_BIG,
            RELATIONSHIP_TYPE_MAMA,
            RELATIONSHIP_TYPE_MAID,
            RELATIONSHIP_TYPE_DAUGHTER,
        )
    ),
    
    # shared through little sister
    (
        RELATIONSHIP_TYPE_SISTER_LIL,
        (
            RELATIONSHIP_TYPE_SISTER_LIL,
            RELATIONSHIP_TYPE_SISTER_BIG,
            RELATIONSHIP_TYPE_WAIFU,
        ),
    ),
    
    # shared through big sister
    (
        RELATIONSHIP_TYPE_SISTER_BIG,
        (
            RELATIONSHIP_TYPE_SISTER_LIL,
            RELATIONSHIP_TYPE_SISTER_BIG,
            RELATIONSHIP_TYPE_WAIFU,
        ),
    ),
    
    # shared through mama
    (
        RELATIONSHIP_TYPE_MAMA,
        (
            RELATIONSHIP_TYPE_WAIFU,
            RELATIONSHIP_TYPE_DAUGHTER,
        ),
    ),
    
    # shared through daughter
    (
        RELATIONSHIP_TYPE_DAUGHTER,
        (
            RELATIONSHIP_TYPE_SISTER_LIL,
            RELATIONSHIP_TYPE_SISTER_BIG,
            RELATIONSHIP_TYPE_WAIFU,
        ),
    ),
    
    # shared through mistress
    (
        RELATIONSHIP_TYPE_MISTRESS,
        (
            RELATIONSHIP_TYPE_WAIFU,
        ),
    ),
    
    # shared through maid
    # nothing yet
)


def determine_relative_sister(source_user_id, target_user_id):
    """
    Determines whether the sister is big or little based on user identifiers.
    If something ends up with `RELATIONSHIP_TYPE_SISTER_RELATIVE` relationship type this function should be called.
    
    Parameters
    ----------
    source_user_id : `int`
        The identifier of the user we are calculating relationship types from.
    
    target_user_id : `int`
        The identifier of the extended user we are calculating relationship towards.
    
    Returns
    -------
    relationship_type : `int`
    """
    return RELATIONSHIP_TYPE_SISTER_BIG if source_user_id > target_user_id else RELATIONSHIP_TYPE_SISTER_LIL 
