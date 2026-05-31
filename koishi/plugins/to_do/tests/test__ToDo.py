from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import DATETIME_FORMAT_CODE

from ..to_do import ToDo


def _assert_fields_set(to_do):
    """
    Asserts whether every fields are set of the to-do.
    
    Parameters
    ----------
    to_do : ``ToDo``
        To-do entry to test.
    """
    vampytest.assert_instance(to_do, ToDo)
    vampytest.assert_instance(to_do.creator_id, int)
    vampytest.assert_instance(to_do.created_at, DateTime)
    vampytest.assert_instance(to_do.entry_id, int)
    vampytest.assert_instance(to_do.description, str)
    vampytest.assert_instance(to_do.name, str)


def test__ToDo__new():
    """
    Tests whether ``ToDo.__new__`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170000
    description = 'nyan nyan'
    name = 'miau'
    
    to_do = ToDo(name, description, created_at, creator_id)
    _assert_fields_set(to_do)
    
    vampytest.assert_eq(to_do.created_at, created_at)
    vampytest.assert_eq(to_do.creator_id, creator_id)
    vampytest.assert_eq(to_do.description, description)
    vampytest.assert_eq(to_do.name, name)



def test__ToDo__repr():
    """
    Tests whether ``to_do.__repr__`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170001
    description = 'nyan nyan'
    name = 'miau'
    entry_id = 100
    
    to_do = ToDo(name, description, created_at, creator_id)
    to_do.entry_id = entry_id
    
    output = repr(to_do)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(ToDo.__name__, output)
    vampytest.assert_in(f'entry_id = {entry_id!r}', output)
    vampytest.assert_in(f'created_at = {created_at:{DATETIME_FORMAT_CODE}}', output)
    vampytest.assert_in(f'creator_id = {creator_id!r}', output)
    vampytest.assert_in(f'description = {description!r}', output)
    vampytest.assert_in(f'name = {name!r}', output)


def test__ToDo__from_entry():
    """
    Tests whether ``ToDo.from_entry`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170006
    description = 'nyan nyan'
    name = 'miau'
    entry_id = 102
    
    entry = {
        'created_at': created_at.replace(tzinfo = None),
        'creator_id': creator_id,
        'description': description,
        'name': name,
        'id': entry_id,
    }
    
    to_do = ToDo.from_entry(entry)
    _assert_fields_set(to_do)
    
    vampytest.assert_eq(to_do.created_at, created_at)
    vampytest.assert_eq(to_do.creator_id, creator_id)
    vampytest.assert_eq(to_do.description, description)
    vampytest.assert_eq(to_do.name, name)
    vampytest.assert_eq(to_do.entry_id, entry_id)
