import vampytest
from hata import Role

from ..content_builders import produce_role_listing


def _iter_options():
    role_id_0 = 202510050020
    role_id_1 = 202510050021
    
    role_0 = Role.precreate(
        role_id_0,
    )
    
    yield (
        (
            role_id_0,
            role_id_1,
        ),
        [
            role_0,
        ],
        (
            f'\n'
            f'- {role_0.mention}\n'
            f'- @\u200bdeleted role'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_role_listing(role_ids, entity_cache):
    """
    Tests whether ``produce_role_listing`` works as intended.
    
    Parameters
    ----------
    role_ids : `tuple<int>`
        Role identifiers.
    
    entity_cache : `list<object>`
        Additional entities to keep cached.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_role_listing(role_ids)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
