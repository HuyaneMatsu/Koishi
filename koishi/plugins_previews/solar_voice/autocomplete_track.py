__all__ = ()

from re import compile as re_compile, escape as re_escape, I as re_ignore_case


def generate_track_autocomplete_form(configured_track):
    result = configured_track.track.title
    if len(result) > 69:
        result = result[:66] + '...'
    
    return result


async def autocomplete_track_name(client, event, value):
    player = client.solarlink.get_player(event.guild_id)
    if player is None:
        return None
    
    collected = 0
    track_names = []
    
    if value is None:
        for configured_track in player.iter_all_track():
            track_names.append(generate_track_autocomplete_form(configured_track))
            
            collected += 1
            if collected == 20:
                break
    else:
        pattern = re_compile(re_escape(value), re_ignore_case)
        
        for configured_track in player.iter_all_track():
            track_name = generate_track_autocomplete_form(configured_track)
            if (pattern.search(track_name) is not None):
                track_names.append(track_name)
            
            collected += 1
            if collected == 20:
                break
    
    return track_names
