import vampytest

from ..relationship_types import (
    RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS,
    RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_UNSET, RELATIONSHIP_TYPE_WAIFU,
    do_relationship_type_flip_basic
)


def _iter_options():
    yield (
        RELATIONSHIP_TYPE_UNSET,
        RELATIONSHIP_TYPE_UNSET,
    )
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
    )
    
    yield (
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
    )
    
    yield (
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_SISTER_LIL,
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_DAUGHTER,
    )
    
    yield (
        RELATIONSHIP_TYPE_DAUGHTER,
        RELATIONSHIP_TYPE_MAMA,
    )
    
    yield (
        RELATIONSHIP_TYPE_MAID,
        RELATIONSHIP_TYPE_MISTRESS,
    )
    
    yield (
        RELATIONSHIP_TYPE_MISTRESS,
        RELATIONSHIP_TYPE_MAID,
    )
    
    yield (
        RELATIONSHIP_TYPE_WAIFU | RELATIONSHIP_TYPE_MAMA | RELATIONSHIP_TYPE_MISTRESS,
        RELATIONSHIP_TYPE_WAIFU | RELATIONSHIP_TYPE_DAUGHTER | RELATIONSHIP_TYPE_MAID,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def tets__do_relationship_type_flip_basic(relationship_type):
    """
    Tests whether ``do_relationship_type_flip_basic`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship type to flip.
    
    Returns
    -------
    relationship_type : `int`
    """
    output = do_relationship_type_flip_basic(relationship_type)
    vampytest.assert_instance(output, int)
    return output
