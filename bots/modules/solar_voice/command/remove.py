from hata.ext.slash import SlasherApplicationCommand, P
from hata.ext.extension_loader import import_extension


create_added_music_embed, get_player_or_abort, create_track_short_description = import_extension(
    '..helpers', 'create_added_music_embed', 'get_player_or_abort', 'create_track_short_description'
)
generate_track_autocomplete_form, autocomplete_track_name = import_extension(
    '..autocomplete_track', 'generate_track_autocomplete_form', 'autocomplete_track_name',
)

COMMAND: SlasherApplicationCommand


@COMMAND.interactions
async def remove(client, event,
    track: P('str', 'Which track to skip?', autocomplete=autocomplete_track_name) = None,
):
    """Removes the selected track from the queue"""
    player = get_player_or_abort(client, event)
    
    if track is None:
        index = 0
    else:
        for index, configured_track in enumerate(player.iter_all_track()):
            if generate_track_autocomplete_form(configured_track) == track:
                break
        else:
            index = -1
    
    configured_track = await player.remove(index)
    if configured_track is None:
        return 'Nothing was removed.'
    
    return create_added_music_embed(
        player,
        event.user,
        'Track removed',
        create_track_short_description(configured_track),
    )
