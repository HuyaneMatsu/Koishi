import vampytest

from ..location import Location, location_create


def test__location_create():
    location_id = 9999
    name = 'Reisen'
    distance = 10000
    target_ids = (13335, 13323)
    level = 1
    
    location = location_create(
        location_id,
        name,
        distance,
        target_ids,
        level,
    )
    
    vampytest.assert_instance(location, Location)
    vampytest.assert_instance(location.distance, int)
    vampytest.assert_instance(location.id, int)
    vampytest.assert_instance(location.level, int)
    vampytest.assert_instance(location.name, str)
    vampytest.assert_instance(location.target_ids, tuple)
    
    vampytest.assert_eq(location.distance, distance)
    vampytest.assert_eq(location.id, location_id)
    vampytest.assert_eq(location.name, name)
    vampytest.assert_eq(location.target_ids, target_ids)
    vampytest.assert_eq(location.level, level)
