from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import render_to_do_listing_element_into
from ..to_do import ToDo


def tes__render_to_do_listing_element_into():
    """
    Tests whether ``render_to_do_listing_element_into`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190008
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id = 133
    
    to_do = ToDo(name, description, created_at, creator_id)
    to_do.entry_id = entry_id
    
    into = render_to_do_listing_element_into(to_do, [])
    output = ''.join(into)
    vampytest.assert_instance(to_do, output)
    vampytest.assert_eq(
        output,
        '#133: miau\n'
    )
