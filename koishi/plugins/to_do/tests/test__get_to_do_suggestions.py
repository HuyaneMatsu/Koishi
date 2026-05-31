from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import get_to_do_suggestions
from ..to_do import ToDo


def _iter_options():
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190008
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 128
    entry_id_1 = 129
    entry_id_2 = 130
    
    to_do_0 = ToDo(name, description, created_at, creator_id)
    to_do_0.entry_id = entry_id_0
    
    to_do_1 = ToDo(name, description, created_at, creator_id)
    to_do_1.entry_id = entry_id_1
    
    to_do_2 = ToDo(name, description, created_at, creator_id)
    to_do_2.entry_id = entry_id_2
    
    to_do_listing = [to_do_0, to_do_1, to_do_2]
    
    yield (
        to_do_listing,
        None,
        [('#128: miau', '#128'), ('#129: miau', '#129'), ('#130: miau', '#130')],
    )
    
    yield (
        to_do_listing,
        'mister',
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_to_do_suggestions(to_do_listing, value):
    """
    Tests whether ``get_to_do_suggestions`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to match.
    
    Returns
    -------
    output : `list<(str, str)>`
    """
    output = get_to_do_suggestions(to_do_listing, value)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 2)
        
        name, value = element
        vampytest.assert_instance(name, str)
        vampytest.assert_instance(value, str)
    
    return output
