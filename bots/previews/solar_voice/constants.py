__all__ = ()

from hata import BUILTIN_EMOJIS, Emoji, Color
from hata.ext.solarlink import ChannelMix, Distortion, Equalizer, Karaoke, LowPass, Rotation, Timescale, Tremolo, \
    Vibrato, Volume

EMOJI_CURRENT_TRACK = BUILTIN_EMOJIS['satellite']
EMOJI_LAST_TRACK = BUILTIN_EMOJIS['closed_umbrella']
EMOJI_QUEUE_TIME = BUILTIN_EMOJIS['clock1']
EMOJI_QUEUE_LENGTH = BUILTIN_EMOJIS['dango']
EMOJI_BEHAVIOR = BUILTIN_EMOJIS['control_knobs']
EMOJI_CHANNEL = BUILTIN_EMOJIS['mega']
EMOJI_VOLUME = BUILTIN_EMOJIS['level_slider']
EMOJI_PLAYING = BUILTIN_EMOJIS['loud_sound']
EMOJI_STOPPED =  BUILTIN_EMOJIS['speaker']

TRACK_PER_PAGE = 10

TRACK_EMOJIS = [
    Emoji.precreate(704393708467912875),
    Emoji.precreate(748504187620294656),
    Emoji.precreate(748506469694963713),
    Emoji.precreate(748507069690282054),
    Emoji.precreate(812069466069663765),
    Emoji.precreate(825074491817852979),
    Emoji.precreate(846320146342477834),
    Emoji.precreate(852856910116945930),
    Emoji.precreate(852857235067371521),
    Emoji.precreate(853152183222272011),
    Emoji.precreate(853152183629774848),
    Emoji.precreate(853507411150897162),
    Emoji.precreate(853507411293765642),
    Emoji.precreate(853507411548831764),
    Emoji.precreate(853507411674661014),
    Emoji.precreate(853507411687112734),
    Emoji.precreate(853507412064600084),
    Emoji.precreate(853507412577484811),
    Emoji.precreate(853685522303680512),
    Emoji.precreate(855417900764626994),
    Emoji.precreate(858609857568964618),
]

EMBED_COLOR = Color(0xFF9612)

LEAVE_TIMEOUT = 120.0

LAVA_VOICE_TRACK_SELECT_CUSTOM_ID = 'lava_voice.select'


BEHAVIOR_NAME_REPEAT_CURRENT = 'loop current'
BEHAVIOR_NAME_REPEAT_QUEUE = 'loop queue'
BEHAVIOR_NAME_SHUFFLE = 'shuffle'

BEHAVIOR_VALUE_GET = 0
BEHAVIOR_VALUE_REPEAT_CURRENT = 1
BEHAVIOR_VALUE_REPEAT_QUEUE = 2
BEHAVIOR_VALUE_SHUFFLE = 3

BEHAVIOR_CHOICES = [
    (BEHAVIOR_NAME_REPEAT_CURRENT, BEHAVIOR_VALUE_REPEAT_CURRENT),
    (BEHAVIOR_NAME_REPEAT_QUEUE, BEHAVIOR_VALUE_REPEAT_QUEUE),
    (BEHAVIOR_NAME_SHUFFLE, BEHAVIOR_VALUE_SHUFFLE),
]


FILTER_NAME_TO_FILTER_TYPE = {
    'channel-mix': ChannelMix,
    'distortion': Distortion,
    'equalizer': Equalizer,
    'karaoke': Karaoke,
    'low-pass': LowPass,
    'rotation': Rotation,
    'timescale': Timescale,
    'tremolo': Tremolo,
    'vibrato': Vibrato,
    'volume': Volume
}

FILTER_TYPE_TO_FILTER_NAME = {
    filter_type: filter_name for filter_name, filter_type in FILTER_NAME_TO_FILTER_TYPE.items()
}
