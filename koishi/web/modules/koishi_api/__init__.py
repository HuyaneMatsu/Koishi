from datetime import datetime as DateTime, timezone as TimeZone

from flask import Blueprint, request, abort, Response
from sqlalchemy.sql import select
from hata.ext.top_gg import BotVote

from config import KOISHI_TOP_GG_AUTHORIZATION

from ....bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression
from ....bot_utils.daily import VOTE_BASE, VOTE_PER_DAY, calculate_daily_new_only, \
    VOTE_BASE_BONUS_WEEKEND, VOTE_PER_DAY_BONUS_WEEKEND

URL_PREFIX = '/project/koishi/api'

ROUTES = Blueprint('vote', '', url_prefix = URL_PREFIX)


@ROUTES.route('/top_gg/vote', methods = ['POST'])
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
        
        now = DateTime.now(TimeZone.utc)
        
        if results:
            entry_id, daily_streak, daily_next = results[0]
            daily_next = daily_next.replace(tzinfo = TimeZone.utc)
            daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
            
            if now > daily_next:
                daily_next = now
            
            daily_streak += 1
        else:
            entry_id = -1
            daily_streak = 0
            daily_next = now
        
        base = VOTE_BASE
        per_day = VOTE_PER_DAY
        
        if  (DateTime.now(TimeZone.utc).weekday() > 4):
            base += VOTE_BASE_BONUS_WEEKEND
            per_day += VOTE_PER_DAY_BONUS_WEEKEND
        
        
        increase = base + (daily_streak * per_day)
        
        if (entry_id != -1):
            connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = user_common_model.total_love + increase,
                    count_top_gg_vote = user_common_model.count_top_gg_vote + 1,
                    daily_streak = daily_streak,
                    daily_next = daily_next,
                )
            )
        else:
            connector.execute(
                get_create_common_user_expression(
                    bot_vote.user_id,
                    total_love = increase,
                    count_top_gg_vote = 1,
                    daily_streak = 1,
                    daily_next = daily_next,
                )
            )
        
    return Response(status = 200)
