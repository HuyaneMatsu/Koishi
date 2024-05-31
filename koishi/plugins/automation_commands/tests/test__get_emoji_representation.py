import vampytest

from hata import BUILTIN_EMOJIS, Emoji

from ..constants import ENTITY_REPRESENTATION_DEFAULT
from ..representation_getters import get_emoji_representation


def _iter_options():
    yield None, [], ENTITY_REPRESENTATION_DEFAULT
    
    emoji_id = 202405300113
    emoji = Emoji.precreate(emoji_id, name = 'pudding')
    yield emoji, [emoji], emoji.as_emoji

    emoji = BUILTIN_EMOJIS['heart']
    yield emoji, [emoji], emoji.as_emoji


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_emoji_representation(emoji, extra):
    """
    Tests whether ``get_emoji_representation`` works as intended.
    
    Parameters
    ----------
    emoji : `None | Emoji`
        Value to get representation for.
    extra : `list<object>`
        Entities to keep in the cache.
    
    Returns
    -------
    output : `str`
    """
    output = get_emoji_representation(emoji)
    vampytest.assert_instance(output, str)
    return output
