import vampytest
from hata import Role

from ..content_building import produce_form_roles_component_long_description


def _iter_options():
    role_id_0 = 202511030000
    role_id_1 = 202511030001
    role_id_2 = 202511030002
    
    role_name_0 = 'shrimp'
    role_name_1 = 'fry'
    
    role_0 = Role.precreate(
        role_id_0,
        name = role_name_0,
    )
    role_1 = Role.precreate(
        role_id_1,
        name = role_name_1,
    )
    
    yield (
        None,
        [],
        (
            '###Roles\n'
            'Limits the Emoji\'s usage only to users with any of the specified roles, current guild only.\n'
            '```\n'
            '*none*\n'
            '```'
        ),
    )
    
    yield (
        (
            role_id_0,
            role_id_1,
            role_id_2,
        ),
        [
            role_0,
            role_1,
        ],
        (
            f'###Roles\n'
            f'Limits the Emoji\'s usage only to users with any of the specified roles, current guild only.\n'
            f'```\n'
            f'@\u200b{role_name_0}, @\u200b{role_name_1}, @\u200bdeleted role\n'
            f'```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_form_roles_component_long_description(role_ids, entity_cache):
    """
    Tests whether ``produce_form_roles_component_long_description`` works as intended.
    
    Parameters
    ----------
    role_ids : `None | tuple<int>`
        ROle identifiers.
    
    entity_cache : `list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_form_roles_component_long_description(role_ids)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
