from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import TO_DOS
from ..helpers import resolve_to_do
from ..to_do import ToDo


def test__resolve_to_do():
    """
    Tests whether ``resolve_to_do`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409180006
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 128
    entry_id_1 = 129
    entry_id_2 = 130
    
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
        
        output = resolve_to_do(None)
        vampytest.assert_is(output, to_do_0)
    
        output = resolve_to_do('mister')
        vampytest.assert_is(output, None)
        
    finally:
        TO_DOS.clear()
