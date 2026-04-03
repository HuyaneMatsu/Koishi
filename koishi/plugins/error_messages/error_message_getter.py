__all__ = ()

from random import choice

from hata import Color, Embed
from hata.ext.slash import InteractionResponse


IMAGES = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994155587833979/okuu-error-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994155075993661/okuu-error-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994154447110205/okuu-error-0002.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994153385824377/okuu-error-0003.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994157483655168/okuu-error-0004.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994156909170698/okuu-error-0005.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994156548329562/okuu-error-0006.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/1264994156070309929/okuu-error-0007.png',
)

COLOR = Color(0x8a0900)


def okuu_error_message_getter():
    """
    Returns a random error message.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return InteractionResponse(
        Embed('An error haz Okuued', color = COLOR).add_image(choice(IMAGES)).add_footer('By guuchama.'),
    )
