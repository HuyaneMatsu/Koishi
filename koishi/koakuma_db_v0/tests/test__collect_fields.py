import vampytest

from ..data_base_field import DataBaseField
from ..data_types import UINT64
from ..structure import collect_fields


def test__collect_fields():
    """
    Tests whether ``collect_fields`` works as intended.
    """
    type_0 = type(
        'type_0',
        (),
        {
            '__fields__': (
                DataBaseField('nyan', UINT64),
                DataBaseField('rawr', UINT64),
            ),
        },
    )
    
    output = collect_fields(
        type,
        (type_0, ),
        {
            'pyon': UINT64,
        },
    )
    
    vampytest.assert_eq(
        output,
        (
            DataBaseField('nyan', UINT64),
            DataBaseField('rawr', UINT64),
            DataBaseField('pyon', UINT64),
        ),
    )


def test__collect_fields__multiple_bases():
    """
    Tests whether ``collect_fields`` works as intended.
    """
    type_0 = type(
        'type_0',
        (),
        {
            '__fields__': (
                DataBaseField('nyan', UINT64),
                DataBaseField('rawr', UINT64),
            ),
        },
    )
    
    with vampytest.assert_raises(RuntimeError):
        collect_fields(
            type,
            (type_0, type_0),
            {
                'pyon': UINT64,
            },
        )
