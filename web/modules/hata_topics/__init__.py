from flask import Blueprint, render_template, abort, send_from_directory

from .utils import get_markdown, TOPICS_ASSETS_FOLDER

URL_PREFIX = '/project/hata/topics'

ROUTES = Blueprint('topics', '', url_prefix=URL_PREFIX)


@ROUTES.route('/<name:str>')
def get_topic(name):
    markdown = get_markdown(name)
    if markdown is None:
        abort(404)
    
    return render_template(
        'hata_topic.html',
        markdown = markdown,
    )

@ROUTES.route('/assets/<name:str>')
def get_topic(name):
    return send_from_directory(TOPICS_ASSETS_FOLDER, name)
