from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import get_to_do_page_count
from ..to_do import ToDo


def _iter_options():
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
    
    yield (
        [],
        0,
    )
    
    yield (
        [to_do_0],
        1,
    )
    
    yield (
        [to_do_0, to_do_1],
        1,
    )
    
    yield (
        [to_do_0, to_do_1, to_do_2],
        2,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def tes__get_to_do_page_count(to_do_listing):
    """
    Tests whether ``get_to_do_page_count`` works as intended.
    
    Parameters
    ----------
    to_do_listing : ``list<ToDo>``
        The matched to-dos.
    
    Returns
    -------
    output : `int`
    """
    mocked = vampytest.mock_globals(
        get_to_do_page_count,
        PAGE_SIZE = 2
    )
    
    output = mocked(to_do_listing)
    vampytest.assert_instance(output, int)
    return output
