__all__ = ('Alice',)

from hata import Client, IntentFlag, Status

import config


Alice = Client(
    config.ALICE_TOKEN,
    client_id = config.ALICE_ID,
    status = Status.online,
    should_request_users = False,
    intents = IntentFlag().update_by_keys(), # no changes
    application_id = config.ALICE_ID,
    extensions = ('slash',),
)
