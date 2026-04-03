from base64 import b64encode as base_64_encode

import vampytest
from hata import Emoji, SoundboardSound, Sticker

from ..constants import (
    CHOICE_TYPE_IDENTIFIER_EMOJI, CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND, CHOICE_TYPE_IDENTIFIER_STICKER
)
from ..entity_packing import pack_entity


def _iter_options():
    emoji_id = 202510300000
    emoji_guild_id = 202510300001
    emoji_animated = True
    emoji_name = 'nyan'
    
    yield (
        Emoji.precreate(
            emoji_id,
            guild_id = emoji_guild_id,
            animated = emoji_animated,
            name = emoji_name,
        ),
        base_64_encode(b''.join([
            CHOICE_TYPE_IDENTIFIER_EMOJI.to_bytes(1, 'little'),
            emoji_guild_id.to_bytes(8, 'little'),
            emoji_id.to_bytes(8, 'little'),
            emoji_animated.to_bytes(1, 'little'),
            emoji_name.encode(),
        ])).decode(),
    )
    
    sticker_id = 202510300002
    sticker_guild_id = 202510300003
    sticker_name = 'nyan'
    
    yield (
        Sticker.precreate(
            sticker_id,
            guild_id = sticker_guild_id,
            name = sticker_name,
        ),
        base_64_encode(b''.join([
            CHOICE_TYPE_IDENTIFIER_STICKER.to_bytes(1, 'little'),
            sticker_guild_id.to_bytes(8, 'little'),
            sticker_id.to_bytes(8, 'little'),
            False.to_bytes(1, 'little'),
            sticker_name.encode(),
        ])).decode(),
    )
    
    soundboard_sound_id = 202510300004
    soundboard_sound_guild_id = 202510300005
    soundboard_sound_name = 'nyan'
    
    yield (
        SoundboardSound.precreate(
            soundboard_sound_id,
            guild_id = soundboard_sound_guild_id,
            name = soundboard_sound_name,
        ),
        base_64_encode(b''.join([
            CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND.to_bytes(1, 'little'),
            soundboard_sound_guild_id.to_bytes(8, 'little'),
            soundboard_sound_id.to_bytes(8, 'little'),
            False.to_bytes(1, 'little'),
            soundboard_sound_name.encode(),
        ])).decode(),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__pack_entity(entity):
    """
    Tests whether ``pack_entity`` works as intended.
    
    Parameters
    ----------
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to pack.
    
    Returns
    -------
    output : `str`
    """
    output = pack_entity(entity)
    vampytest.assert_instance(output, str)
    return output
