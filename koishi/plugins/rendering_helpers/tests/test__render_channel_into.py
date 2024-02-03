import vampytest
from hata import Channel, ChannelType

from ..value_renderers import render_channel_into


def test__render_channel_into():
    """
    Tests whether ``render_channel_into`` works as intended.
    
    Case: No nick.
    """
    channel_id = 202302010000
    channel_type = ChannelType.guild_text
    name = 'koishi'
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = name)
    
    into = render_channel_into([], channel)
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'{name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})')
