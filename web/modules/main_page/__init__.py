from .svg import SVG_GEAR, SVG_LIGHTING, SVG_CLOCK, SVG_CODE, SVG_DISCORD
from flask import Blueprint, render_template, redirect, url_for

ROUTES = Blueprint('main_page', 'main_page')




DESCRIPTION_PARTS = (
    'Hata is an async Discord API wrapper written in Python named after Hata no Kokoro.',
    'It specializes in running multiple simultaneous clients, optimizing performance and getting all the newest '
    'Discord API features before all the other similar wrappers.'
)

FEATURES = (
    (
        'Multiple simultaneous clients',
        'Hata can run multiple clients from the same instance without sacrificing performance, all while being easy '
        'to code.',
        SVG_GEAR,
    ), (
        'Performant',
        'Fast rate limit handling, optimized dispatch event parsers, fast concurrent code using async/await syntax, '
        'cache control, PyPy optimizations and more!',
        SVG_LIGHTING,
    ), (
        'Newest API features',
        'Whatever Discord decides to release/update/break Hata will support it natively in no time!',
        SVG_CLOCK,
    ), (
        '100% Python',
        'Completely relies on Python! Easy to read, easy to understand, easy to code.',
        SVG_CODE,
    ),
)

MAJOR_SELLOUT = (
    'Some of the major sellout reasons.'
)


ADDITIONAL_FEATURES = (
    (
        'Comfy Discord support server',
        'Great server for support and any questions! Also boosting a wide variety of good emojis.',
        SVG_DISCORD,
    ),

)

@ROUTES.route('/home_testing')
def home():
    return render_template('hata_home_page.html',
        description_parts = DESCRIPTION_PARTS,
        features = FEATURES,
        major_sellout = MAJOR_SELLOUT,
        additional_features = ADDITIONAL_FEATURES,
    )

