import os
from flask import Flask
from bot_utils.shared import KOISHI_PATH

ROUTE = ('web', 'modules')

WEBAPP = Flask('koishi_web',
    template_folder = os.path.join(KOISHI_PATH, 'web', 'templates'),
    static_folder = os.path.join(KOISHI_PATH, 'web', 'static'),
        )

from config import WEBAPP_SECRET_KEY as SECRET_KEY
if SECRET_KEY is not None:
    WEBAPP.config['SECRET_KEY'] = SECRET_KEY

@WEBAPP.route('/')
def hello_world():
    return 'Nothing to see here.'

path = None
full_path = None
base_path = os.path.join(KOISHI_PATH, *ROUTE)

for path in os.listdir(base_path):
    full_path = os.path.join(base_path, path)
    if os.path.isfile(full_path):
        if not path.endswith('.py'):
            continue
        path = path[:-3]
    elif os.path.isdir(full_path):
        if path == '__pycache__':
            continue
    else:
        continue
    
    ROUTES = __import__(
        '.'.join((*ROUTE, path)),
        fromlist = (path,)
            ).ROUTES
    
    WEBAPP.register_blueprint(ROUTES)

del path, full_path, base_path
