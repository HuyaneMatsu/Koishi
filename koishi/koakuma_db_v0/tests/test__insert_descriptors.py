from collections import _tuplegetter as TupleGetter

import vampytest

from ..data_base_field import DataBaseField
from ..data_types import UINT64
from ..structure import insert_descriptors


def test__insert_descriptors():
    """
    Tests whether ``insert_descriptors`` works as intended.
    """
    type_attributes = {}
    
    insert_descriptors(
        (
            DataBaseField('nyan', UINT64),
            DataBaseField('rawr', UINT64),
            DataBaseField('pyon', UINT64),
        ),
        type_attributes,
        1,
    )
    
    vampytest.assert_eq(
        {
            ('nyan', 1),
            ('rawr', 2),
            ('pyon', 3),
        },
        {
            (name, value.__reduce__()[1][0])
            for name, value in type_attributes.items()
        },
    )
