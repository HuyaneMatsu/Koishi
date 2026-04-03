from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import TO_DOS
from ..helpers import resolve_to_dos
from ..to_do import ToDo


def test__resolve_to_dos__no_value():
    """
    Tests whether ``resolve_to_dos`` works as intended.
    
    Case: No value.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409180003
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 120
    entry_id_1 = 121
    entry_id_2 = 122
    
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
        
        output = resolve_to_dos(None)
        vampytest.assert_eq(
            output,
            [
                to_do_0,
                to_do_1,
                to_do_2,
            ],
        )
    
    finally:
        TO_DOS.clear()


def test__resolve_to_dos__value_is_index():
    """
    Tests whether ``resolve_to_dos`` works as intended.
    
    Case: value is an index.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409180004
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 120
    entry_id_1 = 121
    entry_id_2 = 122
    
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
        
        output = resolve_to_dos(f'#{entry_id_1}')
        vampytest.assert_eq(
            output,
            [
                to_do_1,
            ],
        )
    
    finally:
        TO_DOS.clear()


def test__resolve_to_dos__value_is_part_of_name():
    """
    Tests whether ``resolve_to_dos`` works as intended.
    
    Case: value is part of name.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409180005
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 120
    entry_id_1 = 121
    entry_id_2 = 122
    
    try:
        to_do_0 = ToDo('mister', description, created_at, creator_id)
        to_do_0.entry_id = entry_id_0
        TO_DOS[entry_id_0] = to_do_0
        
        to_do_1 = ToDo('sister', description, created_at, creator_id)
        to_do_1.entry_id = entry_id_1
        TO_DOS[entry_id_1] = to_do_1
        
        to_do_2 = ToDo(name, description, created_at, creator_id)
        to_do_2.entry_id = entry_id_2
        TO_DOS[entry_id_2] = to_do_2
        
        output = resolve_to_dos(name)
        vampytest.assert_eq(
            output,
            [
                to_do_2,
            ],
        )
    
    finally:
        TO_DOS.clear()
