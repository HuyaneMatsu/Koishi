from hata.ext.top_gg import BotVote

from ....bot_utils.external_event_types import EXTERNAL_EVENT_TYPE_TOP_GG_VOTE
from ....bot_utils.models import DB_ENGINE, EXTERNAL_EVENTS_TABLE

from config import KOISHI_TOP_GG_AUTHORIZATION
from flask import Blueprint, Response, abort, request


URL_PREFIX = '/project/koishi/api'

ROUTES = Blueprint('vote', '', url_prefix = URL_PREFIX)


@ROUTES.route('/top_gg/vote', methods = ['POST'])
def vote():
    authorization = request.headers.get('Authorization', '')
    if authorization != KOISHI_TOP_GG_AUTHORIZATION:
        abort(401)
    
    bot_vote = BotVote.from_data(request.json)
    
    with DB_ENGINE.connect() as connector:
        connector.execute(
            EXTERNAL_EVENTS_TABLE.insert().values(
                client_id = 0,
                user_id = bot_vote.user_id,
                guild_id = 0,
                event_type = EXTERNAL_EVENT_TYPE_TOP_GG_VOTE,
                event_data = None,
                trigger_after = None,
            )
        )

    return Response(status = 200)
