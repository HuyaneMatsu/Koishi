import vampytest

from ..constants import FIELD_FLAG_LISTING
from ..custom_data_types import create_data_type_custom, create_data_type_listing
from ..data_base_field import DataBaseField
from ..data_types import STRING, UINT64
from ..structure import get_fields_description

from .helpers import TestStructure


def _iter_options():
    string_listing = create_data_type_listing(STRING)
    
    structure = create_data_type_custom(TestStructure)
    structure_listing = create_data_type_listing(structure)
    
    yield (
        (),
        (),
    )
    
    yield (
        (
            DataBaseField('nyan', STRING),
            DataBaseField('rawr', UINT64),
        ),
        (
            (0, 'nyan', STRING.id, None),
            (0, 'rawr', UINT64.id, None),
        ),
    )
    
    yield (
        (
            DataBaseField('nyan', string_listing),
        ),
        (
            (FIELD_FLAG_LISTING, 'nyan', STRING.id, None),
        ),
    )
    
    yield (
        (
            DataBaseField('nyan', structure),
        ),
        (
            (
                0,
                'nyan',
                0,
                (
                    (0, 'name', STRING.id, None),
                    (0, 'value', UINT64.id, None),
                ),
            ),
        ),
    )
    
    yield (
        (
            DataBaseField('nyan', structure_listing),
        ),
        (
            (
                FIELD_FLAG_LISTING,
                'nyan',
                0,
                (
                    (0, 'name', STRING.id, None),
                    (0, 'value', UINT64.id, None),
                ),
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_fields_description(fields):
    """
    Tests whether ``get_fields_description`` works as intended.
    
    Parameters
    ----------
    fields : ``tuple<DataBaseField>``
        Fields to describe to.
    
    Returns
    -------
    output : ``tuple<(int, str, int, (None | ...))>``
    """
    output = get_fields_description(fields)
    vampytest.assert_instance(output, tuple)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 4)
        flags, name, data_type_id, sub_description = element
        vampytest.assert_instance(flags, int)
        vampytest.assert_instance(name, str)
        vampytest.assert_instance(data_type_id, int)
        vampytest.assert_instance(sub_description, tuple, nullable = True)
    
    return output
