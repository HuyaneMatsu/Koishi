import vampytest

from ..helpers import wrap_in_code_block


def test__wrap_in_code_block():
    """
    Tests whether ``wrap_in_code_block`` works as intended.
    """
    into = []
    
    for _ in wrap_in_code_block(into):
        pass
    
    output = ''.join(into)
    
    vampytest.assert_eq(output, '```\n```')


def test__wrap_in_code_block__non_empty():
    """
    Tests whether ``wrap_in_code_block`` works as intended.
    
    Case: non empty.
    """
    inner = 'hey mister\n'
    into = []
    
    for _ in wrap_in_code_block(into):
        into.append(inner)
    
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'```\n{inner}```')
