from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle
from hata import DATETIME_FORMAT_CODE

from ....bot_utils.models import DB_ENGINE

from ..constants import (
    RELATIONSHIP_CACHE, RELATIONSHIP_LISTING_CACHE
)
from ..relationship import Relationship
from ..relationship_saver import RelationshipSaver
from ..relationship_types import RELATIONSHIP_TYPE_MAMA, get_relationship_type_name


def _assert_fields_set(relationship):
    """
    Asserts whether every fields are set of the relationship.
    
    Parameters
    ----------
    relationship : ``Relationship``
        Relationship to test.
    """
    vampytest.assert_instance(relationship, Relationship)
    vampytest.assert_instance(relationship.entry_id, int)
    vampytest.assert_instance(relationship.relationship_type, int)
    vampytest.assert_instance(relationship.source_can_boost_at, DateTime)
    vampytest.assert_instance(relationship.source_investment, int)
    vampytest.assert_instance(relationship.source_user_id, int)
    vampytest.assert_instance(relationship.target_can_boost_at, DateTime)
    vampytest.assert_instance(relationship.target_investment, int)
    vampytest.assert_instance(relationship.target_user_id, int)


def test__Relationship__new():
    """
    Tests whether ``Relationship.__new__`` works as intended.
    """
    source_user_id = 202501020000
    target_user_id = 202501020001
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
        _assert_fields_set(relationship)
        
        vampytest.assert_eq(relationship.source_user_id, source_user_id)
        vampytest.assert_eq(relationship.target_user_id, target_user_id)
        vampytest.assert_eq(relationship.source_investment, investment)
        vampytest.assert_eq(relationship.target_investment, 0)
        vampytest.assert_eq(relationship.source_can_boost_at, now)
        vampytest.assert_eq(relationship.target_can_boost_at, now)
        
        vampytest.assert_eq(relationship.relationship_type, relationship_type)
        
        # Should not auto store in cache
        vampytest.assert_is(RELATIONSHIP_CACHE.get(relationship.entry_id, None), None)
        
    finally:
        RELATIONSHIP_CACHE.clear()


def test__Relationship__repr():
    """
    Tests whether ``relationship.__repr__`` works as intended.
    """
    source_user_id = 202501020002
    target_user_id = 202501020003
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    target_investment = 3000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    target_can_boost_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    
    entry_id = 3499
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            source_investment,
            source_can_boost_at,
        )
        
        relationship.entry_id = entry_id
        relationship.target_investment = target_investment
        relationship.target_can_boost_at = target_can_boost_at
        
        output = repr(relationship)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(Relationship.__name__, output)
        vampytest.assert_in(f'entry_id = {entry_id!r}', output)
        vampytest.assert_in(
            f'relationship_type = {get_relationship_type_name(relationship_type)!s} ~ {relationship_type!r}',
            output,
        )
        vampytest.assert_in(f'source_user_id = {source_user_id!r}', output)
        vampytest.assert_in(f'target_user_id = {target_user_id!r}', output)
        vampytest.assert_in(f'source_investment = {source_investment!r}', output)
        vampytest.assert_in(f'target_investment = {target_investment!r}', output)
        vampytest.assert_in(f'source_can_boost_at = {source_can_boost_at:{DATETIME_FORMAT_CODE}}', output)
        vampytest.assert_in(f'target_can_boost_at = {target_can_boost_at:{DATETIME_FORMAT_CODE}}', output)
        
    finally:
        RELATIONSHIP_CACHE.clear()


def test__Relationship__bool():
    """
    Tests whether ``Relationship.__bool__`` works as intended.
    
    Returns
    -------
    output : `bool`
    """
    source_user_id = 202501020004
    target_user_id = 202501020005
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
        
        output = bool(relationship)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__Relationship__get_saver():
    """
    Tests whether ``Relationship.get_saver`` works as intended.
    """
    source_user_id = 202501020006
    target_user_id = 202501020007
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
        
        output = relationship.get_saver()
        vampytest.assert_instance(output, RelationshipSaver)
        vampytest.assert_is(output.entry_proxy, relationship)
        vampytest.assert_is(relationship.saver, output)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__Relationship__get_saver__caching():
    """
    Tests whether ``Relationship.get_saver`` works as intended.
    
    Case: caching.
    """
    source_user_id = 202501020008
    target_user_id = 202501020009
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
        
        output_0 = relationship.get_saver()
        output_1 = relationship.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__Relationship__from_entry():
    """
    Tests whether ``Relationship.from_entry`` works as intended.
    """
    source_user_id = 202501020010
    target_user_id = 202501020011
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    target_investment = 3000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    target_can_boost_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    entry_id = 3501
    
    try:
        entry = {
            'id': entry_id,
            'relationship_type': relationship_type,
            'source_user_id': source_user_id,
            'target_user_id': target_user_id,
            'source_investment': source_investment,
            'target_investment': target_investment,
            'source_can_boost_at': source_can_boost_at.replace(tzinfo = None),
            'target_can_boost_at': target_can_boost_at.replace(tzinfo = None),
        }
        
        relationship = Relationship.from_entry(entry)
        _assert_fields_set(relationship)
        
        # Should auto store in cache
        vampytest.assert_is(RELATIONSHIP_CACHE.get(entry_id, None), relationship)
        
        vampytest.assert_eq(relationship.entry_id, entry_id)
        vampytest.assert_eq(relationship.relationship_type, relationship_type)
        vampytest.assert_eq(relationship.source_user_id, source_user_id)
        vampytest.assert_eq(relationship.target_user_id, target_user_id)
        vampytest.assert_eq(relationship.source_investment, source_investment)
        vampytest.assert_eq(relationship.target_investment, target_investment)
        vampytest.assert_eq(relationship.source_can_boost_at, source_can_boost_at)
        vampytest.assert_eq(relationship.target_can_boost_at, target_can_boost_at)
    
    finally:
        RELATIONSHIP_CACHE.clear()


