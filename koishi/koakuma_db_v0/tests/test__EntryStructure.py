from collections import _tuplegetter as TupleGetter

import vampytest

from ..data_base_field import DataBaseField
from ..data_types import ENTRY_ID, STRING, UINT64
from ..structure import EntryStructure


def test__EntryStructure():
    """
    Tests whether ``EntryStructure`` works as intended.
    """
    class TestType(metaclass = EntryStructure):
        id = ENTRY_ID
        name = STRING
        value = UINT64
    
    vampytest.assert_instance(TestType, EntryStructure)
    vampytest.assert_eq(
        TestType.__fields__,
        (
            DataBaseField('id', ENTRY_ID),
            DataBaseField('name', STRING),
            DataBaseField('value', UINT64),
        ),
    )
    vampytest.assert_instance(TestType.id, TupleGetter)
    vampytest.assert_eq(TestType.id.__reduce__()[1], (2, None))
    vampytest.assert_instance(TestType.name, TupleGetter)
    vampytest.assert_eq(TestType.name.__reduce__()[1], (3, None))
    vampytest.assert_instance(TestType.value, TupleGetter)
    vampytest.assert_eq(TestType.value.__reduce__()[1], (4, None))
