from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import match_to_do_listing
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
        to_do_listing,
    )
    
    yield (
        to_do_listing,
        f'#{entry_id_1}',
        [
            to_do_1,
        ],
    )
    
    yield (
        to_do_listing,
            'mister',
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__match_to_do_listing__no_value(to_do_listing, value):
    """
    Tests whether ``match_to_do_listing`` works as intended.
    
    Parameters
    ----------
    to_do_listing : ``list<ToDo>``
        To do listing to filter from.
    
    value : `None | str`
        Value to match.
    
    Returns
    -------
    matched_to_do_listing : ``list<ToDo>``
    """
    output = match_to_do_listing(to_do_listing, value)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, ToDo)
    
    return output
