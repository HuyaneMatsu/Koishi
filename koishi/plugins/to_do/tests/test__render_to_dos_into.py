from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import render_to_dos_into
from ..to_do import ToDo


def test__render_to_dos_into():
    """
    Tests whether ``render_to_dos_into`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190009
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 134
    entry_id_1 = 135
    entry_id_2 = 136
    
    to_do_0 = ToDo(name, description, created_at, creator_id)
    to_do_0.entry_id = entry_id_0
    to_do_1 = ToDo(name, description, created_at, creator_id)
    to_do_1.entry_id = entry_id_1
    to_do_2 = ToDo(name, description, created_at, creator_id)
    to_do_2.entry_id = entry_id_2
    
    
    into = render_to_dos_into([to_do_0, to_do_1, to_do_2], [])
    output = ''.join(into)
    
    vampytest.assert_eq(
        output,
        (
            '```\n'
            '#134: miau\n'
            '#135: miau\n'
            '#136: miau\n'
            '```'
        ),
    )
