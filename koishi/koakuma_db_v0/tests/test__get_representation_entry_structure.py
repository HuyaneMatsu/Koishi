import vampytest

from ..structure import get_representation_entry_structure

from .helpers import TestEntry


def test__get_representation_entry_structure():
    """
    Tests whether ``get_representation_entry_structure`` works as intended.
    """
    instance = TestEntry((0, 0, 12, 'shrimp', 56),)
    output = get_representation_entry_structure(instance)
    vampytest.assert_instance(output, str)
