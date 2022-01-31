from .svg import SVG_GEAR, SVG_LIGHTING, SVG_CLOCK, SVG_CODE, SVG_DISCORD
from flask import Blueprint, render_template, redirect, url_for
from bot_utils.http_builder import HttpText, HttpUrl, HttpContent
from bot_utils.constants import INVITE__SUPPORT

URL_PREFIX = '/project/hata'
ROUTES = Blueprint(
    'index',
    '',
    url_prefix = URL_PREFIX,
)


ADDITIONAL_FEATURES = (
    (
        HttpText(
            'Multiple simultaneous clients'
        ).render(),
        HttpText(
            'Hata can run multiple clients from the same instance without sacrificing performance'
        ).render(),
        SVG_GEAR,
    ), (
        HttpText(
            'Performant'
        ).render(),
        HttpText(
            'Fast concurrent code using async/await syntax, cache control, PyPy support and more!'
        ).render(),
        SVG_LIGHTING,
    ), (
        HttpText(
            'Newest API features'
        ).render(),
        HttpText(
            'Whatever Discord decides to release/update/break Hata will support it natively in no time!'
        ).render(),
        SVG_CLOCK,
    ), (
        HttpText(
            '100% Python'
        ).render(),
        HttpText(
            'Completely relies on Python! Easy to read, easy to understand, easy to code.'
        ).render(),
        SVG_CODE,
    ),
)

DESCRIPTION = (
    HttpText(
        'Hata is an async Discord API wrapper written in Python named after Hata no Kokoro running on top of scarletio.'
    ).render()
)

FEATURES = (
    HttpText(
        'Asynchronous using async / await syntax'
    ).render(),
    HttpText(
        'Feature rich API'
    ).render(),
    HttpText(
        'Object oriented design'
    ).render(),
    HttpText(
        'Automatic sharding'
    ).render(),
)


GETTING_STARTED = (
    (
        HttpUrl(
            'Support server',
            INVITE__SUPPORT.url,
        ).render(),
        HttpText(
            'If you have issues, suggestions, want to contribute, or just want to hang out, join our discord server.'
        ).render(),
        SVG_DISCORD,
    ),

)


@ROUTES.route('/testing')
def home():
    return render_template(
        'hata_index.html',
        additional_features = ADDITIONAL_FEATURES,
        description = DESCRIPTION,
        features = FEATURES,
        getting_started = GETTING_STARTED,
    )

