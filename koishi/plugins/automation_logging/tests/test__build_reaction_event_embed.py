from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    Channel, ChannelType, Embed, Emoji, Guild, GuildProfile, Message, ReactionAddEvent, ReactionType, User
)

from ..constants import COLOR_ADD
from ..embed_builder_reaction import build_reaction_event_embed


class DateTimeMock(DateTime):
    __slots__ = ()
    
    
    @classmethod
    def now(cls, time_zone):
        return DateTime(2016, 5, 14, tzinfo = time_zone)
    
    
    def __instancecheck__(cls, instance):
        return isinstance(instance, DateTime)


def is_instance_mock(instance, accepted_type):
    if isinstance(instance, DateTime) and (accepted_type is DateTimeMock):
        return True
    
    return isinstance(instance, accepted_type)


def test__build_reaction_event_embed():
    """
    Tests whether ``build_reaction_event_embed`` works as intended.
    """
    emoji_id = 202404280020
    emoji_name = 'sister'
    message_id = 202404280021
    user_id = 202404280024
    reaction_type = ReactionType.burst
    channel_id = 202404280022
    guild_id = 202404280023
    channel_name = 'hey'
    guild_name = 'mister'
    
    emoji = Emoji.precreate(emoji_id, name = emoji_name)
    message = Message.precreate(message_id, channel_id = channel_id, guild_id = guild_id)
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(joined_at = DateTimeMock(2016, 5, 13, tzinfo = TimeZone.utc))
    event = ReactionAddEvent(message, emoji, user, reaction_type = reaction_type)
    channel = Channel.precreate(
        channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = channel_name
    )
    guild = Guild.precreate(
        guild_id, name = guild_name,
    )
    
    
    mocked = vampytest.mock_globals(
        build_reaction_event_embed,
        7,
        DateTime = DateTimeMock,
        isinstance = is_instance_mock,
    )
    
    output = mocked(event)
    
    vampytest.assert_instance(output, Embed)
    vampytest.assert_eq(
        output,
        Embed(
            user.full_name,
            (
                f'Created: 2015-01-01 00:00:48 [*1 year, 4 months, 12 days ago*]\n'
                f'Profile: <@{user_id!s}>\n'
                f'ID: {user_id!s}\n'
                '\n'
                'Joined: 2016-05-13 00:00:00 [*1 day ago*]\n'
                'Roles: *none*'
            ),
            color = COLOR_ADD,
        ).add_author(
            'Reaction added',
        ).add_field(
            'Location',
            (
                f'Channel: {channel_name!s} ({channel_id!s})\n'
                f'Guild: {guild_name!s} ({guild_id!s})'
            ),
        ).add_field(
            'Reaction',
            (
                f'Type: {reaction_type.name!s} ~ {reaction_type.value!r}\n'
                f'Emoji: {emoji_name!s} ({emoji_id!s})'
            ),
        ).add_thumbnail(
            user.avatar_url,
        ).add_footer(
            '2016-05-14 00:00:00',
        ),
    )
