from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import get_to_do_page_count
from ..to_do import ToDo


def tes__get_to_do_page_count():
    """
    Tests whether ``get_to_do_page_count`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 20240919020
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 140
    entry_id_1 = 141
    entry_id_2 = 142
    
    to_do_0 = ToDo(name, description, created_at, creator_id)    
    to_do_0.entry_id = entry_id_0
    to_do_1 = ToDo(name, description, created_at, creator_id)    
    to_do_1.entry_id = entry_id_1
    to_do_2 = ToDo(name, description, created_at, creator_id)    
    to_do_2.entry_id = entry_id_2
    
    mocked = vampytest.mock_globals(
        get_to_do_page_count,
        PAGE_SIZE = 2
    )
    
    output = mocked([])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)

    output = mocked([to_do_0])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)
    
    output = mocked([to_do_0, to_do_1])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)
    
    output = mocked([to_do_0, to_do_1, to_do_2])
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
