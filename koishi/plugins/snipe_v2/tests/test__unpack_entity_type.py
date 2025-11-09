import vampytest
from hata import Emoji, SoundboardSound, Sticker

from ..constants import (
    CHOICE_TYPE_IDENTIFIER_EMOJI, CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND, CHOICE_TYPE_IDENTIFIER_STICKER
)

from ..entity_packing import unpack_entity_type


def _iter_options():
    yield (
        '',
        None,
    )
    
    yield (
        format(CHOICE_TYPE_IDENTIFIER_EMOJI, 'x'),
        Emoji,
    )
    
    yield (
        format(CHOICE_TYPE_IDENTIFIER_STICKER, 'x'),
        Sticker,
    )
    
    yield (
        format(CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND, 'x'),
        SoundboardSound,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__unpack_entity_type(value):
    """
    Tests whether ``unpack_entity_type`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to unpack.
    
    Returns
    -------
    output : ``None | type<Emoji | Sticker | SoundboardSound>``
    """
    output = unpack_entity_type(value)
    vampytest.assert_in(output, (None, Emoji, Sticker, SoundboardSound))
    return output
