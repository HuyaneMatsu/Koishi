import vampytest
from hata import Embed

from ..shared_helpers import add_standalone_field


def test__add_standalone_field():
    """
    Tests whether ``add_standalone_field`` works as intended.
    """
    embed = Embed('Scarlet')
    name = 'Hello'
    value = 'Hell'
    
    add_standalone_field(embed, name, value)
    
    vampytest.assert_eq(embed, Embed('Scarlet').add_field('Hello', f'```\n{value}\n```', inline = True))
