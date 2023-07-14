from flask import Blueprint, render_template, abort, send_from_directory, redirect

from ....bot_utils.http_builder import HttpText, HttpUrl, HttpContent

from .utils import get_markdown, has_markdown, TOPICS_ASSETS_FOLDER

URL_PREFIX = '/project/hata/guides'

ROUTES = Blueprint('guides', '', url_prefix = URL_PREFIX)


@ROUTES.route('/<name>')
def get_topic(name):
    if name.endswith('.md'):
        name = name[:-3]
        if has_markdown(name):
            return redirect(f'./{name}')
        
        abort(404)
    
    markdown, title = get_markdown(name)
    if markdown is None:
        abort(404)
    
    return render_template(
        'hata_guides_topic.html',
        title = title,
        markdown = markdown,
    )

@ROUTES.route('/assets/<name>')
def get_asset(name):
    return send_from_directory(TOPICS_ASSETS_FOLDER, name)


@ROUTES.route('/')
def index():
    return render_template(
        'hata_guides_index.html',
        title = 'guides',
    )
