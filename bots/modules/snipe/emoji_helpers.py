__all__ = ()

from hata import EMOJIS


async def get_emoji(client, emoji_id):
    emoji = EMOJIS.get(emoji_id, None)
    if emoji is None:

