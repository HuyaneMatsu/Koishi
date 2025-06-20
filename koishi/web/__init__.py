import os
from os.path import join as join_paths, split as split_path
from flask import Flask, make_response, redirect, request, send_from_directory


from ..bot_utils.constants import PATH__KOISHI

from .patches import *


ROUTE = (__spec__.parent, 'modules')
ASSETS_DIRECTORY = join_paths(split_path(__file__)[0], 'assets')


WEBAPP = Flask(
    'koishi_web',
    template_folder = os.path.join(PATH__KOISHI, 'koishi', 'web', 'templates'),
)

from config import WEBAPP_SECRET_KEY as SECRET_KEY
if SECRET_KEY is not None:
    WEBAPP.config['SECRET_KEY'] = SECRET_KEY


BOT_NAMES = [
    'petalbot',
    'dotbot',
    'ahrefs',
    'bingbot',
    'semrush',
    'wpbot',
    'yandexbot',
    'dataforseobot',
    'mj12bot',
    'facebookexternalhit',
    'coccocbot',
    'seznambot',
    'bingbot',
    'applebot',
    'baiduspider',
    'gptbot',
    'amazonbot',
    'barkrowler',
    'go-http-client',
    'turnitin',
    'meta-externalagent',
    'dataprovider',
    'oai-searchbot',
    'bravebot',
    'chatgpt-user',
    'censysinspect',
    'imagesiftbot',
    (
        'mozilla/5.0 (iphone; cpu iphone os 13_2_3 like mac os x) applewebkit/605.1.15 (khtml, like gecko) '
        'version/13.0.3 mobile/15e148 safari/604.1'
    ),
    (
        'mozilla/5.0 (linux; android 11; m2004j15sc) applewebkit/537.36 (khtml, like gecko) '
        'chrome/103.0.5060.114 mobile safari/537.36'
    ),
    (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) '
        'chrome/131.0.0.0 safari/537.36 edg/131.0.0.0'
    ),
    'Ai2Bot-Dolma',
    
    # From google:
    'googlebot',
    # Googlebot Smartphone -> Googlebot
    # Googlebot Desktop -> Googlebot
    # Googlebot Image -> Googlebot-Image | Googlebot
    # Googlebot News -> Googlebot-News | Googlebot
    # Googlebot Video -> Googlebot-Video | Googlebot
    'storebot-google',
    # Google StoreBot -> Storebot-Google
    'google-interceptiontool',
    # Google-InspectionTool -> Google-InspectionTool | Googlebot
    'googleother',
    # GoogleOther -> GoogleOther
    # GoogleOther-Image -> GoogleOther-Image | GoogleOther
    # GoogleOther-Video -> GoogleOther-Video | GoogleOther
    'google-extended',
    # Google-Extended -> Google-Extended
    'apis-google',
    # APIs-Google -> APIs-Google
    'adsbot-google',
    # AdsBot Mobile Web -> 	AdsBot-Google-Mobile | AdsBot-Google
    'mediapartners-google',
    # AdSense -> Mediapartners-Google
    # Mobile AdSense -> Mediapartners-Google
    'google-safety',
    # Google-Safety -> Google-Safety
    'feedfetcher-google',
    # Feedfetcher -> FeedFetcher-Google
    'googleproducer',
    # Google Publisher Center -> GoogleProducer | google-speakr (deprecated)
    'google-site-verification',
    # Google Site Verifier -> Google-Site-Verification
    
    # An http client?
    'sindresorhus',
    
    # Content management system checker? huh
    'cms-Checker'
]


def check_is_user_agent_banned():
    user_agent_header = request.headers.get('User-Agent')
    if user_agent_header is None:
        return False
    
    user_agent_header = user_agent_header.casefold()
    if not any(bot_name in user_agent_header for bot_name in BOT_NAMES):
        return False
    
    return True


