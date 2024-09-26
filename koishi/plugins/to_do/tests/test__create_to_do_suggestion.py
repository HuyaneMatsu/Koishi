from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import create_to_do_suggestion
from ..to_do import ToDo


def tes__create_to_do_suggestion():
    """
    Tests whether ``create_to_do_suggestion`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409180006
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id = 132
    
    to_do = ToDo(name, description, created_at, creator_id)
    to_do.entry_id = entry_id
    
    output = create_to_do_suggestion(to_do)
    vampytest.assert_instance(to_do, output)
    vampytest.assert_eq(
        output,
        (
            '#132: miau',
            '#132',
        )
    )
