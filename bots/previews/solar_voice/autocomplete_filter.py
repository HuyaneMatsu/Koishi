__all__ = ()

from .constants import FILTER_TYPE_TO_FILTER_NAME


async def autocomplete_filter_name(client, event, value):
    player = client.solarlink.get_player(event.guild_id)
    if player is None:
        return
    
    filter_names = []
    
    for filter in player.iter_filters():
        try:
            filter_name = FILTER_TYPE_TO_FILTER_NAME[type(filter)]
        except KeyError:
            pass
        else:
            filter_names.append(filter_name)
    
    return filter_names
