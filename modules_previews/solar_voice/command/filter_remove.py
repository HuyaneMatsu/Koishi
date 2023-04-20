__all__ = ('filter_remove_',)

from hata import Embed
from hata.ext.slash import P, abort

from ..autocomplete_filter import autocomplete_filter_name
from ..constants import EMBED_COLOR, FILTER_NAME_TO_FILTER_TYPE
from ..filtering import add_filter_field_to
from ..helpers import get_player_or_abort


async def filter_remove_(client, event,
    type_: P('str', 'The filter to remove', autocomplete=autocomplete_filter_name),
):
    """Removes the filter of the selected type"""
    player = get_player_or_abort(client, event)
    
    filter = player.remove_filter(FILTER_NAME_TO_FILTER_TYPE[type_])
    if filter is None:
        abort(f'The player has no: {type_} filter')
    
    await player.apply_filters()
    return add_filter_field_to(Embed('Filter removed', color = EMBED_COLOR), filter)
