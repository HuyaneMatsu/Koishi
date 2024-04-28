import vampytest
from hata import Channel, ChannelType, Guild

from ..embed_builder_reaction import _build_location_description


def test__build_location_description__no_guild():
    """
    Tests whether ``_build_location_description`` works as intended.
    
    Case: no guild.
    """
    channel_id = 202404280014
    channel_name = 'hey'
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, name = channel_name)
    
    output = _build_location_description(channel)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'Channel: {channel_name!s} ({channel_id!s})\n'
            f'Guild: null'
        ),
    )

def test__build_location_description__with_guild():
    """
    Tests whether ``_build_location_description`` works as intended.
    
    Case: no guild.
    """
    channel_id = 202404280015
    guild_id = 202404280016
    channel_name = 'hey'
    guild_name = 'mister'
    channel = Channel.precreate(
        channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = channel_name
    )
    guild = Guild.precreate(
        guild_id, name = guild_name,
    )
    
    output = _build_location_description(channel)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'Channel: {channel_name!s} ({channel_id!s})\n'
            f'Guild: {guild_name!s} ({guild_id!s})'
        ),
    )
