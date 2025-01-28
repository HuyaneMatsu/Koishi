__all__ = ()

from ..relationships_core import (
    RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS,
    RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_WAIFU
)

RELATIONSHIP_CONNECTION_TYPE_NAME_DEFAULT = 'pudding'

RELATIONSHIP_CONNECTION_TYPE_NONE = 0
RELATIONSHIP_CONNECTION_TYPE_IN_LAW = 2


RELATIONSHIP_CONNECTION_NAMES = {
    RELATIONSHIP_CONNECTION_TYPE_NONE : None,
    RELATIONSHIP_CONNECTION_TYPE_IN_LAW : 'in law',
}


def get_relationship_connection_type_name(relationship_connection_type):
    """
    Gets the relationship connection's name.
    
    Parameters
    ----------
    relationship_connection_type : `int`
        Relationship connection type.
    
    Returns
    -------
    relationship_connection_name : `None | str`
    """
    return RELATIONSHIP_CONNECTION_NAMES.get(relationship_connection_type, RELATIONSHIP_CONNECTION_TYPE_NAME_DEFAULT)


RELATION_TYPE_EXTEND_RESOLUTION = {
    # from waifu
    (
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_SISTER_LIL,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_SISTER_LIL,
    ),
    (
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_SISTER_BIG,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_SISTER_BIG,
    ),
    (
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_MAMA,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_MAMA,
    ),
    (
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_MAID,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_MAID,
    ),
    (
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_DAUGHTER,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_DAUGHTER,
    ),
    
    # from little sister
    (
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_WAIFU,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_SISTER_LIL,
    ),
    
    # from big sister
    (
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_WAIFU,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_SISTER_BIG,
    ),
    
    # from mama
    (
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_WAIFU,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_MAMA,
    ),
    
    # from daughter
    (
        RELATIONSHIP_TYPE_DAUGHTER,
        RELATIONSHIP_TYPE_WAIFU,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_DAUGHTER,
    ),
    
    # from mistress
    (
        RELATIONSHIP_TYPE_MISTRESS,
        RELATIONSHIP_TYPE_WAIFU,
    ) : (
        RELATIONSHIP_CONNECTION_TYPE_IN_LAW,
        RELATIONSHIP_TYPE_MISTRESS,
    ),
    
    # shared through maid
    # nothing yet
}
