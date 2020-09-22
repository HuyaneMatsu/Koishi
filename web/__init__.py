import os
from flask import Flask
from bot_utils.shared import KOISHI_PATH

WEBAPP = Flask('koishi_web')

from config import WEBAPP_SECRET_KEY as SECRET_KEY
if SECRET_KEY is not None:
    WEBAPP.config['SECRET_KEY'] = SECRET_KEY

@WEBAPP.route('/')
def hello_world():
    return 'Nothing to see here.'

path = None
for path in os.listdir(os.path.join(KOISHI_PATH, 'web', 'modules')):
    if not path.endswith('.py'):
        continue
    
    path = path[:-3]
    ROUTES = __import__(
        '.'.join(('web', 'modules', path)),
        fromlist = (path,)
            ).ROUTES
    
    WEBAPP.register_blueprint(ROUTES)
