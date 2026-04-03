import vampytest

from hata import Role

from ..constants import ENTITY_REPRESENTATION_DEFAULT
from ..representation_getters import get_role_id_representation


def _iter_options():
    role_id = 0
    yield role_id, [], ENTITY_REPRESENTATION_DEFAULT
    
    role_id = 202405310000
    yield role_id, [], ENTITY_REPRESENTATION_DEFAULT
    
    
    role_id = 202405310001
    role = Role.precreate(role_id, name = 'pudding')
    yield role_id, [role], role.mention



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_role_id_representation(role_id, extra):
    """
    Tests whether ``get_role_id_representation`` works as intended.
    
    Parameters
    ----------
    role_id : `int`
        Value to get representation for.
    extra : `list<object>`
        Entities to keep in the cache.
    
    Returns
    -------
    output : `str`
    """
    output = get_role_id_representation(role_id)
    vampytest.assert_instance(output, str)
    return output
