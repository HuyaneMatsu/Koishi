__all__ = ('ToyKoishi',)

from hata import Activity, ActivityType, Client, IntentFlag

import config


ToyKoishi = Client(
    config.TOY_KOISHI_TOKEN,
    client_id = config.TOY_KOISHI_ID,
    activity = Activity('All Max Mode....', activity_type = ActivityType.competing),
    should_request_users = False,
    intents = IntentFlag().update_by_keys(), # no changes
    application_id = config.TOY_KOISHI_ID,
    extensions = ('slash',),
)
