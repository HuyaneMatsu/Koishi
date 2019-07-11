from hata.parsers import eventlist
from hata.events import cooldown
from tools import cooldown_handler

commands=eventlist()

@commands
@cooldown(30.,'user',handler=cooldown_handler())
async def ping(client,message,content):
    await client.message_create(message.channel,f'{int(client.kokoro.latency*1000.)} ms')
