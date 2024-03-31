import vampytest

from ..random import random_index


def test__random_index__empty_weights():
    """
    Tests whether ``random_index`` works as intended.
    
    Case: empty weights.
    """
    weights = []
    
    output = random_index(weights)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, -1)
    
    
def test__random_index__zeros():
    """
    Tests whether ``random_index`` works as intended.
    
    Case: zeros.
    """
    weights = [0.0, 0.0, 0.0]
    
    output = random_index(weights)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    
def test__random_index__one_value():
    """
    Tests whether ``random_index`` works as intended.
    
    Case: one value.
    """
    weights = [1.0]
    
    output = random_index(weights)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)


def test__random_index__multiple_values__last():
    """
    Tests whether ``random_index`` works as intended.
    
    Case: multiple values, hit last.
    """
    weights = [0.5, 0.5, 1.0]
    
    def mock_random():
        return 0.8
    
    mocked = vampytest.mock_globals(random_index, random = mock_random)
    output = mocked(weights)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)


def test__random_index__multiple_values__middle():
    """
    Tests whether ``random_index`` works as intended.
    
    Case: multiple values, hit middle.
    """
    weights = [0.5, 0.5, 1.0]
    
    def mock_random():
        return 0.4
    
    mocked = vampytest.mock_globals(random_index, random = mock_random)
    output = mocked(weights)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)