def test__Relationship__from_entry__cache():
    """
    Tests whether ``Relationship.from_entry`` works as intended.
    
    Case: Caching.
    """
    source_user_id = 202501020012
    target_user_id = 202501020013
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    target_investment = 3000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    target_can_boost_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    entry_id = 3502
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            source_investment,
            source_can_boost_at,
        )
        relationship.entry_id = entry_id
        RELATIONSHIP_CACHE[entry_id] = relationship
        
        entry = {
            'id': entry_id,
            'relationship_type': relationship_type,
            'source_user_id': source_user_id,
            'target_user_id': target_user_id,
            'source_investment': source_investment,
            'target_investment': target_investment,
            'source_can_boost_at': source_can_boost_at.replace(tzinfo = None),
            'target_can_boost_at': target_can_boost_at.replace(tzinfo = None),
        }
        
        output = Relationship.from_entry(entry)
        vampytest.assert_is(output, relationship)
        
        vampytest.assert_eq(relationship.entry_id, entry_id)
        vampytest.assert_eq(relationship.relationship_type, relationship_type)
        vampytest.assert_eq(relationship.source_user_id, source_user_id)
        vampytest.assert_eq(relationship.target_user_id, target_user_id)
        vampytest.assert_eq(relationship.source_investment, source_investment)
        vampytest.assert_eq(relationship.target_investment, target_investment)
        vampytest.assert_eq(relationship.source_can_boost_at, source_can_boost_at)
        vampytest.assert_eq(relationship.target_can_boost_at, target_can_boost_at)
    
    finally:
        RELATIONSHIP_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__Relationship__delete():
    """
    Tests whether ``Relationship.delete`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202501020014
    target_user_id = 202501020015
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    entry_id = 3500
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        relationship.entry_id = entry_id
        RELATIONSHIP_CACHE[entry_id] = relationship
        RELATIONSHIP_LISTING_CACHE[source_user_id] = [relationship]
        RELATIONSHIP_LISTING_CACHE[target_user_id] = [relationship]
        
        vampytest.assert_is(relationship.saver, None)
        vampytest.assert_is_not(RELATIONSHIP_CACHE.get(entry_id, None), None)
        
        relationship.delete()
        
        vampytest.assert_is_not(relationship.saver, None)
        vampytest.assert_is(RELATIONSHIP_CACHE.get(entry_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(relationship.saver, None)
        vampytest.assert_is(RELATIONSHIP_CACHE.get(entry_id, None), None)
        vampytest.assert_is(RELATIONSHIP_LISTING_CACHE.get(source_user_id, None), None)
        vampytest.assert_is(RELATIONSHIP_LISTING_CACHE.get(target_user_id, None), None)
    
    finally:
        RELATIONSHIP_CACHE.clear()
        RELATIONSHIP_LISTING_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__Relationship__set__add_field():
    """
    Tests whether ``Relationship.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    source_user_id = 202501020016
    target_user_id = 202501020017
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    entry_id = 3503
    
    new_investment = 2002
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        relationship.entry_id = entry_id
        vampytest.assert_is(relationship.saver, None)
        vampytest.assert_is(RELATIONSHIP_CACHE.get(entry_id, None), None)
        vampytest.assert_eq(relationship.source_investment, investment)
        
        relationship.set('source_investment', new_investment)
        
        vampytest.assert_eq(relationship.source_investment, new_investment)
        vampytest.assert_is_not(relationship.saver, None)
        vampytest.assert_eq(relationship.saver.modified_fields, {'source_investment': new_investment})
        vampytest.assert_is(RELATIONSHIP_CACHE.get(entry_id, None), relationship)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_eq(relationship.source_investment, new_investment)
        vampytest.assert_is(relationship.saver, None)
        vampytest.assert_is(RELATIONSHIP_CACHE.get(entry_id, None), relationship)
        
    finally:
        RELATIONSHIP_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__Relationship__set__save():
    """
    Tests whether ``Relationship.save`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202501020018
    target_user_id = 202501020019
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    entry_id = 3504
    
    try:
        relationship = Relationship(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
            now,
        )
        relationship.entry_id = entry_id
        
        RELATIONSHIP_LISTING_CACHE[source_user_id] = None
        RELATIONSHIP_LISTING_CACHE[target_user_id] = [relationship]
        
        task = Task(get_event_loop(), relationship.save())
        
        await skip_ready_cycle()
        
        vampytest.assert_is_not(relationship.saver, None)
        
        task.apply_timeout(0.1)
        await task
        
        key = next(iter(RELATIONSHIP_CACHE.keys()), None)
        vampytest.assert_is_not(key, None)
        vampytest.assert_eq(relationship.entry_id, key)
        vampytest.assert_is(RELATIONSHIP_CACHE.get(key, None), relationship)
        vampytest.assert_eq(RELATIONSHIP_LISTING_CACHE.get(source_user_id, None), [relationship])
        vampytest.assert_eq(RELATIONSHIP_LISTING_CACHE.get(target_user_id, None), [relationship])
        
        vampytest.assert_is(relationship.saver, None)
        
    finally:
        RELATIONSHIP_CACHE.clear()
        RELATIONSHIP_LISTING_CACHE.clear()
