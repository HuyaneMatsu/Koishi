from hata import Embed
from hata.ext.slash import SlasherApplicationCommand, abort
from hata.ext.extension_loader import import_extension


(
    create_added_music_embed,
    get_player_or_abort,
    duration_to_string,
    add_current_track_field_with_bar,
) = import_extension('..helpers',
    'create_added_music_embed',
    'get_player_or_abort',
    'duration_to_string',
    'add_current_track_field_with_bar',
)

COMMAND: SlasherApplicationCommand


@COMMAND.interactions
async def seek_(client, event,
    seconds: (float, 'Where to seek?'),
):
    """Seeks to the given time in seconds."""
    player = get_player_or_abort(client, event)
    
    track = player.get_current()
    if track is None:
        abort('The player is not playing anything.')
    
    duration = track.duration
    if (seconds < 0.0) or (seconds > duration):
        abort(f'Cannot seek to {seconds:.2f} seconds. Please define a value between `0` and {duration:.0f}.')
    
    await player.seek(seconds)
    
    embed = Embed(None, f'Seeked to {duration_to_string(seconds)}')
    add_current_track_field_with_bar(embed, player)
    return embed
