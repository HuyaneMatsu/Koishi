import os
from flask import Flask, redirect
from bot_utils.constants import PATH__KOISHI

ROUTE = ('web', 'modules')

WEBAPP = Flask('koishi_web',
    template_folder = os.path.join(PATH__KOISHI, 'web', 'templates'),
    static_folder = os.path.join(PATH__KOISHI, 'web', 'static'),
)

from config import WEBAPP_SECRET_KEY as SECRET_KEY
if SECRET_KEY is not None:
    WEBAPP.config['SECRET_KEY'] = SECRET_KEY

@WEBAPP.route('/')
def hello_world():
    return redirect('/project/hata')


path = None
full_path = None
base_path = os.path.join(PATH__KOISHI, *ROUTE)

for path in (
    'hata_docs',
    'hata_index',
    'hata_guides',
    'koishi_api',
    'koishi_static',
):
    
    ROUTES = __import__(
        '.'.join((*ROUTE, path)),
        fromlist = (path,)
    ).ROUTES
    
    WEBAPP.register_blueprint(ROUTES)

del path, full_path, base_path
