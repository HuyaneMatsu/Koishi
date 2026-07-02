from collections import _tuplegetter as TupleGetter

import vampytest

from ..data_base_field import DataBaseField
from ..data_types import STRING, UINT64
from ..structure import Structure


def test__Structure():
    """
    Tests whether ``Structure`` works as intended.
    """
    class TestType(metaclass = Structure):
        name = STRING
        value = UINT64
    
    vampytest.assert_subtype(TestType, tuple)
    vampytest.assert_eq(
        TestType.__fields__,
        (
            DataBaseField('name', STRING),
            DataBaseField('value', UINT64),
        ),
    )
    vampytest.assert_instance(TestType.name, TupleGetter)
    vampytest.assert_eq(TestType.name.__reduce__()[1], (0, None))
    vampytest.assert_instance(TestType.value, TupleGetter)
    vampytest.assert_eq(TestType.value.__reduce__()[1], (1, None))
