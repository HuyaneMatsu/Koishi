from .file import *

__all__ = ()


from ...bot_utils.constants import GUILD__SUPPORT
from ...bots import Marisa


@Marisa.interactions(guild = GUILD__SUPPORT)
async def request_sounds(client):
    await client.request_soundboard_sounds([*client.guilds])
    return 'ayaya'
