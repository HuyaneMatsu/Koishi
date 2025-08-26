import vampytest

from ..location import Location


def _assert_fields_set(location):
    """
    Asserts whether every fields are set of the given location.
    
    Parameters
    ----------
    location : ``Location``
    """
    vampytest.assert_instance(location, Location)
    vampytest.assert_instance(location.distance, int)
    vampytest.assert_instance(location.id, int)
    vampytest.assert_instance(location.name, str)
    vampytest.assert_instance(location.target_ids, tuple)


def test__Location__new():
    """
    Tests whether ``Location.__new__`` works as intended.
    """
    location_id = 9999
    name = 'Reisen'
    distance = 10000
    target_ids = (13335, 13323)
    
    location = Location(
        location_id,
        name,
        distance,
        target_ids,
    )
    
    _assert_fields_set(location)
    
    vampytest.assert_eq(location.distance, distance)
    vampytest.assert_eq(location.id, location_id)
    vampytest.assert_eq(location.name, name)
    vampytest.assert_eq(location.target_ids, target_ids)


def test__Location__repr():
    """
    Tests whether ``Location.__new__`` works as intended.
    """
    location_id = 9999
    name = 'Reisen'
    distance = 10000
    target_ids = (13335, 13323)
    
    location = Location(
        location_id,
        name,
        distance,
        target_ids,
    )
    
    output = repr(location)
    vampytest.assert_instance(output, str)
