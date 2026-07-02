import vampytest

from ..creation import create_seed


def test__create_seed():
    """
    Tests whether ``create_seed`` works as intended.
    """
    output = create_seed()
    vampytest.assert_instance(output, int)
