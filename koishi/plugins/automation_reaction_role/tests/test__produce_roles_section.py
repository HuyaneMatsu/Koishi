import vampytest

from hata import Role

from ..component_builders import produce_roles_section


def _iter_options():
    role_0 = Role.precreate(202509260000)
    role_1 = Role.precreate(202509260001)
    role_2 = Role.precreate(202509260002)
    role_3 = Role.precreate(202509260003)
    
    yield (
        None,
        None,
        [],
        'none',
    )
    
    
    yield (
        (
            role_0.id,
            role_1.id,
        ),
        None,
        [
            role_0,
            role_1,
        ],
        (
            f'Add roles:\n'
            f'- {role_0.mention}\n'
            f'- {role_1.mention}'
        ),
    )
    
    yield (
        None,
        (
            role_2.id,
            role_3.id,
        ),
        [
            role_2,
            role_3,
        ],
        (
            f'Remove roles:\n'
            f'- {role_2.mention}\n'
            f'- {role_3.mention}'
        ),
    )
    
    yield (
        (
            role_0.id,
            role_1.id,
        ),
        (
            role_2.id,
            role_3.id,
        ),
        [
            role_0,
            role_1,
            role_2,
            role_3,
        ],
        (
            f'Add roles:\n'
            f'- {role_0.mention}\n'
            f'- {role_1.mention}\n'
            f'Remove roles:\n'
            f'- {role_2.mention}\n'
            f'- {role_3.mention}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_roles_section(add_role_ids, remove_role_ids, entity_cache):
    """
    Tests whether ``produce_roles_section`` works as intended.
    
    Parameters
    ----------
    add_role_ids : `None | tuple<int>`
        Role identifier to add upon reacting.
    
    remove_role_ids : `None | tuple<int>`
        Role identifiers to remove upon react.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_roles_section(add_role_ids, remove_role_ids)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
