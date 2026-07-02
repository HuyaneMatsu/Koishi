from ..data_types import ENTRY_ID, STRING, UINT64
from ..structure import EntryStructure, Structure


class TestEntry(metaclass = EntryStructure):
    id = ENTRY_ID
    name = STRING
    value = UINT64


class TestEntryDifferent(metaclass = EntryStructure):
    id = ENTRY_ID
    value = UINT64


class TestStructure(metaclass = Structure):
    name = STRING
    value = UINT64
