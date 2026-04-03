from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import TO_DOS
from ..helpers import render_to_do_page
from ..to_do import ToDo


def test__render_to_do_page__no_value():
    """
    Tests whether ``render_to_do_page`` works as intended.
    
    Case: no value.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190012
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
    
    
    into = render_to_do_page([to_do_0, to_do_1, to_do_2], 1, None)
    output = ''.join(into)
    
    vampytest.assert_eq(
        output,
        (
            '```\n'
            '#134: miau\n'
            '#135: miau\n'
            '#136: miau\n'
            '```\n'
            'Page 1 / 1'
        ),
    )


def test__render_to_do_page__with_value():
    """
    Tests whether ``render_to_do_page`` works as intended.
    
    Case: with value.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190013
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 138
    entry_id_1 = 139
    entry_id_2 = 140
    
    to_do_0 = ToDo(name, description, created_at, creator_id)
    to_do_0.entry_id = entry_id_0
    
    to_do_1 = ToDo(name, description, created_at, creator_id)
    to_do_1.entry_id = entry_id_1
    
    to_do_2 = ToDo(name, description, created_at, creator_id)
    to_do_2.entry_id = entry_id_2
    
    
    into = render_to_do_page([to_do_0, to_do_1, to_do_2], 1, 'nyan')
    output = ''.join(into)
    
    vampytest.assert_eq(
        output,
        (
            'To-dos for: nyan\n'
            '```\n'
            '#138: miau\n'
            '#139: miau\n'
            '#140: miau\n'
            '```\n'
            'Page 1 / 1'
        ),
    )
