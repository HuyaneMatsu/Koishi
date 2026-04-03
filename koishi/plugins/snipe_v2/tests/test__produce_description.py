from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import BUILTIN_EMOJIS, Emoji, Guild, Role, SoundboardSound, Sticker, StickerFormat, StickerType, User

from ..content_building import produce_description


class DateTimeMock(DateTime):
    current_date_time = None
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    @classmethod
    def now(cls, time_zone):
        value = cls.current_date_time
        if value is None:
            value = DateTime.now(time_zone)
        return value


def is_instance_mock(instance, accepted_type):
    if isinstance(instance, DateTime) and (accepted_type is DateTimeMock):
        return True
    
    return isinstance(instance, accepted_type)


def _iter_options():
    current_time = DateTime(2015, 1, 1, tzinfo = TimeZone.utc)
    
    emoji_id = 202510300020
    emoji_guild_id = 202510300021
    emoji_user_id = 20251030022
    emoji_animated = True
    emoji_name = 'nyan'
    
    role_id_0 = 20251030023
    role_id_1 = 20251030024
    
    guild_name = 'orin'
    user_name = 'okuu'
    
    guild = Guild.precreate(
        emoji_guild_id,
        name = guild_name,
    )
    
    user = User.precreate(
        emoji_user_id,
        name = user_name,
    )
    
    role_0 = Role.precreate(
        role_id_0,
        guild_id = emoji_guild_id,
    )
    
    role_1 = Role.precreate(
        role_id_1,
        guild_id = emoji_guild_id,
    )
    
    emoji = Emoji.precreate(
        emoji_id,
        animated = emoji_animated,
        guild_id = emoji_guild_id,
        role_ids = [role_id_0, role_id_1],
        name = emoji_name,
        user = user,
    )
    
    yield (
        emoji,
        0,
        0,
        current_time,
        [
            guild,
            user,
            role_0,
            role_1,
        ],
        (
            f'Name: {emoji_name!s}\n'
            f'Identifier: {emoji_id!s}'
        ),
    )
    
    yield (
        emoji,
        emoji_guild_id,
        1,
        current_time,
        [
            guild,
            user,
            role_0,
            role_1,
        ],
        (
            f'Name: {emoji_name!s}\n'
            f'Identifier: {emoji_id!s}\n'
            f'Animated: true\n'
            f'Available: true\n'
            f'Managed: false\n'
            f'Created at: 2015-01-01 00:00:48 | 48 seconds ago\n'
            f'Creator: {user_name!s} | {emoji_user_id!s}\n'
            f'Guild: {guild_name!s} | {emoji_guild_id}\n'
            f'Roles: <@&{role_id_0!s}>, <@&{role_id_1!s}>'
        ),
    )
    
    sticker_id = 202510300030
    sticker_guild_id = 202510300031
    sticker_user_id = 20251030032 
    sticker_name = 'nyan'
    
    sticker_tag_0 = 'shrimp'
    sticker_tag_1 = 'fry'
    
    sticker_format = StickerFormat.apng
    sticker_type = StickerType.guild
    
    guild_name = 'orin'
    user_name = 'okuu'
    
    guild = Guild.precreate(
        sticker_guild_id,
        name = guild_name,
    )
    
    user = User.precreate(
        sticker_user_id,
        name = user_name,
    )
    
    sticker = Sticker.precreate(
        sticker_id,
        guild_id = sticker_guild_id,
        name = sticker_name,
        sticker_format = sticker_format,
        sticker_type = sticker_type,
        tags = [
            sticker_tag_0,
            sticker_tag_1,
        ],
        user = user,
    )
    
    yield (
        sticker,
        0,
        0,
        current_time,
        [
            guild,
            user,
        ],
        (
            f'Name: {sticker_name!s}\n'
            f'Identifier: {sticker_id!s}'
        ),
    )
    
    yield (
        sticker,
        0,
        1,
        current_time,
        [
            guild,
            user,
        ],
        (
            f'Name: {sticker_name!s}\n'
            f'Identifier: {sticker_id!s}\n'
            f'Animated: true\n'
            f'Available: true\n'
            f'Created at: 2015-01-01 00:00:48 | 48 seconds ago\n'
            f'Description: *none*\n'
            f'Type: {sticker_type.name!s}\n'
            f'Format: {sticker_format.name!s}\n'
            f'Tags: {sticker_tag_1!s}, {sticker_tag_0!s}\n'
            f'Creator: {user_name!s} | {sticker_user_id!s}\n'
            f'Guild: {guild_name!s} | {sticker_guild_id}'
        ),
    )
    
    
    soundboard_sound_id = 202510300040
    soundboard_sound_guild_id = 202510300041
    soundboard_sound_user_id = 20251030052
    soundboard_sound_name = 'nyan'
    soundboard_sound_emoji = BUILTIN_EMOJIS['heart']
    soundboard_sound_volume = 0.5
    
    guild = Guild.precreate(
        soundboard_sound_guild_id,
        name = guild_name,
    )
    
    user = User.precreate(
        soundboard_sound_user_id,
        name = user_name,
    )
    
    soundboard_sound = SoundboardSound.precreate(
        soundboard_sound_id,
        guild_id = soundboard_sound_guild_id,
        emoji = soundboard_sound_emoji,
        name = soundboard_sound_name,
        user = user,
        volume = soundboard_sound_volume,
    )
    
    yield (
        soundboard_sound,
        0,
        0,
        current_time,
        [
            guild,
            user,
        ],
        (
            f'Name: {soundboard_sound_name!s}\n'
            f'Identifier: {soundboard_sound_id!s}'
        ),
    )
    
    yield (
        soundboard_sound,
        0,
        1,
        current_time,
        [
            guild,
            user,
        ],
        (
            f'Name: {soundboard_sound_name!s}\n'
            f'Identifier: {soundboard_sound_id!s}\n'
            f'Created at: 2015-01-01 00:00:48 | 48 seconds ago\n'
            f'Volume: {soundboard_sound_volume:.02f}\n'
            f'Emoji: {soundboard_sound_emoji.name!s}\n'
            f'Type: custom\n'
            f'Creator: {user_name!s} | {soundboard_sound_user_id!s}\n'
            f'Guild: {guild_name!s} | {soundboard_sound_guild_id}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_description(entity, guild_id, produce_long, current_date_time, entity_cache):
    """
    Tests whether ``produce_description`` works as intended.
    
    Parameters
    ----------
    entity : ``Emoji | Sticker | SoundboardSound``
        Entity to produce description of.
    
    guild_id : `int`
        The local guild's identifier.
    
    produce_long : `int`
        Whether to produce long description.
    
    current_date_time : `DateTime`
        Current date to use.
    
    entity_cache : `list<object>`
        Entities to keep in cache.
    
    Returns
    ------
    output : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        produce_description,
        4,
        DateTime = DateTimeMock,
        isinstance = is_instance_mock,
    )
    output = [*mocked(entity, guild_id, produce_long)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
