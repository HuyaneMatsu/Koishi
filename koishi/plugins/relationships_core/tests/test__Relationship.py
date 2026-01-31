from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import DATETIME_FORMAT_CODE

from ..relationship import Relationship
from ..relationship_types import RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, get_relationship_type_name_basic


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
    vampytest.assert_instance(relationship.modified_fields, dict, nullable = True)
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


def test__Relationship__repr():
    """
    Tests whether ``Relationship.__repr__`` works as intended.
    """
    source_user_id = 202501020002
    target_user_id = 202501020003
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    target_investment = 3000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    target_can_boost_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    
    entry_id = 3499
    
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
        f'relationship_type = {get_relationship_type_name_basic(relationship_type)!s} ~ {relationship_type!r}',
        output,
    )
    vampytest.assert_in(f'source_user_id = {source_user_id!r}', output)
    vampytest.assert_in(f'target_user_id = {target_user_id!r}', output)
    vampytest.assert_in(f'source_investment = {source_investment!r}', output)
    vampytest.assert_in(f'target_investment = {target_investment!r}', output)
    vampytest.assert_in(f'source_can_boost_at = {source_can_boost_at:{DATETIME_FORMAT_CODE}}', output)
    vampytest.assert_in(f'target_can_boost_at = {target_can_boost_at:{DATETIME_FORMAT_CODE}}', output)


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
    
    vampytest.assert_eq(relationship.entry_id, entry_id)
    vampytest.assert_eq(relationship.relationship_type, relationship_type)
    vampytest.assert_eq(relationship.source_user_id, source_user_id)
    vampytest.assert_eq(relationship.target_user_id, target_user_id)
    vampytest.assert_eq(relationship.source_investment, source_investment)
    vampytest.assert_eq(relationship.target_investment, target_investment)
    vampytest.assert_eq(relationship.source_can_boost_at, source_can_boost_at)
    vampytest.assert_eq(relationship.target_can_boost_at, target_can_boost_at)


def test__Relationship__set_relationship_type():
    """
    Tests whether ``Relationship.set_relationship_type`` works as intended.
    """
    source_user_id = 202601150002
    target_user_id = 202601150003
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    
    relationship = Relationship(
        source_user_id,
        target_user_id,
        relationship_type,
        source_investment,
        source_can_boost_at,
    )
    
    new_relationship_type = RELATIONSHIP_TYPE_MISTRESS
    
    relationship.set_relationship_type(new_relationship_type)
    vampytest.assert_eq(relationship.relationship_type, new_relationship_type)
    vampytest.assert_eq(relationship.modified_fields, {'relationship_type': new_relationship_type})


def test__Relationship__set_source_can_boost_at():
    """
    Tests whether ``Relationship.set_source_can_boost_at`` works as intended.
    """
    source_user_id = 202601150004
    target_user_id = 202601150005
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    
    relationship = Relationship(
        source_user_id,
        target_user_id,
        relationship_type,
        source_investment,
        source_can_boost_at,
    )
    
    new_source_can_boost_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    relationship.set_source_can_boost_at(new_source_can_boost_at)
    vampytest.assert_eq(relationship.source_can_boost_at, new_source_can_boost_at)
    vampytest.assert_eq(relationship.modified_fields, {'source_can_boost_at': new_source_can_boost_at})


def test__Relationship__set_source_investment():
    """
    Tests whether ``Relationship.set_source_investment`` works as intended.
    """
    source_user_id = 202601150006
    target_user_id = 202601150007
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    
    relationship = Relationship(
        source_user_id,
        target_user_id,
        relationship_type,
        source_investment,
        source_can_boost_at,
    )
    
    new_source_investment = 9999
    
    relationship.set_source_investment(new_source_investment)
    vampytest.assert_eq(relationship.source_investment, new_source_investment)
    vampytest.assert_eq(relationship.modified_fields, {'source_investment': new_source_investment})


def test__Relationship__set_target_can_boost_at():
    """
    Tests whether ``Relationship.set_target_can_boost_at`` works as intended.
    """
    source_user_id = 202601150008
    target_user_id = 202601150009
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    
    relationship = Relationship(
        source_user_id,
        target_user_id,
        relationship_type,
        source_investment,
        source_can_boost_at,
    )
    
    new_target_can_boost_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    relationship.set_target_can_boost_at(new_target_can_boost_at)
    vampytest.assert_eq(relationship.target_can_boost_at, new_target_can_boost_at)
    vampytest.assert_eq(relationship.modified_fields, {'target_can_boost_at': new_target_can_boost_at})


def test__Relationship__set_target_investment():
    """
    Tests whether ``Relationship.set_target_investment`` works as intended.
    """
    source_user_id = 202601150010
    target_user_id = 202601150011
    relationship_type = RELATIONSHIP_TYPE_MAMA
    source_investment = 2000
    source_can_boost_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    
    relationship = Relationship(
        source_user_id,
        target_user_id,
        relationship_type,
        source_investment,
        source_can_boost_at,
    )
    
    new_target_investment = 9999
    
    relationship.set_target_investment(new_target_investment)
    vampytest.assert_eq(relationship.target_investment, new_target_investment)
    vampytest.assert_eq(relationship.modified_fields, {'target_investment': new_target_investment})
