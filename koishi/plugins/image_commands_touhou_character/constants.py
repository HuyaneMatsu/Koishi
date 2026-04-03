__all__ = ()

from hata import BUILTIN_EMOJIS, Color, Permission


EMOJI_NEW = BUILTIN_EMOJIS['arrows_counterclockwise']

EMBED_COLOR = Color(0xffc0dd)

EXTRA_PERMISSIONS = Permission().update_by_keys(embed_links = True)
