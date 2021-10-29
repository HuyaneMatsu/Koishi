from .svg import SVG_GEAR, SVG_LIGHTING, SVG_CLOCK, SVG_CODE, SVG_DISCORD
from flask import Blueprint, render_template, redirect, url_for
from bot_utils.http_builder import HttpText, HttpUrl, HttpContent
from bot_utils.constants import INVITE__SUPPORT

URL_PREFIX = '/project/hata'
ROUTES = Blueprint('index', '',
    url_prefix=URL_PREFIX,
)


DESCRIPTION_PARTS = (
    'Hata is an async Discord API wrapper written in Python named after Hata no Kokoro.',
    'It specializes in running multiple simultaneous clients, optimizing performance and getting all the newest '
    'Discord API features before all the other similar wrappers.',
)

FEATURES = (
    (
        HttpText(
            'Multiple simultaneous clients',
        ).render(),
        HttpText(
            'Hata can run multiple clients from the same instance without sacrificing performance, all while being '
            'easy to code.',
        ).render(),
        SVG_GEAR,
    ), (
        HttpText(
            'Performant',
        ).render(),
        HttpText(
            'Fast concurrent code using async/await syntax, cache control, PyPy support and more!',
        ).render(),
        SVG_LIGHTING,
    ), (
        HttpText(
            'Newest API features',
        ).render(),
        HttpText(
            'Whatever Discord decides to release/update/break Hata will support it natively in no time!',
        ).render(),
        SVG_CLOCK,
    ), (
        HttpText(
            '100% Python',
        ).render(),
        HttpText(
            'Completely relies on Python! Easy to read, easy to understand, easy to code.',
        ).render(),
        SVG_CODE,
    ),
)

MAJOR_SELLOUT = (
    HttpText(
        'Some of the major sellout reasons.',
    ).render()
)


ADDITIONAL_FEATURES = (
    (
        HttpUrl(
            'Comfy Discord support server',
            INVITE__SUPPORT.url,
        ).render(),
        HttpText(
            'Great server for support and any questions! Also boosting a wide variety of good emojis.',
        ).render(),
        SVG_DISCORD,
    ),

)


@ROUTES.route('/testing')
def home():
    return render_template('hata_index_page.html',
        description_parts = DESCRIPTION_PARTS,
        features = FEATURES,
        major_sellout = MAJOR_SELLOUT,
        additional_features = ADDITIONAL_FEATURES,
    )

