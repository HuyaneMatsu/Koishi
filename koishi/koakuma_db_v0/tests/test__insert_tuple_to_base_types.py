import vampytest

from ..structure import insert_tuple_to_base_types


def test__insert_tuple_to_base_types__omitted():
    """
    Tests whether ``insert_tuple_to_base_types`` works as intended.
    
    Case: omitted.
    """
    vampytest.assert_eq(
        insert_tuple_to_base_types((int, )),
        (tuple, int),
    )
    

def test__insert_tuple_to_base_types__included():
    """
    Tests whether ``insert_tuple_to_base_types`` works as intended.
    
    Case: included.
    """
    vampytest.assert_eq(
        insert_tuple_to_base_types((int, tuple)),
        (int, tuple),
    )
