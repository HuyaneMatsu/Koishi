import vampytest

from hata import Channel, ChannelType

from ..constants import ENTITY_REPRESENTATION_DEFAULT
from ..representation_getters import get_channel_id_representation


def _iter_options():
    channel_id = 0
    yield channel_id, [], ENTITY_REPRESENTATION_DEFAULT
    
    channel_id = 202405300110
    yield channel_id, [], ENTITY_REPRESENTATION_DEFAULT
    
    
    channel_id = 202405300111
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, name = 'pudding')
    yield channel_id, [channel], channel.mention



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_channel_id_representation(channel_id, extra):
    """
    Tests whether ``get_channel_id_representation`` works as intended.
    
    Parameters
    ----------
    channel_id : `int`
        Value to get representation for.
    extra : `list<object>`
        Entities to keep in the cache.
    
    Returns
    -------
    output : `str`
    """
    output = get_channel_id_representation(channel_id)
    vampytest.assert_instance(output, str)
    return output
