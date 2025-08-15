import vampytest

from ..return_ import Return


def _assert_fields_set(return_):
    """
    Asserts whether every fields are set of the given return.
    
    Parameters
    ----------
    return_ : ``Return``
    """
    vampytest.assert_instance(return_, Return)
    vampytest.assert_instance(return_.id, int)
    vampytest.assert_instance(return_.name, str)


def tets__Return__new():
    """
    Tests whether ``Return.__new__`` works as intended.
    """
    return__id = 9910
    name = 'Collect'
    
    return_ = Return(
        return__id,
        name,
    )
    
    _assert_fields_set(return_)
    
    vampytest.assert_eq(return_.id, return__id)
    vampytest.assert_eq(return_.name, name)


def tets__Return__repr():
    """
    Tests whether ``Return.__new__`` works as intended.
    """
    return__id = 9910
    name = 'Collect'
    
    return_ = Return(
        return__id,
        name,
    )
    
    output = repr(return_)
    vampytest.assert_instance(output, str)
