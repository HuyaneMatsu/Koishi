import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import RELATIONSHIP_REQUEST_CACHE
from ..relationship_request import RelationshipRequest
from ..relationship_request_saver import RelationshipRequestSaver
from ..relationship_types import RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS


def _assert_fields_set(relationship_request_saver):
    """
    Tests whether every fields are set of the given relationship request saver.
    
    Parameters
    ----------
    relationship_request_saver : ``RelationshipRequestSaver``
        The instance to check.
    """
    vampytest.assert_instance(relationship_request_saver, RelationshipRequestSaver)
    vampytest.assert_instance(relationship_request_saver.entry_proxy, RelationshipRequest)
    vampytest.assert_instance(relationship_request_saver.ensured_for_deletion, bool)
    vampytest.assert_instance(relationship_request_saver.modified_fields, dict, nullable = True)
    vampytest.assert_instance(relationship_request_saver.run_task, Task, nullable = True)


def test__RelationshipRequestSaver__new():
    """
    Tests whether ``RelationshipRequestSaver.__new__`` works as intended.
    """
    source_user_id = 202412260020
    target_user_id = 202412260021
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        _assert_fields_set(relationship_request_saver)
        
        vampytest.assert_is(relationship_request_saver.entry_proxy, relationship_request)

    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__RelationshipRequestSaver__repr():
    """
    Tests whether ``RelationshipRequestSaver.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202412260022
    target_user_id = 202412260023
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    new_investment = 2002
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        ensured_for_deletion = True
        modified_fields = {'investment': new_investment}
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        relationship_request_saver.ensured_for_deletion = ensured_for_deletion
        relationship_request_saver.modified_fields = modified_fields
        relationship_request_saver.run_task = Task(get_event_loop(), relationship_request_saver.run())
        
        output = repr(relationship_request_saver)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(RelationshipRequestSaver.__name__, output)
        vampytest.assert_in(f'entry_proxy = {relationship_request!r}', output)
        vampytest.assert_in(f'ensured_for_deletion = {ensured_for_deletion!r}', output)
        vampytest.assert_in(f'modified_fields = {modified_fields!r}', output)
        vampytest.assert_in(f'running = {True!r}', output)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequestSaver__add_modification():
    """
    Tests whether ``RelationshipRequestSaver.add_modification`` works as intended.
    """
    source_user_id = 202412260024
    target_user_id = 202412260025
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    new_investment = 2002
    new_relationship_type = RELATIONSHIP_TYPE_MISTRESS
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        
        vampytest.assert_eq(
            relationship_request_saver.modified_fields,
            None,
        )
        
        relationship_request_saver.add_modification('investment', new_investment)
        
        vampytest.assert_eq(
            relationship_request_saver.modified_fields,
            {
                'investment': new_investment,
            }
        )
        
        relationship_request_saver.add_modification('relationship_type', new_relationship_type)
        
        vampytest.assert_eq(
            relationship_request_saver.modified_fields,
            {
                'investment': new_investment,
                'relationship_type': new_relationship_type,
            }
        )
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequestSaver__ensure_deletion():
    """
    Tests whether ``RelationshipRequestSaver.ensure_deletion`` works as intended.
    """
    source_user_id = 202412260026
    target_user_id = 202412260027
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        
        vampytest.assert_eq(relationship_request_saver.ensured_for_deletion, False)
        
        relationship_request_saver.ensure_deletion()
        
        vampytest.assert_eq(relationship_request_saver.ensured_for_deletion, True)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequestSaver__is_modified__not():
    """
    Tests whether ``RelationshipRequestSaver.is_modified`` works as intended.
    
    Case: not modified.
    """
    source_user_id = 202412260028
    target_user_id = 202412260029
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        
        output = relationship_request_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequestSaver__is_modified__delete():
    """
    Tests whether ``RelationshipRequestSaver.is_modified`` works as intended.
    
    Case: ensured for deletion.
    """
    source_user_id = 202412260030
    target_user_id = 202412260031
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        relationship_request_saver.ensure_deletion()
        
        output = relationship_request_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


def test__RelationshipRequestSaver__is_modified__field():
    """
    Tests whether ``RelationshipRequestSaver.is_modified`` works as intended.
    
    Case: field modified.
    """
    source_user_id = 202412260032
    target_user_id = 202412260033
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    new_investment = 2002
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        relationship_request_saver.add_modification('investment', new_investment)
        
        output = relationship_request_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__RelationshipRequestSaver__begin():
    """
    Tests whether ``RelationshipRequestSaver.begin`` works as intended.
    
    This function is a coroutine.
    """
    source_user_id = 202412260034
    target_user_id = 202412260035
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        relationship_request.saver = relationship_request_saver
        
        output = relationship_request_saver.begin()
        
        vampytest.assert_instance(output, Task)
        vampytest.assert_is(relationship_request_saver.run_task, output)
        vampytest.assert_is(relationship_request.saver, relationship_request_saver)
        
        # do save
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        # after save nothing should be set.
        vampytest.assert_is(relationship_request_saver.run_task, None)
        vampytest.assert_is(relationship_request.saver, None)
    
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def RelationshipRequestSaver__running():
    """
    Tests whether ``RelationshipRequestSaver.running`` works as intended.
    """
    source_user_id = 202412260036
    target_user_id = 202412260037
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    try:
        relationship_request = RelationshipRequest(
            source_user_id,
            target_user_id,
            relationship_type,
            investment,
        )
        
        relationship_request_saver = RelationshipRequestSaver(relationship_request)
        relationship_request.saver = relationship_request_saver
        
        output = relationship_request_saver.running
        vampytest.assert_eq(output, False)
        
        relationship_request_saver.begin()
        
        output = relationship_request_saver.running
        vampytest.assert_eq(output, True)
        
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()
