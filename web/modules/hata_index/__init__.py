from .svg import SVG_GEAR, SVG_LIGHTING, SVG_CLOCK, SVG_CODE, SVG_DISCORD
from flask import Blueprint, render_template

URL_PREFIX = '/project/hata'
ROUTES = Blueprint(
    'index',
    '',
    url_prefix = URL_PREFIX,
)

@ROUTES.route('/testing')
def home():
    return render_template(
        'hata_index.html',
    )
