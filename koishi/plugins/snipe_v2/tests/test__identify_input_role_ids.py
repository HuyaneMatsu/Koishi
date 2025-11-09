import vampytest
from hata import Role

from ..responding_helpers import identify_input_role_ids


def _iter_options():
    role_id_0 = 202511040000
    role_id_1 = 202511040000
    
    role_0 = Role.precreate(
        role_id_0,
    )
    
    role_1 = Role.precreate(
        role_id_1,
    )
    
    yield (
        None,
        (
            True,
            None,
        ),
    )
    
    yield (
        (
            role_0,
            role_1,
        ),
        (
            True,
            (
                role_id_0,
                role_id_1,
            ),
        ),
    )
    
    yield (
        (
            role_1,
            role_0,
        ),
        (
            True,
            (
                role_id_0,
                role_id_1,
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__identify_input_role_ids(input_tags):
    """
    Identifies the identifiers of the given roles.
    
    Parameters
    ----------
    input_roles : ``None | tuple<Role>``
        Roles to identify.
    
    Returns
    -------
    output : `(bool, None | tuple<int>)`
    """
    output = identify_input_role_ids(input_tags)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    identified, tags = output
    vampytest.assert_instance(identified, bool)
    vampytest.assert_instance(tags, tuple, nullable = True)
    if (tags is not None):
        for element in tags:
            vampytest.assert_instance(element, int)
    
    return output
