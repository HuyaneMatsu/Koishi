from base64 import b64encode as base_64_encode

import vampytest
from hata import Emoji, SoundboardSound, Sticker

from ..constants import (
    CHOICE_TYPE_IDENTIFIER_EMOJI, CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND, CHOICE_TYPE_IDENTIFIER_STICKER
)
from ..entity_packing import unpack_entity


def _iter_options():
    yield (
        '',
        None,
    )
    
    emoji_id = 202510300010
    emoji_guild_id = 202510300011
    emoji_animated = True
    emoji_name = 'nyan'
    
    yield (
        base_64_encode(b''.join([
            CHOICE_TYPE_IDENTIFIER_EMOJI.to_bytes(1, 'little'),
            emoji_guild_id.to_bytes(8, 'little'),
            emoji_id.to_bytes(8, 'little'),
            emoji_animated.to_bytes(1, 'little'),
            emoji_name.encode(),
        ])).decode(),
        Emoji.precreate(
            emoji_id,
            guild_id = emoji_guild_id,
            animated = emoji_animated,
            name = emoji_name,
        ),
    )
    
    sticker_id = 202510300012
    sticker_guild_id = 202510300013
    sticker_name = 'nyan'
    
    yield (
        base_64_encode(b''.join([
            CHOICE_TYPE_IDENTIFIER_STICKER.to_bytes(1, 'little'),
            sticker_guild_id.to_bytes(8, 'little'),
            sticker_id.to_bytes(8, 'little'),
            False.to_bytes(1, 'little'),
            sticker_name.encode(),
        ])).decode(),
        Sticker.precreate(
            sticker_id,
            guild_id = sticker_guild_id,
            name = sticker_name,
        ),
    )
    
    soundboard_sound_id = 202510300014
    soundboard_sound_guild_id = 202510300015
    soundboard_sound_name = 'nyan'
    
    yield (
        base_64_encode(b''.join([
            CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND.to_bytes(1, 'little'),
            soundboard_sound_guild_id.to_bytes(8, 'little'),
            soundboard_sound_id.to_bytes(8, 'little'),
            False.to_bytes(1, 'little'),
            soundboard_sound_name.encode(),
        ])).decode(),
        SoundboardSound.precreate(
            soundboard_sound_id,
            guild_id = soundboard_sound_guild_id,
            name = soundboard_sound_name,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__unpack_entity(entity):
    """
    Tests whether ``unpack_entity`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to unpack.
    
    Returns
    -------
    output : ``None | Emoji | Sticker | SoundboardSound``
    """
    output = unpack_entity(entity)
    vampytest.assert_instance(output, Emoji, Sticker, SoundboardSound, nullable = True)
    return output
