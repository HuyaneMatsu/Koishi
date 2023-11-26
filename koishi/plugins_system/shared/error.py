__all__ = ()

from hata import ClientWrapper, KOKORO, cchunkify
from hata.discord.events.default_event_handlers import default_error_event_handler
from scarletio import alchemy_incendiary
from scarletio.utils.trace import render_exception_into

from ...bot_utils.constants import CHANNEL__SUPPORT__LOG_ERROR


ALL_CLIENT = ClientWrapper()


@ALL_CLIENT.events(name = 'error', overwrite = True)
async def error__notify(client, name, err):
    if not CHANNEL__SUPPORT__LOG_ERROR.cached_permissions_for(client).can_send_messages:
        return await default_error_event_handler(client, name, err)
    
    extracted = [client.full_name, ' ignores occurred exception at ', name, '\n',]
    
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
