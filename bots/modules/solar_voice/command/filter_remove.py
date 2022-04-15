from hata import Embed
from hata.ext.slash import SlasherApplicationCommand, abort, P
from hata.ext.extension_loader import import_extension


(
    EMBED_COLOR,
    FILTER_NAME_TO_FILTER_TYPE,
) = import_extension('..constants',
    'EMBED_COLOR',
    'FILTER_NAME_TO_FILTER_TYPE',
)
add_current_track_field, get_player_or_abort = import_extension(
    '..helpers', 'add_current_track_field', 'get_player_or_abort'
)
add_filter_field_to = import_extension('..filtering', 'add_filter_field_to')
autocomplete_filter_name = import_extension('..autocomplete_filter', 'autocomplete_filter_name')


COMMAND: SlasherApplicationCommand


@COMMAND.interactions
async def filter_remove(client, event,
    type_: P('str', 'The filter to remove', autocomplete=autocomplete_filter_name),
):
    """Removes the filter of the selected type"""
    player = get_player_or_abort(client, event)
    
    filter = player.remove_filter(FILTER_NAME_TO_FILTER_TYPE[type_])
    if filter is None:
        abort(f'The player has no: {type_} filter')
    
    await player.apply_filters()
    return add_filter_field_to(Embed('Filter removed', color=EMBED_COLOR), filter)
