__all__ = ()

from hata import ClientWrapper
from scarletio import to_coroutine

from ...bot_utils.constants import CHANNEL__SUPPORT__LOG_DISPATCH
from ...bot_utils.event_payload_analyzer import guess_event_payload_structure, render_payload_states


ALL_CLIENT = ClientWrapper()


@ALL_CLIENT.events(name = 'unknown_dispatch_event')
async def unknown_dispatch_event__structurize(client, event_name, payload):
    guess_event_payload_structure(event_name, payload)


@ALL_CLIENT.events(name = 'unknown_dispatch_event')
@to_coroutine
def unknown_dispatch_event__notify(client, event_name, payload):
    if CHANNEL__SUPPORT__LOG_DISPATCH.cached_permissions_for(client).send_messages:
        yield from client.message_create(
            CHANNEL__SUPPORT__LOG_DISPATCH,
            content = f'# {event_name}',
            file = [
                ('event.txt', repr(payload)),
                ('structures.txt', render_payload_states()),
            ]
        ).__await__()
