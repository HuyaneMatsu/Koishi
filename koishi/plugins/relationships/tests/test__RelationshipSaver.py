from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import RELATIONSHIP_CACHE
from ..relationship import Relationship
from ..relationship_saver import RelationshipSaver
from ..relationship_types import RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MASTER


def _assert_fields_set(relationship_saver):
    """
    Tests whether every fields are set of the given relationship request saver.
    
    Parameters
    ----------
    relationship_saver : ``RelationshipSaver``
        The instance to check.
    """
    vampytest.assert_instance(relationship_saver, RelationshipSaver)
    vampytest.assert_instance(relationship_saver.entry_proxy, Relationship)
    vampytest.assert_instance(relationship_saver.ensured_for_deletion, bool)
    vampytest.assert_instance(relationship_saver.modified_fields, dict, nullable = True)
    vampytest.assert_instance(relationship_saver.run_task, Task, nullable = True)


def test__RelationshipSaver__new():
    """
    Tests whether ``RelationshipSaver.__new__`` works as intended.
    """
    source_user_id = 202501020020
    target_user_id = 202501020021
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        _assert_fields_set(relationship_saver)
        
        vampytest.assert_is(relationship_saver.entry_proxy, relationship)

    finally:
        RELATIONSHIP_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__RelationshipSaver__repr():
    """
    Tests whether ``RelationshipSaver.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202501020022
    target_user_id = 202501020023
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    new_investment = 2002
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        ensured_for_deletion = True
        modified_fields = {'source_investment': new_investment}
        
        relationship_saver = RelationshipSaver(relationship)
        relationship_saver.ensured_for_deletion = ensured_for_deletion
        relationship_saver.modified_fields = modified_fields
        relationship_saver.run_task = Task(get_event_loop(), relationship_saver.run())
        
        output = repr(relationship_saver)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(RelationshipSaver.__name__, output)
        vampytest.assert_in(f'entry_proxy = {relationship!r}', output)
        vampytest.assert_in(f'ensured_for_deletion = {ensured_for_deletion!r}', output)
        vampytest.assert_in(f'modified_fields = {modified_fields!r}', output)
        vampytest.assert_in(f'running = {True!r}', output)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__RelationshipSaver__add_modification():
    """
    Tests whether ``RelationshipSaver.add_modification`` works as intended.
    """
    source_user_id = 202501020024
    target_user_id = 202501020025
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    new_investment = 2002
    new_relationship_type = RELATIONSHIP_TYPE_MASTER
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        
        vampytest.assert_eq(
            relationship_saver.modified_fields,
            None,
        )
        
        relationship_saver.add_modification('source_investment', new_investment)
        
        vampytest.assert_eq(
            relationship_saver.modified_fields,
            {
                'source_investment': new_investment,
            }
        )
        
        relationship_saver.add_modification('relationship_type', new_relationship_type)
        
        vampytest.assert_eq(
            relationship_saver.modified_fields,
            {
                'source_investment': new_investment,
                'relationship_type': new_relationship_type,
            }
        )
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__RelationshipSaver__ensure_deletion():
    """
    Tests whether ``RelationshipSaver.ensure_deletion`` works as intended.
    """
    source_user_id = 202501020026
    target_user_id = 202501020027
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        
        vampytest.assert_eq(relationship_saver.ensured_for_deletion, False)
        
        relationship_saver.ensure_deletion()
        
        vampytest.assert_eq(relationship_saver.ensured_for_deletion, True)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__RelationshipSaver__is_modified__not():
    """
    Tests whether ``RelationshipSaver.is_modified`` works as intended.
    
    Case: not modified.
    """
    source_user_id = 202501020028
    target_user_id = 202501020029
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        
        output = relationship_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__RelationshipSaver__is_modified__delete():
    """
    Tests whether ``RelationshipSaver.is_modified`` works as intended.
    
    Case: ensured for deletion.
    """
    source_user_id = 202501020030
    target_user_id = 202501020031
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        relationship_saver.ensure_deletion()
        
        output = relationship_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__RelationshipSaver__is_modified__field():
    """
    Tests whether ``RelationshipSaver.is_modified`` works as intended.
    
    Case: field modified.
    """
    source_user_id = 202501020032
    target_user_id = 202501020033
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    new_investment = 2002
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        relationship_saver.add_modification('source_investment', new_investment)
        
        output = relationship_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        RELATIONSHIP_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__RelationshipSaver__begin():
    """
    Tests whether ``RelationshipSaver.begin`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202501020034
    target_user_id = 202501020035
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        relationship.saver = relationship_saver
        
        output = relationship_saver.begin()
        
        vampytest.assert_instance(output, Task)
        vampytest.assert_is(relationship_saver.run_task, output)
        vampytest.assert_is(relationship.saver, relationship_saver)
        
        # do save
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        # after save nothing should be set.
        vampytest.assert_is(relationship_saver.run_task, None)
        vampytest.assert_is(relationship.saver, None)
    
    finally:
        RELATIONSHIP_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def RelationshipSaver__running():
    """
    Tests whether ``RelationshipSaver.running`` works as intended.
    """
    source_user_id = 202501020036
    target_user_id = 202501020037
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        
        relationship_saver = RelationshipSaver(relationship)
        relationship.saver = relationship_saver
        
        output = relationship_saver.running
        vampytest.assert_eq(output, False)
        
        relationship_saver.begin()
        
        output = relationship_saver.running
        vampytest.assert_eq(output, True)
        
    finally:
        RELATIONSHIP_CACHE.clear()
