import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import (
    RELATIONSHIP_REQUEST_CACHE, RELATIONSHIP_REQUEST_CACHE_LISTING
)
from ..relationship_request import RelationshipRequest
from ..relationship_request_saver import RelationshipRequestSaver
from ..relationship_types import RELATIONSHIP_TYPE_MAMA, get_relationship_type_name


def _assert_fields_set(relationship_request):
    """
    Asserts whether every fields are set of the relationship request.
    
    Parameters
    ----------
    relationship_request : ``RelationshipRequest``
        Relationship request to test.
    """
    vampytest.assert_instance(relationship_request, RelationshipRequest)
    vampytest.assert_instance(relationship_request.entry_id, int)
    vampytest.assert_instance(relationship_request.investment, int)
    vampytest.assert_instance(relationship_request.source_user_id, int)
    vampytest.assert_instance(relationship_request.relationship_type, int)
    vampytest.assert_instance(relationship_request.target_user_id, int)


def test__RelationshipRequest__new():
    """
    Tests whether ``RelationshipRequest.__new__`` works as intended.
    """
    source_user_id = 202412260000
    target_user_id = 202412260001
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        _assert_fields_set(relationship_request)
        
        vampytest.assert_eq(relationship_request.source_user_id, source_user_id)
        vampytest.assert_eq(relationship_request.target_user_id, target_user_id)
        vampytest.assert_eq(relationship_request.relationship_type, relationship_type)
        vampytest.assert_eq(relationship_request.investment, investment)
        
        # Should not auto store in cache
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(relationship_request.entry_id, None), None)
        
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequest__repr():
    """
    Tests whether ``relationship_request.__repr__`` works as intended.
    """
    source_user_id = 202412260002
    target_user_id = 202412260003
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3499
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request.entry_id = entry_id
        
        output = repr(relationship_request)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(RelationshipRequest.__name__, output)
        vampytest.assert_in(f'investment = {investment!r}', output)
        vampytest.assert_in(f'source_user_id = {source_user_id!r}', output)
        vampytest.assert_in(
            f'relationship_type = {get_relationship_type_name(relationship_type)!s} ~ {relationship_type!r}',
            output,
        )
        vampytest.assert_in(f'target_user_id = {target_user_id!r}', output)
        vampytest.assert_in(f'entry_id = {entry_id!r}', output)
        
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequest__bool():
    """
    Tests whether ``RelationshipRequest.__bool__`` works as intended.
    
    Returns
    -------
    output : `bool`
    """
    source_user_id = 202412260004
    target_user_id = 202412260005
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        output = bool(relationship_request)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequest__get_saver():
    """
    Tests whether ``RelationshipRequest.get_saver`` works as intended.
    """
    source_user_id = 202412260006
    target_user_id = 202412260007
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        output = relationship_request.get_saver()
        vampytest.assert_instance(output, RelationshipRequestSaver)
        vampytest.assert_is(output.entry_proxy, relationship_request)
        vampytest.assert_is(relationship_request.saver, output)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequest__get_saver__caching():
    """
    Tests whether ``RelationshipRequest.get_saver`` works as intended.
    
    Case: caching.
    """
    source_user_id = 202412260008
    target_user_id = 202412260009
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        output_0 = relationship_request.get_saver()
        output_1 = relationship_request.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequest__from_entry():
    """
    Tests whether ``RelationshipRequest.from_entry`` works as intended.
    """
    source_user_id = 202412260010
    target_user_id = 202412260011
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3501
    
    try:
        entry = {
            'id': entry_id,
            'investment': investment,
            'relationship_type': relationship_type,
            'source_user_id': source_user_id,
            'target_user_id': target_user_id,
        }
        
        relationship_request = RelationshipRequest.from_entry(entry)
        _assert_fields_set(relationship_request)
        
        # Should auto store in cache
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(entry_id, None), relationship_request)
        
        vampytest.assert_eq(relationship_request.entry_id, entry_id)
        vampytest.assert_eq(relationship_request.investment, investment)
        vampytest.assert_eq(relationship_request.source_user_id, source_user_id)
        vampytest.assert_eq(relationship_request.relationship_type, relationship_type)
        vampytest.assert_eq(relationship_request.target_user_id, target_user_id)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequest__from_entry__cache():
    """
    Tests whether ``RelationshipRequest.from_entry`` works as intended.
    
    Case: Caching.
    """
    source_user_id = 202412260012
    target_user_id = 202412260013
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3502
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        relationship_request.entry_id = entry_id
        RELATIONSHIP_REQUEST_CACHE[entry_id] = relationship_request
        
        entry = {
            'investment': investment,
            'source_user_id': source_user_id,
            'relationship_type': relationship_type,
            'target_user_id': target_user_id,
            'id': entry_id,
        }
        
        output = RelationshipRequest.from_entry(entry)
        vampytest.assert_is(output, relationship_request)
        
        vampytest.assert_eq(relationship_request.entry_id, entry_id)
        vampytest.assert_eq(relationship_request.investment, investment)
        vampytest.assert_eq(relationship_request.source_user_id, source_user_id)
        vampytest.assert_eq(relationship_request.relationship_type, relationship_type)
        vampytest.assert_eq(relationship_request.target_user_id, target_user_id)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__RelationshipRequest__delete():
    """
    Tests whether ``RelationshipRequest.delete`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202412260014
    target_user_id = 202412260015
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3500
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        relationship_request.entry_id = entry_id
        RELATIONSHIP_REQUEST_CACHE[entry_id] = relationship_request
        RELATIONSHIP_REQUEST_CACHE_LISTING[source_user_id, True] = [relationship_request]
        RELATIONSHIP_REQUEST_CACHE_LISTING[target_user_id, False] = [relationship_request]
        
        vampytest.assert_is(relationship_request.saver, None)
        vampytest.assert_is_not(RELATIONSHIP_REQUEST_CACHE.get(entry_id, None), None)
        
        relationship_request.delete()
        
        vampytest.assert_is_not(relationship_request.saver, None)
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(entry_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(relationship_request.saver, None)
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(entry_id, None), None)
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE_LISTING.get((source_user_id, True), None), None)
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE_LISTING.get((target_user_id, False), None), None)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()
        RELATIONSHIP_REQUEST_CACHE_LISTING.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__RelationshipRequest__set__add_field():
    """
    Tests whether ``RelationshipRequest.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    source_user_id = 202412260016
    target_user_id = 202412260017
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3503
    
    new_investment = 2002
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        relationship_request.entry_id = entry_id
        vampytest.assert_is(relationship_request.saver, None)
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(entry_id, None), None)
        vampytest.assert_eq(relationship_request.investment, investment)
        
        relationship_request.set('investment', new_investment)
        
        vampytest.assert_eq(relationship_request.investment, new_investment)
        vampytest.assert_is_not(relationship_request.saver, None)
        vampytest.assert_eq(relationship_request.saver.modified_fields, {'investment': new_investment})
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(entry_id, None), relationship_request)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_eq(relationship_request.investment, new_investment)
        vampytest.assert_is(relationship_request.saver, None)
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(entry_id, None), relationship_request)
        
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__RelationshipRequest__set__save():
    """
    Tests whether ``RelationshipRequest.save`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202412260018
    target_user_id = 202412260019
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3504
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        relationship_request.entry_id = entry_id
        
        RELATIONSHIP_REQUEST_CACHE_LISTING[source_user_id, True] = [relationship_request]
        RELATIONSHIP_REQUEST_CACHE_LISTING[target_user_id, False] = None
        
        task = Task(get_event_loop(), relationship_request.save())
        
        await skip_ready_cycle()
        
        vampytest.assert_is_not(relationship_request.saver, None)
        
        task.apply_timeout(0.1)
        await task
        
        key = next(iter(RELATIONSHIP_REQUEST_CACHE.keys()), None)
        vampytest.assert_is_not(key, None)
        vampytest.assert_eq(relationship_request.entry_id, key)
        vampytest.assert_is(RELATIONSHIP_REQUEST_CACHE.get(key, None), relationship_request)
        vampytest.assert_eq(
            RELATIONSHIP_REQUEST_CACHE_LISTING.get((source_user_id, True), None),
            [relationship_request],
        )
        vampytest.assert_eq(
            RELATIONSHIP_REQUEST_CACHE_LISTING.get((target_user_id, False), None),
            [relationship_request],
        )
        
        vampytest.assert_is(relationship_request.saver, None)
        
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()
        RELATIONSHIP_REQUEST_CACHE_LISTING.clear()
