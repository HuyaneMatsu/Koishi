import vampytest

from ..reminding import request_interval


async def test__request_interval__interval_getter():
    """
    Tests whether ``request_interval`` works as intended.
    
    This function is a coroutine.
    
    Case: Using interval getter.
    """
    location = 'hell'
    interval_default = 60.5
    interval_custom = 60.0
    
    async def interval_getter(input_interval_default):
        nonlocal interval_custom
        return interval_custom
    
    output = await request_interval(location, interval_default, interval_getter)
    vampytest.assert_instance(output, float)
    vampytest.assert_eq(output, interval_custom)


async def test__request_interval__interval_default():
    """
    Tests whether ``request_interval`` works as intended.
    
    This function is a coroutine.
    
    Case: Using interval default.
    """
    location = 'hell'
    interval_default = 60.5
    interval_getter = None
    
    output = await request_interval(location, interval_default, interval_getter)
    vampytest.assert_instance(output, float)
    vampytest.assert_eq(output, interval_default)
