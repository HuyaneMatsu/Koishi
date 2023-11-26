from io import BytesIO
from math import ceil, floor

from hata import ClientUserBase, Color, create_ansi_format_code, AnsiForegroundColor, AnsiTextDecoration
from hata.ext.slash import InteractionResponse, abort
from numpy import array as Array, around, uint8 as u8
from PIL import Image, ImageOps

from ..bots import FEATURE_CLIENTS


STYLE_NAME_CHARACTER_SHORT = 'character short'
STYLE_CHARACTER_SHORT = ' .:-=oX8@'

STYLE_NAME_CHARACTER_EXTENDED = 'character extended'
STYLE_CHARACTER_EXTENDED = ' .\'`^",:Il!i><~+_-?}{1)(|\\/tfjrxnuvczXYUJCLQ0OZ#MW&8%B@$'

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

COLOR_CODE_NONE = create_ansi_format_code(text_decoration = AnsiTextDecoration.none)

COLOR_CODE_RED = create_ansi_format_code(foreground_color = AnsiForegroundColor.red)
COLOR_CODE_ORANGE = create_ansi_format_code(foreground_color = AnsiForegroundColor.orange)
COLOR_CODE_GREEN = create_ansi_format_code(foreground_color = AnsiForegroundColor.green)
COLOR_CODE_BLUE = create_ansi_format_code(foreground_color = AnsiForegroundColor.blue)
COLOR_CODE_TEAL = create_ansi_format_code(foreground_color = AnsiForegroundColor.teal)
COLOR_CODE_PINK = create_ansi_format_code(foreground_color = AnsiForegroundColor.pink)


COLOR_CODES = (
    COLOR_CODE_RED,
    COLOR_CODE_ORANGE,
    COLOR_CODE_GREEN,
    COLOR_CODE_BLUE,
    COLOR_CODE_TEAL,
    COLOR_CODE_PINK,
    COLOR_CODE_NONE,
)


SIZE_ALLOWED = [16, 20, 32, 40, 64, 80]
SIZE_DEFAULT = 80


ANNOTATION_STYLE = (STYLE_NAMES, 'Monochrome to character mapping.', 'style')
ANNOTATION_SIZE = (SIZE_ALLOWED, 'The preferred size of the image.')
ANNOTATION_INVERT = (bool, 'Whether the style should be inverted.')
ANNOTATION_COLORED = (bool, 'Whether should use ansi color codes should be used.')


def mush(image):
    """
    Mushes the image, halves it's height.
    
    Parameters
    ----------
    image : `PIL.PngImagePlugin.PngImageFile`
        Image array.
    
    Returns
    -------
    image : `PIL.PngImagePlugin.PngImageFile`
    """
    width, height = image.size
    return image.resize((width, ceil(height * 0.5)))


def create_grayscale(image, scale):
    """
    Creates a grayscale representation of the image.
    
    Parameters
    ----------
    image : `PIL.PngImagePlugin.PngImageFile`
        The image to process.
    
    Returns
    -------
    output : `str`
    """
    image = mush(ImageOps.grayscale(image))
    
    scale_ratio = (len(scale) - 1 ) / 255
    array = around((Array(image) * scale_ratio)).astype(u8)
    
    output_parts = []
    for line in array:
        for scale_index in line:
            output_parts.append(scale[scale_index])
        output_parts.append('\n')

    return ''.join(output_parts)


def create_colored(image, scale):
    """
    Creates a colored representation of the image.
    
    Parameters
    ----------
    image : `PIL.PngImagePlugin.PngImageFile`
        The image to process.
    
    Returns
    -------
    output : `str`
    """
    image = mush(image).convert('RGB')
    
    scale_ratio = len(scale) - 1
    width, height = image.size
    
    output_parts = []
    pixels = image.load()
    
    output_parts.append(COLOR_CODE_NONE)
    last_color_index = 6
    
    for y in range(height):
        for x in range(width):
            hue, saturation, lightness = Color.from_rgb_tuple(pixels[x, y]).as_hsl_float_tuple
            
            scale_index = round(lightness * scale_ratio)
            
            if scale_index:
                if saturation <= 0.20:
                    color_index = 6
                else:
                    color_index = floor((hue + (1 / 12) % 1.0) * 6)
                
                if color_index != last_color_index:
                    last_color_index = color_index
                    output_parts.append(COLOR_CODES[color_index])
            
            output_parts.append(scale[scale_index])
        
        output_parts.append('\n')

    return ''.join(output_parts)


async def get_ascii_art_of(client, image_url, scale, colored):
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
    colored : `bool`
        Whether the output should use color ansi color codes.
    
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
    
    return (create_colored if colored else create_grayscale)(Image.open(BytesIO(data)), scale)


ASCII_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    is_global = True,
    name = 'ascii',
    description = 'Create ascii art!',
)


async def output_ascii_art(client, image_url, style_name, invert, colored):
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
    output = await get_ascii_art_of(client, image_url, STYLE_NAME_TO_VALUE[style_name][invert], colored)
    yield InteractionResponse(file = ('out.ansi' if colored else 'out.txt', output))


@ASCII_COMMANDS.interactions
async def avatar(
    client,
    event,
    user : (ClientUserBase, 'Select a user.') = None,
    style_name : ANNOTATION_STYLE = STYLE_NAME_CHARACTER_SHORT,
    size : ANNOTATION_SIZE = SIZE_DEFAULT,
    invert : ANNOTATION_INVERT = False,
    colored : ANNOTATION_COLORED = False,
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
    colored : `bool` = `False`, Optional
        Whether the output should use color ansi color codes.
    
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
        
        avatar_url = user.avatar_url_as(size = size, ext = 'jpg')
    
    return output_ascii_art(client, avatar_url, style_name, invert, colored)


@ASCII_COMMANDS.interactions
async def guild_icon(
    client,
    event,
    style_name : ANNOTATION_STYLE = STYLE_NAME_CHARACTER_SHORT,
    size : ANNOTATION_SIZE = SIZE_DEFAULT,
    invert : ANNOTATION_INVERT = False,
    colored : ANNOTATION_COLORED = False,
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
    colored : `bool` = `False`, Optional
        Whether the output should use color ansi color codes.
    
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
    
    return output_ascii_art(client, icon_url, style_name, invert, colored)
