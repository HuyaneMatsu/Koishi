from flask import Blueprint

URL_PREFIX = '/project/hata/topics'

ROUTES = Blueprint('vote', '', url_prefix=URL_PREFIX)
