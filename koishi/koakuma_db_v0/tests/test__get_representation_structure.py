import vampytest

from ..structure import get_representation_structure

from .helpers import TestStructure


def test__get_representation_structure():
    """
    Tests whether ``get_representation_structure`` works as intended.
    """
    instance = TestStructure(('shrimp', 56),)
    output = get_representation_structure(instance)
    vampytest.assert_instance(output, str)
