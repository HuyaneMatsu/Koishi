import vampytest
from scarletio import skip_ready_cycle
from hata import Client, Embed, EmbedImage, Message

from ..refresh import _invoke_image_refresh, _invoke_image_refresh, _invoke_image_refresh


async def test__invoke_image_refresh__not_needed():
    """
    Tests whether ``_invoke_image_refresh`` works as intended.
    
    Case: No need to refresh.
    
    This function is a coroutine.
    """
    called = False
    
    async def mock_image_refresh(client, message, interaction_event, retry):
        nonlocal called
        vampytest.assert_eq(retry, 1)
        called = True
    
    
    mocked = vampytest.mock_globals(_invoke_image_refresh, _image_refresh = mock_image_refresh)
    
    image = EmbedImage('https://orindance.party/')
    image.height = 420
    image.width = 420
    message = Message(embeds = [Embed(image = image)])
    
    client = Client(
        'token_20231209_0002',
        client_id = 202312090002,
    )

    try:
        mocked(client, message, None)
        
        await skip_ready_cycle()
        
        vampytest.assert_false(called)
    finally:
        client._delete()
        client = None


async def test__invoke_image_refresh__needed():
    """
    Tests whether ``_invoke_image_refresh`` works as intended.
    
    Case: refresh needed.
    
    This function is a coroutine.
    """
    called = False
    called_with_client = None
    called_with_message = None
    called_with_interaction_event = None
    
    
    async def mock_image_refresh(client, message, interaction_event, retry):
        nonlocal called
        nonlocal called_with_client
        nonlocal called_with_message
        nonlocal called_with_interaction_event
        
        vampytest.assert_eq(retry, 1)
        
        called = True
        called_with_client = client
        called_with_message = message
        called_with_interaction_event = interaction_event
    
    
    mocked = vampytest.mock_globals(_invoke_image_refresh, _image_refresh = mock_image_refresh)
    
    image = EmbedImage('https://orindance.party/')
    message = Message(embeds = [Embed(image = image)])
    
    
    client = Client(
        'token_20231209_0003',
        client_id = 202312090003,
    )

    try:
        mocked(client, message, None)
        
        await skip_ready_cycle()
        
        vampytest.assert_true(called)
        vampytest.assert_is(called_with_client, client)
        vampytest.assert_is(called_with_message, message)
        vampytest.assert_is(called_with_interaction_event, None)
    finally:
        client._delete()
        client = None
