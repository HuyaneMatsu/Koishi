from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort, Response
from sqlalchemy.sql import select
from hata.ext.top_gg import BotVote

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression
from bot_utils.daily import DAILY_BASE, DAILY_VOTE_PER_DAY, calculate_daily_new_only
from config import KOISHI_TOP_GG_AUTHORIZATION

URL_PREFIX = '/project/koishi/api'

ROUTES = Blueprint('vote', '', url_prefix=URL_PREFIX)


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
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                ]
            ).where(
                user_common_model.user_id == bot_vote.user_id,
            )
        )
        
        results = response.fetchall()
        
        now = datetime.utcnow()
        
        if results:
            entry_id, daily_streak, daily_next = results[0]
            daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
            
            increase = DAILY_BASE + (daily_streak*DAILY_VOTE_PER_DAY)
            
            if now > daily_next:
                daily_next = now
            
            daily_streak += 1
            
            connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = user_common_model.total_love+increase,
                    count_top_gg_vote = user_common_model.count_top_gg_vote+1,
                    daily_streak = daily_streak,
                    daily_next = daily_next,
                )
            )
        else:
            connector.execute(
                get_create_common_user_expression(
                    bot_vote.user_id,
                    total_love = DAILY_BASE,
                    count_top_gg_vote = 1,
                    daily_streak = 1,
                    daily_next = now,
                )
            )
    
    return Response(status=200)
