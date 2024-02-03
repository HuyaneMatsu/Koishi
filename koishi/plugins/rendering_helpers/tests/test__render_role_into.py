import vampytest
from hata import Role

from ..value_renderers import render_role_into


def test__render_role_into():
    """
    Tests whether ``render_role_into`` works as intended.
    
    Case: No nick.
    """
    role_id = 202401300004
    name = 'koishi'
    role = Role.precreate(role_id, name = name)
    
    into = render_role_into([], role)
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'{name!s} ({role_id!s})')