BLOCKED_IPS = {
    # Someone trying to break the site from hongkong.
    # They try to request various urls getting always 404 lol,
    # I dont use any shitty js framework that they could get into.
    '118.193.44.32',
    '152.32.192.176',
    
    # Tries to request Wordpress Blog login page (and then login), for real its not a wordpress site
    '34.64.218.102',
    '144.91.119.115',
    
    # Tries to request env variable file & redirect to google???
    '79.110.62.123',
    
    # Tries to request env variable file
    '78.153.140.223',
    '78.153.140.222',
    '45.148.10.235',
    
    # This its php, lol
    '78.153.140.222',
    
    # Tries to access git
    '196.251.83.148',
    
    # Random bot
    '171.244.43.14',
    '3.228.138.194',
    
    # spams | https://coder.social | "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43" 
    '47.82.8.101',
    '47.82.8.112',
    '47.82.8.127',
    '47.82.8.128',
    '47.82.8.130',
    '47.82.8.133',
    '47.82.8.27',
    '47.82.8.29',
    '47.82.8.30',
    '47.82.8.42',
    '47.82.8.48',
    '47.82.8.49',
    '47.82.8.65',
    '47.82.8.72',
    '47.82.8.82',
    '47.82.8.89',
    '47.82.9.114',
    '47.82.9.126',
    '47.82.9.133',
    '47.82.9.135',
    '47.82.9.147',
    '47.82.9.175',
    '47.82.9.179',
    '47.82.9.183',
    '47.82.9.193',
    '47.82.9.228',
    '47.82.9.230',
    '47.82.9.249',
    '47.82.9.28',
    '47.82.9.29',
    '47.82.9.31',
    '47.82.9.35',
    '47.82.9.50',
    '47.82.9.68',
    '47.82.9.81',
    '47.82.9.82',
    '47.82.9.85',
    '47.82.10.105',
    '47.82.10.115',
    '47.82.10.122',
    '47.82.10.130',
    '47.82.10.133',
    '47.82.10.136',
    '47.82.10.152',
    '47.82.10.162',
    '47.82.10.166',
    '47.82.10.182',
    '47.82.10.19',
    '47.82.10.200',
    '47.82.10.204',
    '47.82.10.224',
    '47.82.10.234',
    '47.82.10.245',
    '47.82.10.26',
    '47.82.10.45',
    '47.82.10.54',
    '47.82.10.6',
    '47.82.10.60',
    '47.82.10.63',
    '47.82.10.65',
    '47.82.10.73',
    '47.82.10.75',
    '47.82.10.77',
    '47.82.10.82',
    '47.82.11.104',
    '47.82.11.107',
    '47.82.11.109',
    '47.82.11.11',
    '47.82.11.115',
    '47.82.11.119',
    '47.82.11.130',
    '47.82.11.152',
    '47.82.11.156',
    '47.82.11.173',
    '47.82.11.189',
    '47.82.11.192',
    '47.82.11.200',
    '47.82.11.208',
    '47.82.11.210',
    '47.82.11.216',
    '47.82.11.220',
    '47.82.11.38',
    '47.82.11.4',
    '47.82.11.43',
    '47.82.11.44',
    '47.82.11.45',
    '47.82.11.46',
    '47.82.11.52',
    '47.82.11.58',
    '47.82.11.69',
    '47.82.11.75',
    '47.82.11.86',
    '47.82.11.9',
    '47.82.11.90',
    '47.82.11.92',
    
    # Scraper "Mozilla/5.0 (compatible) Ai2Bot-Dolma (+https://www.allenai.org/crawl)"
    '104.238.140.158',
    '144.202.84.81',
    '207.148.6.129',
    '45.76.6.132',
    '45.77.164.21',
    '50.28.107.56',
    '50.28.107.59',
    '50.28.40.163',
    '67.225.188.31',
    '67.227.250.168',
    '72.52.132.18',
    '72.52.196.79',
    
    # Scraper "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    '47.238.13.0',
    '47.238.13.1',
    '47.238.13.10',
    '47.238.13.11',
    '47.238.13.12',
    '47.238.13.13',
    '47.238.13.14',
    '47.238.13.15',
    '47.238.13.16',
    '47.238.13.17',
    '47.238.13.18'
    '47.238.13.2',
    '47.238.13.3',
    '47.238.13.4',
    '47.238.13.6',
    '47.238.13.7',
    '47.238.13.8',
    '47.238.13.9',
    '47.238.14.12',
    '47.242.200.220',
    '47.242.230.146'
    '47.242.77.69',
    '47.243.161.234'
    '47.243.56.196',
    '8.210.10.143',
    '8.210.108.0',
    '8.210.11.248',
    '8.210.146.98',
    '8.210.15.252',
    '8.210.152.184',
    '8.210.218.201',
    '8.210.230.104',
    '8.210.8.206',
                                                                                                          
    # Search engine "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/116.0.1938.76 Safari/537.36"
    '157.55.39.202',
    '207.46.13.18',
    '207.46.13.150',
    '40.77.167.247',
    '40.77.167.61',
    '40.77.167.68',
    '40.77.188.140',
    '40.77.188.64',
    '40.77.189.243',
    '52.167.144.159',
    '52.167.144.16',
    '52.167.144.183',
    '52.167.144.19'
    
    # Bot sindresorhus
    '100.28.128.3',
    '18.234.64.190',
    '98.81.123.187',
    
    # cms-checker "Mozilla/5.0 (compatible; CMS-Checker/1.0; +https://example.com)"
    '34.125.200.116',
}


def check_is_ip_banned():
    return request.remote_addr in BLOCKED_IPS


@WEBAPP.before_request
def block_bots():
    if check_is_user_agent_banned() or check_is_ip_banned():
        return make_response('I am a teapot', 418)


@WEBAPP.route('/assets/<path:file_name>', endpoint = 'assets')
def assets(file_name):
    response = make_response(send_from_directory(ASSETS_DIRECTORY, file_name))
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    response.headers['Expires'] = '31536000'
    return response


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
