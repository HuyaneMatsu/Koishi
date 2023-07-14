from flask import Blueprint, render_template

URL_PREFIX = '/project/hata'
ROUTES = Blueprint(
    'index',
    '',
    url_prefix = URL_PREFIX,
)

@ROUTES.route('/')
def home():
    return render_template(
        'hata_index.html',
    )
