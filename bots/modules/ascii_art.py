from io import BytesIO
from math import ceil

from hata import Client
from hata.ext.slash import InteractionResponse, abort
import numpy
from PIL import Image, ImageOps


SLASH_CLIENT : Client

SCALE = '@%#*+=-:. '
SCALE_RATIO = (len(SCALE) - 1 ) / 255


def mush(image):
    width, height = image.size
    return image.resize((width, ceil(height * 0.5)))


async def get_ascii_art_of(client, url):
    async with client.http.get(url) as response:
        data = await response.read()
    
    image = mush(ImageOps.grayscale(Image.open(BytesIO(data))))
    array = numpy.around((numpy.array(image) * SCALE_RATIO)).astype(numpy.uint8)
    output_parts = []
    for line in array:
        for scale in line:
            output_parts.append(SCALE[scale])
        output_parts.append('\n')

    return ''.join(output_parts)


ASCII_COMMANDS = SLASH_CLIENT.interactions(
    None,
    is_global = True,
    name = 'ascii',
    description = 'Create ascii art!',
)


@ASCII_COMMANDS.interactions
async def avatar(
    client,
    event,
    user: ('user', 'Select a user') = None,
):
    """Create ascii art from your avatar"""
    if user is None:
        user = event.user
    
    avatar_url = user.avatar_url_for_as(event.guild_id, size = 80, ext = 'jpg')
    if avatar_url is None:
        if not user.avatar:
            abort('The user has no avatar')
        
        avatar_url = user.avatar_url_as(size = 80, ext = 'jpg')
    
    yield
    output = await get_ascii_art_of(client, avatar_url)
    yield InteractionResponse(file = ('out.txt', output))
