import vampytest

from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL, determine_relative_sister


def _iter_options():
    user_id_0 = 202502040000
    user_id_1 = 202502040001
    
    yield user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_LIL
    yield user_id_1, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__determine_relative_sister(source_user_id, target_user_id):
    """
    Tests whether ``determine_relative_sister`` works as intended.
    
    Parameters
    ----------
    source_user_id : `int`
        The identifier of the user we are calculating relationship types from.
    
    target_user_id : `int`
        The identifier of the extended user we are calculating relationship towards.
    
    Returns
    -------
    output : `int`
    """
    output = determine_relative_sister(source_user_id, target_user_id)
    vampytest.assert_instance(output, int)
    return output
