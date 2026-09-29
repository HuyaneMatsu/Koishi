import vampytest

from ..return_ import Return, return_create


def test__return_create():
    return_id = 9910
    name = 'Collect'
    
    return_ = return_create(
        return_id,
        name,
    )
    
    vampytest.assert_instance(return_, Return)
    vampytest.assert_instance(return_.id, int)
    vampytest.assert_instance(return_.name, str)
    
    vampytest.assert_eq(return_.id, return_id)
    vampytest.assert_eq(return_.name, name)
