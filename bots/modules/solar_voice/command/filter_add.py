from hata import Embed
from hata.ext.slash import SlasherApplicationCommand, P
from hata.ext.solarlink import ChannelMix, Distortion, Equalizer, Karaoke, LowPass, Rotation, Timescale, Tremolo, \
    Vibrato, Volume
from hata.ext.extension_loader import import_extension


EMBED_COLOR = import_extension('..constants', 'EMBED_COLOR')
add_current_track_field, get_player_or_abort = import_extension(
    '..helpers', 'add_current_track_field', 'get_player_or_abort'
)
add_filter_field_to = import_extension('..filtering', 'add_filter_field_to')


COMMAND: SlasherApplicationCommand


def create_filter_added_embed(filter):
    return add_filter_field_to(Embed('Filter added', color=EMBED_COLOR), filter)
    

FILTER_ADD = COMMAND.interactions(
    None,
    name = 'filter-add',
    description = 'add a filter',
)


@FILTER_ADD.interactions
async def channel_mix(client, event,
    left_to_left: P('float', 'left to left factor', min_value=0.0, max_value=5.0),
    left_to_right: P('float', 'left to left factor', min_value=0.0, max_value=5.0),
    right_to_right: P('float', 'left to left factor', min_value=0.0, max_value=5.0),
    right_to_left: P('float', 'left to left factor', min_value=0.0, max_value=5.0),
):
    """Mixes both channels (left and right)"""
    player = get_player_or_abort(client, event)
    
    filter = ChannelMix(left_to_left, left_to_right, right_to_right, right_to_left)
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def distortion(client, event,
    offset: P('float', 'offset', min_value=0.0, max_value=100.0) = 0.0,
    scale: P('float', 'scale', min_value=0.0, max_value=100.0) = 1.0,
    sin_offset: P('float', 'sin offset', min_value=0.0, max_value=100.0) = 0.0,
    sin_scale: P('float', 'sin scale', min_value=0.0, max_value=100.0) = 1.0,
    cos_offset: P('float', 'cos offset', min_value=0.0, max_value=100.0) = 0.0,
    cos_scale: P('float', 'cos scale', min_value=0.0, max_value=100.0) = 1.0,
    tan_offset: P('float', 'tan offset', min_value=0.0, max_value=100.0) = 0.0,
    tan_scale: P('float', 'tan scale', min_value=0.0, max_value=100.0) = 1.0,
):
    """Distortion effect"""
    player = get_player_or_abort(client, event)
    
    filter = Distortion(
        sin_offset = sin_offset,
        sin_scale = sin_scale,
        cos_offset = cos_offset,
        cos_scale = cos_scale,
        tan_offset = tan_offset,
        tan_scale = tan_scale,
        offset = offset,
        scale = scale,
    )
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def equalizer(client, event,
    band_00: P('float', 'band 0' , min_value=-0.25, max_value=1.0) = 0.0,
    band_01: P('float', 'band 1' , min_value=-0.25, max_value=1.0) = 0.0,
    band_02: P('float', 'band 2' , min_value=-0.25, max_value=1.0) = 0.0,
    band_03: P('float', 'band 3' , min_value=-0.25, max_value=1.0) = 0.0,
    band_04: P('float', 'band 4' , min_value=-0.25, max_value=1.0) = 0.0,
    band_05: P('float', 'band 5' , min_value=-0.25, max_value=1.0) = 0.0,
    band_06: P('float', 'band 6' , min_value=-0.25, max_value=1.0) = 0.0,
    band_07: P('float', 'band 7' , min_value=-0.25, max_value=1.0) = 0.0,
    band_08: P('float', 'band 8' , min_value=-0.25, max_value=1.0) = 0.0,
    band_09: P('float', 'band 9' , min_value=-0.25, max_value=1.0) = 0.0,
    band_10: P('float', 'band 10', min_value=-0.25, max_value=1.0) = 0.0,
    band_11: P('float', 'band 11', min_value=-0.25, max_value=1.0) = 0.0,
    band_12: P('float', 'band 12', min_value=-0.25, max_value=1.0) = 0.0,
    band_13: P('float', 'band 13', min_value=-0.25, max_value=1.0) = 0.0,
    band_14: P('float', 'band 14', min_value=-0.25, max_value=1.0) = 0.0,
):
    """There are 15 bands (0-14) that can be changed"""
    player = get_player_or_abort(client, event)
    
    filter = Equalizer(
        (0, band_00),
        (1, band_01),
        (2, band_02),
        (3, band_03),
        (4, band_04),
        (5, band_05),
        (6, band_06),
        (7, band_07),
        (8, band_08),
        (9, band_09),
        (10, band_10),
        (11, band_11),
        (12, band_12),
        (13, band_13),
        (14, band_14),
    )
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def karaoke(client, event,
    filter_band : P('float', 'Filter band'      , min_value=0.0, max_value=48000.0) = 220.0,
    filter_width: P('float', 'Filter width'     , min_value=0.0, max_value=48000.0) = 100.0,
    level       : P('float', 'Effect level'     , min_value=0.0, max_value=5.0    ) = 1.0  ,
    mono_level  : P('float', 'Effect mono level', min_value=0.0, max_value=5.0    ) = 1.0  ,
):
    """Eliminates part of a band"""
    player = get_player_or_abort(client, event)
    
    filter = Karaoke(filter_band=filter_band, filter_width=filter_width, level=level, mono_level=mono_level)
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def low_pass(client, event,
    smoothing: P('float', 'smoothing', min_value=0.0, max_value=5.0),
):
    """Higher frequencies get suppressed, lower pass through"""
    player = get_player_or_abort(client, event)
    
    filter = LowPass(smoothing)
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def rotation(client, event,
    rotation: P('float', 'rotation / second', min_value=0.0, max_value=20.0),
):
    """Rotates the sound around the stereo channels"""
    player = get_player_or_abort(client, event)
    
    filter = Rotation(rotation)
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def timescale(client, event,
    pitch: P('float', 'pitch', min_value=0.0, max_value=5.0) = 1.0,
    rate : P('float', 'rate' , min_value=0.0, max_value=5.0) = 1.0,
    speed: P('float', 'speed', min_value=0.0, max_value=5.0) = 1.0,
):
    """Changes the speed, pitch, and rate"""
    player = get_player_or_abort(client, event)
    
    filter = Timescale(pitch=pitch, rate=rate, speed=speed)
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def tremolo(client, event,
    frequency: P('float', 'frequency', min_value=0.0, max_value=5.0),
    depth    : P('float', 'depth'    , min_value=0.0, max_value=5.0),
):
    """Uses amplification to create a shuddering effect"""
    player = get_player_or_abort(client, event)
    
    filter = Tremolo(frequency, depth)
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def vibrato(client, event,
    frequency: P('float', 'frequency', min_value=0.0, max_value=5.0),
    depth    : P('float', 'depth'    , min_value=0.0, max_value=5.0),
):
    """Similar to tremolo, but oscillates the pitch"""
    player = get_player_or_abort(client, event)
    
    filter = Vibrato(frequency, depth)
    player.add_filter(filter)
    
    return create_filter_added_embed(filter)


@FILTER_ADD.interactions
async def volume(client, event,
    volume: P('float', 'volume', min_value=0.0, max_value=5.0),
):
    """Float value where 1.0 is 100%"""
    player = get_player_or_abort(client, event)
    
    filter = Volume(volume)
    player.add_filter(filter)
    await player.apply_filters()
    
    return create_filter_added_embed(filter)
