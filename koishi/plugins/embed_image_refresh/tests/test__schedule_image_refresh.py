import vampytest
from hata import Client, Embed, EmbedImage, Message

from ..refresh import _invoke_image_refresh, schedule_image_refresh


class MockEventLoop:
    __slots__ = ('call_after',)
    
    def __init__(self, call_after):
        self.call_after = call_after


def test__schedule_image_refresh__not_needed():
    """
    Tests whether ``schedule_image_refresh`` works as intended.
    
    Case: No need to refresh.
    """
    called = False
    
    def mock_call_after(delay, function, *parameters):
        nonlocal called
        
        called = True
    
    
    mocked = vampytest.mock_globals(schedule_image_refresh, KOKORO = MockEventLoop(mock_call_after))
    
    image = EmbedImage('https://orindance.party/')
    image.height = 420
    image.width = 420
    message = Message(embeds = [Embed(image = image)])
    
    
    client = Client(
        'token_20231209_0000',
        client_id = 202312090000,
    )

    try:
        mocked(client, message, None)
        
        vampytest.assert_false(called)
    finally:
        client._delete()
        client = None


def test__schedule_image_refresh__needed():
    """
    Tests whether ``schedule_image_refresh`` works as intended.
    
    Case: refresh needed.
    """
    called = False
    called_with_delay = 0.0
    called_with_function = None
    called_with_parameters = None
    
    def mock_call_after(delay, function, *parameters):
        nonlocal called
        nonlocal called_with_delay
        nonlocal called_with_function
        nonlocal called_with_parameters
        
        called = True
        called_with_delay = delay
        called_with_function = function
        called_with_parameters = parameters
    
    
    mocked = vampytest.mock_globals(schedule_image_refresh, KOKORO = MockEventLoop(mock_call_after))
    
    image = EmbedImage('https://orindance.party/')
    message = Message(embeds = [Embed(image = image)])
    
    
    client = Client(
        'token_20231209_0001',
        client_id = 202312090001,
    )

    try:
        mocked(client, message, None)
        
        vampytest.assert_true(called)
        vampytest.assert_instance(called_with_delay, float)
        vampytest.assert_true(called_with_delay > 0.0)
        vampytest.assert_is(called_with_function, _invoke_image_refresh)
        vampytest.assert_eq(called_with_parameters, (client, message, None))
    finally:
        client._delete()
        client = None
