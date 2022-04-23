__all__ = ()

from hata.ext.solarlink import ChannelMix, Distortion, Equalizer, Karaoke, LowPass, Rotation, Timescale, Tremolo, \
    Vibrato, Volume

def get_channel_mix_filer_name_and_value(filter):
    return (
        'Channel mix',
        (
            f'```\n'
            f'left  to left  : {filter._left_to_left:.3f}\n'
            f'left  to right : {filter._left_to_right:.3f}\n'
            f'right to left  : {filter._right_to_left:.3f}\n'
            f'right to right : {filter._right_to_right:.3f}\n'
            f'```'
        ),
    )


DISTORTION_ADJUST = 10

def maybe_add_distortion_parts_to(value_parts, offset, scale, offset_name, scale_name):
    if (offset != 0.0) or (scale != 1.0):
        value_parts.append(offset_name.rjust(DISTORTION_ADJUST, ' '))
        value_parts.append(' : ')
        value_parts.append(format(offset, '.3f'))
        value_parts.append('\n')
        value_parts.append(scale_name.rjust(DISTORTION_ADJUST, ' '))
        value_parts.append(' : ')
        value_parts.append(format(scale, '.3f'))
        value_parts.append('\n')


def get_distortion_filer_name_and_value(filter):
    value_parts = ['```\n']
    maybe_add_distortion_parts_to(value_parts, filter._offset    , filter._scale    , 'offset'    , 'scale'    )
    maybe_add_distortion_parts_to(value_parts, filter._sin_offset, filter._sin_scale, 'sin offset', 'sin scale')
    maybe_add_distortion_parts_to(value_parts, filter._cos_offset, filter._cos_scale, 'cos offset', 'cos scale')
    maybe_add_distortion_parts_to(value_parts, filter._tan_offset, filter._tan_scale, 'tan offset', 'tan scale')
    value_parts.append('```')
    
    return (
        'Distortion',
        ''.join(value_parts),
    )


def get_equalizer_filer_name_and_value(filter):
    value_parts = ['```\n']
    
    bands = filter._bands
    if (bands is not None):
        for band_index, gain in bands.items():
            value_parts.append(format(band_index, '<2'))
            value_parts.append(' : ')
            value_parts.append(format(gain, '.3f'))
            value_parts.append('\n')
    
    value_parts.append('```')
    
    return (
        'Equalizer',
        ''.join(value_parts)
    )


def get_karaoke_filter_name_and_value(filter):
    return (
        'Karaoke',
        (
            f'```\n'
            f'filter band  : {filter._filter_band:.3f}\n'
            f'filter width : {filter._filter_width:.3f}\n'
            f'level        : {filter._level:.3f}\n'
            f'mono level   : {filter._mono_level:.3f}\n'
            f'```'
        ),
    )


def get_low_pass_filter_name_and_value(filter):
    return (
        'Low pass',
        (
            f'```\n'
            f'smoothing  : {filter._smoothing:.3f}\n'
            f'```'
        ),
    )


def get_rotation_filter_name_and_value(filter):
    return (
        'Rotation',
        (
            f'```\n'
            f'rotation : {filter._rotation:.3f}\n'
            f'```'
        ),
    )


def get_timescale_filter_name_and_value(filter):
    return (
        'Timescale',
        (
            f'```\n'
            f'pitch : {filter._pitch:.3f}\n'
            f'rate  : {filter._rate:.3f}\n'
            f'speed : {filter._speed:.3f}\n'
            f'```'
        ),
    )


def get_tremolo_filter_name_and_value(filter):
    return (
        'Tremolo',
        (
            f'```\n'
            f'depth     : {filter._depth:.3f}\n'
            f'frequency : {filter._frequency:.3f}\n'
            f'```'
        ),
    )


def get_vibrato_filter_name_and_value(filter):
    return (
        'Vibrato',
        (
            f'```\n'
            f'depth     : {filter._depth:.3f}\n'
            f'frequency : {filter._frequency:.3f}\n'
            f'```'
        ),
    )


def get_volume_filter_name_and_value(filter):
    return (
        'Volume',
        (
            f'```\n'
            f'volume : {filter._volume:.3f}\n'
            f'```'
        ),
    )

FILTER_FIELD_GENERATORS = {
    ChannelMix: get_channel_mix_filer_name_and_value,
    Distortion: get_distortion_filer_name_and_value,
    Equalizer: get_equalizer_filer_name_and_value,
    Karaoke: get_karaoke_filter_name_and_value,
    LowPass: get_low_pass_filter_name_and_value,
    Rotation: get_rotation_filter_name_and_value,
    Timescale: get_timescale_filter_name_and_value,
    Tremolo: get_tremolo_filter_name_and_value,
    Vibrato: get_vibrato_filter_name_and_value,
    Volume: get_volume_filter_name_and_value,
}


def add_filter_field_to(embed, filter):
    filter_field_generator = FILTER_FIELD_GENERATORS.get(type(filter), None)
    if filter_field_generator is None:
        title = type(filter).__name__
        description = '*unknown filter*'
        
    else:
        title, description = filter_field_generator(filter)
    
    return embed.add_field(title, description)
