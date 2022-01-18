from hata import Client, KOKORO, cchunkify, ClientWrapper
from scarletio import alchemy_incendiary, to_coroutine
from scarletio.utils.trace import render_exception_into

from bot_utils.tools import MessageDeleteWaitfor, GuildDeleteWaitfor, RoleDeleteWaitfor, EmojiDeleteWaitfor, \
    RoleEditWaitfor
from bot_utils.constants import CHANNEL__SUPPORT__DEFAULT_TEST
from bot_utils.event_payload_analyzer import guess_event_payload_structure, render_payload_states

Koishi: Client


Koishi.events(MessageDeleteWaitfor)
Koishi.events(GuildDeleteWaitfor)
Koishi.events(RoleDeleteWaitfor)
Koishi.events(EmojiDeleteWaitfor)
Koishi.events(RoleEditWaitfor)

@Koishi.events
async def unknown_dispatch_event(client, name, data):
    await client.events.error(client, name, repr(data))


@Koishi.events(overwrite=True)
async def error(client, name, err):
    extracted = [
        client.full_name,
        ' ignores occurred exception at ',
        name,
        '\n',
    ]
    
    if isinstance(err, BaseException):
        await KOKORO.run_in_executor(alchemy_incendiary(render_exception_into, (err, extracted)))
    else:
        if not isinstance(err, str):
            err = repr(err)
        
        extracted.append(err)
        extracted.append('\n')
    
    extracted = ''.join(extracted).split('\n')
    for chunk in cchunkify(extracted, lang='py'):
        await client.message_create(CHANNEL__SUPPORT__DEFAULT_TEST, chunk)


# Add the event payload analyzer to all client's events.
ALL = ClientWrapper()
@ALL.events()
async def unknown_dispatch_event(client, event_name, payload):
    guess_event_payload_structure(event_name, payload)


@Koishi.events
@to_coroutine
def unknown_dispatch_event(client, event_name, payload):
    yield # This makes sure, the event above is called first.
    
    file_content = render_payload_states()
    
    yield from client.message_create(
        CHANNEL__SUPPORT__DEFAULT_TEST,
        file = ('unknown_dispatch_event.txt', file_content)
    ).__await__()
