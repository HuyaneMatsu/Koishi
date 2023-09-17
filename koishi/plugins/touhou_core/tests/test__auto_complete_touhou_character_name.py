import vampytest

from ..auto_completion import auto_complete_touhou_character_name


def _iter_options():
    yield (
        None,
        [
            'Komeiji Koishi',
            'Kirisame Marisa',
            'Hakurei Reimu',
            'Scarlet Flandre',
            'Izayoi Sakuya',
            'Scarlet Remilia',
            'Fujiwara no Mokou',
            'Komeiji Satori',
            'Saigyouji Yuyuko',
            'Shameimaru Aya',
            'Margatroid Alice',
            'Kochiya Sanae',
            'Reisen Udongein Inaba',
            'Hinanawi Tenshi',
            'Yakumo Yukari',
            'Hata no Kokoro',
            'Chiruno',
            'Patchouli Knowledge',
            'Tatara Kogasa',
            'Rumia',
            'Moriya Suwako',
            'Shiki Eiki Yamaxanadu',
            'Kazami Yuuka',
            'Hong Meiling',
            'Toyosatomimi no Miko',
        ],
    )
    
    yield (
        'y',
        [
            'yuugi',
            'yuuka',
            'yachie',
            'youmu',
            'yamame kurodani',
            'yoshika',
            'yuyuko',
            'yuuma toutetsu',
            'yorihime',
            'yagokoro eirin',
            'yakumo ran',
            'yakumo yukari',
            'yamashiro takane',
            'yasaka kanako',
            'yatadera narumi',
            'yomotsu hisami',
            'yorigami joon',
            'yorigami shion',
        ],
    )
    
    yield (
        'aya',
        [
            'aya',
            'sakuya',
            'kaguya',
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__auto_complete_touhou_character_name(value):
    """
    Tests whether ``auto_complete_touhou_character_name`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    value : `None | str`
        The value to autocomplete.
    
    Returns
    -------
    output : `list<str>`
    """
    return await auto_complete_touhou_character_name(value)
