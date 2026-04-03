import vampytest

from ..relationship_request import RelationshipRequest
from ..relationship_types import RELATIONSHIP_TYPE_MAMA, get_relationship_type_name_basic


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
    vampytest.assert_instance(relationship_request.modified_fields, dict, nullable = True)
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


def test__RelationshipRequest__repr():
    """
    Tests whether ``relationship_request.__repr__`` works as intended.
    """
    source_user_id = 202412260002
    target_user_id = 202412260003
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3499
    
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
    vampytest.assert_in(f'entry_id = {entry_id!r}', output)
    vampytest.assert_in(f'investment = {investment!r}', output)
    vampytest.assert_in(f'source_user_id = {source_user_id!r}', output)
    vampytest.assert_in(
        f'relationship_type = {get_relationship_type_name_basic(relationship_type)!s} ~ {relationship_type!r}',
        output,
    )
    vampytest.assert_in(f'target_user_id = {target_user_id!r}', output)
    vampytest.assert_in(f'entry_id = {entry_id!r}', output)


def test__RelationshipRequest__from_entry():
    """
    Tests whether ``RelationshipRequest.from_entry`` works as intended.
    """
    source_user_id = 202412260010
    target_user_id = 202412260011
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 3501
    
    entry = {
        'id': entry_id,
        'investment': investment,
        'relationship_type': relationship_type,
        'source_user_id': source_user_id,
        'target_user_id': target_user_id,
    }
    
    relationship_request = RelationshipRequest.from_entry(entry)
    _assert_fields_set(relationship_request)
    
    vampytest.assert_eq(relationship_request.entry_id, entry_id)
    vampytest.assert_eq(relationship_request.investment, investment)
    vampytest.assert_eq(relationship_request.source_user_id, source_user_id)
    vampytest.assert_eq(relationship_request.relationship_type, relationship_type)
    vampytest.assert_eq(relationship_request.target_user_id, target_user_id)


def test__RelationshipRequest__set_investment():
    """
    Tests whether ``RelationshipRequest.set_investment`` works as intended.
    """
    source_user_id = 202601150006
    target_user_id = 202601150007
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    
    relationship = RelationshipRequest(
        source_user_id,
        target_user_id,
        relationship_type,
        investment,
    )
    
    new_investment = 9999
    
    relationship.set_investment(new_investment)
    vampytest.assert_eq(relationship.investment, new_investment)
    vampytest.assert_eq(relationship.modified_fields, {'investment': new_investment})

