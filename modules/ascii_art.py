from io import BytesIO
from math import ceil

from hata import Client, ClientUserBase
from hata.ext.slash import InteractionResponse, abort
import numpy
from PIL import Image, ImageOps


SLASH_CLIENT : Client

STYLE_NAME_CHARACTER_SHORT = 'character short'
STYLE_CHARACTER_SHORT = ' .:-=+¤#%@'

STYLE_NAME_CHARACTER_EXTENDED = 'character extended'
STYLE_CHARACTER_EXTENDED = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao¤#MW&8%B@$'

STYLE_NAME_SHADE = 'shade'
STYLE_SHADE = ' ░▒▓█'

STYLE_NAMES = [
    STYLE_NAME_CHARACTER_SHORT,
    STYLE_NAME_CHARACTER_EXTENDED,
    STYLE_NAME_SHADE,
]

STYLE_NAME_TO_VALUE = {
    STYLE_NAME_CHARACTER_SHORT: (STYLE_CHARACTER_SHORT, STYLE_CHARACTER_SHORT[::-1]),
    STYLE_NAME_CHARACTER_EXTENDED: (STYLE_CHARACTER_EXTENDED, STYLE_CHARACTER_EXTENDED[::-1]),
    STYLE_NAME_SHADE: (STYLE_SHADE, STYLE_SHADE[::-1]),
}


SIZE_ALLOWED = [16, 20, 32, 40, 64, 80]
SIZE_DEFAULT = 80


ANNOTATION_STYLE = (STYLE_NAMES, 'Monochrome to character mapping.', 'style')
ANNOTATION_SIZE = (SIZE_ALLOWED, 'The preferred size of the image.')
ANNOTATION_INVERT = (bool, 'Whether the style should be inverted.')


def mush(image):
    """
    Mushes the image, halves it's height.
    
    Parameters
    ----------
    image : `numpy.ndarray`
        Image array.
    
    Returns
    -------
    image : `numpy.ndarray`
    """
    width, height = image.size
    return image.resize((width, ceil(height * 0.5)))


async def get_ascii_art_of(client, image_url, scale):
    """
    Gets the ascii art for the given url.
    
    This function is a coroutine
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    image_url : `str`
        The url to get.
    scale : `str`
        Ascii scaling to use to map a character to a monochrome value.
    
    Returns
    -------
    output : `str`
        The built image.
    """
    async with client.http.get(image_url) as response:
        if response.status != 200:
            return abort(
                f'Get asset response status is not 200 (OK), got: {response.status!r}.\n'
                f'Please try again later.'
            )
        
        data = await response.read()
    
    scale_ratio = (len(scale) - 1 ) / 255
    image = mush(ImageOps.grayscale(Image.open(BytesIO(data))))
    array = numpy.around((numpy.array(image) * scale_ratio)).astype(numpy.uint8)
    output_parts = []
    for line in array:
        for scale_index in line:
            output_parts.append(scale[scale_index])
        output_parts.append('\n')

    return ''.join(output_parts)


ASCII_COMMANDS = SLASH_CLIENT.interactions(
    None,
    is_global = True,
    name = 'ascii',
    description = 'Create ascii art!',
)


async def output_ascii_art(client, image_url, style_name, invert):
    """
    Converts the given image url to an ascii art and yields an interaction response with it as file attached.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    image_url : `str`
        The target image's url.
    style : `str`
        The monochrome to character mapping style's name.
    invert : `bool`
        Whether to use an inverted style.
    
    Yields
    ------
    response : `None`, ``InteractionResponse``
    """
    yield
    output = await get_ascii_art_of(client, image_url, STYLE_NAME_TO_VALUE[style_name][invert])
    yield InteractionResponse(file = ('out.txt', output))


@ASCII_COMMANDS.interactions
async def avatar(
    client,
    event,
    user: (ClientUserBase, 'Select a user.') = None,
    style_name: ANNOTATION_STYLE = STYLE_NAME_CHARACTER_SHORT,
    size: ANNOTATION_SIZE = SIZE_DEFAULT,
    invert: ANNOTATION_INVERT = False,
):
    """
    Create ascii art from your or a select user's avatar.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user : `None`, ``ClientUserBase`` = `None`, Optional
        The defined user to get the avatar of.
    style_name : `str` = `default`, Optional
        The monochrome to character mapping style's name.
    size : `int` = `default`, Optional
        The size of the image to process.
    
    Returns
    -------
    responder : `CoroutineGenerator`
    """
    if user is None:
        user = event.user
    
    avatar_url = user.avatar_url_for_as(event.guild_id, size = size, ext = 'jpg')
    if avatar_url is None:
        if not user.avatar:
            abort('The user has no avatar.')
        
        avatar_url = user.avatar_url_as(size = 80, ext = 'jpg')
    
    return output_ascii_art(client, avatar_url, style_name, invert)


@ASCII_COMMANDS.interactions
async def guild_icon(
    client,
    event,
    style_name: ANNOTATION_STYLE = STYLE_NAME_CHARACTER_SHORT,
    size: ANNOTATION_SIZE = SIZE_DEFAULT,
    invert: ANNOTATION_INVERT = False,
):
    """
    Create ascii art from the guild's icon.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    style_name : `str` = `default`, Optional
        The monochrome to character mapping style's name.
    size : `int` = `default`, Optional
        The size of the image to process.
    
    Returns
    -------
    responder : `CoroutineGenerator`
    """
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    icon_url = guild.icon_url_as(size = size, ext = 'jpg')
    if icon_url is None:
        abort('The guild has no icon.')
    
    return output_ascii_art(client, icon_url, style_name, invert)
