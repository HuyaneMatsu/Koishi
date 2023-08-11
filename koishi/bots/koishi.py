__all__ = ('Koishi',)

from hata import Activity, Client, ClientWrapper, IntentFlag, KOKORO, cchunkify
from scarletio import alchemy_incendiary, to_coroutine
from scarletio.utils.trace import render_exception_into

import config

from ..bot_utils.constants import CHANNEL__SUPPORT__LOG_DISPATCH, CHANNEL__SUPPORT__LOG_ERROR
from ..bot_utils.event_payload_analyzer import guess_event_payload_structure, render_payload_states
from ..bot_utils.tools import EmojiDeleteWaitfor, MessageDeleteWaitfor, RoleDeleteWaitfor, RoleUpdateWaitfor


Koishi = Client(
    config.KOISHI_TOKEN,
    secret = config.KOISHI_SECRET,
    client_id = config.KOISHI_ID,
    activity = Activity('with Kokoro'),
    shard_count = 2,
    should_request_users = False,
    intents = IntentFlag().update_by_keys(
        guild_users = True, # We need this
        guild_presences = True, # Now this too, :KoishiFail:
        _17 = 1,
        _18 = 1,
        _19 = 1,
        _21 = 1, # Gonna catch them all
    ),
    application_id = config.KOISHI_ID,
    extensions = ('command_utils', 'slash', 'top_gg'),
    top_gg_token = config.KOISHI_TOP_GG_TOKEN,
)


Koishi.events(MessageDeleteWaitfor)
Koishi.events(RoleDeleteWaitfor)
Koishi.events(EmojiDeleteWaitfor)
Koishi.events(RoleUpdateWaitfor)


@Koishi.events(overwrite = True)
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
    for chunk in cchunkify(extracted, lang = 'py'):
        await client.message_create(CHANNEL__SUPPORT__LOG_ERROR, chunk)


# Add the event payload analyzer to all client's events.
ALL = ClientWrapper()
@ALL.events
async def unknown_dispatch_event(client, event_name, payload):
    guess_event_payload_structure(event_name, payload)


@Koishi.events
@to_coroutine
def unknown_dispatch_event(client, event_name, payload):
    yield from client.message_create(
        CHANNEL__SUPPORT__LOG_DISPATCH,
        content = f'# {event_name}',
        file = [
            ('event.txt', repr(payload)),
            ('structures.txt', render_payload_states()),
        ]
    ).__await__()
