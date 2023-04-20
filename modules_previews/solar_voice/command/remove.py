__all__ = ('remove_',)

from hata.ext.slash import P

from ..autocomplete_track import autocomplete_track_name, generate_track_autocomplete_form
from ..helpers import create_added_music_embed, create_track_short_description, get_player_or_abort


async def remove_(client, event,
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
