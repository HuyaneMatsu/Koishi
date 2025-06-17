import vampytest
from hata import Embed, EmbedImage, Message

from ..refresh import _should_image_refresh


def _iter_options():
    yield None, False
    yield Message(content = '0'), False
    yield Message(content = '01', embeds = [Embed()]), False
    yield Message(content = '012', embeds = [Embed(image = EmbedImage('https://orindance.party/'))]), True
    
    image = EmbedImage('https://orindance.party/')
    image.height = 420
    image.width = 420
    yield Message(content = '0123', embeds = [Embed(image = image)]), False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__should_image_refresh(message):
    """
    Tests whether ``_should_image_refresh`` works as intended.
    
    Parameters
    ----------
    message : ``None | Message``
        Message to test.
    
    Returns
    -------
    output : `bool`
    """
    output = _should_image_refresh(message)
    vampytest.assert_instance(output, bool)
    return output
