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
    # AdsBot Mobile Web -> AdsBot-Google-Mobile | AdsBot-Google
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
    'cms-checker',
    
    # amazon
    'mozilla/5.0 applewebkit/605.1.15 (khtml, like gecko) chrome/139.0.0.0 safari/605.1.15',
    
    # blex
    'mozilla/5.0 (compatible; blexbot/1.0; +https://help.seranking.com/en/blex-crawler)',
    
    # tiktok
    (
        'mozilla/5.0 (linux; android 5.0) applewebkit/537.36 (khtml, like gecko) mobile safari/537.36 '
        '(compatible; tiktokspider; ttspider-feedback@tiktok.com)'
    ),
    
    # Alibaba
    (
        'mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) '
        'chrome/109.0.0.0 safari/537.36'
    ),
    
    # Google - notion
    'mozilla/5.0 (x11; linux x86_64; rv:135.0) gecko/20100101 firefox/135.0',
    
    # netcup GmbH 
    (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/100.0.7793.533 '
        'safari/537.36'
    ),
    (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/100.0.8521.617 '
        'safari/537.36'
    ),
    
    # gigenet
    (
        'mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/140.0.0.0 '
        'safari/537.36'
    ),
    
    # proxy
    (
        'mozilla/5.0 (linux; android 5.0; sm-g900p build/lrx21t) applewebkit/537.36 (khtml, like gecko) '
        'chrome/39.0.3861.1048 mobile safari/537.36'
    ),
    
    # hostroyale
    (
        'mozilla/5.0 (iphone; cpu iphone os 11_0 like mac os x) applewebkit/537.36 (khtml, like gecko) '
        'chrome/54.0.6116.1453 mobile safari/537.36'
    ),
    
    # huawei clouds
    (
        'mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/123.0.0.0 '
        'safari/537.36'
    ),
    
    # at&t
    (
        'mozilla/5.0 (iphone; cpu iphone os 11_0 like mac os x) applewebkit/537.36 (khtml, like gecko) '
        'chrome/60.0.3527.1389 mobile safari/537.36'
    ),
    
    # comcast cable communications
    (
        'mozilla/5.0 (linux; android 5.0; sm-g900p build/lrx21t) applewebkit/537.36 (khtml, like gecko) '
        'chrome/49.0.6450.1934 mobile safari/537.36'
    ),
    
    # Charter communications
    (
        'mozilla/5.0 (linux; android 6.0; nexus 5 build/mra58n) applewebkit/537.36 (khtml, like gecko) '
        'chrome/47.0.5862.1343 mobile safari/537.36'
    ),
    
    # Leibniz-Rechenzentrum
    (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/103.0.5060.134 '
        'safari/537.36'
    ),
    
    # Deutsche telekom
    (
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/44.0.4281.1601 Mobile Safari/537.36'
    ),
    
    # Claro NXT Telecomunicacoes Ltda 
    (
        'mozilla/5.0 (macintosh; intel mac os x 10_7_3) applewebkit/537.36 (khtml, like gecko, mediapartners-google) '
        'chrome/77.0.3865.99 safari/537.36'
    ),
    
    # amazon crawler?
    'mozilla/5.0 (compatible; crawler)'
    
    # TruffleHog
    'trufflehog'
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
    # They try to request various urls getting always 404 lol,
    # I dont use any shitty js framework that they could get into.
    IPFilterRule(*parse_ip('118.193.44.0'), 8), # Hongkong - UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED
    IPFilterRule(*parse_ip('152.32.192.0'), 8), # Hongkong - UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED
    IPFilterRule(*parse_ip('40.68.0.0'), 18), # Dublin - Microsoft Corporation
    
    # Tries to access the site through rpc
    IPFilterRule(*parse_ip('113.96.0.0'), 20), # Shenzhen - CHINANET Guangdong province network
    
    # Tries to request Wordpress Blog login page (and then login), for real its not a wordpress site
    IPFilterRule(*parse_ip('34.64.208.0'), 12), # Seoul - Google Asia Pacific Pte. Ltd.
    IPFilterRule(*parse_ip('144.91.118.0'), 9), # Frankfurt - Contabo GmbH
    
    # Tries to request git configuration
    IPFilterRule(*parse_ip('34.122.224.0'), 12), # Councilbluffs - Google LLC
    IPFilterRule(*parse_ip('34.16.0.0'), 15), # Councilbluffs - Google LLC
    
    # Tries to request env variable file & redirect to google???
    IPFilterRule(*parse_ip('79.110.62.0'), 8), # Frankfurt - Vecna Hosting Limited
    
    # Tries to request env variable file
    IPFilterRule(*parse_ip('78.153.140.0'), 8), # London - HOSTGLOBAL.PLUS LTD
    IPFilterRule(*parse_ip('45.148.10.0'), 8), # Amsterdam - TECHOFF SRV LIMITED
    IPFilterRule(*parse_ip('45.139.104.0'), 10), # Frankfurtammain - 49.3 Networking LLC
    
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
    
    # spams | https://coder.social | tries JS vulnerabilities
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    IPFilterRule(*parse_ip('47.82.8.0'), 10), # Sanmateo - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.238.0.0'), 16), # HonKong - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.242.0.0'), 16), # HonKong - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.243.0.0'), 16), # HonKong - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('8.210.0.0'), 15), # HonKong - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.88.64.0'), 14), # Losangeles - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.251.0.0'), 14), # Losangeles - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.89.192.0'), 13), # Losangeles - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('8.210.128.0'), 15), # HonKong - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.254.64.0'), 14), # Losangeles - Alibaba (US) Technology Co., Ltd.
    IPFilterRule(*parse_ip('47.88.0.0'), 14), # Losangeles - Alibaba (US) Technology Co., Ltd.
    
    
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
    
    # Notion
    # "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"
    IPFilterRule(*parse_ip('34.174.0.0'), 15), # Dallas - Google LLC
    
    # Scraper openai
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot"
    # GPTBot
    # "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)"
    IPFilterRule(*parse_ip('104.208.0.0'), 19), # Sanantonio - Microsoft Corporation
    IPFilterRule(*parse_ip('20.160.0.0'), 20), # Phoenix - Microsoft Corporation
    IPFilterRule(*parse_ip('20.160.0.0'), 20), # Phoenix - Microsoft Corporation
    IPFilterRule(*parse_ip('4.224.0.0'), 20), # Phoenix - Microsoft Corporation
    
    # sindresorhus # others
    # "Mozilla/5.0 AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/605.1.15"
    # "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36"
    # "Mozilla/5.0 (compatible; crawler)"
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
    IPFilterRule(*parse_ip('184.73.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.221.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('107.23.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('184.72.64.0'), 13), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('107.22.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('107.21.64.0'), 14), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('35.153.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.198.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('107.21.128.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('50.19.0.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('54.237.0.0'), 16), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('107.23.0.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('107.23.0.0'), 15), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('13.214.0.0'), 17), # Singapore - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('18.142.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('18.140.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('18.136.0.0'), 16), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('3.0.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('13.250.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('18.138.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('122.248.192.0'), 14), # Singapore - Amazon Web Services, Elastic Compute Cloud, EC2, SG
    IPFilterRule(*parse_ip('52.220.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('52.74.0.0'), 16), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('13.228.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('46.137.224.0'), 13), # Singapore - AMAZON SIN
    IPFilterRule(*parse_ip('13.212.0.0'), 17), # Singapore - Amazon Data Services Singapore
    IPFilterRule(*parse_ip('54.254.0.0'), 15), # Singapore - Amazon Data Services Japan
    
    
    # Petalbot
    # "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)"
    IPFilterRule(*parse_ip('114.119.128.0'), 13), # Singapore - HUAWEI CLOUDS
     
    
    # Yandex
    # "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
    IPFilterRule(*parse_ip('95.108.128.0'), 15), # Moscow - YANDEX LLC
    IPFilterRule(*parse_ip('87.250.224.0'), 13), # Moscow - YANDEX LLC
    IPFilterRule(*parse_ip('5.255.192.0'), 14), # Moscow - YANDEX LLC
    IPFilterRule(*parse_ip('213.180.192.0'), 13), # Moscow - YANDEX LLC
    
    # Facebook
    # "meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)"
    # "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
    IPFilterRule(*parse_ip('57.141.0.0'), 8), # Sterling - Facebook, Inc.
    IPFilterRule(*parse_ip('69.63.184.0'), 11), # Huntsville - Facebook, Inc.
    IPFilterRule(*parse_ip('69.171.240.0'), 12), # Ashburn - Facebook, Inc.
    IPFilterRule(*parse_ip('173.252.64.0'), 13), # Fortworth - Facebook, Inc.
    IPFilterRule(*parse_ip('69.171.224.0'), 14), # Prineville - Facebook, Inc.
    
    # tries to login with php
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_1; rv:120.0) Gecko/20100101 Firefox/120.0"
    IPFilterRule(*parse_ip('141.98.11.0'), 8), # Vilnius - UAB Host Baltic
    IPFilterRule(*parse_ip('91.224.92.0'), 8), # Vilnius - UAB Host Baltic
    
    # blex
    # "Mozilla/5.0 (compatible; BLEXBot/1.0; +https://help.seranking.com/en/blex-crawler)"
    IPFilterRule(*parse_ip('37.27.0.0'), 16), # Helsinki - Hetzner Online GmbH
    
    # Trying to hack python with php
    IPFilterRule(*parse_ip('185.177.72.0'), 8), # Paris - FBW NETWORKS SAS
    
    # Tencent
    # "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    IPFilterRule(*parse_ip('43.130.0.0'), 14), # Santaclara - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('43.156.192.0'), 14), # Singapore - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('43.165.64.0'), 14), # Santaclara - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('117.33.128.0'), 14), # Xian - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('43.157.128.0'), 14), # Saopaulo - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('49.51.200.0'), 10), # Santaclara - Tencent cloud computing (Beijing) Co., Ltd.
    IPFilterRule(*parse_ip('101.33.52.0'), 10), # Tokyo - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('101.88.0.0'), 19), # Shanghai - CHINANET SHANGHAI PROVINCE NETWORK (likely a proxy)
    IPFilterRule(*parse_ip('43.153.64.0'), 14), # Santaclara - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('43.143.192.0'), 14), # Beijing - Tencent Cloud Computing (Beijing) Co., Ltd
    IPFilterRule(*parse_ip('170.106.164.0'), 14), # Santaclara - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('170.106.192.0'), 11), # Santaclara - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('43.157.0.0'), 14), # Frankfurtammain - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('222.79.64.0'), 14), # Dongjie - CHINANET fujian province network
    IPFilterRule(*parse_ip('119.28.140.0'), 9), # Hongkong - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('43.173.128.0'), 14), # Singapore - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('43.153.192.0'), 14), # Singapore - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('49.51.46.0'), 9), # Santaclara - Tencent Building, Kejizhongyi Avenue
    
    
    # The Lewin Group
    IPFilterRule(*parse_ip('128.241.235.0'), 10), # Losangeles - The Lewin Group
    
    # Tiktok
    # "Mozilla/5.0 (Linux; Android 5.0) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; TikTokSpider; ttspider-feedback@tiktok.com)"
    IPFilterRule(*parse_ip('47.128.0.0'), 18), # Singapore - Amazon.com, Inc.
    
    # netcup GmbH
    IPFilterRule(*parse_ip('5.45.108.0'), 10), # Nürnberg - netcup GmbH
    
    # censys
    # "Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)"
    IPFilterRule(*parse_ip('206.168.34.0'), 8), # Chicago - Censys, Inc.
    
    # Kingsoft
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    IPFilterRule(*parse_ip('104.250.52.0'), 10), # Singapore - Kingsoft Cloud Corporation Limited
    
    # semrushbot
    # "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)"
    IPFilterRule(*parse_ip('85.208.96.0'), 10), # Leesburg - SEMrush CY LTD
    
    # GigeNET
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    IPFilterRule(*parse_ip('85.208.96.0'), 10), # Ashburn - GigeNET
    
    # proxy crawler
    # "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.3861.1048 Mobile Safari/537.36"
    IPFilterRule(*parse_ip('104.223.93.0'), 10), # Losangeles - HostRoyale Technologies Pvt Ltd
    IPFilterRule(*parse_ip('89.36.237.0'), 10), # Kotabharu - The Constant Company, LLC
    IPFilterRule(*parse_ip('58.68.208.0'), 12), # Rioclaro - M247 Europe SRL
    
    # hostroyale
    # "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.6116.1453 Mobile Safari/537.36"
    IPFilterRule(*parse_ip('204.152.199.0'), 10), # Moscow - HostRoyale Technologies Pvt Ltd
    IPFilterRule(*parse_ip('93.180.224.0'), 8), # Dallas - HostRoyale Technologies Pvt Ltd
    IPFilterRule(*parse_ip('192.161.59.0'), 8), # Mumbai - HostRoyale Technologies Pvt Ltd
    
    
    # huawei clouds
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    IPFilterRule(*parse_ip('190.92.224.0'), 13), # Hongkong - HUAWEI CLOUDS
    IPFilterRule(*parse_ip('166.108.224.0'), 12), # Singapore - HUAWEI CLOUDS
    
    # AT&T Enterprises, LLC
    IPFilterRule(*parse_ip('71.136.128.0'), 15), # Arlington - AT&T Enterprises,
    IPFilterRule(*parse_ip('99.96.0.0'), 19), # Royalpalmbeach - AT&T Enterprises, LLC
    
    # Comcast Cable Communications, LLC 
    IPFilterRule(*parse_ip('76.16.0.0'), 20), # Concord - Comcast Cable Communications, LLC
    
    # Charter Communications Inc
    IPFilterRule(*parse_ip('70.63.64.0'), 14), # Charlotte - Charter Communications Inc
    
    # Leibniz-Rechenzentrum 
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"
    IPFilterRule(*parse_ip('138.246.0.0'), 16), # Munich - Leibniz-Rechenzentrum
    
    # Deutsche Telekom AG 
    # "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.4281.1601 Mobile Safari/537.36"
    IPFilterRule(*parse_ip('87.128.0.0'), 22), # Altenburg - Deutsche Telekom AG
    
    # Wes-Tex Telecommunications LTD
    IPFilterRule(*parse_ip('69.55.192.0'), 22), # Stanton - Wes-Tex Telecommunications LTD
    
    # TruffleHog
    IPFilterRule(*parse_ip('35.168.0.0'), 19), # Ashburn - Amazon.com, Inc.
    
    # wpbot
    IPFilterRule(*parse_ip('44.224.0.0'), 21), # Boardman - Amazon.com, Inc.
    
    # Claro NXT Telecomunicacoes Ltda 
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/537.36 (KHTML, like Gecko, Mediapartners-Google) Chrome/77.0.3865.99 Safari/537.36""
    IPFilterRule(*parse_ip('186.207.240.0'), 12), # Agudos - Claro NXT Telecomunicacoes Ltda
    
    # Endless spam
    IPFilterRule(*parse_ip('177.121.208.0'), 12), # Sãopaulo - TIM S/A
    IPFilterRule(*parse_ip('45.4.2.0'), 10), # Santiago - TLINK SPA
    IPFilterRule(*parse_ip('189.36.194.0'), 9), # Fortaleza - ORN TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('113.189.192.0'), 12), # Tuyênquang - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('186.249.144.0'), 12), # Campinas - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('191.177.0.0'), 16), # Curitiba - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('86.210.128.0'), 15), # Muret - Orange S.A.
    IPFilterRule(*parse_ip('45.170.180.0'), 9), # Campinagrande - POINT TELECOM SERVIÇOS LTDA
    IPFilterRule(*parse_ip('14.191.96.0'), 12), # Biênhòa - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('123.27.144.0'), 12), # Hanoi - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('177.221.182.0'), 8), # Formiga - MAP Piumhi Ltda - ME
    IPFilterRule(*parse_ip('186.132.0.0'), 18), # Adrogué - Telefonica de Argentina
    IPFilterRule(*parse_ip('14.186.128.0'), 12), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('113.190.224.0'), 12), # Hoànkiếm - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('177.220.176.0'), 12), # Curitiba - Ligga Telecomunicações S.A.
    IPFilterRule(*parse_ip('131.161.226.0'), 8), # Fortaleza - NEONET SERVICOS DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('14.169.208.0'), 12), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('189.61.0.0'), 15), # Brasília - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.19.160.0'), 12), # Maceió - BRISANET SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('201.148.244.0'), 10), # Caxiasdosul - Adylnet Telecom 
    IPFilterRule(*parse_ip('14.188.224.0'), 12), # Bắcgiang - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('213.230.114.0'), 9), # Tashkent - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('187.3.224.0'), 13), # Resende - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('168.181.128.0'), 8), # Sãomigueldoscampos -S.M.C Redes e Informatica LTDA
    IPFilterRule(*parse_ip('14.187.128.0'), 12), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('186.204.224.0'), 13), # Diadema - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('168.227.211.0'), 8), # Campogrande - 67 TELECOM
    IPFilterRule(*parse_ip('179.0.46.0'), 8), #  Flexeiras - JOSE MARCOS DA SILVA INFORMATICA ME
    IPFilterRule(*parse_ip('102.223.56.0'), 10), # Durban - AFRIHOST SP (PTY) LTD
    IPFilterRule(*parse_ip('189.113.64.0'), 10), # Novafriburgo - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('45.170.66.0'), 8), # Jacareí - VIVAS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.86.37.0'), 8), # Santaluzia - NET PREMIUM LTDA - ME
    IPFilterRule(*parse_ip('118.70.128.0'), 12), # Hanoi - FPT Telecom Company
    IPFilterRule(*parse_ip('138.94.130.138'), 8), # Barramansa - GL DUARTE MULTIMIDIA LTDA ME
    IPFilterRule(*parse_ip('186.226.49.0'), 8), # Guarapuava - LINE TELECOM LTDA
    IPFilterRule(*parse_ip('189.89.160.0'), 13), # Salvador - ITS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('138.185.40.0'), 8), # Pelotas - WordNet Internet Banda Larga
    IPFilterRule(*parse_ip('46.98.0.0'), 16), # Dnipro - TRADITIONAL LLC
    IPFilterRule(*parse_ip('14.225.64.0'), 8), # Hanoi - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('45.172.1.0'), 8), # Pontagrossa - FIBER GIGA PROVEDORES DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.82.128.0'), 11), # Sãopedrodaaldeia - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('45.191.85.0'), 8), # Buenosaires - ROMERO JOSE ALBERTO
    IPFilterRule(*parse_ip('123.21.16.0'), 12), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('179.97.128.0'), 14), # Sãobernardodocampo - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.97.128.0'), 14), # Sãobernardodocampo - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('45.165.18.0'), 9), # Montesclaros - NET MAIS SOLUCOES EM REDE LTDA - ME
    IPFilterRule(*parse_ip('110.39.163.0'), 8), # Deraghazikhan - National WiMAX/IMS environment
    IPFilterRule(*parse_ip('179.51.143.0'), 8), # Milagro - IN.PLANET S. A
    IPFilterRule(*parse_ip('190.60.62.0'), 8), # Barranquilla - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('14.169.96.0'), 12), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('179.181.64.0'), 12), # Portoalegre - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('45.237.1.0'), 8), # Corrente - LOUZEIRO & MORAIS LTDA
    IPFilterRule(*parse_ip('168.228.187.0'), 8), # Jataí - Abenet Provedora de Acesso a Internet LTDA
    IPFilterRule(*parse_ip('187.86.28.0'), 10), # Bomjesusdogalho - Fibron Telecom
    IPFilterRule(*parse_ip('45.176.73.0'), 8), # Riopomba - Plácido e Siqueira Som e Imagem LTDA-ME
    IPFilterRule(*parse_ip('177.11.187.0'), 8), # Franca - Multpontos Telecomunicações Ltda - ME
    IPFilterRule(*parse_ip('187.74.0.0'), 17), # Sãopaulo - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.129.216.0'), 10), # Portão - Bitcom Internet Provider LTDA
    IPFilterRule(*parse_ip('14.180.28.0'), 10), # Namđịnh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('200.124.249.0'), 8), # Guayaquil - Ecuadortelecom S.A.
    IPFilterRule(*parse_ip('113.179.208.0'), 12), # Ninhbình - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('179.63.128.0'), 8), # Sãopaulo - SIMPSON INTERNET VIA RADIO WI-FI - EIRELI
    IPFilterRule(*parse_ip('14.224.176.0'), 12), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('188.70.0.0'), 9), # Alfarwānīyah - NATIONAL MOBILE TELECOMMUNICATIONS COMPANY K.S.C.P.
    IPFilterRule(*parse_ip('45.235.197.0'), 8), # Feiradesantana - Rios Network
    IPFilterRule(*parse_ip('123.27.64.0'), 12), # Tuyênquang - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('132.255.200.0'), 8), # Laplata - SURPORAIRE SA
    IPFilterRule(*parse_ip('45.4.144.0'), 10), # Santacruzdocapibaribe - Rede.com Telecom Ltda - ME
    IPFilterRule(*parse_ip('38.51.35.0'), 8), # Quito - PUNTONET S.A.
    IPFilterRule(*parse_ip('82.114.73.0'), 8), # Pejë - Kujtesa Net Sh.p.k.
    IPFilterRule(*parse_ip('113.191.112.0'), 12), # Bắcninh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('201.131.182.0'), 9), # Pousoredondo - Sincroniza Digital LTDA
    IPFilterRule(*parse_ip('45.165.243.0'), 8), # Ortigueira - City Turbo Telecom
    IPFilterRule(*parse_ip('123.25.112.0'), 12), # Tuyênquang - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('177.128.146.0'), 8), # Cerqueiracésar - ZAAZ PROVEDOR DE INTERNET E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.131.160.0'), 13), # Sãobernardodocampo - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('189.50.232.0'), 9), # Matão - PROCESS SOLUTIONS TECNOLOGIA DA INFORMAÇÃO LTDA
    IPFilterRule(*parse_ip('24.152.37.0'), 8), # Belohorizonte - MASTER DA WEB DATACENTER LTDA
    IPFilterRule(*parse_ip('113.183.176.0'), 12), # Bếntre - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('113.183.176.0'), 12), # Bếntre - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('131.196.150.0'), 8), # Belojardim - TELEINFOR COMERCIO E SERVIÇO LTDA-ME
    IPFilterRule(*parse_ip('14.231.224.0'), 12), # Hanoi - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('110.44.115.0'), 8), # Kathmandu - VIA NET COMMUNICATION LTD.
    IPFilterRule(*parse_ip('113.166.192.0'), 12), # Ðàlạt - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('17.128.0.0'), 23), # Leesburg - Apple Inc.
    IPFilterRule(*parse_ip('186.249.20.0'), 9), # Serrabranca - CARIRIWEB PROVEDORES DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.179.80.0'), 8), # Novohamburgo - Plus Networks
    IPFilterRule(*parse_ip('181.24.0.0'), 18), # Laplata - Telefonica de Argentina
    IPFilterRule(*parse_ip('187.44.176.0'), 12), # Salvador - ITS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('14.183.236.0'), 19), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('187.85.245.0'), 8), # Governadorvaladares - Ibituruna TV por assinatura S/C Ltda
    IPFilterRule(*parse_ip('189.29.192.0'), 13), # Diadema - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('190.100.0.0'), 16), # Santiago - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('191.222.64.0'), 14), # Goiânia - V tal
    IPFilterRule(*parse_ip('177.129.24.0'), 9), # Osório - VERO S.A
    IPFilterRule(*parse_ip('45.175.48.0'), 8), # Contagem - SPARKNET TELECOMUNICACOES EIRELI
    IPFilterRule(*parse_ip('190.89.0.0'), 8), # Franciscomorato - WORLD WIFI TELECOMUNICAÇÕES LTDA - ME
    IPFilterRule(*parse_ip('14.164.176.0'), 12), # Vũngtàu - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('177.149.64.0'), 12), # Manaus - TIM S/A
    IPFilterRule(*parse_ip('34.95.176.0'), 12), # Diadema - Google LLC
    IPFilterRule(*parse_ip('131.161.218.0'), 9), # Almirantetamandaré - NetBrasil Telecom LTDA
    IPFilterRule(*parse_ip('45.167.63.0'), 8), # Touros - PROXXIMA TELECOMUNICACOES SA
    IPFilterRule(*parse_ip('200.95.180.0'), 9), # Goianésia - Braudes e Sá Ltda
    IPFilterRule(*parse_ip('113.173.224.0'), 12), # Hochiminh - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('113.172.176.0'), 12), # Quậnmườimột - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('222.254.0.0'), 12), # Hanoi - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('45.70.202.0'), 8), # Quito - NEGOCIOS Y TELEFONIA NEDETEL S.A.
    IPFilterRule(*parse_ip('192.141.123.0'), 8), # Poções - Lincomfá Andrade Fontes
    IPFilterRule(*parse_ip('45.179.222.0'), 8), # Mangaratiba - 2 M TELECOM EIRELI
    IPFilterRule(*parse_ip('45.166.204.0'), 9), # Palhoça - VERO S.A
    IPFilterRule(*parse_ip('168.197.157.0'), 8), # Belohorizonte - UP NET TELECOM
    IPFilterRule(*parse_ip('177.234.234.0'), 8), # Quito - NEGOCIOS Y TELEFONIA NEDETEL S.A.
    IPFilterRule(*parse_ip('177.104.0.0'), 11), # Joinville - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('179.49.33.0'), 8), # Quito - PUNTONET S.A.
    IPFilterRule(*parse_ip('177.220.160.0'), 12), # Curitiba - Ligga Telecomunicações S.A.
    IPFilterRule(*parse_ip('14.240.0.0'), 12), # Biênhòa - Vietnam Posts and Telecommunications Group
    IPFilterRule(*parse_ip('179.172.0.0'), 17), # Sãopaulo - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('91.135.221.0'), 8), # Orël - MTS OJSC
    IPFilterRule(*parse_ip('90.156.162.0'), 8), # Tashkent - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('88.135.192.0'), 13), # Ivanofrankivsk - Uteam LTD
    IPFilterRule(*parse_ip('79.175.0.0'), 10), # Saintpetersburg - Quantum CJSC
    IPFilterRule(*parse_ip('69.224.0.0'), 18), # Losangeles - AT&T Enterprises, LLC
    IPFilterRule(*parse_ip('45.71.146.0'), 8), # Dionísiocerqueira - NetTri Telecom
    IPFilterRule(*parse_ip('45.71.122.0'), 8), # Dionísiocerqueira - AGRESTE TELECOMUNICAÇÕES EIRELI-ME
    IPFilterRule(*parse_ip('45.70.72.0'), 8), # Recife - Hilink Comunicações
    IPFilterRule(*parse_ip('45.70.34.0'), 9), # Caratinga - SIGNET INTERNET LTDA - EPP
    IPFilterRule(*parse_ip('45.70.148.0'), 10), # Caratinga - SH TELECOM LTDA
    IPFilterRule(*parse_ip('45.65.160.0'), 8), # Caruaru - Antonio Carlos Correia Filho Serv. de Telecom.-ME
    IPFilterRule(*parse_ip('45.6.35.0'), 8), # Osasco - ZAAZ PROVEDOR DE INTERNET E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.6.30.0'), 9), # Osasco - ZAAZ PROVEDOR DE INTERNET E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.237.72.0'), 9), # Riodejaneiro - WESTLINK TECNOLOGIA E COMUNICACAO LTDA. - ME
    IPFilterRule(*parse_ip('45.235.208.0'), 9), # Gravataí - schossler e silva ltda - me
    IPFilterRule(*parse_ip('45.235.164.0'), 8), # Delta - MATHEUS SCANDIUZE NEHME
    
    
])


def check_is_ip_banned():
    address = request.environ.get('HTTP_X_FORWARDED_FOR', None)
    if address is None:
        address = request.environ.get('REMOTE_ADDR', None)
        if address is None:
            return
    
    return match_ip_to_structure(IP_MATCHER_STRUCTURE, *parse_ip(address))


@WEBAPP.before_request
def block_bots():
    if check_is_ip_banned():
        return make_response('You are a teapot', 419)
    
    if check_is_user_agent_banned():
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
