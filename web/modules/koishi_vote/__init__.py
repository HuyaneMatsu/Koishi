from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort

from hata.ext.top_gg import BotVote

from config import KOISHI_TOP_GG_AUTHORIZATION

URL_PREFIX = '/project/koishi/api'

ROUTES = Blueprint('vote', '', url_prefix=URL_PREFIX)

@ROUTES.route('/top_gg/vote', methods=['POST'])
def vote():
    authorization = request.headers.get('Authorization', '')
    if authorization != KOISHI_TOP_GG_AUTHORIZATION:
        abort(401)
    
    bot_vote = BotVote.from_data(request.json)
    abort(201)
