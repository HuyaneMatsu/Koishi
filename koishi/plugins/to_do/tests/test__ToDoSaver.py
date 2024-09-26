from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..to_do import ToDo
from ..to_do_saver import ToDoSaver
from ..constants import TO_DOS


def _assert_fields_set(to_do_saver):
    """
    Tests whether every fields are set of the given automation configuration saver.
    
    Parameters
    ----------
    to_do_saver : ``ToDoSaver``
        The instance to check.
    """
    vampytest.assert_instance(to_do_saver, ToDoSaver)
    vampytest.assert_instance(to_do_saver.entry_proxy, ToDo)
    vampytest.assert_instance(to_do_saver.ensured_for_deletion, bool)
    vampytest.assert_instance(to_do_saver.modified_fields, dict, nullable = True)
    vampytest.assert_instance(to_do_saver.run_task, Task, nullable = True)


def test__ToDoSaver__new():
    """
    Tests whether ``ToDoSaver.__new__`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170013
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        _assert_fields_set(to_do_saver)
        
        vampytest.assert_is(to_do_saver.entry_proxy, to_do)

    finally:
        TO_DOS.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__ToDoSaver__repr():
    """
    Tests whether ``ToDoSaver.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170014
    description = 'nyan nyan'
    name = 'miau'
    
    new_name = 'nyan'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        ensured_for_deletion = True
        modified_fields = {'name': new_name}
        
        to_do_saver = ToDoSaver(to_do)
        to_do_saver.ensured_for_deletion = ensured_for_deletion
        to_do_saver.modified_fields = modified_fields
        to_do_saver.run_task = Task(get_event_loop(), to_do_saver.run())
        
        output = repr(to_do_saver)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(ToDoSaver.__name__, output)
        vampytest.assert_in(f'entry_proxy = {to_do!r}', output)
        vampytest.assert_in(f'ensured_for_deletion = {ensured_for_deletion!r}', output)
        vampytest.assert_in(f'modified_fields = {modified_fields!r}', output)
        vampytest.assert_in(f'running = {True!r}', output)
    
    finally:
        TO_DOS.clear()


def test__ToDoSaver__add_modification():
    """
    Tests whether ``ToDoSaver.add_modification`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170015
    description = 'nyan nyan'
    name = 'miau'
    
    new_name = 'nyan'
    new_description = 'hey mister'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        
        vampytest.assert_eq(
            to_do_saver.modified_fields,
            None,
        )
        
        to_do_saver.add_modification('name', new_name)
        
        vampytest.assert_eq(
            to_do_saver.modified_fields,
            {
                'name': new_name,
            }
        )
        
        to_do_saver.add_modification('description', new_description)
        
        vampytest.assert_eq(
            to_do_saver.modified_fields,
            {
                'name': new_name,
                'description': new_description,
            }
        )
    
    finally:
        TO_DOS.clear()


def test__ToDoSaver__ensure_deletion():
    """
    Tests whether ``ToDoSaver.ensure_deletion`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170016
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        
        vampytest.assert_eq(to_do_saver.ensured_for_deletion, False)
        
        to_do_saver.ensure_deletion()
        
        vampytest.assert_eq(to_do_saver.ensured_for_deletion, True)
    
    finally:
        TO_DOS.clear()


def test__ToDoSaver__is_modified__not():
    """
    Tests whether ``ToDoSaver.is_modified`` works as intended.
    
    Case: not modified.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170017
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        
        output = to_do_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        TO_DOS.clear()


def test__ToDoSaver__is_modified__delete():
    """
    Tests whether ``ToDoSaver.is_modified`` works as intended.
    
    Case: ensured for deletion.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170018
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        to_do_saver.ensure_deletion()
        
        output = to_do_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        TO_DOS.clear()


def test__ToDoSaver__is_modified__field():
    """
    Tests whether ``ToDoSaver.is_modified`` works as intended.
    
    Case: field modified.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170019
    description = 'nyan nyan'
    name = 'miau'
    
    new_name = 'nyan'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        to_do_saver.add_modification('name', new_name)
        
        output = to_do_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        TO_DOS.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__ToDoSaver__begin():
    """
    Tests whether ``ToDoSaver.begin`` works as intended.
    
    This function is a coroutine.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170020
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        to_do.saver = to_do_saver
        
        output = to_do_saver.begin()
        
        vampytest.assert_instance(output, Task)
        vampytest.assert_is(to_do_saver.run_task, output)
        vampytest.assert_is(to_do.saver, to_do_saver)
        
        # do save
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        # after save nothing should be set.
        vampytest.assert_is(to_do_saver.run_task, None)
        vampytest.assert_is(to_do.saver, None)
    
    finally:
        TO_DOS.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def ToDoSaver__running():
    """
    Tests whether ``ToDoSaver.running`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409190001
    description = 'nyan nyan'
    name = 'miau'
    
    try:
        to_do = ToDo(name, description, created_at, creator_id)
        
        to_do_saver = ToDoSaver(to_do)
        to_do.saver = to_do_saver
        
        output = to_do_saver.running
        vampytest.assert_eq(output, False)
        
        to_do_saver.begin()
        
        output = to_do_saver.running
        vampytest.assert_eq(output, True)
        
    finally:
        TO_DOS.clear()
