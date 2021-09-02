import re

from hata import Client

from bot_utils.shared import GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__MODERATOR

Satori : Client

FILTER = re.compile(
    (
        'd(?:iscord)?[\.\_]?[pр]y|'
        'danny|'
        'rapptz|'
        'discord\.ext|'
        '[pр]y\.discord|'
        'D¡\$€0rd\.[pр]¥|'
        '[pр]ycord'
    ),
    re.I|re.M|re.S|re.U,
)


@Satori.events
async def message_create(client, message):
    await filter(client, message)

@Satori.events
async def message_edit(client, message, old_attributes):
    await filter(client, message)


async def filter(client, message):
    if message.guild is not GUILD__NEKO_DUNGEON:
        return
    
    user = message.author
    if user.is_bot or user.has_role(ROLE__NEKO_DUNGEON__MODERATOR):
        return
    
    content = message.content
    if (not content) or (FILTER.search(content) is None):
        return
    
    await client.message_delete(message)
