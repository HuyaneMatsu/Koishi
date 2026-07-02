import vampytest

from ..data_base_connected import _make_serialised_entry_parts

from .helpers import TestEntry


def test__make_serialised_entry_parts():
    """
    Tests whether ``_make_serialised_entry_parts`` works as intended.
    """
    entry_type = TestEntry
    entry_values = [0, 0, 23, 'shrimp', 44444]
    output = _make_serialised_entry_parts(entry_type, entry_values)
    vampytest.assert_instance(output, list)
    vampytest.assert_eq(
        output,
        [
            b'',
            (23).to_bytes(8, 'little'),
            (6).to_bytes(1, 'little'),
            b'shrimp',
            (44444).to_bytes(8, 'little'),
        ],
    )
