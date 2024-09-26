from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import TO_DOS
from ..helpers import get_to_do_suggestions
from ..to_do import ToDo


def test__get_to_do_suggestions():
    """
    Tests whether ``get_to_do_suggestions`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190008
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
        
        output = get_to_do_suggestions(None)
        vampytest.assert_eq(output, [('#128: miau', '#128'), ('#129: miau', '#129'), ('#130: miau', '#130')])
    
        output = get_to_do_suggestions('mister')
        vampytest.assert_eq(output, [])
        
    finally:
        TO_DOS.clear()
