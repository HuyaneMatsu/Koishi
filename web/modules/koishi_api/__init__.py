from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort, Response
from sqlalchemy.sql import select
from hata.ext.top_gg import BotVote

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression
from config import KOISHI_TOP_GG_AUTHORIZATION

URL_PREFIX = '/project/koishi/api'

ROUTES = Blueprint('vote', '', url_prefix=URL_PREFIX)

DAILY_BASE = 100
DAILY_LIMIT = 300
DAILY_PER_DAY_BONUS = 5


@ROUTES.route('/top_gg/vote', methods=['POST'])
def vote():
    authorization = request.headers.get('Authorization', '')
    if authorization != KOISHI_TOP_GG_AUTHORIZATION:
        abort(401)
    
    bot_vote = BotVote.from_data(request.json)

    with DB_ENGINE.connect() as connector:
        response = connector.execute(
            select(
                [
                    user_common_model.id,
                ]
            ).where(
                user_common_model.user_id == bot_vote.user_id,
            )
        )
        
        results = response.fetchall()
        if results:
            connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == results[0][0],
                ).values(
                    total_love = user_common_model.total_love+100,
                    count_top_gg_vote = user_common_model.count_top_gg_vote+1,
                )
            )
        else:
            connector.execute(
                get_create_common_user_expression(
                    bot_vote.user_id,
                    total_love = 100,
                    count_top_gg_vote = 1,
                )
            )
    
    return Response(200)
