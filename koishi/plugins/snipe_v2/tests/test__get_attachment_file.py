import vampytest
from hata import Client, Emoji, SoundboardSound, Sticker, StickerFormat
from scarletio.streaming import ResourceStream

from ..responding_helpers import get_attachment_file


def _iter_options():
    client_id = 202511010000
    emoji_id = 202511010001
    
    emoji = Emoji.precreate(
        emoji_id,
    )
    
    yield (
        client_id,
        emoji,
        None,
    )
    
    client_id = 202511010002
    sticker_id = 202511010003
    
    sticker = Sticker.precreate(
        sticker_id,
        sticker_format = StickerFormat.apng,
    )
    
    yield (
        client_id,
        sticker,
        None,
    )
    
    client_id = 202511010004
    sticker_id = 202511010005
    
    sticker = Sticker.precreate(
        sticker_id,
        sticker_format = StickerFormat.lottie,
    )
    
    yield (
        client_id,
        sticker,
        sticker.url,
    )
    
    client_id = 202511010006
    soundboard_sound_id = 202511010007
    
    soundboard_sound = SoundboardSound.precreate(
        soundboard_sound_id,
    )
    
    yield (
        client_id,
        soundboard_sound,
        soundboard_sound.url,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_attachment_file(client_id, entity):
    """
    Tests whether ``get_attachment_file`` works as intended.
    
    Parameters
    ----------
    client_id : `int`
        Client identifier to use.
    
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity being shown.
    
    Returns
    -------
    url : `None | str`
    """
    client = Client(
        f'token_{client_id:x}',
        client_id = client_id
    )
    
    try:
        output = get_attachment_file(client, entity)
        vampytest.assert_instance(output, tuple, nullable = True)
        if output is None:
            return
        
        file_name, resource_stream = output
        
        vampytest.assert_instance(file_name, str)
        vampytest.assert_instance(resource_stream, ResourceStream)
        
        positional_parameters = resource_stream.positional_parameters
        vampytest.assert_eq(len(positional_parameters), 2)
        
        http_client, url = positional_parameters
        vampytest.assert_is(http_client, client.http)
        vampytest.assert_instance(url, str)
        return url
    
    finally:
        client._delete()
        client = None
