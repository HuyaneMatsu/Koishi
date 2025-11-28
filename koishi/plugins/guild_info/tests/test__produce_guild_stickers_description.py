import vampytest
from hata import Guild, Sticker, StickerFormat

from ..content_building import produce_guild_stickers_description


def _iter_options():
    guild_id = 202511210020
    guild = Guild.precreate(
        guild_id,
    )
    
    yield (
        guild,
        False,
        (
            ''
        ),
    )
    
    
    guild_id = 202511210023
    sticker_id_0 = 202511210024
    sticker_id_1 = 202511210025
    sticker_id_2 = 202511210026
    sticker_id_3 = 202511210027
    
    guild = Guild.precreate(
        guild_id,
        stickers = [
            Sticker.precreate(sticker_id_0, sticker_format = StickerFormat.png),
            Sticker.precreate(sticker_id_1, sticker_format = StickerFormat.png),
            Sticker.precreate(sticker_id_2, sticker_format = StickerFormat.gif),
            Sticker.precreate(sticker_id_3, sticker_format = StickerFormat.lottie),
        ]
    )
    
    yield (
        guild,
        False,
        (
            '## Stickers\n'
            '**Total: 4** [1 free]\n'
            '**Static stickers: 2**\n'
            '**Animated stickers: 1**\n'
            '**Lottie stickers: 1**'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_guild_stickers_description(guild, even_if_empty):
    """
    Tests whether ``produce_guild_stickers_description`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_guild_stickers_description(guild, even_if_empty)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
