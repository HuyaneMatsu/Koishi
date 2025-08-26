import os
from os.path import join as join_paths, split as split_path
from flask import Flask, make_response, redirect, request, send_from_directory


from ..bot_utils.constants import PATH__KOISHI
from ..bot_utils.ip_filtering import IPFilterRule, build_ip_matcher_structure, match_ip_to_structure, parse_ip 

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
    'ai2bot-dolma',
    
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
    'cms-checker'
    
    # amazon
    "Mozilla/5.0 AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/605.1.15",
]


def check_is_user_agent_banned():
    user_agent_header = request.headers.get('User-Agent')
    if user_agent_header is None:
        return False
    
    user_agent_header = user_agent_header.casefold()
    if not any(bot_name in user_agent_header for bot_name in BOT_NAMES):
        return False
    
    return True


IP_MATCHER_STRUCTURE = build_ip_matcher_structure([
    # Someone trying to break the site from hongkong.
    # They try to request various urls getting always 404 lol,
    # I dont use any shitty js framework that they could get into.
    IPFilterRule(*parse_ip('118.193.44.0'), 8), # Hongkong - UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED
    IPFilterRule(*parse_ip('152.32.192.0'), 8), # Hongkong - UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED
    
    # Tries to request Wordpress Blog login page (and then login), for real its not a wordpress site
    IPFilterRule(*parse_ip('34.64.208.0'), 12), # Seoul - Google Asia Pacific Pte. Ltd.
    IPFilterRule(*parse_ip('144.91.118.0'), 9), # Frankfurt - Contabo GmbH
    
    # Tries to request env variable file & redirect to google???
    IPFilterRule(*parse_ip('79.110.62.0'), 8), # Frankfurt - Vecna Hosting Limited
    
    # Tries to request env variable file
    IPFilterRule(*parse_ip('78.153.140.0'), 8), # London - HOSTGLOBAL.PLUS LTD
    IPFilterRule(*parse_ip('45.148.10.0'), 8), # Amsterdam - TECHOFF SRV LIMITED
    
    # Tries to access git
    IPFilterRule(*parse_ip('196.251.83.0'), 8), # Amsterdam - internet-security-cheapyhost
    
    
    # Scraper "Mozilla/5.0 (compatible) Ai2Bot-Dolma (+https://www.allenai.org/crawl)"
    IPFilterRule(*parse_ip('104.238.140.0'), 10), # Losangeles - Vultr Holdings, LLC
    IPFilterRule(*parse_ip('144.202.80.0'), 12), # Kent - Vultr Holdings, LLC
    IPFilterRule(*parse_ip('207.148.0.0'), 11), # Dallas - Vultr Holdings, LLC
    IPFilterRule(*parse_ip('45.76.0.0'), 12), # Piscataway - Vultr Holdings, LLC
    
    IPFilterRule(*parse_ip('50.28.96.0'), 13), # Phoenix - Liquid Web Inc
    IPFilterRule(*parse_ip('50.28.0.0'), 14), # Lansing - Liquid Web Inc
    IPFilterRule(*parse_ip('67.225.128.0'), 15), # Lansing - Liquid Web Inc
    IPFilterRule(*parse_ip('72.52.128.0'), 15), # Lansing - Liquid Web Inc
    
    # spams | https://coder.social | "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    IPFilterRule(*parse_ip('47.82.8.0'), 10), # Sanmateo - Alibaba (US) Technology Co., Ltd. 
    IPFilterRule(*parse_ip('47.238.0.0'), 16), # HonKong - Alibaba (US) Technology Co., Ltd. 
    IPFilterRule(*parse_ip('47.242.0.0'), 16), # HonKong - Alibaba (US) Technology Co., Ltd. 
    IPFilterRule(*parse_ip('47.243.0.0'), 16), # HonKong - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('8.210.0.0'), 15), # HonKong - Alibaba (US) Technology Co., Ltd.
                                                                                        
    # Bingbot
    # "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/116.0.1938.76 Safari/537.36"
    IPFilterRule(*parse_ip('157.55.0.0'), 16), # Moseslake - Microsoft Corporation
    IPFilterRule(*parse_ip('207.46.0.0'), 13), # Moseslake - Microsoft Corporation
    IPFilterRule(*parse_ip('40.76.0.0'), 18), # Boydton - Microsoft Corporation
    IPFilterRule(*parse_ip('52.160.0.0'), 21), # Boydton - Microsoft Corporation
    
    # Random bot
    IPFilterRule(*parse_ip('171.244.0.0'), 16), # Hochiminh - Viettel Group
    
    # CMS-Checker
    # "Mozilla/5.0 (compatible; CMS-Checker/1.0; +https://example.com)"
    IPFilterRule(*parse_ip('34.125.192.0'), 12), # Lasvegas - Google LLC
    IPFilterRule(*parse_ip('34.46.0.0'), 16), # Councilbluffs - Google LLC
    
    # Google bot
    # "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.183 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    IPFilterRule(*parse_ip('66.249.64.0'), 12), # Oklahoma - Google LLC
    
    
    # Scraper openai
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot"
    # GPTBot
    # "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)"
    IPFilterRule(*parse_ip('104.208.0.0'), 19), # Sanantonio - Microsoft Corporation
    IPFilterRule(*parse_ip('20.160.0.0'), 20), # Phoenix - Microsoft Corporation
    IPFilterRule(*parse_ip('20.160.0.0'), 20), # Phoenix - Microsoft Corporation
    IPFilterRule(*parse_ip('4.224.0.0'), 20), # Phoenix - Microsoft Corporation
    
    # sindresorhus # others
    # "Mozilla/5.0 AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/605.1.15
    # "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36"
    IPFilterRule(*parse_ip('100.24.0.0'), 19), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('3.224.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('18.232.0.0'), 18), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('98.80.0.0'), 19), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('18.208.0.0'), 21), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('107.20.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('13.216.0.0'), 19), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('174.129.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('18.204.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('18.208.0.0'), 21), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('18.232.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('184.72.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('184.72.96.0'), 13), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('204.236.224.0'), 13), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('23.20.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('23.22.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('3.208.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('3.80.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('34.192.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('34.224.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('35.168.0.0'), 19), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('44.192.0.0'), 21), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('50.16.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('50.17.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('50.19.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.0.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.2.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.20.0.0'), 18), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.20.0.0'), 18), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.200.0.0'), 19), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.20.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.44.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.4.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.54.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.70.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.72.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('52.86.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.144.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.152.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.156.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.160.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.164.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.166.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.172.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.174.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.196.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.204.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.208.0.0'), 19), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.210.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.211.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.224.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.226.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.234.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.236.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.236.64.0'), 14), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.242.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.80.0.0'), 20), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.84.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.86.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.88.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.90.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.92.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('75.101.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('75.101.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('98.80.0.0'), 19), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.90.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.90.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.90.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('43.166.224.0'), 13), # Ashburn - Amazon Technologies Inc.
    
    # Petalbot
    # "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)"
    IPFilterRule(*parse_ip('114.119.128.0'), 13), # Singapore - HUAWEI CLOUDS
    
    # Yandex
    # "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
    IPFilterRule(*parse_ip('95.108.128.0'), 15), # Moscow - YANDEX LLC
    
    # Facebook
    # "meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)"
    IPFilterRule(*parse_ip('57.141.0.0'), 8), # Sterling - Facebook, Inc.
    
    # tries to login with php
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_1; rv:120.0) Gecko/20100101 Firefox/120.0"
    IPFilterRule(*parse_ip('141.98.11.0'), 8), # Vilnius - UAB Host Baltic
    IPFilterRule(*parse_ip('91.224.92.0'), 8), # Vilnius - UAB Host Baltic
])


def check_is_ip_banned():
    return match_ip_to_structure(IP_MATCHER_STRUCTURE, *parse_ip(request.remote_addr))


@WEBAPP.before_request
def block_bots():
    if check_is_user_agent_banned():
        return make_response('I am a teapot', 418)
    
    if check_is_ip_banned():
        return make_response('You are a teapot', 419)


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
