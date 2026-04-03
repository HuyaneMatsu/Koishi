import vampytest

from hata import Role

from ..helpers import iter_role_ids_of_roles_nullable


def _iter_options():
    role_id_0 = 202510050040
    role_id_1 = 202510050041
    
    role_0 = Role.precreate(
        role_id_0,
    )
    role_1 = Role.precreate(
        role_id_1,
    )
    
    yield (
        None,
        set(),
    )
    
    yield (
        (
            role_0,
            role_1,
        ),
        {
            role_id_0,
            role_id_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_role_ids_of_roles_nullable(roles):
    """
    Tests whether ``iter_role_ids_of_roles_nullable`` works as intended.
    
    Parameters
    ----------
    roles : ``None | tuple<Role>``
        Roles to iterate through their items.
    
    Returns
    -------
    output : `set<int>`
    """
    output = {*iter_role_ids_of_roles_nullable(roles)}
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
