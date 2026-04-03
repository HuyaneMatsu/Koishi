import vampytest
from hata import Channel, ChannelType

from ..field_renderers import render_channel_field_into


def _iter_options():
    channel_id = 202302010002
    channel_type = ChannelType.guild_text
    name = 'koishi'
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = name)
    
    yield False, None, False, 'Channel', ('Channel: *none*', True)
    yield True, None, False, 'Channel', ('\nChannel: *none*', True)
    
    yield (
        False, channel, False, 'Channel',
        (f'Channel: {name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})', True),
    )
    yield (
        True, channel, False, 'Channel',
        (f'\nChannel: {name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})', True),
    )
    yield False, None, True, 'Channel', ('', False)
    yield True, None, True, 'Channel', ('', True)
    yield (
        False, channel, True, 'Channel',
        (f'Channel: {name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})', True),
    )
    yield (
        True, channel, True, 'Channel',
        (f'\nChannel: {name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})', True),
    )
    
    # title
    yield (
        False, channel, True, 'Mister',
        (f'Mister: {name!s} [*{channel_type.name!s} ~ {channel_type.value!s}*] ({channel_id!s})', True),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_channel_field_into(field_added, channel, optional, title):
    """
    Tests whether ``render_channel_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether a field was already added.
    
    channel : `None | Channel`
        The channel to render.
    
    title : `str`
        The title to use.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_channel_field_into(
        [], field_added, channel, optional = optional, title = title
    ) 
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into), field_added
