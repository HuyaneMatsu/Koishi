from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import TO_DOS
from ..helpers import get_to_dos_sorted
from ..to_do import ToDo


def test__get_to_dos_sorted():
    """
    Tests whether ``get_to_dos_sorted`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409180000
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 120
    entry_id_1 = 121
    entry_id_2 = 122
    
    try:
        to_do_0 = ToDo(name, description, created_at, creator_id)
        to_do_0.entry_id = entry_id_0
        TO_DOS[entry_id_0] = to_do_0
        
        to_do_1 = ToDo(name, description, created_at, creator_id)
        to_do_1.entry_id = entry_id_1
        TO_DOS[entry_id_1] = to_do_1
        
        to_do_2 = ToDo(name, description, created_at, creator_id)
        to_do_2.entry_id = entry_id_2
        TO_DOS[entry_id_2] = to_do_2
        
        output = get_to_dos_sorted()
        vampytest.assert_eq(
            output,
            [
                to_do_0,
                to_do_1,
                to_do_2,
            ],
        )
    
    finally:
        TO_DOS.clear()
