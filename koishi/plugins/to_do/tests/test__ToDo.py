from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import DATETIME_FORMAT_CODE
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import TO_DOS
from ..to_do import ToDo
from ..to_do_saver import ToDoSaver


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
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        _assert_fields_set(to_do)
        
        vampytest.assert_eq(to_do.created_at, created_at)
        vampytest.assert_eq(to_do.creator_id, creator_id)
        vampytest.assert_eq(to_do.description, description)
        vampytest.assert_eq(to_do.name, name)
        
        # Should not auto store in cache
        vampytest.assert_is(TO_DOS.get(to_do.entry_id, None), None)
        
    finally:
        TO_DOS.clear()


def test__ToDo__repr():
    """
    Tests whether ``to_do.__repr__`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170001
    description = 'nyan nyan'
    name = 'miau'
    entry_id = 100
    
    try:
        
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
        
    finally:
        TO_DOS.clear()


def test__ToDo__bool():
    """
    Tests whether ``ToDo.__bool__`` works as intended.
    
    Returns
    -------
    output : `bool`
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170002
    description = 'nyan nyan'
    name = 'miau'
    entry_id = 101
    
    try:
        
        to_do = ToDo(name, description, created_at, creator_id)
        to_do.entry_id = entry_id
        
        output = bool(to_do)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        TO_DOS.clear()


def test__ToDo__get_saver():
    """
    Tests whether ``ToDo.get_saver`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170004
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        output = to_do.get_saver()
        vampytest.assert_instance(output, ToDoSaver)
        vampytest.assert_is(output.entry_proxy, to_do)
        vampytest.assert_is(to_do.saver, output)
    
    finally:
        TO_DOS.clear()


def test__ToDo__get_saver__caching():
    """
    Tests whether ``ToDo.get_saver`` works as intended.
    
    Case: caching.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170005
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        output_0 = to_do.get_saver()
        output_1 = to_do.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        TO_DOS.clear()


def test__ToDo__from_entry():
    """
    Tests whether ``ToDo.from_entry`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170006
    description = 'nyan nyan'
    name = 'miau'
    entry_id = 102
    
    try:
        entry = {
            'created_at': created_at.replace(tzinfo = None),
            'creator_id': creator_id,
            'description': description,
            'name': name,
            'id': entry_id,
        }
        
        to_do = ToDo.from_entry(entry)
        _assert_fields_set(to_do)
        
        # Should auto store in cache
        vampytest.assert_is(TO_DOS.get(entry_id, None), to_do)
        
        vampytest.assert_eq(to_do.created_at, created_at)
        vampytest.assert_eq(to_do.creator_id, creator_id)
        vampytest.assert_eq(to_do.description, description)
        vampytest.assert_eq(to_do.name, name)
        vampytest.assert_eq(to_do.entry_id, entry_id)
    
    finally:
        TO_DOS.clear()


def test__ToDo__from_entry__cache():
    """
    Tests whether ``ToDo.from_entry`` works as intended.
    
    Case: Caching.
    """
    old_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_creator_id = 202409170007
    old_description = 'nyan nyan'
    old_name = 'miau'
    
    new_created_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_creator_id = 202409170008
    new_description = 'miau miau'
    new_name = 'nyan'
    
    entry_id = 103
    
    try:
        to_do = ToDo(old_name, old_description, old_created_at, old_creator_id)
        to_do.entry_id = entry_id
        TO_DOS[entry_id] = to_do
        
        entry = {
            'created_at': new_created_at.replace(tzinfo = None),
            'creator_id': new_creator_id,
            'description': new_description,
            'name': new_name,
            'id': entry_id,
        }
        
        output = ToDo.from_entry(entry)
        vampytest.assert_is(output, to_do)
        
        vampytest.assert_eq(to_do.entry_id, entry_id)
        vampytest.assert_eq(to_do.created_at, new_created_at)
        vampytest.assert_eq(to_do.creator_id, new_creator_id)
        vampytest.assert_eq(to_do.description, new_description)
        vampytest.assert_eq(to_do.name, new_name)
    
    finally:
        TO_DOS.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__ToDo__delete():
    """
    Tests whether ``ToDo.delete`` works as intended.
    
    This function is a coroutine.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170010
    description = 'nyan nyan'
    name = 'miau'
    entry_id = 105
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        to_do.entry_id = entry_id
        TO_DOS[entry_id] = to_do
        
        vampytest.assert_is(to_do.saver, None)
        vampytest.assert_is_not(TO_DOS.get(entry_id, None), None)
        
        to_do.delete()
        
        vampytest.assert_is_not(to_do.saver, None)
        vampytest.assert_is(TO_DOS.get(entry_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(to_do.saver, None)
        vampytest.assert_is(TO_DOS.get(entry_id, None), None)
    
    finally:
        TO_DOS.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__ToDo__set__add_field():
    """
    Tests whether ``ToDo.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170011
    description = 'nyan nyan'
    name = 'miau'
    
    new_name = 'hey mister'
    
    entry_id = 0
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        vampytest.assert_is(to_do.saver, None)
        vampytest.assert_is(TO_DOS.get(entry_id, None), None)
        vampytest.assert_eq(to_do.name, name)
        
        to_do.set('name', new_name)
        
        vampytest.assert_eq(to_do.name, new_name)
        vampytest.assert_is_not(to_do.saver, None)
        vampytest.assert_eq(to_do.saver.modified_fields, {'name': new_name})
        vampytest.assert_is(TO_DOS.get(entry_id, None), to_do)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_eq(to_do.name, new_name)
        vampytest.assert_is(to_do.saver, None)
        vampytest.assert_is(TO_DOS.get(entry_id, None), to_do)
        
    finally:
        TO_DOS.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__ToDo__set__save():
    """
    Tests whether ``ToDo.save`` works as intended.
    
    This function is a coroutine.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170011
    description = 'nyan nyan'
    name = 'miau'

    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        task = Task(get_event_loop(), to_do.save())
        
        await skip_ready_cycle()
        
        vampytest.assert_is_not(to_do.saver, None)
        
        task.apply_timeout(0.1)
        await task
        
        key = next(iter(TO_DOS.keys()), None)
        vampytest.assert_is_not(key, None)
        vampytest.assert_eq(to_do.entry_id, key)
        vampytest.assert_is(TO_DOS.get(key, None), to_do)
        
        vampytest.assert_is(to_do.saver, None)
        
    finally:
        TO_DOS.clear()
