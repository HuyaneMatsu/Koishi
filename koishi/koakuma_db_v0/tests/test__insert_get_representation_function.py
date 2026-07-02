import vampytest

from ..structure import insert_get_representation_function


def _iter_options():
    yield (
        (),
        {},
        object.__repr__,
        {
            '__repr__': object.__repr__,
        },
    )
    
    yield (
        (),
        {
            '__repr__': tuple.__repr__,
        },
        object.__repr__,
        {
            '__repr__': tuple.__repr__,
        },
    )
    
    yield (
        (
            tuple,
        ),
        {},
        object.__repr__,
        {
            '__repr__': object.__repr__,
        },
    )
    
    yield (
        (
            int,
        ),
        {},
        object.__repr__,
        {},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__insert_get_representation_function(base_types, type_attributes, get_representation_function):
    """
    Tests whether ``insert_get_representation_function`` works as intended.
    
    Parameters
    ----------
    base_types : `tuple<type>`
        Base types.
    
    type_attributes : `dict<str, object>`
        Attributes to create the types with.
    
    get_representation_function : `Function`
        Function to insert if non found.
    
    Returns
    -------
    type_attributes : `dict<str, object>`
    """
    type_attributes = type_attributes.copy()
    insert_get_representation_function(base_types, type_attributes, get_representation_function)
    return type_attributes
