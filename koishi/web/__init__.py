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
    # Try to explot any vulnerabilities
    IPFilterRule(*parse_ip('118.193.44.0'), 8), # Hongkong - UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED
    IPFilterRule(*parse_ip('152.32.192.0'), 8), # Hongkong - UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED
    IPFilterRule(*parse_ip('40.68.0.0'), 18), # Dublin - Microsoft Corporation
    IPFilterRule(*parse_ip('113.96.0.0'), 20), # Shenzhen - CHINANET Guangdong province network
    IPFilterRule(*parse_ip('34.64.208.0'), 12), # Seoul - Google Asia Pacific Pte. Ltd.
    IPFilterRule(*parse_ip('144.91.118.0'), 9), # Frankfurt - Contabo GmbH
    IPFilterRule(*parse_ip('34.122.224.0'), 12), # Councilbluffs - Google LLC
    IPFilterRule(*parse_ip('34.16.0.0'), 15), # Councilbluffs - Google LLC
    IPFilterRule(*parse_ip('35.194.192.0'), 12), # Taipei - Google LLC
    IPFilterRule(*parse_ip('79.110.62.0'), 8), # Frankfurt - Vecna Hosting Limited
    IPFilterRule(*parse_ip('78.153.140.0'), 8), # London - HOSTGLOBAL.PLUS LTD
    IPFilterRule(*parse_ip('45.148.10.0'), 8), # Amsterdam - TECHOFF SRV LIMITED
    IPFilterRule(*parse_ip('45.139.104.0'), 10), # Frankfurtammain - 49.3 Networking LLC
    IPFilterRule(*parse_ip('196.251.83.0'), 8), # Amsterdam - internet-security-cheapyhost
    IPFilterRule(*parse_ip('213.209.157.0'), 8), # Kerkrade - VIRTUALINE TECHNOLOGIES
    IPFilterRule(*parse_ip('118.212.0.0'), 16), # Nanchang - China Unicom Jiangxi province network
    IPFilterRule(*parse_ip('188.166.64.0'), 14), # Amsterdam - Digital Ocean, Inc.
    IPFilterRule(*parse_ip('206.81.16.0'), 12), # Amsterdam - Digital Ocean, Inc.
    IPFilterRule(*parse_ip('3.24.0.0'), 18), # Sydney - Amazon Corporate Services Pty Ltd
    IPFilterRule(*parse_ip('195.178.110.0'), 8), # Amsterdam - TECHOFF SRV LIMITED
    IPFilterRule(*parse_ip('2.57.122.0'), 8), # Timişoara - TECHOFF SRV LIMITED
    IPFilterRule(*parse_ip('45.130.202.0'), 9), # Frankfurtammain - Legaco Networks B.V.
    
    
    
    
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
    IPFilterRule(*parse_ip('107.21.0.0'), 14), # Ashburn - Amazon Technologies Inc.
    
    
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
    IPFilterRule(*parse_ip('43.155.128.0'), 14), # Seoul - Asia Pacific Network Information Center, Pty. Ltd.
    IPFilterRule(*parse_ip('43.166.128.0'), 14), # Ashburn - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('60.188.56.0'), 10), # Hangzhou - CHINANET-ZJ Taizhou node network
    IPFilterRule(*parse_ip('101.32.0.0'), 12), # Hongong - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('117.62.232.0'), 11), # Nanjing - CHINANET jiangsu province network
    IPFilterRule(*parse_ip('170.106.106.0'), 9), # Santaclara - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('124.156.224.0'), 12), # Tokyo - Asia Pacific Network Information Centre
    IPFilterRule(*parse_ip('43.164.192.0'), 14), # Sãopaulo - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('43.167.192.0'), 14), # Tokyo - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('114.80.0.0'), 16), # Shanghai - CHINANET SHANGHAI PROVINCE NETWORK
    IPFilterRule(*parse_ip('101.32.48.0'), 12), # Hongkong - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('43.130.224.0'), 13), # Tokyo - Asia Pacific Network Information Centre
    IPFilterRule(*parse_ip('43.163.0.0'), 15), # Singapore - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('43.173.0.0'), 13), # Singapore - ACEVILLE PTE.LTD.
    IPFilterRule(*parse_ip('119.28.100.0'), 9), # Singapore - Tencent cloud computing (Beijing) Co., Ltd.
    IPFilterRule(*parse_ip('129.226.196.0'), 10), # Singapore - Tencent Building, Kejizhongyi Avenue 
    
    
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
    
    # robots.txt
    IPFilterRule(*parse_ip('76.16.0.0'), 20), # Concord - Comcast Cable Communications, LLC
    IPFilterRule(*parse_ip('70.63.64.0'), 14), # Charlotte - Charter Communications Inc
    IPFilterRule(*parse_ip('138.246.0.0'), 16), # Munich - Leibniz-Rechenzentrum
    IPFilterRule(*parse_ip('87.128.0.0'), 22), # Altenburg - Deutsche Telekom AG
    IPFilterRule(*parse_ip('69.55.192.0'), 22), # Stanton - Wes-Tex Telecommunications LTD
    IPFilterRule(*parse_ip('173.2.0.0'), 17), # Bridgeport - Optimum Online (Cablevision Systems)
    IPFilterRule(*parse_ip('71.136.128.0'), 15), # Arlington - AT&T Enterprises,
    IPFilterRule(*parse_ip('99.96.0.0'), 19), # Royalpalmbeach - AT&T Enterprises, LLC
    IPFilterRule(*parse_ip('199.188.87.0'), 8), # Pooler - Clearwave Communications
    IPFilterRule(*parse_ip('47.144.0.0'), 19), # Menifee - Frontier Communications of America, Inc.
    IPFilterRule(*parse_ip('72.220.0.0'), 16), # Sandiego - Cox Communications
    IPFilterRule(*parse_ip('52.160.0.0'), 21), # Boydton - Microsoft Corporation
    IPFilterRule(*parse_ip('54.84.0.0'), 17), # Ashburn - Amazon Technologies Inc.
    IPFilterRule(*parse_ip('104.208.0.0'), 19), # Sanantonio - Microsoft Corporation
    IPFilterRule(*parse_ip('74.7.0.0'), 16), # Atlanta - Microsoft Corporation
    IPFilterRule(*parse_ip('66.249.64.0'), 12), # Monckscorner - Google LLC
    
    # TruffleHog
    IPFilterRule(*parse_ip('35.168.0.0'), 19), # Ashburn - Amazon.com, Inc.
    
    # wpbot
    IPFilterRule(*parse_ip('44.224.0.0'), 21), # Boardman - Amazon.com, Inc.
    
    # Endless spam
    IPFilterRule(*parse_ip('177.120.0.0'), 18), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('45.4.0.0'), 10), # Chile - TLINK SPA
    IPFilterRule(*parse_ip('189.36.192.0'), 12), # Brazil - ORN TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('113.176.0.0'), 20), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('186.249.128.0'), 13), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('191.176.0.0'), 19), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('86.210.0.0'), 16), # France - Orange S.A.
    IPFilterRule(*parse_ip('45.170.180.0'), 10), # Brazil - POINT TELECOM SERVIÇOS LTDA
    IPFilterRule(*parse_ip('14.160.0.0'), 21), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.24.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('177.221.176.0'), 11), # Brazil - WI-MAX INTERNET LTDA
    IPFilterRule(*parse_ip('186.128.0.0'), 19), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('177.220.128.0'), 14), # Brazil - Ligga Telecomunicações S.A.
    IPFilterRule(*parse_ip('131.161.224.0'), 10), # Brazil - NEONET SERVICOS DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('189.60.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.19.128.0'), 15), # Brazil - BRISANET SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('201.148.244.0'), 10), # Brazil - Adylnet Telecom
    IPFilterRule(*parse_ip('213.230.64.0'), 14), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('187.2.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('168.181.128.0'), 10), # Brazil - S.M.C Redes e Informatica LTDA
    IPFilterRule(*parse_ip('186.204.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('168.227.208.0'), 10), # Brazil - 67 TELECOM
    IPFilterRule(*parse_ip('179.0.44.0'), 10), # Brazil - JOSE MARCOS DA SILVA INFORMATICA ME
    IPFilterRule(*parse_ip('102.223.56.0'), 10), # South Africa - AFRIHOST SP (PTY) LTD
    IPFilterRule(*parse_ip('189.113.64.0'), 12), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('45.170.64.0'), 10), # Brazil - VIVAS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.86.36.0'), 10), # Brazil - NET PREMIUM LTDA - ME
    IPFilterRule(*parse_ip('118.70.128.0'), 15), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('138.94.128.0'), 10), # Brazil - GL DUARTE MULTIMIDIA LTDA ME
    IPFilterRule(*parse_ip('186.226.48.0'), 11), # Brazil - LINE TELECOM LTDA
    IPFilterRule(*parse_ip('189.89.128.0'), 14), # Brazil - ITS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('138.185.40.0'), 10), # Brazil - WordNet Internet Banda Larga
    IPFilterRule(*parse_ip('46.98.0.0'), 16), # Ukraine - TRADITIONAL LLC
    IPFilterRule(*parse_ip('14.225.0.0'), 16), # Vietnam - VIETNAM POSTS AND TELECOMMUNICATIONS GROUP
    IPFilterRule(*parse_ip('45.172.0.0'), 10), # Brazil - FIBER GIGA PROVEDORES DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.80.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('45.191.84.0'), 10), # Argentina - ROMERO JOSE ALBERTO
    IPFilterRule(*parse_ip('123.16.0.0'), 19), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('179.97.128.0'), 14), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('45.165.16.0'), 10), # Brazil - NET MAIS SOLUCOES EM REDE LTDA - ME
    IPFilterRule(*parse_ip('110.39.128.0'), 15), # Pakistan - National WiMAX/IMS environment
    IPFilterRule(*parse_ip('179.51.140.0'), 10), # Ecuador - IN.PLANET S. A
    IPFilterRule(*parse_ip('190.60.62.0'), 8), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('179.180.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('45.237.0.0'), 10), # Brazil - SUPRINET TELECOM
    IPFilterRule(*parse_ip('168.228.184.0'), 10), # Brazil - Abenet Provedora de Acesso a Internet LTDA
    IPFilterRule(*parse_ip('187.86.24.0'), 11), # Brazil - Fibron Telecom
    IPFilterRule(*parse_ip('45.176.72.0'), 10), # Brazil - Plácido e Siqueira Som e Imagem LTDA-ME
    IPFilterRule(*parse_ip('177.11.184.0'), 11), # Brazil - Multpontos Telecomunicações Ltda - ME
    IPFilterRule(*parse_ip('187.74.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.129.216.0'), 10), # Brazil - Bitcom Internet Provider LTDA
    IPFilterRule(*parse_ip('200.124.224.0'), 13), # Ecuador - Ecuadortelecom S.A.
    IPFilterRule(*parse_ip('179.63.128.0'), 9), # Brazil - SIMPSON INTERNET VIA RADIO WI-FI - EIRELI
    IPFilterRule(*parse_ip('14.224.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('188.70.0.0'), 17), # Kuwait - NATIONAL MOBILE TELECOMMUNICATIONS COMPANY K.S.C.P.
    IPFilterRule(*parse_ip('45.235.196.0'), 10), # Brazil - Rios Network
    IPFilterRule(*parse_ip('132.255.200.0'), 9), # Argentina - SURPORAIRE SA
    IPFilterRule(*parse_ip('45.4.144.0'), 10), # Brazil - Rede.com Telecom Ltda - ME
    IPFilterRule(*parse_ip('38.51.32.0'), 12), # Ecuador - PUNTONET S.A.
    IPFilterRule(*parse_ip('82.114.73.0'), 5), # Kosovo - Kujtesa Net Sh.p.k.
    IPFilterRule(*parse_ip('201.131.180.0'), 10), # Brazil - Sincroniza Digital LTDA
    IPFilterRule(*parse_ip('45.165.240.0'), 10), # Brazil - City Turbo Telecom
    IPFilterRule(*parse_ip('177.128.144.0'), 12), # Brazil - ZAAZ PROVEDOR DE INTERNET E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.131.160.0'), 13), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('189.50.224.0'), 13), # Brazil - PROCESS SOLUTIONS TECNOLOGIA DA INFORMAÇÃO LTDA
    IPFilterRule(*parse_ip('24.152.36.0'), 10), # Brazil - MASTER DA WEB DATACENTER LTDA
    IPFilterRule(*parse_ip('131.196.148.0'), 10), # Brazil - TELEINFOR COMERCIO E SERVIÇO LTDA-ME
    IPFilterRule(*parse_ip('14.228.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('110.44.112.0'), 12), # Nepal - VIA NET COMMUNICATION LTD.
    IPFilterRule(*parse_ip('113.166.0.0'), 17), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('17.128.0.0'), 17), # United States - Apple Inc.
    IPFilterRule(*parse_ip('186.249.16.0'), 11), # Brazil - CARIRIWEB PROVEDORES DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.179.80.0'), 10), # Brazil - Plus Networks
    IPFilterRule(*parse_ip('181.24.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('187.44.128.0'), 15), # Brazil - ITS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('187.85.245.0'), 8), # Brazil - Ibituruna TV por assinatura S/C Ltda
    IPFilterRule(*parse_ip('189.29.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('190.100.0.0'), 17), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('191.216.0.0'), 19), # Brazil - V tal
    IPFilterRule(*parse_ip('177.129.24.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('45.175.48.0'), 8), # Brazil - LIKEE FIBRA LTDA
    IPFilterRule(*parse_ip('190.89.0.0'), 10), # Brazil - WORLD WIFI TELECOMUNICAÇÕES LTDA - ME
    IPFilterRule(*parse_ip('177.148.0.0'), 18), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('34.95.128.0'), 15), # Brazil - Google LLC
    IPFilterRule(*parse_ip('131.161.216.0'), 10), # Brazil - NetBrasil Telecom LTDA
    IPFilterRule(*parse_ip('45.167.60.0'), 10), # Brazil - PROXXIMA TELECOMUNICACOES SA
    IPFilterRule(*parse_ip('200.95.180.0'), 10), # Brazil - Braudes e Sá Ltda
    IPFilterRule(*parse_ip('113.172.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.254.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('45.70.200.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('192.141.120.0'), 10), # Brazil - MVF NETWORK
    IPFilterRule(*parse_ip('45.179.220.0'), 10), # Brazil - unknown
    IPFilterRule(*parse_ip('45.166.204.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('168.197.156.0'), 10), # Brazil - UP NET TELECOM
    IPFilterRule(*parse_ip('177.234.232.0'), 11), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('177.104.0.0'), 12), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('179.49.0.0'), 14), # Ecuador - PUNTONET S.A.
    IPFilterRule(*parse_ip('14.240.0.0'), 20), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('179.172.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('91.135.216.0'), 11), # Russia - MTS OJSC
    IPFilterRule(*parse_ip('90.156.160.0'), 11), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('88.135.192.0'), 13), # Ukraine - Uteam LTD
    IPFilterRule(*parse_ip('79.175.0.0'), 13), # Russia - Quantum CJSC
    IPFilterRule(*parse_ip('69.224.0.0'), 18), # United States - AT&T Enterprises, LLC
    IPFilterRule(*parse_ip('45.71.144.0'), 10), # Brazil - NetTri Telecom
    IPFilterRule(*parse_ip('45.71.120.0'), 10), # Brazil - AGRESTE TELECOMUNICAÇÕES EIRELI-ME
    IPFilterRule(*parse_ip('45.70.72.0'), 10), # Brazil - Hilink Comunicações
    IPFilterRule(*parse_ip('45.70.32.0'), 10), # Brazil - SIGNET INTERNET LTDA - EPP
    IPFilterRule(*parse_ip('45.70.148.0'), 10), # Brazil - SH TELECOM LTDA
    IPFilterRule(*parse_ip('45.65.160.0'), 10), # Brazil - Antonio Carlos Correia Filho Serv. de Telecom.-ME
    IPFilterRule(*parse_ip('45.6.32.0'), 10), # Brazil - ZAAZ PROVEDOR DE INTERNET E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.6.28.0'), 10), # Brazil - SUPER SONIC TELECOM LTDA
    IPFilterRule(*parse_ip('45.237.72.0'), 10), # Brazil - WESTLINK TECNOLOGIA E COMUNICACAO LTDA. - ME
    IPFilterRule(*parse_ip('45.235.208.0'), 10), # Brazil - schossler e silva ltda - me
    IPFilterRule(*parse_ip('45.235.164.0'), 10), # Brazil - MATHEUS SCANDIUZE NEHME
    IPFilterRule(*parse_ip('45.236.104.0'), 10), # Ecuador - Eliana Vanessa Morocho Oña
    IPFilterRule(*parse_ip('181.51.32.0'), 13), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('212.1.64.0'), 8), # Ukraine - Joint Ukrainan-German Enterprise "INFOCOM" LLC
    IPFilterRule(*parse_ip('38.3.228.0'), 10), # Iraq - Horizon Scope Mobile Telecom WLL
    IPFilterRule(*parse_ip('170.83.144.0'), 10), # Brazil - ACESSANET TELECON LTDA
    IPFilterRule(*parse_ip('14.232.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('169.0.0.0'), 17), # South Africa - AFRIHOST SP (PTY) LTD
    IPFilterRule(*parse_ip('220.247.129.0'), 8), # Bangladesh - Techno Asia InfoTech Pvt. ltd
    IPFilterRule(*parse_ip('94.154.39.0'), 8), # Ukraine - Individual entrepreneur Dyachenko Valentina Ivanovna
    IPFilterRule(*parse_ip('91.218.100.0'), 10), # Russia - Lukyanov Evgeniy Vladimirovich PE
    IPFilterRule(*parse_ip('84.54.64.0'), 13), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('84.240.192.0'), 14), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('5.59.105.0'), 8), # Kazakhstan - TOO Telco Construction
    IPFilterRule(*parse_ip('49.7.64.0'), 14), # China - IDC, China Telecommunications Corporation
    IPFilterRule(*parse_ip('49.7.0.0'), 11), # China - IDC, China Telecommunications Corporation
    IPFilterRule(*parse_ip('49.7.128.0'), 15), # China - IDC, China Telecommunications Corporation
    IPFilterRule(*parse_ip('47.92.0.0'), 18), # China - Hangzhou Alibaba Advertising Co.,Ltd.
    IPFilterRule(*parse_ip('45.234.212.0'), 10), # Brazil - ÁGIL TECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.234.136.0'), 10), # Brazil - PRONTO FIBRA LTDA
    IPFilterRule(*parse_ip('45.233.76.0'), 10), # Brazil - Lopez Santos Sat Nit Telecomunicacoes LTDA
    IPFilterRule(*parse_ip('45.233.36.0'), 10), # Brazil - satynet telecom ltda -me
    IPFilterRule(*parse_ip('45.233.196.0'), 10), # Brazil - ALLREDE TELECOM LTDA
    IPFilterRule(*parse_ip('1.52.128.0'), 14), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('109.161.128.0'), 15), # Bahrain - ZAIN BAHRAIN B.S.C.
    IPFilterRule(*parse_ip('106.38.176.0'), 11), # China - IDC, China Telecommunications Corporation
    IPFilterRule(*parse_ip('111.12.0.0'), 17), # China - China Mobile Communications Group Co., Ltd.
    IPFilterRule(*parse_ip('114.248.0.0'), 18), # China - China Unicom Beijing Province Network
    IPFilterRule(*parse_ip('39.156.0.0'), 16), # China - China Mobile Communications Group Co., Ltd.
    IPFilterRule(*parse_ip('45.233.112.0'), 10), # Brazil - NKM RAMOS INFORMATICA LTDA
    IPFilterRule(*parse_ip('45.230.96.0'), 10), # Brazil - JARDIMNET SERVICOS DE INFORMATICA E REDES
    IPFilterRule(*parse_ip('45.230.8.0'), 10), # Argentina - Gimenez Pedro Santiago (Clorindaconectada)
    IPFilterRule(*parse_ip('45.229.4.0'), 10), # Ecuador - MENA CORNEJO HECTOR ELIAS (TECMESH)
    IPFilterRule(*parse_ip('45.229.152.0'), 10), # Brazil - CONECTELL TELECOM
    IPFilterRule(*parse_ip('45.228.44.0'), 10), # Brazil - PROVEDORES SERVICO EQUIPAMENTO NIVE NET EIRELI
    IPFilterRule(*parse_ip('45.228.188.0'), 10), # Argentina - OBERCOM S.R.L.
    IPFilterRule(*parse_ip('45.228.164.0'), 10), # Brazil - FLASHNET EMPREENDIMENTOS LTDA
    IPFilterRule(*parse_ip('45.227.216.0'), 10), # Argentina - ZE.NET WISP SRL
    IPFilterRule(*parse_ip('45.227.112.0'), 10), # Brazil - ULTRANET RS
    IPFilterRule(*parse_ip('45.226.216.0'), 10), # Brazil - Ideal Network Informatica Ltda ME
    IPFilterRule(*parse_ip('45.225.168.0'), 10), # Brazil - Nicnet S.A.
    IPFilterRule(*parse_ip('45.221.12.0'), 10), # South Africa - BETHNET cc
    IPFilterRule(*parse_ip('45.188.88.0'), 10), # Brazil - IMPERTECH Telecom
    IPFilterRule(*parse_ip('45.186.212.0'), 10), # Brazil - Out Service Telecom Serviços Eireli
    IPFilterRule(*parse_ip('45.184.76.0'), 10), # Brazil - RONILSON SILVA SANTANA
    IPFilterRule(*parse_ip('45.183.88.0'), 10), # Brazil - JECONIAS ARAUJO SILVA - EPP
    IPFilterRule(*parse_ip('45.182.42.0'), 8), # Brazil - FIBERLINK NETWORK
    IPFilterRule(*parse_ip('45.181.36.0'), 10), # Brazil - STALKER ENGENHARIA EIRELI
    IPFilterRule(*parse_ip('45.181.132.0'), 10), # Brazil - LUC FIBRA
    IPFilterRule(*parse_ip('45.180.91.0'), 8), # Brazil - OPTIMUS FIBER TELECOM LTDA
    IPFilterRule(*parse_ip('45.179.132.0'), 10), # Brazil - SUPERNETMAIS TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('45.177.208.0'), 10), # Brazil - Fronteira Internet
    IPFilterRule(*parse_ip('45.177.204.0'), 10), # Paraguay - RODRIGUEZ PAEZ HUGO HERNAN (TELNET PARAGUAY)
    IPFilterRule(*parse_ip('45.175.140.0'), 10), # Argentina - BOCA ROJA S.A.
    IPFilterRule(*parse_ip('45.172.180.0'), 10), # Brazil - MUVNET TELECOM
    IPFilterRule(*parse_ip('45.170.112.0'), 10), # Brazil - S.P. TELECOM LTDA
    IPFilterRule(*parse_ip('45.169.216.0'), 10), # Brazil - Jequie Telecom Servicos Ltda.
    IPFilterRule(*parse_ip('45.168.236.0'), 10), # Mexico - Wantelco SAS de CV
    IPFilterRule(*parse_ip('45.168.168.0'), 10), # Brazil - WEBLINK TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('45.168.156.0'), 10), # Brazil - MIO TELECOM LTDA
    IPFilterRule(*parse_ip('45.167.220.0'), 10), # Argentina - MAGDALENA VIRTUAL S.A.
    IPFilterRule(*parse_ip('45.167.188.0'), 10), # Brazil - CENTRO SUL TELECOM INFORMATICAEIRELIME
    IPFilterRule(*parse_ip('45.166.244.0'), 10), # Brazil - G.V.R. TELECOMUNICAÇÕES E SERVIÇOS LTDA - ME
    IPFilterRule(*parse_ip('45.166.188.0'), 10), # Brazil - Falcon Net
    IPFilterRule(*parse_ip('45.163.200.0'), 10), # Brazil - Turbonet Telecom Ltda ME
    IPFilterRule(*parse_ip('45.163.172.0'), 10), # Brazil - RG Correa Telecomunicaçoes
    IPFilterRule(*parse_ip('45.162.56.0'), 10), # Brazil - L.L Informatica LTDA - ME
    IPFilterRule(*parse_ip('45.160.192.0'), 10), # Brazil - Estrelas Internet Ltda
    IPFilterRule(*parse_ip('45.143.30.0'), 8), # Iraq - Noor Al-Bedaya for General Trading, agricultural investments, Technical production and distribution, internet services, general services, Information technology and software Ltd
    IPFilterRule(*parse_ip('43.246.220.0'), 10), # Pakistan - Ebone Network (PVT.) Limited
    IPFilterRule(*parse_ip('41.56.0.0'), 16), # South Africa - RAIN GROUP HOLDINGS (PTY) LTD
    IPFilterRule(*parse_ip('41.232.0.0'), 19), # Egypt - TE-AS
    IPFilterRule(*parse_ip('41.214.0.0'), 11), # Senegal - SONATEL-AS Autonomous System
    IPFilterRule(*parse_ip('41.193.244.0'), 10), # South Africa - Vox Telecom Ltd
    IPFilterRule(*parse_ip('41.132.0.0'), 14), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('41.96.0.0'), 20), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('39.40.0.0'), 19), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('38.92.20.0'), 9), # Venezuela - INVERSIONES ABDO 77, C.A.
    IPFilterRule(*parse_ip('38.56.81.0'), 8), # Brazil - costa & rodrigues serviço de telecomunicações ltda
    IPFilterRule(*parse_ip('38.41.0.0'), 13), # Venezuela - MDS TELECOM C.A.
    IPFilterRule(*parse_ip('95.32.64.0'), 13), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('95.26.0.0'), 17), # Russia - PJSC "Vimpelcom"
    IPFilterRule(*parse_ip('102.156.0.0'), 18), # Tunisia - TOPNET
    IPFilterRule(*parse_ip('102.184.0.0'), 19), # Egypt - Vodafone Data
    IPFilterRule(*parse_ip('102.211.144.0'), 10), # Kenya - Unwired Communications Limited
    IPFilterRule(*parse_ip('102.40.0.0'), 19), # Egypt - TE-AS
    IPFilterRule(*parse_ip('103.112.148.0'), 10), # Bangladesh - Royalnet
    IPFilterRule(*parse_ip('103.133.140.0'), 10), # Bangladesh - APPLE NET
    IPFilterRule(*parse_ip('103.133.200.0'), 10), # Bangladesh - Antaranga Dot Com Ltd
    IPFilterRule(*parse_ip('103.134.254.0'), 9), # Bangladesh - City Net Communication
    IPFilterRule(*parse_ip('103.138.144.0'), 9), # Bangladesh - NEEF IT LIMITED
    IPFilterRule(*parse_ip('103.139.9.0'), 8), # Bangladesh - ICC Communication
    IPFilterRule(*parse_ip('103.140.166.0'), 8), # Bangladesh - Search IT
    IPFilterRule(*parse_ip('103.150.234.0'), 9), # Bangladesh - Quad Technology and Infotech Limited
    IPFilterRule(*parse_ip('103.158.158.0'), 9), # Bangladesh - IQ-TEL
    IPFilterRule(*parse_ip('103.158.62.0'), 9), # Bangladesh - Search IT
    IPFilterRule(*parse_ip('103.190.228.0'), 9), # Bangladesh - EARTH TELECOMMUNICATION (Pvt) LTD.
    IPFilterRule(*parse_ip('103.205.68.0'), 10), # Bangladesh - Mazeda Networks Limited
    IPFilterRule(*parse_ip('103.211.28.0'), 10), # Bangladesh - Business Network
    IPFilterRule(*parse_ip('103.24.16.0'), 9), # Bangladesh - C Net Broadband
    IPFilterRule(*parse_ip('103.74.230.0'), 8), # Bangladesh - Sustainable Development Networking Program
    IPFilterRule(*parse_ip('103.78.254.0'), 8), # Bangladesh - Spark Online
    IPFilterRule(*parse_ip('103.86.52.0'), 10), # Pakistan - Optix Pakistan (Pvt.) Limited
    IPFilterRule(*parse_ip('105.96.0.0'), 20), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('105.156.0.0'), 17), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('105.184.0.0'), 18), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('109.126.0.0'), 14), # Russia - Krivets Sergey Sergeevich
    IPFilterRule(*parse_ip('109.68.112.0'), 11), # Russia - MTS PJSC
    IPFilterRule(*parse_ip('111.119.192.0'), 14), # Singapore - HUAWEI CLOUDS
    IPFilterRule(*parse_ip('113.160.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('209.14.148.0'), 10), # Brazil - FIBRANET BRASIL
    IPFilterRule(*parse_ip('200.24.98.0'), 9), # Brazil - M B Telecom
    IPFilterRule(*parse_ip('113.164.128.0'), 15), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.165.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('103.150.69.0'), 8), # Bangladesh - Windstream Communication Limited
    IPFilterRule(*parse_ip('190.89.116.0'), 10), # Brazil - Jean Franck Ximenes
    IPFilterRule(*parse_ip('177.125.184.0'), 11), # Brazil - AZZA TELECOM SERVIÇOS EM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('95.190.0.0'), 17), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('94.207.0.0'), 13), # United Arab Emirates - Emirates Integrated Telecommunications Company PJSC
    IPFilterRule(*parse_ip('94.19.0.0'), 16), # Russia - SkyNet Ltd.
    IPFilterRule(*parse_ip('93.172.0.0'), 17), # Israel - Cellcom Fixed Line Communication L.P
    IPFilterRule(*parse_ip('93.123.128.0'), 15), # Russia - Information and Communication Technologies LLC
    IPFilterRule(*parse_ip('92.255.128.0'), 13), # Russia - JSC "ER-Telecom Holding"
    IPFilterRule(*parse_ip('92.253.0.0'), 15), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('92.124.0.0'), 18), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('92.118.182.0'), 8), # Venezuela - SOLUCION TV 555, C.A
    IPFilterRule(*parse_ip('91.240.96.0'), 9), # Ukraine - Luch, LLC
    IPFilterRule(*parse_ip('91.240.12.0'), 10), # Uzbekistan - Nano Telecom LLC
    IPFilterRule(*parse_ip('91.217.244.0'), 8), # Ukraine - TRK Sirius LTD
    IPFilterRule(*parse_ip('91.215.201.0'), 8), # Russia - Evroline severo-zapad LLC
    IPFilterRule(*parse_ip('91.205.199.0'), 8), # Armenia - Meganet HD LLC
    IPFilterRule(*parse_ip('86.96.0.0'), 18), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('83.170.192.0'), 14), # Ukraine - Kyivstar PJSC
    IPFilterRule(*parse_ip('82.129.23.0'), 8), # Iraq - SUPER CELL NETWORK FOR INTERNET SERVICES LTD
    IPFilterRule(*parse_ip('79.139.128.0'), 15), # Russia - PJSC Moscow city telephone network
    IPFilterRule(*parse_ip('79.106.0.0'), 16), # Albania - ONE ALBANIA SH.A.
    IPFilterRule(*parse_ip('77.83.38.0'), 8), # Bulgaria - AYOSOFT LTD
    IPFilterRule(*parse_ip('72.27.0.0'), 15), # Jamaica - FLOW
    IPFilterRule(*parse_ip('72.27.132.0'), 10), # Jamaica - FLOW
    IPFilterRule(*parse_ip('62.61.160.0'), 13), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('62.114.0.0'), 12), # Egypt - ETISALAT MISR
    IPFilterRule(*parse_ip('1.54.0.0'), 17), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('179.125.128.0'), 15), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('181.44.0.0'), 18), # Argentina - Telecentro S.A.
    IPFilterRule(*parse_ip('101.47.0.0'), 14), # Singapore - Byteplus Pte. Ltd.
    IPFilterRule(*parse_ip('125.162.0.0'), 16), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('125.164.0.0'), 18), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('171.245.0.0'), 16), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('175.107.211.0'), 8), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('177.192.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.87.104.0'), 10), # Brazil - SUPER CONNECT TELECOM LTDA
    IPFilterRule(*parse_ip('179.208.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.232.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.236.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('179.97.24.0'), 11), # Brazil - GABRIEL S S SERVICOS DE TELECOMUNICACOES EIRELI
    IPFilterRule(*parse_ip('181.119.84.0'), 10), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('187.109.128.0'), 13), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('191.7.192.0'), 13), # Brazil - ONLINE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('200.75.176.0'), 11), # Brazil - MICRORCIM PRO NET DO BRASIL INFORMÁTICA LTDA
    IPFilterRule(*parse_ip('201.210.128.0'), 14), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('45.175.112.0'), 10), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('102.210.120.0'), 10), # Angola - Finstar - Sociedade de Investimento e Participacoes S.A
    IPFilterRule(*parse_ip('116.71.160.0'), 13), # Pakistan - PTML-PK
    IPFilterRule(*parse_ip('95.212.0.0'), 16), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('95.182.104.0'), 10), # Kazakhstan - TOO Kainar-Media
    IPFilterRule(*parse_ip('95.181.234.0'), 9), # United Arab Emirates - M247 Europe SRL
    IPFilterRule(*parse_ip('95.158.184.0'), 10), # Bulgaria - Skynet Ltd
    IPFilterRule(*parse_ip('94.76.0.0'), 13), # Bahrain - STC BAHRAIN B.S.C CLOSED
    IPFilterRule(*parse_ip('94.230.228.0'), 10), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('94.124.166.0'), 8), # Ukraine - Therecom Ltd
    IPFilterRule(*parse_ip('92.96.0.0'), 18), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('91.229.160.0'), 10), # Uzbekistan - Net Television Ltd
    IPFilterRule(*parse_ip('91.225.148.0'), 10), # Russia - KETIS Ltd.
    IPFilterRule(*parse_ip('91.215.232.0'), 10), # Russia - SerDi TeleCom, LTD
    IPFilterRule(*parse_ip('89.198.0.0'), 17), # Iran - Mobile Communication Company of Iran PLC
    IPFilterRule(*parse_ip('89.148.0.0'), 14), # Bahrain - BEYON B.S.C.
    IPFilterRule(*parse_ip('89.147.80.0'), 12), # Serbia - Sat-Trakt D.O.O.
    IPFilterRule(*parse_ip('88.147.128.0'), 15), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('86.57.0.0'), 14), # Iran - Asiatech Data Transmission company
    IPFilterRule(*parse_ip('86.108.0.0'), 15), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('85.249.16.0'), 12), # Russia - PJSC "Vimpelcom"
    IPFilterRule(*parse_ip('85.187.200.0'), 10), # Bulgaria - Springs-Net EOOD
    IPFilterRule(*parse_ip('85.154.0.0'), 16), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('85.116.184.0'), 11), # Kazakhstan - FREEDOM TELECOM LLP
    IPFilterRule(*parse_ip('84.53.192.0'), 9), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('84.237.128.0'), 14), # Latvia - SIA Tet
    IPFilterRule(*parse_ip('83.136.238.0'), 9), # Russia - Malnet LTD.
    IPFilterRule(*parse_ip('81.24.92.0'), 10), # Russia - LTD "Erline"
    IPFilterRule(*parse_ip('45.7.212.0'), 10), # Brazil - Companhia Itabirana Telecomunicações Ltda
    IPFilterRule(*parse_ip('45.7.248.0'), 10), # Argentina - AGRUPACION DE PROVEEDORES DE SERVICIOS
    IPFilterRule(*parse_ip('45.7.76.0'), 10), # Brazil - Sevennet Telecom
    IPFilterRule(*parse_ip('45.70.56.0'), 10), # Ecuador - Gavilanes Parreño Irene Del Rocío
    IPFilterRule(*parse_ip('45.70.8.0'), 10), # Argentina - Ruben Oscar Mosso(INTERZONA WIFI)
    IPFilterRule(*parse_ip('45.71.160.0'), 10), # Brazil - Wind Telecomunicação do Brasil Ltda - ME
    IPFilterRule(*parse_ip('45.71.196.0'), 10), # Argentina - Infomaster S.R.L.
    IPFilterRule(*parse_ip('45.80.196.0'), 10), # Ecuador - TVDATOS S.C.C
    IPFilterRule(*parse_ip('46.118.0.0'), 17), # Ukraine - Kyivstar PJSC
    IPFilterRule(*parse_ip('46.160.192.0'), 14), # Russia - Information and Communication Technologies LLC
    IPFilterRule(*parse_ip('46.184.92.0'), 8), # Saudi Arabia - Vercara, LLC
    IPFilterRule(*parse_ip('46.248.192.0'), 13), # Jordan - Batelco Jordan
    IPFilterRule(*parse_ip('46.32.192.0'), 12), # Palestinian Territory - Mada Al-Arab General Services Company
    IPFilterRule(*parse_ip('47.30.0.0'), 17), # India - Reliance Jio Infocomm Limited
    IPFilterRule(*parse_ip('49.32.0.0'), 19), # India - Reliance Jio Infocomm Limited
    IPFilterRule(*parse_ip('49.40.0.0'), 18), # India - Reliance Jio Infocomm Limited
    IPFilterRule(*parse_ip('5.1.48.0'), 11), # Russia - "Russian company" LLC
    IPFilterRule(*parse_ip('5.140.0.0'), 15), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('5.155.0.0'), 16), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('5.175.148.0'), 10), # Iraq - SUPER CELL NETWORK FOR INTERNET SERVICES LTD
    IPFilterRule(*parse_ip('5.21.0.0'), 16), # Oman - Omani Qatari Telecommunication Company SAOC
    IPFilterRule(*parse_ip('5.246.0.0'), 16), # Saudi Arabia - Etihad Etisalat, a joint stock company
    IPFilterRule(*parse_ip('5.29.0.0'), 16), # Israel - Hot-Net internet services Ltd.
    IPFilterRule(*parse_ip('5.30.0.0'), 17), # United Arab Emirates - Emirates Integrated Telecommunications Company PJSC
    IPFilterRule(*parse_ip('5.36.0.0'), 17), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('5.45.128.0'), 12), # Jordan - Batelco Jordan
    IPFilterRule(*parse_ip('5.77.128.0'), 15), # Armenia - Ucom CJSC
    IPFilterRule(*parse_ip('50.60.0.0'), 17), # Saudi Arabia - Saudi Telecom Company JSC
    IPFilterRule(*parse_ip('58.186.192.0'), 14), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('58.187.0.0'), 16), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('59.153.100.0'), 10), # Bangladesh - Dot Internet
    IPFilterRule(*parse_ip('59.153.224.0'), 13), # Vietnam - MOBIFONE Corporation
    IPFilterRule(*parse_ip('62.217.128.0'), 13), # Azerbaijan - "AZERONLINE LTD" JOINT ENTERPRISE
    IPFilterRule(*parse_ip('65.20.128.0'), 15), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('66.181.160.0'), 13), # Mongolia - Univision LLC
    IPFilterRule(*parse_ip('72.255.40.0'), 11), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('77.245.96.0'), 12), # Kazakhstan - Jusan Mobile JSC
    IPFilterRule(*parse_ip('77.31.192.0'), 14), # Saudi Arabia - Saudi Telecom Company JSC
    IPFilterRule(*parse_ip('79.106.0.0'), 16), # Albania - ONE ALBANIA SH.A.
    IPFilterRule(*parse_ip('79.177.128.0'), 13), # Israel - "Bezeq"- THE ISRAEL TELECOMMUNICATION CORP. LTD.
    IPFilterRule(*parse_ip('81.182.0.0'), 17), # Hungary - Magyar Telekom Plc.
    IPFilterRule(*parse_ip('45.117.60.0'), 8), # Bangladesh - Paradise Technologies Limited
    IPFilterRule(*parse_ip('45.134.219.0'), 8), # Moldova - Interlink Comunicatii SRL
    IPFilterRule(*parse_ip('45.160.244.0'), 10), # Brazil - FLASH + TELECOM
    IPFilterRule(*parse_ip('45.161.252.0'), 10), # Brazil - VIVAS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.162.72.0'), 10), # Ecuador - ALCIVAR ESPIN DANNY ALEXANDER (OptiCom)
    IPFilterRule(*parse_ip('45.163.112.0'), 10), # Brazil - CONECT TELECOM LTDA - ME
    IPFilterRule(*parse_ip('45.163.132.0'), 10), # Brazil - HENRIQUE CANGUSSU ALVES
    IPFilterRule(*parse_ip('45.163.140.0'), 10), # Argentina - TELCAB ARGENTINA S.A
    IPFilterRule(*parse_ip('45.163.236.0'), 10), # Brazil - Intercol Serv de Aux a Internet eireli Me
    IPFilterRule(*parse_ip('45.163.36.0'), 10), # Argentina - COOPERATIVA DE SERVICIOS PUBLICOS TRANSITO LTDA.
    IPFilterRule(*parse_ip('45.164.244.0'), 10), # Brazil - ABQUECIA BARBOSA DA SILVA
    IPFilterRule(*parse_ip('45.166.204.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('45.166.68.0'), 10), # Brazil - BNET SOLUÇÕES EM INTERNET LTDA-ME
    IPFilterRule(*parse_ip('45.166.84.0'), 10), # Brazil - L E M TELECOMUNICAÇÕES LTDA -ME
    IPFilterRule(*parse_ip('45.167.104.0'), 10), # Brazil - GIGA NET INFORMATICA LTDA ME
    IPFilterRule(*parse_ip('45.167.184.0'), 10), # Brazil - FIBRA PRIME SERVICOS DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.167.32.0'), 10), # Brazil - Gilberto Leandro Peron e Cia Ltda
    IPFilterRule(*parse_ip('45.168.34.0'), 9), # Brazil - SpeedyNet Comunicacao Multimídia - Eireli
    IPFilterRule(*parse_ip('45.169.108.0'), 10), # Brazil - Link Speed
    IPFilterRule(*parse_ip('45.169.152.0'), 10), # Brazil - S-NET TELECOM ME
    IPFilterRule(*parse_ip('45.169.48.0'), 10), # Brazil - MEGACOM INTERNET LTDA
    IPFilterRule(*parse_ip('45.170.112.0'), 10), # Brazil - S.P. TELECOM LTDA
    IPFilterRule(*parse_ip('45.170.228.0'), 10), # Brazil - YES FIBRA TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.170.92.0'), 10), # Brazil - 3One Telecomunicações e Serviços - LTDA
    IPFilterRule(*parse_ip('45.171.172.0'), 10), # Brazil - ISP PREMIUM TELECOM S/A
    IPFilterRule(*parse_ip('45.171.184.0'), 10), # Brazil - TOPNET SERVIÇOS DE TELECOMU E MULTIMÍDIA EIRELI-ME
    IPFilterRule(*parse_ip('45.171.240.0'), 10), # Brazil - MaetingaNET Informática e Telecomunicações
    IPFilterRule(*parse_ip('45.171.44.0'), 10), # Brazil - M3 Net Fibra LTDA - ME
    IPFilterRule(*parse_ip('45.172.108.0'), 10), # Argentina - MORAN DOLORES GRACIELA
    IPFilterRule(*parse_ip('45.172.19.0'), 8), # Argentina - Wireless Provider
    IPFilterRule(*parse_ip('45.172.208.0'), 10), # Brazil - RIO CABLE TELECOM LTDA
    IPFilterRule(*parse_ip('45.172.252.0'), 10), # Brazil - DIRECT INTERNET LTDA
    IPFilterRule(*parse_ip('45.172.68.0'), 10), # Brazil - N-MULTIMIDIA TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('45.172.80.0'), 10), # Brazil - JustWeb Telecomunicações LTDA
    IPFilterRule(*parse_ip('45.173.164.0'), 10), # Brazil - Acelera Telecom
    IPFilterRule(*parse_ip('45.173.84.0'), 10), # Brazil - 74JC INFORMATICA EIRELI - ME
    IPFilterRule(*parse_ip('45.174.236.0'), 10), # Brazil - Luiza Maria de Souza Sindelar ME
    IPFilterRule(*parse_ip('45.175.148.0'), 10), # Argentina - NETCOMM ARGENTINA SRL
    IPFilterRule(*parse_ip('45.176.196.0'), 10), # Brazil - FiberNet Telecom
    IPFilterRule(*parse_ip('45.176.224.0'), 10), # Brazil - FLY NET SERVICOS EM TECNOLOGIA DA INFORMACAO LTDA
    IPFilterRule(*parse_ip('45.178.12.0'), 10), # Colombia - WALIX S.A.S.
    IPFilterRule(*parse_ip('45.178.92.0'), 10), # Brazil - UPNET TELECOM LTDA
    IPFilterRule(*parse_ip('45.179.100.0'), 10), # Brazil - ESM NET INFORMATICA
    IPFilterRule(*parse_ip('45.180.140.0'), 9), # Ecuador - DECERET CIA. LTDA.
    IPFilterRule(*parse_ip('45.180.148.0'), 10), # Brazil - MOV TELECOM SERVICOS DE PROVEDORES DE INTERNET LTD
    IPFilterRule(*parse_ip('45.182.140.0'), 9), # Venezuela - NETCOM PLUS, C.A
    IPFilterRule(*parse_ip('45.182.248.0'), 10), # Brazil - CABO FIBRA TELECOM
    IPFilterRule(*parse_ip('45.183.208.0'), 10), # Brazil - Next Provedor de Acesso a Internet Ltda Me
    IPFilterRule(*parse_ip('45.183.224.0'), 10), # Brazil - NETFLY LTDA ME
    IPFilterRule(*parse_ip('45.184.220.0'), 10), # Brazil - UAU TELECOM PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.184.44.0'), 10), # Brazil - DNET BRASIL LTDA
    IPFilterRule(*parse_ip('45.184.96.0'), 10), # Brazil - SUPORT TELECOM LTDA
    IPFilterRule(*parse_ip('45.185.160.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('45.185.172.0'), 10), # Brazil - P&N NET PROVEDOR
    IPFilterRule(*parse_ip('45.185.192.0'), 10), # Brazil - REDE ONLINE INTERNET LTDA
    IPFilterRule(*parse_ip('45.185.228.0'), 10), # Brazil - LINK TELECOM SERVIÇOS DE INTERNET LTDA.
    IPFilterRule(*parse_ip('45.186.192.0'), 10), # Brazil - Weclix Telecom S/A
    IPFilterRule(*parse_ip('45.186.248.0'), 10), # Brazil - GLFIBRA SERVICOS DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.187.232.0'), 10), # Brazil - Onitel Telecomunicacoes
    IPFilterRule(*parse_ip('45.187.4.0'), 10), # Venezuela - T.V ZAMORA, C.A.
    IPFilterRule(*parse_ip('45.187.96.0'), 10), # Brazil - FIBRANETBR TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('45.188.72.0'), 10), # Brazil - SPACENET PROVEDOR TELECOM LTDA
    IPFilterRule(*parse_ip('45.189.122.0'), 9), # Brazil - DIO SERVIÇOS DE COMUNICAÇAO MULTIMIDIA LTDA-ME
    IPFilterRule(*parse_ip('45.190.184.0'), 10), # Honduras - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('45.190.208.0'), 10), # Brazil - SC TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('45.191.152.0'), 10), # Brazil - Gerson Cerqueira
    IPFilterRule(*parse_ip('45.191.156.0'), 10), # Argentina - LOGANET SRL
    IPFilterRule(*parse_ip('45.191.248.0'), 9), # Brazil - filipe roberto dos santos-me
    IPFilterRule(*parse_ip('45.216.0.0'), 18), # Morocco - MEDITELECOM
    IPFilterRule(*parse_ip('45.220.0.0'), 13), # South Africa - Level 7 Wireless (Pty) Ltd
    IPFilterRule(*parse_ip('45.224.148.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('45.224.48.0'), 10), # Brazil - Une Telecom Ltda
    IPFilterRule(*parse_ip('45.224.80.0'), 10), # Brazil - FEGUI-DS NET TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('45.225.200.0'), 10), # Brazil - VELOZ NET SERVIÇOS E COMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('45.225.52.0'), 10), # Brazil - NAVEGADOR INTERNET LTDA ME
    IPFilterRule(*parse_ip('45.226.16.0'), 10), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('45.226.244.0'), 10), # Brazil - BRENO NOGUEIRA DOS REIS EIRELLI ME
    IPFilterRule(*parse_ip('45.226.72.0'), 10), # Brazil - Arias Telecomunicações Ltda
    IPFilterRule(*parse_ip('45.227.164.0'), 10), # Argentina - CENTENARO ADRIANO (ADRYANO TELECOM)
    IPFilterRule(*parse_ip('45.227.92.0'), 10), # Argentina - ANDROS-NET COMUNICACIONES S.R.L.
    IPFilterRule(*parse_ip('45.228.136.0'), 10), # Paraguay - FLYTEC TELECOM SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('45.228.16.0'), 10), # Argentina - COOPERATIVA DE AGUA , ENERGIA Y OTROS SERVICIOS COMUNITARIOS DE DOS DE MAYO LTDA
    IPFilterRule(*parse_ip('45.228.232.0'), 10), # Guatemala - INFINITUM S.A.
    IPFilterRule(*parse_ip('45.229.0.0'), 10), # Brazil - VIRTUALNET PROVEDORES LTDA ME
    IPFilterRule(*parse_ip('45.229.86.0'), 8), # Argentina - GABRIEL FRANCISCO ERBETTA Y MARIANO ANDRES CARRIZO RICHELET SOCIEDAD DE HECHO (TELNET SOLUCIONES)
    IPFilterRule(*parse_ip('45.229.88.0'), 10), # Brazil - NETFIBRA TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('45.230.228.0'), 10), # Brazil - Wagner Rafael Eckert
    IPFilterRule(*parse_ip('45.230.24.0'), 10), # Brazil - P4 TELECOM LTDA
    IPFilterRule(*parse_ip('45.231.166.0'), 9), # Brazil - Netsoluti Soluções em Informática e Internet Eirel
    IPFilterRule(*parse_ip('45.231.252.0'), 10), # Brazil - Elevalink Telecomunicações LTDA - ME
    IPFilterRule(*parse_ip('45.232.200.0'), 10), # Brazil - G3 Telecom EIRELI
    IPFilterRule(*parse_ip('45.232.220.0'), 10), # Brazil - JORGE L S MARTINS TELECOM INFORMATICA
    IPFilterRule(*parse_ip('45.232.4.0'), 10), # Brazil - Connections X Serv e Sist de Info LTDA EPP
    IPFilterRule(*parse_ip('45.232.76.0'), 10), # Brazil - GARCIA TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.233.213.0'), 8), # Brazil - Via Rapida Internet
    IPFilterRule(*parse_ip('45.233.228.0'), 10), # Brazil - Go INTERNET E TELECOM LTDA ME
    IPFilterRule(*parse_ip('45.233.244.0'), 10), # Brazil - PROVEDOR NET MAIS LTDA - ME
    IPFilterRule(*parse_ip('45.233.84.0'), 10), # Brazil - G & N SERVICOS DE COMUNICACAO E MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('45.234.116.0'), 10), # Argentina - TRIMOTION S.R.L.
    IPFilterRule(*parse_ip('45.234.120.0'), 10), # Argentina - A. DOS S.R.L
    IPFilterRule(*parse_ip('45.234.48.0'), 10), # Brazil - Porto Franco TI
    IPFilterRule(*parse_ip('45.234.64.0'), 10), # Brazil - ILIMITECH TELECOM JUSSARA EIRELI
    IPFilterRule(*parse_ip('45.236.140.0'), 10), # Ecuador - INTERCOMMERCE S.A.
    IPFilterRule(*parse_ip('45.236.52.0'), 10), # Brazil - FIBER BANDA LARGA SERV DE CONEXAO INT E LIVROS DIG
    IPFilterRule(*parse_ip('45.237.128.0'), 10), # Brazil - MEGA WIFI - EIRELI
    IPFilterRule(*parse_ip('45.237.180.0'), 10), # Brazil - NET WORK FIBER COMERCIO E SERVICOS DE COMUNICACAO
    IPFilterRule(*parse_ip('45.237.220.0'), 10), # Argentina - ALIANZA PYMES S.A.
    IPFilterRule(*parse_ip('45.237.248.0'), 10), # Brazil - SPEED SOLUÇÕES WIRELESS E INFORMÁTICA LTDA ME
    IPFilterRule(*parse_ip('45.237.76.0'), 10), # Brazil - T C DA SILVA DAVI - ME
    IPFilterRule(*parse_ip('45.237.80.0'), 10), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('45.238.124.0'), 10), # Brazil - MARIA DE LOURDES ZAMIAN PENASSO EQUIPAMENTO - ME
    IPFilterRule(*parse_ip('45.239.164.0'), 10), # Brazil - ALTERNATIVA REDE DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.239.188.0'), 10), # Brazil - ISABELA GUIMARAES VALVERDE
    IPFilterRule(*parse_ip('45.239.64.0'), 10), # Costa Rica - Comunicaciones Metropolitanas METROCOM, S.A.
    IPFilterRule(*parse_ip('45.4.188.0'), 10), # Brazil - VIRTUA MAX COMUNICACAO LTDA - ME
    IPFilterRule(*parse_ip('45.5.100.0'), 10), # Brazil - SIM TELECOM EIRELI
    IPFilterRule(*parse_ip('45.5.116.0'), 10), # Guatemala - INFINITUM S.A.
    IPFilterRule(*parse_ip('45.5.32.0'), 10), # Brazil - RE Servicos de Comunicacao Multimidia
    IPFilterRule(*parse_ip('45.6.156.0'), 10), # Brazil - NETLINK INFORMÁTICA LTDA ME
    IPFilterRule(*parse_ip('45.6.220.0'), 10), # Brazil - NetSV Serviço de Comunicação Multimídia LTDA
    IPFilterRule(*parse_ip('45.65.188.0'), 10), # Costa Rica - Comunicaciones Metropolitanas METROCOM, S.A.
    IPFilterRule(*parse_ip('45.65.208.0'), 10), # Brazil - JND - PROVEDOR
    IPFilterRule(*parse_ip('45.65.224.0'), 10), # Argentina - SOLUTION LAN S.A
    IPFilterRule(*parse_ip('43.245.84.0'), 10), # Nepal - VIA NET COMMUNICATION LTD.
    IPFilterRule(*parse_ip('42.108.0.0'), 18), # India - Vodafone Idea Ltd
    IPFilterRule(*parse_ip('42.112.192.0'), 14), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('42.116.192.0'), 14), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('41.96.0.0'), 20), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('41.135.0.0'), 14), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('41.139.128.0'), 15), # Kenya - Safaricom Limited
    IPFilterRule(*parse_ip('41.140.0.0'), 15), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('41.141.192.0'), 13), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('41.143.0.0'), 15), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('41.150.32.0'), 13), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('41.158.0.0'), 17), # Gabon - Gabon Telecom / Office of Posts and Telecommunications of Gabon
    IPFilterRule(*parse_ip('41.193.64.0'), 13), # South Africa - Vox Telecom Ltd
    IPFilterRule(*parse_ip('41.198.128.0'), 13), # South Africa - Echotel Pty Ltd
    IPFilterRule(*parse_ip('41.200.0.0'), 14), # Algeria - Optimum Telecom Algeria
    IPFilterRule(*parse_ip('41.232.0.0'), 19), # Egypt - TE-AS
    IPFilterRule(*parse_ip('41.248.0.0'), 15), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('41.248.128.0'), 14), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('41.40.0.0'), 19), # Egypt - TE-AS
    IPFilterRule(*parse_ip('41.56.0.0'), 16), # South Africa - RAIN GROUP HOLDINGS (PTY) LTD
    IPFilterRule(*parse_ip('41.63.160.0'), 13), # Angola - TV CABO ANGOLA LDA
    IPFilterRule(*parse_ip('41.65.212.0'), 10), # Egypt - ETISALAT MISR
    IPFilterRule(*parse_ip('41.82.0.0'), 17), # Senegal - SONATEL-AS Autonomous System
    IPFilterRule(*parse_ip('41.90.176.0'), 12), # Kenya - Safaricom Limited
    IPFilterRule(*parse_ip('41.90.192.0'), 13), # Kenya - Safaricom Limited
    IPFilterRule(*parse_ip('41.92.0.0'), 15), # Morocco - MEDITELECOM
    IPFilterRule(*parse_ip('24.139.64.0'), 14), # Puerto Rico - Liberty Communications of Puerto Rico LLC
    IPFilterRule(*parse_ip('24.152.68.0'), 10), # Brazil - MEGABYTE TELECOM LTDA
    IPFilterRule(*parse_ip('24.152.80.0'), 10), # Brazil - Atec Informatica Telecom Martinez e Rocha LTDA
    IPFilterRule(*parse_ip('27.147.128.0'), 15), # Bangladesh - Link3 Technologies Ltd.
    IPFilterRule(*parse_ip('27.34.0.0'), 15), # Nepal - WorldLink Communications Pvt Ltd
    IPFilterRule(*parse_ip('27.50.12.0'), 10), # Ecuador - TELEALFACOM S.A.S.
    IPFilterRule(*parse_ip('27.59.0.0'), 16), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('27.71.64.0'), 14), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('27.72.0.0'), 19), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('31.11.64.0'), 14), # North Macedonia - Company for communications services A1 Makedonija DOOEL Skopje
    IPFilterRule(*parse_ip('31.135.107.128'), 7), # Ukraine - Ltd. "Cypher"
    IPFilterRule(*parse_ip('31.171.152.0'), 10), # Albania - Keminet SHPK
    IPFilterRule(*parse_ip('31.185.0.0'), 11), # Russia - PHAETON PLUS d.o.o
    IPFilterRule(*parse_ip('31.23.0.0'), 16), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('31.41.56.0'), 11), # Russia - LLC "YUGTELSET"
    IPFilterRule(*parse_ip('31.42.91.0'), 8), # Latvia - ERNIS SIA
    IPFilterRule(*parse_ip('36.255.98.192'), 6), # The Netherlands - Feo Prest SRL
    IPFilterRule(*parse_ip('36.50.11.0'), 8), # Bangladesh - Digicon Telecommunication Ltd
    IPFilterRule(*parse_ip('37.111.192.0'), 12), # Bangladesh - GrameenPhone Ltd.
    IPFilterRule(*parse_ip('37.111.224.0'), 12), # Bangladesh - GrameenPhone Ltd.
    IPFilterRule(*parse_ip('37.114.160.0'), 13), # Azerbaijan - Uninet LLC
    IPFilterRule(*parse_ip('37.157.216.0'), 10), # Armenia - Ucom CJSC
    IPFilterRule(*parse_ip('37.186.32.0'), 10), # Qatar - Vodafone Qatar P.Q.S.C
    IPFilterRule(*parse_ip('37.192.0.0'), 18), # Russia - Novotelecom Ltd
    IPFilterRule(*parse_ip('37.205.112.0'), 11), # Iraq - SUPER CELL NETWORK FOR INTERNET SERVICES LTD
    IPFilterRule(*parse_ip('37.212.0.0'), 18), # Belarus - Republican Unitary Telecommunication Enterprise Beltelecom
    IPFilterRule(*parse_ip('37.230.158.0'), 8), # Russia - OOO "SPETSTELECOM-YUG"
    IPFilterRule(*parse_ip('37.231.0.0'), 16), # Kuwait - Kuwait Telecommunications Company K.S.C.C.
    IPFilterRule(*parse_ip('37.236.96.0'), 13), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.236.0.0'), 11), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.236.82.0'), 9), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.237.192.0'), 13), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.238.128.0'), 13), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.238.48.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.238.64.0'), 10), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.238.80.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.239.0.0'), 15), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.239.144.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.26.99.0'), 8), # North Macedonia - Signal NET d.o.o.
    IPFilterRule(*parse_ip('37.32.73.0'), 8), # Kazakhstan - NLS Kazakhstan LLC
    IPFilterRule(*parse_ip('37.41.0.0'), 16), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('37.8.0.0'), 15), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('38.10.152.0'), 9), # Brazil - World Fibra
    IPFilterRule(*parse_ip('38.10.96.0'), 10), # Brazil - ULTRANET NETWORK
    IPFilterRule(*parse_ip('38.121.208.0'), 12), # Venezuela - GALANET SOLUTION C.A.
    IPFilterRule(*parse_ip('38.147.74.0'), 9), # Venezuela - NAVEGANTE NETWORK, C.A.
    IPFilterRule(*parse_ip('38.159.224.0'), 9), # Argentina - COOPERATIVA DE TRABAJO LARA LIMITADA
    IPFilterRule(*parse_ip('38.159.48.0'), 12), # Venezuela - BOOM SOLUTIONS C.A.
    IPFilterRule(*parse_ip('38.166.0.0'), 16), # Venezuela - Airtek Solutions C.A.
    IPFilterRule(*parse_ip('38.183.224.0'), 13), # Venezuela - MARAVECA TELECOMUNICACIONES C.A
    IPFilterRule(*parse_ip('38.188.98.0'), 8), # Venezuela - INVERSIONES SMARTBYTE, C.A.
    IPFilterRule(*parse_ip('38.191.124.0'), 10), # Brazil - SE77E TELECOM EIRELI ME
    IPFilterRule(*parse_ip('38.210.172.0'), 10), # Peru - INTERNET PERU CABLE SOCIEDAD COMERCIAL DE RESPONSABILIDAD LIMITADA - INPECABLE S.R.L.
    IPFilterRule(*parse_ip('38.210.180.0'), 10), # Brazil - BRSULNET TELECOM LTDA
    IPFilterRule(*parse_ip('38.222.0.0'), 16), # Venezuela - Airtek Solutions C.A.
    IPFilterRule(*parse_ip('38.224.192.0'), 12), # Brazil - NEXNETT Brasil Telecom
    IPFilterRule(*parse_ip('38.248.128.0'), 12), # Venezuela - THUNDERNET, C.A.
    IPFilterRule(*parse_ip('38.250.128.0'), 11), # Peru - DESARROLLO DE INFRAESTRUCTURA DE TELECOMUNICACIONES PERU S.A.C. (INFRATEL)
    IPFilterRule(*parse_ip('38.250.144.0'), 12), # Peru - DESARROLLO DE INFRAESTRUCTURA DE TELECOMUNICACIONES PERU S.A.C. (INFRATEL)
    IPFilterRule(*parse_ip('38.253.128.0'), 14), # Peru - WI-NET TELECOM S.A.C.
    IPFilterRule(*parse_ip('38.3.152.0'), 11), # Argentina - CESOP
    IPFilterRule(*parse_ip('38.51.120.0'), 10), # Venezuela - BESSER SOLUTIONS C.A.
    IPFilterRule(*parse_ip('38.56.200.0'), 10), # Brazil - Lastnet Telecom
    IPFilterRule(*parse_ip('38.9.216.0'), 11), # Colombia - SOMOS NETWORKS COLOMBIA S.A.S. BIC
    IPFilterRule(*parse_ip('39.192.0.0'), 22), # Indonesia - PT. Telekomunikasi Selular
    IPFilterRule(*parse_ip('39.34.0.0'), 15), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('39.40.0.0'), 19), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('39.48.0.0'), 20), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('169.224.0.0'), 15), # Iraq - Earthlink Telecommunications Equipment Trading & Services DMCC
    IPFilterRule(*parse_ip('170.0.68.0'), 10), # Brazil - LUMIAR TELECOMUNICAÇÔES
    IPFilterRule(*parse_ip('170.0.92.0'), 10), # Argentina - Conrado Cagnoli
    IPFilterRule(*parse_ip('170.150.20.0'), 10), # Brazil - Nethouse Telecom
    IPFilterRule(*parse_ip('170.231.0.0'), 10), # Brazil - Saber Informática LTDA
    IPFilterRule(*parse_ip('170.231.188.0'), 10), # Brazil - Plínio Honório Sartori
    IPFilterRule(*parse_ip('170.231.232.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('170.231.4.0'), 10), # Brazil - Sul Online Telecom Ltda - EPP
    IPFilterRule(*parse_ip('170.233.128.0'), 10), # Brazil - LANCA SERVICOS DE INFORMATICA LTDA - ME
    IPFilterRule(*parse_ip('170.233.148.0'), 10), # Brazil - PRGNET SERVIÇOS DE TELECOMUNICAÇÕES
    IPFilterRule(*parse_ip('170.233.196.0'), 10), # Brazil - UltraWeb Telecomunicações LTDA
    IPFilterRule(*parse_ip('170.233.204.0'), 10), # Brazil - ILOGNET PROVEDOR
    IPFilterRule(*parse_ip('170.233.28.0'), 10), # Argentina - Sebastian Souto (SSSERVICIOS)
    IPFilterRule(*parse_ip('170.233.32.0'), 10), # Brazil - GUARATIBA TELECOM SERVICOS DE COMUNICACOES LTDA ME
    IPFilterRule(*parse_ip('170.233.4.0'), 10), # Brazil - MOTTANET TI - SERVICOS DE TECNOLOGIA DA INFO
    IPFilterRule(*parse_ip('170.233.52.0'), 10), # Brazil - AVATO TECNOLOGIA S.A
    IPFilterRule(*parse_ip('170.233.80.0'), 10), # Brazil - CAMALEÃO NETWORK LTDA
    IPFilterRule(*parse_ip('170.238.10.0'), 9), # Argentina - WNet Internet y Hosting
    IPFilterRule(*parse_ip('170.238.184.0'), 10), # Brazil - HDL SOLUCOES EM TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('170.238.196.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('170.238.200.0'), 10), # Chile - BITRED GROUP SPA
    IPFilterRule(*parse_ip('170.238.48.0'), 10), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('170.238.52.0'), 10), # Brazil - ALLREDE TELECOM LTDA
    IPFilterRule(*parse_ip('170.238.80.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('170.239.160.0'), 10), # Brazil - EGR NET TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('170.239.207.0'), 8), # Colombia - FIBERNET
    IPFilterRule(*parse_ip('170.239.60.0'), 10), # Brazil - MATHEUS HENRIQUE SANTOS AMORIM - ME
    IPFilterRule(*parse_ip('170.244.209.0'), 8), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('170.244.56.0'), 10), # Argentina - Internet Services S.A.
    IPFilterRule(*parse_ip('170.246.68.0'), 10), # Brazil - AZZA TELECOM SERVIÇOS EM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('170.247.56.0'), 10), # Argentina - Cicchetti Joel Alejandro
    IPFilterRule(*parse_ip('170.254.160.0'), 10), # Brazil - Companhia Itabirana Telecomunicações Ltda
    IPFilterRule(*parse_ip('170.254.180.0'), 10), # Brazil - REDE G2 LTDA - ME
    IPFilterRule(*parse_ip('170.254.236.0'), 10), # Brazil - FRANCINE TALLIS LOURENZONI RIBEIRO INFORMATICA
    IPFilterRule(*parse_ip('170.254.72.0'), 10), # Brazil - FIUZA INFORMÁTICA & TELECOMUNICAÇÃO LTDA ME
    IPFilterRule(*parse_ip('170.78.164.0'), 10), # Brazil - Gigalink de Nova Friburgo Soluções em Rede Multimi
    IPFilterRule(*parse_ip('170.78.20.0'), 10), # Brazil - L E M TELECOMUNICAÇÕES LTDA -ME
    IPFilterRule(*parse_ip('170.78.60.0'), 10), # Brazil - MAIQVOX TELECOM
    IPFilterRule(*parse_ip('170.79.148.0'), 10), # Brazil - MARCOS SINDOR RIBEIRAO BRANCO EIRELI - ME
    IPFilterRule(*parse_ip('170.79.180.0'), 10), # Argentina - TECHTRON ARGENTINA S.A.
    IPFilterRule(*parse_ip('170.79.52.0'), 10), # Brazil - JustWeb Telecomunicações LTDA
    IPFilterRule(*parse_ip('170.79.8.0'), 10), # Brazil - DATAZOOM TELECOM
    IPFilterRule(*parse_ip('170.80.40.0'), 10), # Brazil - INFO TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('170.81.152.0'), 10), # Brazil - R L A World Net LTDA
    IPFilterRule(*parse_ip('170.81.156.0'), 10), # Brazil - EXPRESS NETWORK-ME
    IPFilterRule(*parse_ip('170.81.64.0'), 10), # Brazil - ANANET Telecomunicações e Informática LTDA. ME
    IPFilterRule(*parse_ip('170.82.148.0'), 10), # Brazil - BrPhonia Provedor Ip Ltda
    IPFilterRule(*parse_ip('170.82.168.0'), 10), # Brazil - BJ NET Provedor de Internet Ltda. - ME
    IPFilterRule(*parse_ip('170.82.48.0'), 10), # Brazil - GNS FIBRA
    IPFilterRule(*parse_ip('170.82.76.0'), 10), # Brazil - THE FIBER INTERNET BANDA LARGA
    IPFilterRule(*parse_ip('170.82.88.0'), 10), # Brazil - AGATANGELO TELECOM E INFORMATICA LTDA
    IPFilterRule(*parse_ip('170.83.0.0'), 10), # Brazil - EXPAND TELECOM LTDA
    IPFilterRule(*parse_ip('170.83.220.0'), 10), # Argentina - BREÑAS CABLE COLOR S.R.L
    IPFilterRule(*parse_ip('170.84.148.0'), 10), # Brazil - Infoway Telecom Araruna Ltda
    IPFilterRule(*parse_ip('170.84.160.0'), 10), # Brazil - Ampernet Telecomunicações Ltda
    IPFilterRule(*parse_ip('170.84.80.0'), 10), # Brazil - LagosNet Internet Banda Larga Ltda
    IPFilterRule(*parse_ip('171.224.0.0'), 17), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('171.232.0.0'), 19), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('171.248.0.0'), 17), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('171.250.0.0'), 16), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('171.251.192.0'), 14), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('171.252.0.0'), 18), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('171.76.224.0'), 12), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('175.107.204.0'), 9), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('175.107.208.0'), 8), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('175.136.0.0'), 19), # Malaysia - TM TECHNOLOGY SERVICES SDN. BHD.
    IPFilterRule(*parse_ip('176.114.128.0'), 14), # Russia - Teleradiocompany Teleos-1 Ltd
    IPFilterRule(*parse_ip('176.118.224.0'), 13), # Russia - Timer, LLC
    IPFilterRule(*parse_ip('176.202.0.0'), 17), # Qatar - Ooredoo Q.S.C.
    IPFilterRule(*parse_ip('176.204.0.0'), 17), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('176.212.88.0'), 11), # Russia - JSC "ER-Telecom Holding"
    IPFilterRule(*parse_ip('176.224.0.0'), 16), # Saudi Arabia - Etihad Etisalat, a joint stock company
    IPFilterRule(*parse_ip('176.241.176.0'), 9), # Bulgaria - Telehouse EAD
    IPFilterRule(*parse_ip('176.28.128.0'), 15), # Jordan - Jordanian mobile phone services Ltd
    IPFilterRule(*parse_ip('176.29.0.0'), 16), # Jordan - Jordanian mobile phone services Ltd
    IPFilterRule(*parse_ip('176.36.0.0'), 17), # Ukraine - Lanet Network Ltd
    IPFilterRule(*parse_ip('176.39.32.0'), 9), # Ukraine - Lanet Network Ltd
    IPFilterRule(*parse_ip('176.97.96.0'), 12), # Russia - CityLink Ltd
    IPFilterRule(*parse_ip('177.10.144.0'), 11), # Brazil - PLIM TELECOMUNICACOES LTDA-ME
    IPFilterRule(*parse_ip('177.10.224.0'), 11), # Brazil - VIAFIBRA TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.100.192.0'), 13), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.102.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.104.240.0'), 12), # Brazil - NORTE TELECOMUNICAÇÕES SERVIÇOS DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.106.0.0'), 16), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('177.107.80.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('177.11.136.0'), 11), # Brazil - Mantiqueira Tecnologia Ltda.
    IPFilterRule(*parse_ip('177.11.16.0'), 10), # Brazil - G1Telecom Provedor de Internet LTDA ME
    IPFilterRule(*parse_ip('177.11.32.0'), 11), # Brazil - Mcnet Serviços de Comunicações Ltda
    IPFilterRule(*parse_ip('177.112.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.124.8.0'), 11), # Brazil - VIVAS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.124.0.0'), 11), # Brazil - IMBRANET TELECOM
    IPFilterRule(*parse_ip('177.124.64.0'), 11), # Brazil - ROS Telecom
    IPFilterRule(*parse_ip('177.125.128.0'), 10), # Brazil - VNO Telecom LTDA
    IPFilterRule(*parse_ip('177.125.184.0'), 11), # Brazil - AZZA TELECOM SERVIÇOS EM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('177.126.192.0'), 12), # Brazil - MHNET TELECOM
    IPFilterRule(*parse_ip('177.126.16.0'), 12), # Brazil - 3D TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.127.48.0'), 12), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.128.192.0'), 11), # Brazil - VOANET Telecomunicações Ltda.
    IPFilterRule(*parse_ip('177.128.248.0'), 11), # Brazil - Neolink Telecomunicações LTDA
    IPFilterRule(*parse_ip('177.128.80.0'), 11), # Brazil - IBI TELECOM EIRELI
    IPFilterRule(*parse_ip('177.129.220.0'), 10), # Brazil - INFOVALE INFORMATICA LTDA
    IPFilterRule(*parse_ip('177.129.248.0'), 11), # Brazil - MAXCOMM LTDA EPP
    IPFilterRule(*parse_ip('177.130.224.0'), 12), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('177.131.64.0'), 13), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('177.134.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.136.96.0'), 11), # Brazil - WSNET TELECOM LTDA ME
    IPFilterRule(*parse_ip('177.137.144.0'), 11), # Brazil - Weclix Telecom S/A
    IPFilterRule(*parse_ip('177.137.192.0'), 12), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('177.137.224.0'), 12), # Brazil - Dinamica Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.137.80.0'), 11), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('177.152.176.0'), 11), # Brazil - AVATO TECNOLOGIA S.A
    IPFilterRule(*parse_ip('177.152.80.0'), 11), # Brazil - IWNET TELECOM LTDA ME
    IPFilterRule(*parse_ip('177.155.64.0'), 11), # Brazil - Seitel - Seixas Telecomunicações
    IPFilterRule(*parse_ip('177.156.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.168.0.0'), 19), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.181.0.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.182.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.185.16.0'), 12), # Brazil - SEMPRE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.188.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.190.208.0'), 10), # Brazil - DB3 SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('177.192.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.0.0.0'), 19), # Brazil - V tal
    IPFilterRule(*parse_ip('177.200.32.0'), 12), # Brazil - LINQ TELECOMUNICACOES
    IPFilterRule(*parse_ip('177.200.80.0'), 12), # Brazil - SOBRALNET SERVICOS E TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('177.205.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.206.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.208.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('177.22.160.0'), 12), # Brazil - Osirnet Info Telecom Ltda.
    IPFilterRule(*parse_ip('177.221.120.0'), 11), # Brazil - R7 TELECOMUNICAÇÕES EIRELI ME
    IPFilterRule(*parse_ip('177.221.0.0'), 13), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('177.222.192.0'), 11), # Brazil - PONTOCOMNET SERVIÇOS DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.222.96.0'), 13), # Bolivia - Telefónica Celular de Bolivia S.A.
    IPFilterRule(*parse_ip('177.223.0.0'), 12), # Brazil - ITANET CONECTA LTDA
    IPFilterRule(*parse_ip('177.230.0.0'), 16), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('177.234.216.0'), 11), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('177.236.0.0'), 12), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('177.239.32.0'), 12), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('177.248.16.0'), 12), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('177.25.128.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.32.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.36.160.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('177.37.128.0'), 15), # Brazil - BRISANET SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('177.38.112.0'), 12), # Brazil - TECMIDIAWEB LTDA
    IPFilterRule(*parse_ip('177.44.0.0'), 15), # Brazil - MASTER S/A
    IPFilterRule(*parse_ip('177.44.128.0'), 11), # Brazil - InterSoft Internet Software EIRELI
    IPFilterRule(*parse_ip('177.45.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.46.4.0'), 10), # Brazil - ASSOCIAÇÃO NACIONAL PARA INCLUSÃO DIGITAL - ANID
    IPFilterRule(*parse_ip('177.47.88.0'), 11), # Brazil - NOVELTY TELECOM LTDA
    IPFilterRule(*parse_ip('177.48.0.0'), 18), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('177.52.212.0'), 10), # Brazil - OS CONNECT INFORMATICA EIRELI - EPP
    IPFilterRule(*parse_ip('177.53.152.0'), 10), # Peru - MORENO YANOC NEMIAS BERNARDO
    IPFilterRule(*parse_ip('177.53.212.0'), 10), # Ecuador - Eliana Vanessa Morocho Oña
    IPFilterRule(*parse_ip('177.54.0.0'), 12), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('177.60.32.0'), 13), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.64.128.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.66.80.0'), 11), # Brazil - Ambiente Virtual Sistemas e Conectividade Ltda
    IPFilterRule(*parse_ip('177.67.224.0'), 11), # Brazil - RazaoInfo Internet Ltda
    IPFilterRule(*parse_ip('177.67.34.0'), 8), # Brazil - COOPERNORTE COOPERATIVA DE GERACAO E DESENV
    IPFilterRule(*parse_ip('177.70.160.0'), 12), # Brazil - infotec- serviços de provedor da internet ltda
    IPFilterRule(*parse_ip('177.70.64.0'), 12), # Brazil - RazaoInfo Internet Ltda
    IPFilterRule(*parse_ip('177.71.0.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('177.72.108.0'), 10), # Brazil - RL NET INTERNET
    IPFilterRule(*parse_ip('177.72.224.0'), 11), # Brazil - Adylnet Telecom
    IPFilterRule(*parse_ip('177.72.40.0'), 11), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('177.73.96.0'), 11), # Brazil - TELECOM FOZ
    IPFilterRule(*parse_ip('177.73.192.0'), 11), # Brazil - SEMPRE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.73.92.0'), 10), # Brazil - SPEEDING TELECOM
    IPFilterRule(*parse_ip('177.74.164.0'), 10), # Brazil - POWERNET TELECOMUNICACOES
    IPFilterRule(*parse_ip('177.74.224.0'), 12), # Brazil - BIZZ INTERNET LTDA
    IPFilterRule(*parse_ip('177.75.96.0'), 12), # Brazil - MHNET TELECOM
    IPFilterRule(*parse_ip('177.75.128.0'), 13), # Brazil - MHNET TELECOM
    IPFilterRule(*parse_ip('177.76.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.8.48.0'), 11), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('177.80.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.84.16.0'), 10), # Brazil - R4 TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('177.84.240.0'), 11), # Brazil - 4iNET Communications
    IPFilterRule(*parse_ip('177.84.251.0'), 8), # Brazil - R. A. NOGUEIRA COMERCIO DE EQUIPAMENTOS DE INFORMA
    IPFilterRule(*parse_ip('177.84.32.0'), 11), # Brazil - EASY EMBRANET SERVIÇOS DE COMUNICAÇÃO LTDA
    IPFilterRule(*parse_ip('177.84.44.0'), 10), # Brazil - Link Web
    IPFilterRule(*parse_ip('177.85.0.0'), 11), # Brazil - OnNet Telecomunicacoes LTDA
    IPFilterRule(*parse_ip('177.85.48.0'), 11), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('177.86.96.0'), 11), # Brazil - ASERNET TELECOM
    IPFilterRule(*parse_ip('177.87.204.0'), 10), # Brazil - CONECTA LTDA.
    IPFilterRule(*parse_ip('177.87.32.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('177.89.0.0'), 16), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('177.9.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.91.164.0'), 10), # Brazil - SEM LIMITE COMUNICAÇÕES LTDA - ME
    IPFilterRule(*parse_ip('177.92.136.0'), 11), # Brazil - ZAP TELECOMUNICAÇÕES LTDA - EPP
    IPFilterRule(*parse_ip('177.92.144.0'), 11), # Brazil - STARNET COMUNICACAO MULTIMIDIA LTDA ME
    IPFilterRule(*parse_ip('177.92.0.0'), 14), # Brazil - Ligga Telecomunicações S.A.
    IPFilterRule(*parse_ip('177.93.240.0'), 11), # Brazil - Netpal Telecom
    IPFilterRule(*parse_ip('177.93.0.0'), 12), # Costa Rica - Telecable Economico S.A.
    IPFilterRule(*parse_ip('177.94.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.96.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('178.120.0.0'), 19), # Belarus - Republican Unitary Telecommunication Enterprise Beltelecom
    IPFilterRule(*parse_ip('178.130.136.0'), 10), # Russia - Production co-operative Economic-legal laboratory
    IPFilterRule(*parse_ip('178.135.0.0'), 15), # Lebanon - OGERO
    IPFilterRule(*parse_ip('178.148.0.0'), 17), # Serbia - Serbia BroadBand-Srpske Kablovske mreze d.o.o.
    IPFilterRule(*parse_ip('178.151.0.0'), 15), # Ukraine - CONTENT DELIVERY NETWORK LTD
    IPFilterRule(*parse_ip('178.152.0.0'), 17), # Qatar - Ooredoo Q.S.C.
    IPFilterRule(*parse_ip('178.176.72.0'), 11), # Russia - PJSC MegaFon
    IPFilterRule(*parse_ip('178.217.152.0'), 11), # Russia - Mediagrand Ltd.
    IPFilterRule(*parse_ip('178.44.0.0'), 18), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('178.74.192.0'), 14), # Ukraine - EVEREST TV AND RADIO COMPANY LLC
    IPFilterRule(*parse_ip('178.88.96.0'), 13), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('178.89.0.0'), 16), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('179.0.116.0'), 10), # Brazil - INOVANET TELECOMUNICACOES E MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('179.0.172.0'), 9), # Brazil - WM INTERNET LTDA
    IPFilterRule(*parse_ip('179.1.102.0'), 9), # Colombia - INTERNEXA S.A. E.S.P
    IPFilterRule(*parse_ip('179.105.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.106.176.0'), 12), # Brazil - SBS-NET TELECOMUNICACOES LTDA ME
    IPFilterRule(*parse_ip('179.106.0.0'), 12), # Brazil - Click.com telecomunicações ltda-me
    IPFilterRule(*parse_ip('179.107.208.0'), 11), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('179.108.224.0'), 12), # Brazil - CONECTA LTDA.
    IPFilterRule(*parse_ip('179.109.120.0'), 10), # Brazil - UNO INTERNET LTDA
    IPFilterRule(*parse_ip('179.110.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.112.0.0'), 19), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.124.160.0'), 10), # Brazil - EXTREMA NETWORK
    IPFilterRule(*parse_ip('179.125.128.0'), 15), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('179.125.64.0'), 13), # Brazil - Pombonet Telecomunicações e Informática
    IPFilterRule(*parse_ip('179.126.0.0'), 16), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('179.127.96.0'), 12), # Brazil - WISP ICONECTA SERVICOS DE REDE LTDA
    IPFilterRule(*parse_ip('179.127.248.0'), 11), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('179.132.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.136.0.0'), 19), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.146.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.148.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.152.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.160.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.176.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.180.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.189.128.0'), 13), # Brazil - VETORIALNET INF. E SERVIÇOS DE INTERNET LTDA
    IPFilterRule(*parse_ip('179.189.40.0'), 11), # Brazil - Nova Rede de Telecomunicações Ltda
    IPFilterRule(*parse_ip('179.189.64.0'), 12), # Brazil - Adylnet Telecom
    IPFilterRule(*parse_ip('179.191.42.0'), 8), # Brazil - FNET TELECOM
    IPFilterRule(*parse_ip('179.193.0.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.198.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('179.208.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.211.128.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.214.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.216.128.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.217.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.221.128.0'), 13), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.222.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.224.0.0'), 19), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.232.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.233.64.0'), 14), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.234.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.236.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('179.248.0.0'), 18), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('179.252.0.0'), 18), # Brazil - V tal
    IPFilterRule(*parse_ip('179.24.0.0'), 18), # Uruguay - Administracion Nacional de Telecomunicaciones
    IPFilterRule(*parse_ip('179.32.0.0'), 16), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('179.36.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('179.40.40.0'), 9), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('179.40.46.0'), 9), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('179.42.148.0'), 10), # Brazil - Conect Provedor de Acesso a Internet Ltda Me
    IPFilterRule(*parse_ip('179.42.48.0'), 10), # Brazil - FAST WEB
    IPFilterRule(*parse_ip('179.48.92.0'), 10), # Brazil - NAVEGAI SERVICOS DE TELECOMUNICACOES E INFORMATICA
    IPFilterRule(*parse_ip('179.49.120.0'), 11), # Argentina - ApInter
    IPFilterRule(*parse_ip('179.49.0.0'), 14), # Ecuador - PUNTONET S.A.
    IPFilterRule(*parse_ip('179.51.148.0'), 10), # Brazil - OLIVEIRA & CARVALHO COMUNICACAO E MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('179.6.0.0'), 17), # Peru - America Movil Peru S.A.C.
    IPFilterRule(*parse_ip('179.60.96.0'), 12), # Argentina - Coop. de Obras y Serv. Pub. Ltda. de Rio Tercero
    IPFilterRule(*parse_ip('179.60.128.0'), 10), # Brazil - MP INFORMATICA LTDA
    IPFilterRule(*parse_ip('179.60.188.0'), 10), # Ecuador - Eliana Vanessa Morocho Oña
    IPFilterRule(*parse_ip('179.60.232.0'), 10), # Argentina - WICORP SA
    IPFilterRule(*parse_ip('179.60.64.0'), 13), # Chile - Pacifico Cable SPA.
    IPFilterRule(*parse_ip('179.63.32.0'), 10), # Argentina - Garay Diego Sebastian
    IPFilterRule(*parse_ip('179.63.52.0'), 10), # Argentina - LEIRIA HUGO LEANDRO (GEO FIBER)
    IPFilterRule(*parse_ip('179.67.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('179.82.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.83.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.84.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.88.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('180.244.0.0'), 18), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('181.104.0.0'), 14), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.112.90.0'), 9), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('181.112.92.0'), 9), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('181.114.32.0'), 12), # Argentina - Coop. Popular de Elec., Obras y Servicios Pub. de Santa Rosa LTDA
    IPFilterRule(*parse_ip('181.115.128.0'), 15), # Bolivia - EMPRESA NACIONAL DE TELECOMUNICACIONES SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('181.116.40.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.116.48.0'), 12), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.117.0.0'), 12), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.117.184.0'), 11), # Paraguay - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.118.128.0'), 12), # Argentina - SITERNET SRL
    IPFilterRule(*parse_ip('181.120.0.0'), 19), # Paraguay - Telecel S.A.
    IPFilterRule(*parse_ip('181.13.248.0'), 11), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.128.0.0'), 20), # Colombia - UNE EPM TELECOMUNICACIONES S.A.
    IPFilterRule(*parse_ip('181.168.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.174.252.0'), 10), # Brazil - Super Giga Net Ltda
    IPFilterRule(*parse_ip('181.189.40.0'), 10), # Brazil - Cuiabá Telecom
    IPFilterRule(*parse_ip('181.191.142.0'), 9), # Argentina - Sebastian Souto (SSSERVICIOS)
    IPFilterRule(*parse_ip('181.191.204.0'), 10), # Brazil - Ultracom Telecomunicações Ltda
    IPFilterRule(*parse_ip('181.191.64.0'), 10), # Argentina - SOLUCIONES WISP S.A.
    IPFilterRule(*parse_ip('181.192.100.0'), 10), # Argentina - NEAR S.A.
    IPFilterRule(*parse_ip('181.196.240.0'), 12), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('181.197.96.0'), 12), # Panama - Cable Onda
    IPFilterRule(*parse_ip('181.199.160.0'), 11), # Argentina - PERGAMINO CELP INFRACOM S.A.
    IPFilterRule(*parse_ip('181.199.0.0'), 15), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('181.20.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('181.209.0.0'), 15), # Argentina - ARSAT - Empresa Argentina de Soluciones Satelitales S.A.
    IPFilterRule(*parse_ip('181.216.32.0'), 13), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('181.224.96.0'), 13), # Argentina - ETERNET S.R.L.
    IPFilterRule(*parse_ip('181.224.4.0'), 10), # Brazil - GILBERTO DE AGUIAR
    IPFilterRule(*parse_ip('181.225.156.0'), 10), # Brazil - EDIVAM FRANCI ALVES EIRELI
    IPFilterRule(*parse_ip('181.232.240.0'), 10), # Brazil - FIBRANET TELECOM EIRELI
    IPFilterRule(*parse_ip('181.233.16.0'), 10), # Brazil - NORT TELECOM
    IPFilterRule(*parse_ip('181.233.76.0'), 10), # Ecuador - ECUAFIBRA S.A.
    IPFilterRule(*parse_ip('181.233.93.0'), 8), # Brazil - NETLIFE TECNOLOGIA EIRELI
    IPFilterRule(*parse_ip('181.234.128.0'), 14), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('181.28.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.36.188.0'), 10), # Dominican Republic - ALTICE DOMINICANA S.A.
    IPFilterRule(*parse_ip('181.36.0.0'), 15), # Dominican Republic - ALTICE DOMINICANA S.A.
    IPFilterRule(*parse_ip('181.4.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.42.128.0'), 15), # Chile - ENTEL CHILE S.A.
    IPFilterRule(*parse_ip('181.43.0.0'), 16), # Chile - ENTEL CHILE S.A.
    IPFilterRule(*parse_ip('181.44.0.0'), 18), # Argentina - Telecentro S.A.
    IPFilterRule(*parse_ip('181.51.80.0'), 12), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('181.53.99.0'), 8), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('181.59.0.0'), 12), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('181.64.0.0'), 18), # Peru - Telefonica del Peru S.A.A.
    IPFilterRule(*parse_ip('181.68.0.0'), 18), # Colombia - Colombia Móvil
    IPFilterRule(*parse_ip('181.78.16.0'), 11), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('181.78.192.0'), 12), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('181.78.27.0'), 8), # Paraguay - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('181.79.80.0'), 12), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('181.81.0.0'), 15), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.84.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.85.152.0'), 8), # Argentina - AGENCIA CONECTIVIDAD CORDOBA SOCIEDAD DEL ESTADO
    IPFilterRule(*parse_ip('181.91.128.0'), 15), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.91.84.0'), 10), # Paraguay - Núcleo S.A.
    IPFilterRule(*parse_ip('181.91.88.0'), 11), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.93.0.0'), 15), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.94.196.0'), 8), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.94.224.0'), 11), # Paraguay - Núcleo S.A.
    IPFilterRule(*parse_ip('182.0.0.0'), 20), # Indonesia - PT. Telekomunikasi Selular
    IPFilterRule(*parse_ip('182.253.240.0'), 11), # Indonesia - BIZNET NETWORKS
    IPFilterRule(*parse_ip('182.253.80.0'), 12), # Indonesia - BIZNET NETWORKS
    IPFilterRule(*parse_ip('182.48.72.0'), 10), # Bangladesh - EARTH TELECOMMUNICATION (Pvt) LTD.
    IPFilterRule(*parse_ip('183.171.0.0'), 16), # Malaysia - Celcom Axiata Berhad
    IPFilterRule(*parse_ip('185.146.112.0'), 10), # Azerbaijan - AG Telekom MMC.
    IPFilterRule(*parse_ip('185.147.100.0'), 10), # Iraq - SUPER CELL NETWORK FOR INTERNET SERVICES LTD
    IPFilterRule(*parse_ip('185.156.212.0'), 10), # Lebanon - EagleNet s.a.r.l.
    IPFilterRule(*parse_ip('185.169.160.0'), 10), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('185.179.28.0'), 10), # Kosovo - TelKos L.L.C
    IPFilterRule(*parse_ip('185.184.84.0'), 10), # Lebanon - ZINA sarl
    IPFilterRule(*parse_ip('185.213.228.0'), 10), # Uzbekistan - UNIVERSAL MOBILE SYSTEMS LCC
    IPFilterRule(*parse_ip('185.228.133.172'), 2), # Russia - SYSTEMA Ltd
    IPFilterRule(*parse_ip('185.23.110.0'), 8), # Albania - IH-NETWORK SHPK
    IPFilterRule(*parse_ip('185.23.80.0'), 10), # Russia - OJSC Telecom-Service
    IPFilterRule(*parse_ip('185.239.104.0'), 10), # Iran - AbrArvan CDN and IaaS
    IPFilterRule(*parse_ip('185.239.8.0'), 8), # Albania - Albanian Telecommunications Union SH. P.K.
    IPFilterRule(*parse_ip('185.244.152.0'), 10), # Iraq - Kurdistan Net Company for Computer and Internet Ltd.
    IPFilterRule(*parse_ip('185.38.216.0'), 10), # Ukraine - CONTENT DELIVERY NETWORK LTD
    IPFilterRule(*parse_ip('185.85.152.0'), 10), # Albania - I.B.C - Telecom Sh.p.k.
    IPFilterRule(*parse_ip('186.0.184.0'), 10), # Argentina - Vito Hugo Gonzalez
    IPFilterRule(*parse_ip('186.112.192.0'), 14), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('186.113.28.0'), 9), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('186.121.162.0'), 9), # Mexico - FIBRA A LA CASA
    IPFilterRule(*parse_ip('186.121.191.0'), 8), # Argentina - DSOL INTERNET S.A.S.
    IPFilterRule(*parse_ip('186.122.0.0'), 12), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.122.96.0'), 12), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.124.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('186.126.0.0'), 17), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('186.148.224.0'), 10), # Argentina - DODOLINK INTERNACIONAL SRL
    IPFilterRule(*parse_ip('186.15.192.0'), 12), # Costa Rica - Cable Tica
    IPFilterRule(*parse_ip('186.152.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('186.158.120.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.158.144.0'), 11), # Argentina - AMX Argentina S.A.
    IPFilterRule(*parse_ip('186.158.200.0'), 9), # Paraguay - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.158.220.0'), 9), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.158.224.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.167.0.0'), 15), # Venezuela - Corporacion Digitel C.A.
    IPFilterRule(*parse_ip('186.168.224.0'), 13), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('186.169.64.0'), 14), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('186.172.0.0'), 18), # Chile - Telmex Servicios Empresariales S.A.
    IPFilterRule(*parse_ip('186.18.0.0'), 17), # Argentina - Telecentro S.A.
    IPFilterRule(*parse_ip('186.183.0.0'), 15), # Argentina - Alpha Tel S.A.
    IPFilterRule(*parse_ip('186.189.96.0'), 13), # Chile - WOM S.A.
    IPFilterRule(*parse_ip('186.189.80.0'), 12), # Chile - WOM S.A.
    IPFilterRule(*parse_ip('186.194.192.0'), 12), # Brazil - Friburgo Online LTDA ME
    IPFilterRule(*parse_ip('186.194.16.0'), 12), # Brazil - Holistica Provedor Internet Ltda
    IPFilterRule(*parse_ip('186.195.224.0'), 12), # Brazil - ISP PREMIUM TELECOM S/A
    IPFilterRule(*parse_ip('186.203.0.0'), 16), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('186.204.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('186.208.144.0'), 12), # Brazil - Osirnet Info Telecom Ltda.
    IPFilterRule(*parse_ip('186.209.108.0'), 10), # Brazil - CINTE Telecom Comercio e Servicos Ltda.
    IPFilterRule(*parse_ip('186.209.184.0'), 11), # Brazil - NOVACIA TECNOLOGIA E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('186.210.0.0'), 16), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('186.211.128.0'), 14), # Brazil - BR.Digital Provider
    IPFilterRule(*parse_ip('186.216.152.0'), 11), # Brazil - VERAO COMUNICACOES EIRELI ME
    IPFilterRule(*parse_ip('186.216.160.0'), 13), # Brazil - VOCE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('186.216.216.0'), 11), # Brazil - START TELECOM LTDA
    IPFilterRule(*parse_ip('186.219.128.0'), 12), # Brazil - SEBRATEL TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('186.22.0.0'), 17), # Argentina - Telecentro S.A.
    IPFilterRule(*parse_ip('186.223.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('186.224.224.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('186.225.32.0'), 13), # Brazil - SOBRALNET SERVICOS E TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('186.227.216.0'), 11), # Brazil - WZNET TELECOM LTDA
    IPFilterRule(*parse_ip('186.232.208.0'), 11), # Brazil - NETSTAR SOLUÇÕES LTDA
    IPFilterRule(*parse_ip('186.233.48.0'), 10), # Brazil - POWERNET SOLUTIONS LTDA
    IPFilterRule(*parse_ip('186.233.52.0'), 9), # Brazil - Cubo Networks Ltda.
    IPFilterRule(*parse_ip('186.235.120.0'), 11), # Brazil - K1 Telecom e Multimidia LTDA
    IPFilterRule(*parse_ip('186.235.32.0'), 12), # Brazil - ZAAZ PROVEDOR DE INTERNET E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('186.237.208.0'), 11), # Brazil - MEGA NET PROVEDOR INTERNET LTDA
    IPFilterRule(*parse_ip('186.242.144.0'), 12), # Brazil - V tal
    IPFilterRule(*parse_ip('186.244.0.0'), 15), # Brazil - V tal
    IPFilterRule(*parse_ip('186.247.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('186.249.128.0'), 13), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('186.249.248.0'), 11), # Brazil - JF PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('186.250.220.0'), 10), # Brazil - infinity brasil telecom ltda me
    IPFilterRule(*parse_ip('186.251.124.0'), 10), # Brazil - FLIX TELECOM
    IPFilterRule(*parse_ip('186.27.128.0'), 14), # Colombia - EMPRESAS MUNICIPALES DE CALI E.I.C.E. E.S.P.
    IPFilterRule(*parse_ip('186.33.35.0'), 8), # Paraguay - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('186.39.0.0'), 16), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('186.42.24.0'), 9), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('186.46.16.0'), 8), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('186.48.0.0'), 19), # Uruguay - Administracion Nacional de Telecomunicaciones
    IPFilterRule(*parse_ip('186.60.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('186.64.128.0'), 15), # Costa Rica - Cable Tica
    IPFilterRule(*parse_ip('186.65.64.0'), 11), # Argentina - Sociedad Cooperativa Popular Limitada de Comodoro
    IPFilterRule(*parse_ip('186.65.80.0'), 10), # Argentina - SERVICIOS DE TECNOLOGIA APLICADA SRL
    IPFilterRule(*parse_ip('186.65.84.0'), 10), # Argentina - Sista S.A.
    IPFilterRule(*parse_ip('186.72.0.0'), 18), # Panama - Cable & Wireless Panama
    IPFilterRule(*parse_ip('186.80.28.0'), 10), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.81.100.0'), 9), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.81.104.0'), 11), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.81.56.0'), 11), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.82.102.0'), 8), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.84.80.0'), 12), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.88.0.0'), 16), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('186.91.0.0'), 15), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('187.0.0.0'), 12), # Brazil - Adylnet Telecom
    IPFilterRule(*parse_ip('187.101.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.106.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.109.112.0'), 10), # Brazil - FASTNET FIBRA
    IPFilterRule(*parse_ip('187.109.96.0'), 12), # Brazil - Ampernet Telecomunicações Ltda
    IPFilterRule(*parse_ip('187.111.128.0'), 12), # Brazil - Infornet Consultoria e Assessoria Ltda
    IPFilterRule(*parse_ip('187.120.16.0'), 12), # Brazil - GOLDEN LINK
    IPFilterRule(*parse_ip('187.121.0.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.122.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.136.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.12.0.0'), 18), # Brazil - V tal
    IPFilterRule(*parse_ip('187.148.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.158.192.0'), 14), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.17.140.0'), 10), # Brazil - VNT FIBRAS INTERNET LTDA
    IPFilterRule(*parse_ip('187.17.228.0'), 10), # Brazil - LANTEC COMUNICACAO MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('187.17.48.0'), 12), # Brazil - AMI Telecomunicações LTDA
    IPFilterRule(*parse_ip('187.173.128.0'), 15), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.180.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.187.196.0'), 10), # Mexico - Mexico Red de Telecomunicaciones, S. de R.L. de C.V.
    IPFilterRule(*parse_ip('187.188.14.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.189.127.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.189.246.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.189.58.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.189.92.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.19.112.0'), 12), # Brazil - UNIDASNET COMUNICACOES LTDA
    IPFilterRule(*parse_ip('187.19.128.0'), 15), # Brazil - BRISANET SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('187.190.78.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.191.36.0'), 10), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.2.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.204.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.208.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.222.128.0'), 15), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.224.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.230.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.232.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.245.64.0'), 12), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('187.251.128.0'), 13), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.251.240.0'), 12), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.33.192.0'), 12), # Brazil - OAI LTDA
    IPFilterRule(*parse_ip('187.34.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.45.64.0'), 12), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('187.49.12.0'), 10), # Brazil - WN INTERNET
    IPFilterRule(*parse_ip('187.52.0.0'), 18), # Brazil - V tal
    IPFilterRule(*parse_ip('187.61.100.0'), 10), # Brazil - CINTE Telecom Comercio e Servicos Ltda.
    IPFilterRule(*parse_ip('187.61.92.0'), 10), # Ecuador - TELEALFACOM S.A.S.
    IPFilterRule(*parse_ip('187.62.76.0'), 10), # Brazil - VOO TELECOM AP LTDA
    IPFilterRule(*parse_ip('187.63.148.0'), 10), # Brazil - G4 Conectividade SVA Eireli
    IPFilterRule(*parse_ip('187.73.192.0'), 13), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('187.73.64.0'), 13), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('187.79.0.0'), 15), # Brazil - V tal
    IPFilterRule(*parse_ip('187.84.152.0'), 10), # Brazil - Connect LP - SERVICO DE COMUNICACAO MULTIMIDIA LTD
    IPFilterRule(*parse_ip('187.84.240.0'), 12), # Brazil - SEMPRE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('187.84.32.0'), 10), # Brazil - MULTIVELOX SERVICOS DE PROVEDOR DE ACESSO A INTERN
    IPFilterRule(*parse_ip('187.85.80.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('187.86.240.0'), 12), # Brazil - INETVIP TELECOM LTDA
    IPFilterRule(*parse_ip('187.88.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.95.160.0'), 12), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('188.0.160.0'), 13), # Russia - JSC Vainah Telecom
    IPFilterRule(*parse_ip('188.172.96.0'), 12), # Albania - Vodafone Albania Sh.A.
    IPFilterRule(*parse_ip('188.236.0.0'), 16), # Kuwait - Mobile Telecommunications Company K.S.C.P.
    IPFilterRule(*parse_ip('188.237.0.0'), 16), # Moldova - Moldtelecom SA
    IPFilterRule(*parse_ip('188.244.128.0'), 14), # Russia - Limited Liability Company "TTK-Svyaz"
    IPFilterRule(*parse_ip('188.253.208.0'), 12), # Azerbaijan - Baku Telephone Communication LLC
    IPFilterRule(*parse_ip('188.70.0.0'), 17), # Kuwait - NATIONAL MOBILE TELECOMMUNICATIONS COMPANY K.S.C.P.
    IPFilterRule(*parse_ip('188.72.41.0'), 8), # Iraq - Steps Telecom For Internet Ltd.
    IPFilterRule(*parse_ip('189.113.224.0'), 13), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('189.113.64.0'), 12), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('189.120.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.126.80.0'), 10), # Brazil - ACESSE WI-FI SERVICOS, INSTALACAO E MANUTENCAO
    IPFilterRule(*parse_ip('189.128.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.139.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.141.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.15.0.0'), 16), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('189.172.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.203.137.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('189.203.150.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('189.204.128.0'), 14), # Mexico - Operbes, S.A. de C.V.
    IPFilterRule(*parse_ip('189.219.64.0'), 14), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('189.224.0.0'), 19), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.238.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.242.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.26.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.28.144.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('189.28.176.0'), 12), # Brazil - ENGEPLUS INFORMATICA LTDA
    IPFilterRule(*parse_ip('189.28.64.0'), 13), # Bolivia - Telefónica Celular de Bolivia S.A.
    IPFilterRule(*parse_ip('189.30.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('189.32.128.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.34.128.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.35.0.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.37.0.0'), 15), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('189.38.32.0'), 12), # Brazil - WGO MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('189.4.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.41.0.0'), 16), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('189.46.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.50.52.0'), 10), # Brazil - Faiser Telecomunicações
    IPFilterRule(*parse_ip('189.50.60.0'), 10), # Brazil - CANDIBANET LTDA
    IPFilterRule(*parse_ip('189.56.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.68.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.70.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('189.72.0.0'), 18), # Brazil - V tal
    IPFilterRule(*parse_ip('189.90.112.0'), 12), # Brazil - Brasilnet Telecomunicações Ltda ME
    IPFilterRule(*parse_ip('189.90.192.0'), 12), # Brazil - SEMPRE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('190.1.0.0'), 14), # Argentina - BVNET S.A.
    IPFilterRule(*parse_ip('190.10.128.0'), 15), # Ecuador - SERVICIOS DE TELECOMUNICACIONES SETEL S.A. (XTRIM EC)
    IPFilterRule(*parse_ip('190.103.16.0'), 11), # Argentina - CYBERTAP
    IPFilterRule(*parse_ip('190.104.124.0'), 9), # Guatemala - Servicios Innovadores de Comunicación y Entretenimiento, S.A.
    IPFilterRule(*parse_ip('190.104.224.0'), 13), # Argentina - CPS
    IPFilterRule(*parse_ip('190.104.48.0'), 12), # Argentina - COOP. LIMITADA DE CONSUMO DE ELECTRICIDAD DE SALTO
    IPFilterRule(*parse_ip('190.105.208.0'), 12), # Argentina - Pogliotti & Pogliotti Construcciones S.A.
    IPFilterRule(*parse_ip('190.105.0.0'), 15), # Argentina - Ver Tv S.A.
    IPFilterRule(*parse_ip('190.108.96.0'), 13), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('190.11.176.0'), 10), # Argentina - Power VT S.A.
    IPFilterRule(*parse_ip('190.11.220.0'), 10), # Brazil - 2 M TELECOM EIRELI
    IPFilterRule(*parse_ip('190.110.176.0'), 11), # Argentina - Internet Local
    IPFilterRule(*parse_ip('190.110.48.0'), 12), # Ecuador - PUNTONET S.A.
    IPFilterRule(*parse_ip('190.112.64.0'), 14), # Argentina - Internet Para Todos - Gobierno de La Rioja
    IPFilterRule(*parse_ip('190.112.176.0'), 12), # Argentina - Jumpnet Soluciones de Internet S.R.L.
    IPFilterRule(*parse_ip('190.112.204.0'), 10), # Brazil - AR3 Servicos EIRELI ME
    IPFilterRule(*parse_ip('190.112.216.0'), 10), # Argentina - WNet Internet y Hosting
    IPFilterRule(*parse_ip('190.113.128.0'), 14), # Argentina - ARLINK S.A.
    IPFilterRule(*parse_ip('190.113.48.0'), 10), # Argentina - DEBONA RODOLFO DANIEL (INFORMÁTICA CURUZÚ)
    IPFilterRule(*parse_ip('190.114.102.0'), 8), # Argentina - Alvarez Cable Hogar S.A.
    IPFilterRule(*parse_ip('190.114.32.0'), 13), # Chile - Pacifico Cable SPA.
    IPFilterRule(*parse_ip('190.115.104.0'), 10), # Brazil - GIGA FIBRA
    IPFilterRule(*parse_ip('190.120.248.0'), 11), # Venezuela - CORPORACION FIBEX TELECOM, C.A.
    IPFilterRule(*parse_ip('190.122.0.0'), 13), # Argentina - RSO APOLO HIDALGO S.R.L.
    IPFilterRule(*parse_ip('190.122.88.0'), 9), # Argentina - Servicios y Telecomunicaciones S.A.
    IPFilterRule(*parse_ip('190.128.128.0'), 15), # Paraguay - Telecel S.A.
    IPFilterRule(*parse_ip('190.129.0.0'), 16), # Bolivia - EMPRESA NACIONAL DE TELECOMUNICACIONES SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.132.0.0'), 18), # Uruguay - Administracion Nacional de Telecomunicaciones
    IPFilterRule(*parse_ip('190.136.64.0'), 14), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.14.240.0'), 12), # Colombia - Media Commerce Partners S.A
    IPFilterRule(*parse_ip('190.14.32.0'), 10), # Argentina - Atlantica Video Cable S.A.
    IPFilterRule(*parse_ip('190.141.173.0'), 8), # Panama - Cable Onda
    IPFilterRule(*parse_ip('190.142.0.0'), 16), # Venezuela - Corporación Telemic C.A.
    IPFilterRule(*parse_ip('190.143.236.0'), 10), # Guatemala - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.143.240.0'), 10), # Nicaragua - Telefonia Celular de Nicaragua SA.
    IPFilterRule(*parse_ip('190.15.96.0'), 13), # Brazil - ALOO TELECOM - FSF TECNOLOGIA SA
    IPFilterRule(*parse_ip('190.150.160.0'), 12), # El Salvador - MILLICOM CABLE EL SALVADOR S.A. DE C.V.
    IPFilterRule(*parse_ip('190.152.187.0'), 8), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('190.152.236.0'), 9), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('190.153.104.0'), 9), # Venezuela - Net Uno, C.A.
    IPFilterRule(*parse_ip('190.153.112.0'), 12), # Venezuela - Net Uno, C.A.
    IPFilterRule(*parse_ip('190.160.0.0'), 18), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('190.164.0.0'), 16), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('190.165.0.0'), 16), # Colombia - UNE EPM TELECOMUNICACIONES S.A.
    IPFilterRule(*parse_ip('190.171.96.0'), 13), # Costa Rica - Telecable Economico S.A.
    IPFilterRule(*parse_ip('190.172.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('190.176.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('190.183.0.0'), 16), # Argentina - Gigared S.A.
    IPFilterRule(*parse_ip('190.16.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.2.64.0'), 10), # Brazil - SUPRIFIBRA SOLUCOES TECNOLOGICA LTDA
    IPFilterRule(*parse_ip('190.20.0.0'), 17), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('190.214.132.0'), 8), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('190.216.48.0'), 11), # Argentina - Level 3 Parent, LLC
    IPFilterRule(*parse_ip('190.227.182.0'), 9), # Argentina - Teledifusora S.A.
    IPFilterRule(*parse_ip('190.227.188.0'), 10), # Argentina - COOPERATIVA TELEFONICA Y OSPA DE TOSTADO LDA.
    IPFilterRule(*parse_ip('190.227.32.0'), 13), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.232.0.0'), 19), # Peru - Telefonica del Peru S.A.A.
    IPFilterRule(*parse_ip('190.242.106.0'), 8), # Ecuador - Eliana Vanessa Morocho Oña
    IPFilterRule(*parse_ip('190.242.24.0'), 10), # Honduras - Telefónica Celular S.A
    IPFilterRule(*parse_ip('190.244.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.27.0.0'), 15), # Colombia - ETB - Colombia
    IPFilterRule(*parse_ip('190.28.0.0'), 17), # Colombia - UNE EPM TELECOMUNICACIONES S.A.
    IPFilterRule(*parse_ip('190.31.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.32.0.0'), 17), # Panama - Cable & Wireless Panama
    IPFilterRule(*parse_ip('190.48.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('190.5.32.0'), 13), # Chile - Pacifico Cable SPA.
    IPFilterRule(*parse_ip('190.52.68.0'), 10), # Brazil - USUAL TELECOM LTDA
    IPFilterRule(*parse_ip('190.52.80.0'), 12), # Argentina - COOP. ELÉCTRICA Y DE SERVICIOS MARIANO MORENO LTDA.
    IPFilterRule(*parse_ip('190.55.0.0'), 16), # Argentina - Telecentro S.A.
    IPFilterRule(*parse_ip('190.6.32.0'), 12), # Venezuela - Net Uno, C.A.
    IPFilterRule(*parse_ip('190.6.8.0'), 11), # Venezuela - Net Uno, C.A.
    IPFilterRule(*parse_ip('190.60.32.0'), 12), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('190.61.54.0'), 8), # Argentina - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('190.62.80.0'), 11), # El Salvador - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.7.0.0'), 14), # Argentina - Gigared S.A.
    IPFilterRule(*parse_ip('190.80.0.0'), 15), # Guyana - Guyana Telephone & Telegraph Co.
    IPFilterRule(*parse_ip('190.83.8.0'), 10), # Guatemala - SKYWAY
    IPFilterRule(*parse_ip('190.83.112.0'), 10), # Paraguay - CAMPOS FARIAS GUILHERME
    IPFilterRule(*parse_ip('190.83.84.0'), 10), # Brazil - NETCOM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('190.85.0.0'), 16), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('190.86.208.0'), 10), # El Salvador - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.86.72.0'), 10), # El Salvador - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.89.46.0'), 8), # Ecuador - ALFATV CABLE S.A
    IPFilterRule(*parse_ip('190.89.88.0'), 10), # Brazil - MAXNET PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('190.9.64.0'), 10), # Brazil - MR Digital Servicos e Comunicacoes Ltda
    IPFilterRule(*parse_ip('190.96.112.0'), 9), # Argentina - Empresa Provincial de Energia de Cordoba
    IPFilterRule(*parse_ip('190.97.224.0'), 13), # Venezuela - VIGINET C.A
    IPFilterRule(*parse_ip('191.102.244.0'), 10), # Argentina - ApInter
    IPFilterRule(*parse_ip('191.104.0.0'), 16), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('191.112.0.0'), 18), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('191.13.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.176.0.0'), 19), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('191.185.0.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('191.188.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('191.19.0.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.193.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.216.0.0'), 19), # Brazil - V tal
    IPFilterRule(*parse_ip('191.23.0.0'), 12), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.242.112.0'), 12), # Brazil - PLIM TELECOMUNICACOES LTDA-ME
    IPFilterRule(*parse_ip('191.243.160.0'), 12), # Brazil - SIMNET TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('191.243.216.0'), 11), # Brazil - Franca e Franca Com e Serv Ltda. ME
    IPFilterRule(*parse_ip('191.243.4.0'), 10), # Brazil - Brasrede Telecomunicações LTDA
    IPFilterRule(*parse_ip('191.253.0.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('191.254.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.32.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.37.72.0'), 11), # Brazil - CNT Fiber
    IPFilterRule(*parse_ip('191.42.0.0'), 16), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('191.5.192.0'), 12), # Brazil - Natel Telecom Ltda. - ME
    IPFilterRule(*parse_ip('191.5.240.0'), 12), # Brazil - VARZEA NET TELECOMUNICACOES LTDA ME
    IPFilterRule(*parse_ip('191.5.32.0'), 12), # Brazil - SEMPRE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('191.54.0.0'), 17), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('191.6.248.0'), 11), # Brazil - TORPEDOLINK TELECOM
    IPFilterRule(*parse_ip('191.6.48.0'), 11), # Brazil - DTEL TELECOM
    IPFilterRule(*parse_ip('191.6.56.0'), 11), # Brazil - Entornet Fibra
    IPFilterRule(*parse_ip('191.6.88.0'), 11), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('191.7.96.0'), 11), # Brazil - GRV FIBRA
    IPFilterRule(*parse_ip('191.80.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('191.84.0.0'), 17), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('191.95.0.0'), 16), # Colombia - Colombia Móvil
    IPFilterRule(*parse_ip('191.97.68.0'), 10), # Argentina - ENLACE SOLUCIONES INFORMATICAS SRL
    IPFilterRule(*parse_ip('191.99.0.0'), 16), # Ecuador - Ecuadortelecom S.A.
    IPFilterRule(*parse_ip('192.140.116.0'), 10), # Brazil - A2 TELECOM EIRELI - ME
    IPFilterRule(*parse_ip('192.140.44.0'), 10), # Brazil - BrasilNET Telecomunicações do Parana LTDA
    IPFilterRule(*parse_ip('192.140.48.0'), 10), # Brazil - ONCABO LTDA
    IPFilterRule(*parse_ip('192.140.64.0'), 10), # Brazil - WTD TELECOM
    IPFilterRule(*parse_ip('192.140.92.0'), 10), # Ecuador - KOLVECH S.A. (TELECOMVAS)
    IPFilterRule(*parse_ip('192.141.112.0'), 10), # Brazil - ALL CONECTA INTERNET LTDA - ME
    IPFilterRule(*parse_ip('193.106.48.0'), 10), # Kyrgyzstan - NUR Telecom LLC
    IPFilterRule(*parse_ip('193.107.112.0'), 10), # Ukraine - PE Tsibrankov Konstantin Igorevich
    IPFilterRule(*parse_ip('193.187.156.0'), 9), # Russia - OOO Dontel
    IPFilterRule(*parse_ip('193.233.120.0'), 10), # Russia - LLC AVANTA TELECOM
    IPFilterRule(*parse_ip('193.38.33.0'), 8), # Albania - SPEED LINE SHPK
    IPFilterRule(*parse_ip('194.127.108.0'), 8), # Iraq - Noor Al-Bedaya for General Trading, agricultural investments, Technical production and distribution, internet services, general services, Information technology and software Ltd
    IPFilterRule(*parse_ip('194.15.98.0'), 8), # Georgia - GeNet Marneuli
    IPFilterRule(*parse_ip('194.163.0.0'), 12), # Oman - Awaser Oman LLC
    IPFilterRule(*parse_ip('194.246.88.0'), 10), # Lebanon - Ferrari-Networks SARL
    IPFilterRule(*parse_ip('194.44.80.0'), 11), # Ukraine - UARNet-Eksintech
    IPFilterRule(*parse_ip('194.54.152.0'), 10), # Russia - Crimeainfocom Ltd
    IPFilterRule(*parse_ip('195.208.40.0'), 10), # Russia - RossTel Company LLC
    IPFilterRule(*parse_ip('195.80.140.0'), 9), # Ukraine - Comcor Service LLC
    IPFilterRule(*parse_ip('196.112.0.0'), 20), # Morocco - MEDITELECOM
    IPFilterRule(*parse_ip('196.176.0.0'), 18), # Tunisia - OOREDOO TUNISIE SA
    IPFilterRule(*parse_ip('196.188.0.0'), 16), # Ethiopia - Ethio Telecom
    IPFilterRule(*parse_ip('196.190.0.0'), 17), # Ethiopia - Ethio Telecom
    IPFilterRule(*parse_ip('196.196.52.0'), 9), # Latvia - Orion Network Limited
    IPFilterRule(*parse_ip('196.25.192.0'), 14), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('196.39.0.0'), 16), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('196.74.0.0'), 17), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('197.0.0.0'), 17), # Tunisia - TOPNET
    IPFilterRule(*parse_ip('197.17.0.0'), 13), # Tunisia - OOREDOO TUNISIE SA
    IPFilterRule(*parse_ip('197.184.0.0'), 17), # South Africa - RAIN GROUP HOLDINGS (PTY) LTD
    IPFilterRule(*parse_ip('197.2.0.0'), 16), # Tunisia - TOPNET
    IPFilterRule(*parse_ip('197.20.0.0'), 18), # Tunisia - OOREDOO TUNISIE SA
    IPFilterRule(*parse_ip('197.237.128.0'), 14), # Kenya - Wananchi Group (Kenya) Limited
    IPFilterRule(*parse_ip('197.244.0.0'), 16), # Tunisia - TOPNET
    IPFilterRule(*parse_ip('197.25.128.0'), 15), # Tunisia - 3S INF
    IPFilterRule(*parse_ip('197.32.0.0'), 21), # Egypt - TE-AS
    IPFilterRule(*parse_ip('197.64.0.0'), 19), # South Africa - MTN SA
    IPFilterRule(*parse_ip('197.89.128.0'), 14), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('197.89.20.0'), 10), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('197.95.0.0'), 15), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('197.98.128.0'), 15), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('198.160.165.0'), 8), # Iraq - Al Atheer Telecommunication-Iraq Co. Ltd. Incorporated in Cayman Islands
    IPFilterRule(*parse_ip('198.163.192.0'), 11), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('2.132.0.0'), 18), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('2.57.204.0'), 10), # Ukraine - Kaluska informatsiyna merezha LLC
    IPFilterRule(*parse_ip('200.101.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('200.102.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('200.107.224.0'), 11), # Argentina - NETPATAGONIA SAS
    IPFilterRule(*parse_ip('200.107.88.0'), 11), # Argentina - Sociedad Cooperativa Popular Limitada de Comodoro
    IPFilterRule(*parse_ip('200.108.184.0'), 10), # Mexico - TELTAN TELECOMUNICACIONES, S. DE R.L. DE C.V.
    IPFilterRule(*parse_ip('200.109.192.0'), 14), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('200.118.60.0'), 10), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('200.12.0.0'), 12), # Brazil - ALEXANDRE BISPO COMUNICAÇÃO ME
    IPFilterRule(*parse_ip('200.125.168.0'), 10), # Dominican Republic - WIRELESS MULTI SERVICE VARGAS CABRERA, S. R. L
    IPFilterRule(*parse_ip('200.125.228.0'), 10), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('200.152.0.0'), 11), # Brazil - Directnet Prestacao de Servicos Ltda.
    IPFilterRule(*parse_ip('200.152.20.0'), 10), # Brazil - Directnet Prestacao de Servicos Ltda.
    IPFilterRule(*parse_ip('200.158.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('200.159.128.0'), 13), # Brazil - Winfnet Telecom Wireless Ltda
    IPFilterRule(*parse_ip('200.164.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('200.176.16.0'), 10), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('200.176.4.0'), 9), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('200.189.72.0'), 10), # Brazil - ACESSE WIFI
    IPFilterRule(*parse_ip('200.215.240.0'), 10), # Brazil - Soft System Informatica Ltda
    IPFilterRule(*parse_ip('200.222.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('200.24.134.0'), 9), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('200.24.144.0'), 12), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('200.28.16.0'), 12), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('200.36.154.0'), 9), # Venezuela - NAVEGANTE NETWORK, C.A.
    IPFilterRule(*parse_ip('200.36.216.0'), 10), # Brazil - RAYAI FIBRA - PROVEDOR DE ACESSO A INTERNET EIRELI
    IPFilterRule(*parse_ip('200.4.112.0'), 10), # Brazil - MS NET
    IPFilterRule(*parse_ip('200.5.48.0'), 12), # Costa Rica - COOPERATIVA DE ELECTRIFICACIÓN RURAL DE GUANACASTE R.L.
    IPFilterRule(*parse_ip('200.50.228.0'), 8), # Brazil - AP INTERNET
    IPFilterRule(*parse_ip('200.52.16.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('200.53.192.0'), 13), # Brazil - Redfox Telecomunicações Ltda.
    IPFilterRule(*parse_ip('200.59.64.0'), 14), # Argentina - SION S.A
    IPFilterRule(*parse_ip('200.59.184.0'), 11), # Venezuela - TotalCom Venezuela C.A.
    IPFilterRule(*parse_ip('200.6.136.0'), 11), # Brazil - MOV TELECOM LTDA
    IPFilterRule(*parse_ip('200.6.88.0'), 10), # Brazil - FIBRA MAIS
    IPFilterRule(*parse_ip('200.63.192.0'), 14), # Ecuador - SERVICIOS DE TELECOMUNICACIONES SETEL S.A. (XTRIM EC)
    IPFilterRule(*parse_ip('200.66.112.0'), 12), # Brazil - K.H.D. SILVESTRI E CIA LTDA
    IPFilterRule(*parse_ip('200.68.180.0'), 10), # Mexico - RadioMovil Dipsa, S.A. de C.V.
    IPFilterRule(*parse_ip('200.7.208.0'), 10), # Ecuador - Otecel S.A.
    IPFilterRule(*parse_ip('200.80.124.0'), 10), # Brazil - CS+TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('200.9.16.0'), 10), # Brazil - INTERNET ULTRA LTDA
    IPFilterRule(*parse_ip('200.94.64.0'), 13), # Mexico - Alestra, S. de R.L. de C.V.
    IPFilterRule(*parse_ip('201.0.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('201.100.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('201.10.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.130.88.0'), 11), # Brazil - 3E TELECOM
    IPFilterRule(*parse_ip('201.131.176.0'), 10), # Brazil - Ipunet Telecomunicações Ltda
    IPFilterRule(*parse_ip('201.131.236.0'), 10), # Mexico - Telecable del Mineral, S. A. de C.V.
    IPFilterRule(*parse_ip('201.131.68.0'), 10), # Brazil - TURBONET TELECOM LTDA
    IPFilterRule(*parse_ip('201.131.80.0'), 11), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('201.141.96.0'), 13), # Mexico - Cablevisión, S.A. de C.V.
    IPFilterRule(*parse_ip('201.148.180.0'), 10), # Brazil - PRIME SYSTEM TELECOM
    IPFilterRule(*parse_ip('201.157.214.0'), 9), # Brazil - TASCOM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('201.159.72.0'), 11), # Brazil - Poxley Provedor de Internet Ltda
    IPFilterRule(*parse_ip('201.16.128.0'), 12), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('201.176.0.0'), 18), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('201.182.124.0'), 10), # Brazil - Technik Internet Ltda - ME
    IPFilterRule(*parse_ip('201.182.60.0'), 10), # Brazil - DIGITAL LIFE
    IPFilterRule(*parse_ip('201.182.78.0'), 9), # Ecuador - FIBERGO-TELECOM S.A.
    IPFilterRule(*parse_ip('201.18.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.190.173.0'), 8), # Argentina - ARLINK S.A.
    IPFilterRule(*parse_ip('201.191.0.0'), 16), # Costa Rica - Instituto Costarricense de Electricidad y Telecom.
    IPFilterRule(*parse_ip('201.2.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.210.0.0'), 15), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('201.217.244.0'), 10), # Argentina - ECOM CHACO S.A.
    IPFilterRule(*parse_ip('201.219.160.0'), 13), # Argentina - MERCO COMUNICACIONES
    IPFilterRule(*parse_ip('201.219.248.0'), 10), # Brazil - BRASIL-IP TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('201.220.16.0'), 11), # Argentina - MADACOM SRL
    IPFilterRule(*parse_ip('201.224.0.0'), 18), # Panama - Cable & Wireless Panama
    IPFilterRule(*parse_ip('201.251.104.0'), 11), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('201.26.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('201.29.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('201.33.160.0'), 12), # Brazil - K2 Telecom e Multimidia LTDA ME
    IPFilterRule(*parse_ip('201.34.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.4.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('201.42.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('201.47.0.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('201.49.244.0'), 10), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('201.50.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.71.28.0'), 10), # Brazil - GUZZO TERRAPLANAGEM LTDA
    IPFilterRule(*parse_ip('201.77.160.0'), 12), # Brazil - BTT TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('201.77.55.0'), 8), # Panama - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('201.78.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.8.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('201.80.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('201.87.240.0'), 12), # Brazil - ALLREDE TELECOM LTDA
    IPFilterRule(*parse_ip('201.92.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('201.96.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('202.152.192.0'), 12), # Indonesia - PT. Eka Mas Republik
    IPFilterRule(*parse_ip('202.165.250.0'), 8), # Pakistan - Optix Pakistan (Pvt.) Limited
    IPFilterRule(*parse_ip('202.44.104.0'), 11), # Bangladesh - GramBangla Systems Limites, Internet and Data Communication
    IPFilterRule(*parse_ip('202.51.69.0'), 8), # Nepal - Subisu Cablenet (Pvt) Ltd, Baluwatar, Kathmandu, Nepal
    IPFilterRule(*parse_ip('202.51.80.0'), 8), # Nepal - Subisu Cablenet (Pvt) Ltd, Baluwatar, Kathmandu, Nepal
    IPFilterRule(*parse_ip('202.51.88.0'), 9), # Nepal - Subisu Cablenet (Pvt) Ltd, Baluwatar, Kathmandu, Nepal
    IPFilterRule(*parse_ip('203.162.224.0'), 12), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('203.162.72.0'), 10), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('203.162.84.0'), 10), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('203.210.128.0'), 15), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('204.157.234.0'), 8), # Brazil - FASTNET TELECOM LTDA - ME
    IPFilterRule(*parse_ip('206.1.128.0'), 15), # Venezuela - Airtek Solutions C.A.
    IPFilterRule(*parse_ip('209.45.88.0'), 10), # Peru - Red Cientifica Peruana
    IPFilterRule(*parse_ip('212.106.80.0'), 12), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('212.164.0.0'), 16), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('212.233.128.0'), 15), # Bulgaria - Optisprint OOD
    IPFilterRule(*parse_ip('212.32.192.0'), 13), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('212.45.80.0'), 12), # Kazakhstan - JSC Alma Telecommunications
    IPFilterRule(*parse_ip('212.47.128.0'), 12), # Azerbaijan - Aztelekom LLC
    IPFilterRule(*parse_ip('212.47.144.0'), 11), # Azerbaijan - Aztelekom LLC
    IPFilterRule(*parse_ip('212.70.108.0'), 10), # Qatar - Vodafone Qatar P.Q.S.C
    IPFilterRule(*parse_ip('213.147.160.0'), 13), # Austria - A1 Telekom Austria AG
    IPFilterRule(*parse_ip('213.151.0.0'), 13), # Russia - Ekaterinburg-2000 LLC
    IPFilterRule(*parse_ip('213.230.64.0'), 14), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('213.242.0.0'), 14), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('213.81.128.0'), 15), # Slovakia - Slovak Telekom, a.s.
    IPFilterRule(*parse_ip('216.48.176.0'), 12), # India - 282, Sector 19
    IPFilterRule(*parse_ip('217.142.20.0'), 10), # Bulgaria - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('217.145.228.0'), 10), # Iraq - Hilal Al-Rafidain for Computer and Internet Services Co., Ltd.
    IPFilterRule(*parse_ip('217.164.0.0'), 17), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('217.29.16.0'), 12), # Kyrgyzstan - CJSC SAIMA TELECOM
    IPFilterRule(*parse_ip('217.72.4.0'), 9), # Russia - Thyphone Communications LLC
    IPFilterRule(*parse_ip('221.132.0.0'), 13), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.252.0.0'), 17), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.254.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.255.104.0'), 11), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.255.128.0'), 14), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.255.240.0'), 12), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.255.40.0'), 11), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.255.64.0'), 13), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('223.123.124.0'), 10), # Pakistan - CMPak Limited
    IPFilterRule(*parse_ip('14.1.104.0'), 10), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('14.160.0.0'), 21), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('14.224.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('14.225.0.0'), 16), # Vietnam - VIETNAM POSTS AND TELECOMMUNICATIONS GROUP
    IPFilterRule(*parse_ip('14.226.0.0'), 17), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('14.228.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('14.232.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('14.236.0.0'), 17), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('14.239.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('14.240.0.0'), 20), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('141.105.138.0'), 8), # Ukraine - Private Enterprise "Enterra"
    IPFilterRule(*parse_ip('141.8.0.0'), 15), # Malta - Melita Limited
    IPFilterRule(*parse_ip('142.93.176.0'), 12), # United States - DigitalOcean, LLC
    IPFilterRule(*parse_ip('143.0.188.0'), 10), # Brazil - AGT NET
    IPFilterRule(*parse_ip('143.0.228.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('143.0.36.0'), 10), # Brazil - TD Telecom
    IPFilterRule(*parse_ip('143.0.64.0'), 10), # Argentina - DOVA SRL
    IPFilterRule(*parse_ip('143.0.72.0'), 10), # Brazil - Matek Soluções de Informatica Ltda
    IPFilterRule(*parse_ip('143.137.156.0'), 10), # Brazil - STIW Sistema de Telecom. Inf e Wireless LTDA
    IPFilterRule(*parse_ip('143.14.151.0'), 8), # Hong Kong - STARLIGHT TECH TRADING CO., LIMITED
    IPFilterRule(*parse_ip('143.20.81.0'), 8), # Hong Kong - STARLIGHT TECH TRADING CO., LIMITED
    IPFilterRule(*parse_ip('143.202.144.0'), 10), # Argentina - COOP DE GRAL VIAMONTE
    IPFilterRule(*parse_ip('143.202.252.0'), 10), # Nicaragua - TECOMUNICA NICARAGUA
    IPFilterRule(*parse_ip('143.202.52.0'), 10), # Brazil - I3 Telecomunicacoes - EIRELI
    IPFilterRule(*parse_ip('143.208.232.0'), 10), # Brazil - Ivatel Redes e Internet LTDA
    IPFilterRule(*parse_ip('143.255.144.0'), 10), # Brazil - Pontonet Computadores e Redes Ltda Epp
    IPFilterRule(*parse_ip('143.255.164.0'), 10), # Brazil - Giganet Comunicações Multimidia Ltda
    IPFilterRule(*parse_ip('143.255.192.0'), 10), # Brazil - NETBE TELECOM LTDA
    IPFilterRule(*parse_ip('143.255.204.0'), 10), # Brazil - Fibralink LTDA
    IPFilterRule(*parse_ip('143.255.208.0'), 10), # Brazil - MC Telecom
    IPFilterRule(*parse_ip('143.255.232.0'), 10), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('145.255.160.0'), 13), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('146.158.96.0'), 13), # Russia - SM Ltd.
    IPFilterRule(*parse_ip('146.158.80.0'), 11), # Russia - Telecom.ru Ltd
    IPFilterRule(*parse_ip('147.30.0.0'), 16), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('148.0.0.0'), 16), # Dominican Republic - Compañía Dominicana de Teléfonos S. A.
    IPFilterRule(*parse_ip('148.230.28.0'), 8), # Guatemala - COMCEL GUATEMALA S.A.
    IPFilterRule(*parse_ip('149.102.232.0'), 8), # Slovakia - Datacamp Limited
    IPFilterRule(*parse_ip('150.241.237.0'), 8), # Hong Kong - STARLIGHT TECH TRADING CO., LIMITED
    IPFilterRule(*parse_ip('150.253.32.0'), 13), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('151.236.160.0'), 12), # Iraq - Al Atheer Telecommunication-Iraq Co. Ltd. Incorporated in Cayman Islands
    IPFilterRule(*parse_ip('151.236.176.0'), 11), # Iraq - Al Atheer Telecommunication-Iraq Co. Ltd. Incorporated in Cayman Islands
    IPFilterRule(*parse_ip('151.244.144.0'), 12), # Iraq - Noor Al-Bedaya for General Trading, agricultural investments, Technical production and distribution, internet services, general services, Information technology and software Ltd
    IPFilterRule(*parse_ip('151.249.128.0'), 15), # Belarus - Unitary enterprise A1
    IPFilterRule(*parse_ip('152.110.0.0'), 16), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('152.168.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('152.200.128.0'), 14), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('152.240.0.0'), 19), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('152.248.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('152.249.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('152.56.0.0'), 18), # India - Reliance Jio Infocomm Limited
    IPFilterRule(*parse_ip('154.124.0.0'), 17), # Senegal - SONATEL-AS Autonomous System
    IPFilterRule(*parse_ip('154.127.128.0'), 15), # Angola - TV CABO ANGOLA LDA
    IPFilterRule(*parse_ip('154.176.0.0'), 20), # Egypt - TE-AS
    IPFilterRule(*parse_ip('154.208.32.0'), 10), # Pakistan - IN CABLE INTERNET (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('154.208.48.0'), 12), # Pakistan - IN CABLE INTERNET (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('154.240.0.0'), 20), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('154.41.184.0'), 10), # Venezuela - FULL DATA COMUNICACIONES C.A.
    IPFilterRule(*parse_ip('154.57.208.0'), 11), # Pakistan - Trans World Enterprise Services (Private) Limited
    IPFilterRule(*parse_ip('154.57.216.0'), 10), # Pakistan - Trans World Enterprise Services (Private) Limited
    IPFilterRule(*parse_ip('155.117.163.0'), 8), # Hong Kong - STARLIGHT TECH TRADING CO., LIMITED
    IPFilterRule(*parse_ip('156.146.60.0'), 8), # Austria - Datacamp Limited
    IPFilterRule(*parse_ip('156.155.0.0'), 15), # South Africa - AFRIHOST SP (PTY) LTD
    IPFilterRule(*parse_ip('156.192.0.0'), 21), # Egypt - TE-AS
    IPFilterRule(*parse_ip('156.247.128.0'), 15), # Venezuela - Airtek Solutions C.A.
    IPFilterRule(*parse_ip('156.255.128.0'), 11), # Venezuela - CORPORACION MATRIX TV, C.A.
    IPFilterRule(*parse_ip('157.100.96.0'), 13), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('157.100.128.0'), 14), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('157.100.192.0'), 11), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('157.100.52.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('157.100.64.0'), 10), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('157.100.80.0'), 12), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('158.140.160.0'), 12), # Indonesia - PT. Eka Mas Republik
    IPFilterRule(*parse_ip('160.176.0.0'), 18), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('160.187.159.0'), 8), # Bangladesh - Sara Networking System
    IPFilterRule(*parse_ip('160.20.164.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('160.20.200.0'), 10), # Brazil - A M TELECOM LTDA
    IPFilterRule(*parse_ip('160.20.204.0'), 10), # Brazil - PLANETCLICK TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('160.20.84.0'), 10), # Brazil - G2G COM PROD ELETRO E SERV LTDA
    IPFilterRule(*parse_ip('164.163.140.0'), 10), # Brazil - Micropic Ltda
    IPFilterRule(*parse_ip('164.163.148.0'), 10), # Brazil - Itnet ltda
    IPFilterRule(*parse_ip('164.163.16.0'), 10), # Brazil - Rap 10 Telecomunicações Eireli
    IPFilterRule(*parse_ip('164.163.248.0'), 10), # Brazil - WM TELECOM
    IPFilterRule(*parse_ip('165.16.160.0'), 13), # South Africa - South African Digital Villages (Pty) Ltd
    IPFilterRule(*parse_ip('165.165.64.0'), 14), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('165.50.0.0'), 17), # Tunisia - Orange Tunisie
    IPFilterRule(*parse_ip('167.148.117.0'), 8), # Hong Kong - STARLIGHT TECH TRADING CO., LIMITED
    IPFilterRule(*parse_ip('167.249.48.0'), 10), # Brazil - PROXXIMA TELECOMUNICACOES SA
    IPFilterRule(*parse_ip('167.250.208.0'), 10), # Argentina - Coop. Energía Elect. y Otros Servicios Las Varillas
    IPFilterRule(*parse_ip('167.250.220.0'), 10), # Guatemala - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('167.250.244.0'), 10), # Brazil - TefNet Tecnologia - Internet Service Provider
    IPFilterRule(*parse_ip('167.56.0.0'), 19), # Uruguay - Administracion Nacional de Telecomunicaciones
    IPFilterRule(*parse_ip('168.0.128.0'), 10), # Brazil - BRT Comercio de Produtos de Informática LTDA
    IPFilterRule(*parse_ip('168.0.216.0'), 10), # Brazil - Intermicro Ltda
    IPFilterRule(*parse_ip('168.121.152.0'), 10), # Brazil - ANDERLINE TELECOMUNICACOES E MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('168.121.176.0'), 10), # Brazil - BINDNET RJ
    IPFilterRule(*parse_ip('168.121.72.0'), 10), # Brazil - SULCATEL COMERCIO DE TELEFONIA LTDA - ME
    IPFilterRule(*parse_ip('168.194.140.0'), 10), # Argentina - SWISSNET S.R.L.
    IPFilterRule(*parse_ip('168.196.48.0'), 10), # Brazil - Henet Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('168.196.8.0'), 10), # Brazil - Netsul Servico de Provedor Ltda
    IPFilterRule(*parse_ip('168.196.88.0'), 10), # Brazil - RedeBr Telecom
    IPFilterRule(*parse_ip('168.197.140.0'), 10), # Brazil - NET EXPRESS BRASIL LTDA - ME
    IPFilterRule(*parse_ip('168.197.152.0'), 10), # Brazil - CLICK ENTER LTDA - ME
    IPFilterRule(*parse_ip('168.197.220.0'), 10), # Brazil - Conectja Telecom
    IPFilterRule(*parse_ip('168.197.244.0'), 10), # Brazil - Nova Net Telecomunicações Ltda
    IPFilterRule(*parse_ip('168.205.108.0'), 10), # Brazil - PROXXIMA TELECOMUNICACOES SA
    IPFilterRule(*parse_ip('168.205.152.0'), 10), # Brazil - MEGALINK TELECOMUNICACOES LTDA ME
    IPFilterRule(*parse_ip('168.205.172.0'), 10), # Brazil - POWERNET SOLUTIONS LTDA
    IPFilterRule(*parse_ip('168.205.60.0'), 10), # Brazil - TCF Telecomunicações Campo Florido Ltda
    IPFilterRule(*parse_ip('168.227.112.0'), 10), # Brazil - PORTAL LINK TELECOM
    IPFilterRule(*parse_ip('168.227.160.0'), 9), # Brazil - WEB LACERDA PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('168.227.164.0'), 10), # Brazil - FLIX TELECOM
    IPFilterRule(*parse_ip('168.228.112.0'), 10), # Brazil - PKNET PROVEDOR DE ACESSO A INTERNET LTDA - ME
    IPFilterRule(*parse_ip('168.228.204.0'), 10), # Brazil - ADVANX INFORMATICA LTDA
    IPFilterRule(*parse_ip('168.228.36.0'), 10), # Brazil - AVATO TECNOLOGIA S.A
    IPFilterRule(*parse_ip('168.232.160.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('168.232.212.0'), 10), # Brazil - Torres Soares Telecomunicação LTDA
    IPFilterRule(*parse_ip('168.232.80.0'), 10), # Brazil - FIBRA ONDA MAIS LTDA
    IPFilterRule(*parse_ip('168.90.190.0'), 8), # Brazil - IZCOMPANY BRASIL LTDA ME
    IPFilterRule(*parse_ip('168.90.192.0'), 10), # Brazil - tecbuy telecomunicações ltda - me
    IPFilterRule(*parse_ip('168.90.212.0'), 10), # Brazil - Handrigo jose Antunes
    IPFilterRule(*parse_ip('102.0.5.0'), 7), # Kenya - Airtel Networks Kenya Limited
    IPFilterRule(*parse_ip('102.0.8.0'), 11), # Kenya - Airtel Networks Kenya Limited
    IPFilterRule(*parse_ip('102.141.0.0'), 14), # Republic of the Congo - GVA Cote d'Ivoire SAS
    IPFilterRule(*parse_ip('102.184.0.0'), 19), # Egypt - Vodafone Data
    IPFilterRule(*parse_ip('102.207.191.0'), 8), # Kenya - Avitech Solutions LTD
    IPFilterRule(*parse_ip('102.209.216.0'), 11), # Ivory Coast - Orange Côte d'Ivoire
    IPFilterRule(*parse_ip('102.209.76.0'), 10), # Kenya - SAFHOME FIBRE LIMITED
    IPFilterRule(*parse_ip('102.216.176.0'), 10), # South Africa - Mdantsane Mobile
    IPFilterRule(*parse_ip('102.216.44.0'), 10), # Angola - Finstar - Sociedade de Investimento e Participacoes S.A
    IPFilterRule(*parse_ip('102.216.72.0'), 10), # South Africa - Rapid Networks (Pty) Ltd
    IPFilterRule(*parse_ip('102.220.208.0'), 10), # South Africa - Vox Telecom Ltd
    IPFilterRule(*parse_ip('102.254.0.0'), 15), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('102.254.128.0'), 15), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('102.66.0.0'), 16), # South Africa - HERO TELECOMS (PTY) LTD
    IPFilterRule(*parse_ip('102.67.192.0'), 14), # Ivory Coast - GVA Cote d'Ivoire SAS
    IPFilterRule(*parse_ip('102.67.64.0'), 13), # South Africa - Sunset Rose Investments (PTY) LTD
    IPFilterRule(*parse_ip('102.68.120.0'), 10), # South Africa - Too Much Wifi
    IPFilterRule(*parse_ip('102.68.76.0'), 10), # Kenya - Unwired Communications Limited
    IPFilterRule(*parse_ip('102.96.0.0'), 17), # Morocco - MEDITELECOM
    IPFilterRule(*parse_ip('103.10.52.0'), 10), # Bangladesh - Drik ICT Ltd
    IPFilterRule(*parse_ip('103.100.234.0'), 8), # Bangladesh - Gmax
    IPFilterRule(*parse_ip('103.104.28.0'), 10), # Nepal - Firstlink Communications Pvt. Ltd.
    IPFilterRule(*parse_ip('103.108.60.0'), 10), # Bangladesh - INCOMIT SOLUTION
    IPFilterRule(*parse_ip('103.112.52.0'), 10), # Bangladesh - Systems Solutions & development Technologies Limited
    IPFilterRule(*parse_ip('103.121.104.0'), 10), # Bangladesh - Salim Khan & Milon Raihan
    IPFilterRule(*parse_ip('103.121.136.0'), 10), # Indonesia - PT. Cyberindo Aditama
    IPFilterRule(*parse_ip('103.121.76.0'), 9), # Bangladesh - Match Net
    IPFilterRule(*parse_ip('103.121.96.0'), 11), # Indonesia - PT. Cyberindo Aditama
    IPFilterRule(*parse_ip('103.126.150.0'), 8), # Bangladesh - Windstream Communication Limited
    IPFilterRule(*parse_ip('103.133.134.0'), 9), # Bangladesh - Global Network
    IPFilterRule(*parse_ip('103.133.200.0'), 10), # Bangladesh - Antaranga Dot Com Ltd
    IPFilterRule(*parse_ip('103.133.60.0'), 10), # Indonesia - PT Tunas Link Indonesia
    IPFilterRule(*parse_ip('103.134.216.0'), 10), # Nepal - Sajilo Net Pvt Ltd
    IPFilterRule(*parse_ip('103.136.56.0'), 10), # Indonesia - PT Mora Telematika Indonesia
    IPFilterRule(*parse_ip('103.138.123.0'), 8), # Bangladesh - Business Network
    IPFilterRule(*parse_ip('103.139.253.0'), 8), # Bangladesh - NTECH COMMUNICATION
    IPFilterRule(*parse_ip('103.142.0.0'), 9), # Bangladesh - M AMIN Network
    IPFilterRule(*parse_ip('103.143.243.0'), 8), # Bangladesh - Skynet Broadband Service
    IPFilterRule(*parse_ip('103.147.8.0'), 9), # Indonesia - PT. Cemerlang Multimedia
    IPFilterRule(*parse_ip('103.15.246.0'), 9), # Bangladesh - Summit Communications Ltd
    IPFilterRule(*parse_ip('103.152.100.0'), 9), # Pakistan - PLAY BROADBAND (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('103.152.102.0'), 9), # Bangladesh - Dhamrai Network
    IPFilterRule(*parse_ip('103.155.118.0'), 8), # Bangladesh - Race Online Limited
    IPFilterRule(*parse_ip('103.162.230.0'), 9), # Bangladesh - Net-E-Zen
    IPFilterRule(*parse_ip('103.162.56.0'), 8), # Bangladesh - Orange Communication
    IPFilterRule(*parse_ip('103.165.176.0'), 8), # Pakistan - Multinet Pakistan Pvt. Ltd.
    IPFilterRule(*parse_ip('103.165.240.0'), 9), # Indonesia - PT iForte Global Internet
    IPFilterRule(*parse_ip('103.167.102.0'), 9), # India - INTERCITY FIBER NETWORKS PRIVATE LIMITED
    IPFilterRule(*parse_ip('103.168.8.0'), 8), # Bangladesh - Salauddin Cybernet
    IPFilterRule(*parse_ip('103.172.120.0'), 9), # Indonesia - PT Digital Akses Nusantara
    IPFilterRule(*parse_ip('103.173.120.0'), 9), # India - Juweriyah Networks Private Limited
    IPFilterRule(*parse_ip('103.176.18.0'), 8), # Bangladesh - Xplore Net BD
    IPFilterRule(*parse_ip('103.179.248.0'), 9), # Indonesia - PT INDONESIA COMNETS PLUS
    IPFilterRule(*parse_ip('103.185.25.0'), 8), # Bangladesh - Orange Communication
    IPFilterRule(*parse_ip('103.186.52.0'), 8), # Bangladesh - Wave Net
    IPFilterRule(*parse_ip('103.188.172.0'), 9), # Indonesia - PT Satria Digital Media
    IPFilterRule(*parse_ip('103.19.122.0'), 9), # Bangladesh - Deshnet Broadband
    IPFilterRule(*parse_ip('103.197.248.0'), 10), # Bangladesh - S.M. ZAKIR HOSSAIN t/a EUROtelbd Online Ltd.
    IPFilterRule(*parse_ip('103.20.180.0'), 10), # Bangladesh - RADIANT COMMUNICATIONS LTD IIG
    IPFilterRule(*parse_ip('103.200.36.0'), 10), # Bangladesh - Skyview Online Ltd
    IPFilterRule(*parse_ip('103.205.134.0'), 9), # Bangladesh - ICC Communication
    IPFilterRule(*parse_ip('103.227.186.0'), 9), # Indonesia - PT Master Star Network
    IPFilterRule(*parse_ip('103.239.252.0'), 10), # Bangladesh - Systems Solutions & development Technologies Limited
    IPFilterRule(*parse_ip('103.24.124.0'), 9), # India - Pioneer Elabs Ltd.
    IPFilterRule(*parse_ip('103.241.195.0'), 8), # Bangladesh - Dot Internet
    IPFilterRule(*parse_ip('103.245.192.0'), 10), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('103.66.230.0'), 9), # Bangladesh - STAR VISION CLASSIC CABLE NETWORK
    IPFilterRule(*parse_ip('103.77.136.0'), 10), # India - Alliance Broadband Services Pvt. Ltd.
    IPFilterRule(*parse_ip('103.77.188.0'), 10), # Bangladesh - NETSCOPE
    IPFilterRule(*parse_ip('103.82.202.0'), 9), # Bangladesh - Hire Electronic & Networking
    IPFilterRule(*parse_ip('104.236.0.0'), 16), # United States - DigitalOcean, LLC
    IPFilterRule(*parse_ip('104.244.224.0'), 11), # Jamaica - Digicel Jamaica
    IPFilterRule(*parse_ip('105.96.0.0'), 20), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('105.158.0.0'), 16), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('105.184.0.0'), 18), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('105.188.0.0'), 18), # Morocco - MEDITELECOM
    IPFilterRule(*parse_ip('105.209.128.0'), 14), # South Africa - MTN SA
    IPFilterRule(*parse_ip('105.245.0.0'), 15), # South Africa - Vodacom
    IPFilterRule(*parse_ip('105.64.0.0'), 20), # Morocco - Wana Corporate
    IPFilterRule(*parse_ip('106.192.64.0'), 14), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('106.205.128.0'), 15), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('106.219.160.0'), 12), # India - Bharti Airtel Ltd., Telemedia Services
    IPFilterRule(*parse_ip('109.60.0.0'), 15), # Croatia - A1 Hrvatska d.o.o.
    IPFilterRule(*parse_ip('109.80.0.0'), 17), # Czechia - O2 Czech Republic, a.s.
    IPFilterRule(*parse_ip('110.136.0.0'), 18), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('110.226.160.0'), 12), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('113.160.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.164.128.0'), 15), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.164.32.0'), 13), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.164.64.0'), 14), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.165.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.166.0.0'), 17), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.168.0.0'), 17), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.170.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.171.160.0'), 13), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.172.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.176.0.0'), 20), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('113.212.108.0'), 10), # Bangladesh - City Online Ltd.
    IPFilterRule(*parse_ip('114.120.0.0'), 19), # Indonesia - PT. Telekomunikasi Selular
    IPFilterRule(*parse_ip('116.108.112.0'), 12), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('116.108.80.0'), 12), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('116.111.184.0'), 11), # Vietnam - Viettel Corporation
    IPFilterRule(*parse_ip('116.71.64.0'), 14), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('116.98.0.0'), 10), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('117.4.0.0'), 18), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('118.179.0.0'), 10), # Bangladesh - Alo Communications limited
    IPFilterRule(*parse_ip('118.179.16.0'), 12), # Bangladesh - bdHUB Limited
    IPFilterRule(*parse_ip('119.160.168.0'), 10), # Brunei - Unified National Networks
    IPFilterRule(*parse_ip('122.50.1.0'), 8), # Pakistan - Logon Broadband Pvt. Limited
    IPFilterRule(*parse_ip('123.16.0.0'), 19), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.24.0.0'), 18), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.28.0.0'), 16), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.30.208.0'), 12), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.30.0.0'), 14), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.30.80.0'), 11), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.31.128.0'), 15), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.31.48.0'), 12), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('123.31.64.0'), 14), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('125.162.0.0'), 16), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('125.164.0.0'), 18), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('128.201.236.0'), 10), # Argentina - REDES BANDA ANCHA SOLUCIONES S.R.L
    IPFilterRule(*parse_ip('128.201.32.0'), 10), # Brazil - ERICK TELECOM
    IPFilterRule(*parse_ip('128.201.76.0'), 10), # Brazil - 18.843.555 LTDA
    IPFilterRule(*parse_ip('130.255.88.0'), 10), # Iraq - Nawand Telecom Ltd./private company
    IPFilterRule(*parse_ip('131.0.112.0'), 10), # Brazil - UAI TELECOM COMUNICACAO MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('131.0.28.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('131.0.48.0'), 10), # Brazil - VILAVNET SOLUCOES EM INFORMATICA LTDA-ME
    IPFilterRule(*parse_ip('131.100.16.0'), 10), # Brazil - MARIA NEUSA PEREIRA DE SOUSA E CIA LTDA EPP
    IPFilterRule(*parse_ip('131.108.176.0'), 8), # Brazil - Ferabraznet Comenrcio e Serv. de Telecom. Ltda-ME
    IPFilterRule(*parse_ip('131.108.220.0'), 10), # Brazil - GUIGO NET EMPRESA TOP NET PROVEDORES EIRELE
    IPFilterRule(*parse_ip('131.161.104.0'), 10), # Brazil - CORPORATIVA TELECOMUNICACOES EIRELI ME
    IPFilterRule(*parse_ip('131.196.12.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('131.196.56.0'), 10), # Brazil - Livenet telecom
    IPFilterRule(*parse_ip('131.196.76.0'), 10), # Brazil - CONEXAO - TELECOM. E INTERNET LTDA
    IPFilterRule(*parse_ip('131.196.82.0'), 8), # Argentina - Ruben Oscar Mosso(INTERZONA WIFI)
    IPFilterRule(*parse_ip('131.196.8.0'), 10), # Ecuador - ANGEL BENIGNO CONDOLO GUAYA
    IPFilterRule(*parse_ip('131.255.68.0'), 10), # Brazil - TURBONET TELECOM LTDA
    IPFilterRule(*parse_ip('131.72.148.0'), 10), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('131.72.252.0'), 10), # Brazil - SINTNET-TELECOMUNICACOES E INFORMATICA LTDA
    IPFilterRule(*parse_ip('131.72.84.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('132.191.0.0'), 16), # Peru - ENTEL PERU S.A.
    IPFilterRule(*parse_ip('132.255.128.0'), 10), # Brazil - G.F. SERVICOS DE COMUNICACAO LTDA
    IPFilterRule(*parse_ip('138.0.112.0'), 10), # Brazil - SUPER NOVA TELECOM LTDA
    IPFilterRule(*parse_ip('138.0.72.0'), 10), # Brazil - HET INTERNET LTDA
    IPFilterRule(*parse_ip('138.117.76.0'), 10), # Argentina - MARANDU COMUNICACIONES SOCIEDAD DEL ESTADO
    IPFilterRule(*parse_ip('138.118.184.0'), 10), # Brazil - MUTUM FIBRA LTDA
    IPFilterRule(*parse_ip('138.121.204.0'), 10), # Brazil - Nova Net Telecomunicações Ltda
    IPFilterRule(*parse_ip('138.185.220.0'), 10), # Brazil - DELTA TELECOM
    IPFilterRule(*parse_ip('138.185.88.0'), 10), # Brazil - INTERNETUP TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('138.186.160.0'), 10), # Argentina - RESEARCH SRL
    IPFilterRule(*parse_ip('138.204.208.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('138.204.212.0'), 10), # Brazil - Adaptlink Serviços de Comunicação Multimídia Ltda.
    IPFilterRule(*parse_ip('138.219.200.0'), 10), # Brazil - MALTA E CARVALHO LTDA - EPP
    IPFilterRule(*parse_ip('138.219.212.0'), 10), # Argentina - GRUPO EQUIS S.A.
    IPFilterRule(*parse_ip('138.219.216.0'), 10), # Argentina - Jose Luis Zurakouski (MIX SERVICIOS & COMUNICACIONES)
    IPFilterRule(*parse_ip('138.36.56.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('138.59.28.0'), 10), # Brazil - TOKFIBRA Provedor de Internet
    IPFilterRule(*parse_ip('138.84.42.0'), 9), # Brazil - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('138.97.116.0'), 10), # Brazil - NC BRASIL TELECOM E SERVICOS LTDA- ME
    IPFilterRule(*parse_ip('138.97.188.0'), 10), # Brazil - Eagnet Telecomunicações Eireli-Me
    IPFilterRule(*parse_ip('139.0.64.0'), 14), # Indonesia - Linknet-Fastnet ASN
    IPFilterRule(*parse_ip('102.100.0.0'), 18), # Morocco - MEDITELECOM
    IPFilterRule(*parse_ip('102.168.0.0'), 19), # Tunisia - OOREDOO TUNISIE SA
    IPFilterRule(*parse_ip('102.209.4.0'), 10), # Angola - Finstar - Sociedade de Investimento e Participacoes S.A
    IPFilterRule(*parse_ip('102.22.120.0'), 10), # South Africa - Vaal Networking Consultants (PTY) LTD
    IPFilterRule(*parse_ip('102.220.68.0'), 10), # South Africa - Silver Solutions 1234
    IPFilterRule(*parse_ip('102.32.0.0'), 17), # South Africa - Metrofibre Networx
    IPFilterRule(*parse_ip('103.10.194.0'), 8), # Bangladesh - MIR INFO SYSTEMS LTD.
    IPFilterRule(*parse_ip('103.10.195.0'), 8), # Bangladesh - HOMENET BROADBAND COMMUNICATION AND TECHNOLOGIES
    IPFilterRule(*parse_ip('103.109.238.0'), 9), # Bangladesh - ICC Communication
    IPFilterRule(*parse_ip('103.112.128.0'), 10), # Bangladesh - Sayem Online Communication
    IPFilterRule(*parse_ip('103.14.151.0'), 8), # Bangladesh - IP Communications Limited
    IPFilterRule(*parse_ip('103.145.134.0'), 9), # Bangladesh - Smart Online
    IPFilterRule(*parse_ip('103.148.26.0'), 9), # Bangladesh - The Smart Network
    IPFilterRule(*parse_ip('103.166.234.0'), 8), # Indonesia - KitaNet
    IPFilterRule(*parse_ip('103.175.245.0'), 8), # Bangladesh - Orange Communication
    IPFilterRule(*parse_ip('103.183.17.0'), 8), # Bangladesh - I Communication
    IPFilterRule(*parse_ip('103.191.122.0'), 9), # Pakistan - WellNetworks (Private) Limited
    IPFilterRule(*parse_ip('103.209.199.0'), 8), # Bangladesh - Md. Shariful Islam T/A BRISK SYSTEMS
    IPFilterRule(*parse_ip('103.220.204.0'), 10), # Bangladesh - KS Network Limited
    IPFilterRule(*parse_ip('103.244.140.0'), 10), # Bangladesh - BlueNet Communication JV Ltd.
    IPFilterRule(*parse_ip('103.253.102.0'), 9), # Bangladesh - G Net Service
    IPFilterRule(*parse_ip('103.54.108.0'), 9), # Bangladesh - Maijdee Supernet
    IPFilterRule(*parse_ip('103.65.226.0'), 9), # Bangladesh - Master IT
    IPFilterRule(*parse_ip('103.70.140.0'), 10), # Bangladesh - Mir Mosharrof Hossain t/a IT Base
    IPFilterRule(*parse_ip('103.84.36.0'), 10), # Bangladesh - City Online Ltd.
    IPFilterRule(*parse_ip('103.86.56.0'), 9), # Nepal - Web Networks Pvt. Ltd.
    IPFilterRule(*parse_ip('106.0.48.0'), 10), # Indonesia - PT SOLNET INDONESIA
    IPFilterRule(*parse_ip('109.107.224.0'), 13), # Jordan - Batelco Jordan
    IPFilterRule(*parse_ip('109.234.232.0'), 11), # Albania - ONE ALBANIA SH.A.
    IPFilterRule(*parse_ip('115.72.0.0'), 19), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('116.97.104.0'), 11), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('118.179.64.0'), 14), # Bangladesh - AmberIT Limited
    IPFilterRule(*parse_ip('118.70.128.0'), 15), # Vietnam - FPT Telecom Company
    IPFilterRule(*parse_ip('129.45.0.0'), 15), # Algeria - Optimum Telecom Algeria
    IPFilterRule(*parse_ip('131.0.64.0'), 10), # Brazil - Acesse Comunicação Ltda
    IPFilterRule(*parse_ip('131.108.160.0'), 10), # Brazil - GRANDE REDE TELECOM EIRELLE
    IPFilterRule(*parse_ip('131.161.152.0'), 10), # Argentina - Cotesma
    IPFilterRule(*parse_ip('131.196.104.0'), 10), # Brazil - SMART LINCK TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('131.72.100.0'), 10), # Brazil - SINALNET Comunicações
    IPFilterRule(*parse_ip('138.0.24.0'), 10), # Brazil - Erik Lucas Barbosa
    IPFilterRule(*parse_ip('138.0.36.0'), 10), # Brazil - JPP PANCINI LTDA
    IPFilterRule(*parse_ip('138.0.60.0'), 10), # Brazil - WELLINGTON SEVERINO DA SILVA - ME
    IPFilterRule(*parse_ip('138.122.132.0'), 10), # Brazil - ALCANS TELECOM LTDA
    IPFilterRule(*parse_ip('138.122.148.0'), 10), # Brazil - NET COM INFORMATICA LTDA - ME
    IPFilterRule(*parse_ip('138.219.60.0'), 10), # Argentina - SGS VALLEVISION SRL
    IPFilterRule(*parse_ip('138.59.124.0'), 10), # Brazil - DIGITAL PROVEDOR DE ACESSO A INTERNET LTDA
    IPFilterRule(*parse_ip('138.59.152.0'), 10), # Brazil - 3R INTERNET SOLUCOES EM INFORMATICA LTDA
    IPFilterRule(*parse_ip('138.59.24.0'), 10), # Trinidad and Tobago - Columbus Communications Trinidad Limited.
    IPFilterRule(*parse_ip('138.97.132.0'), 10), # Brazil - BrasilNET Telecomunicações do Parana LTDA
    IPFilterRule(*parse_ip('138.99.72.0'), 10), # Brazil - Coonexao Telecom e Informatica EIRELI
    IPFilterRule(*parse_ip('14.192.192.0'), 14), # Malaysia - Binariang Berhad
    IPFilterRule(*parse_ip('143.0.16.0'), 10), # Brazil - FASTNET COMUNICACAO EIRELI - ME
    IPFilterRule(*parse_ip('148.222.206.0'), 9), # Brazil - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('148.244.128.0'), 15), # Mexico - Alestra, S. de R.L. de C.V.
    IPFilterRule(*parse_ip('149.88.98.0'), 8), # Canada - Datacamp Limited
    IPFilterRule(*parse_ip('151.0.48.0'), 10), # Russia - Consumer Internet Cooperative PG-19
    IPFilterRule(*parse_ip('151.236.188.0'), 10), # Iraq - Al Atheer Telecommunication-Iraq Co. Ltd. Incorporated in Cayman Islands
    IPFilterRule(*parse_ip('154.121.0.0'), 16), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('158.181.40.0'), 11), # Azerbaijan - Aztelekom LLC
    IPFilterRule(*parse_ip('160.20.168.0'), 10), # Brazil - NEW NET TELECOM LTDA
    IPFilterRule(*parse_ip('161.0.192.0'), 13), # Honduras - Newcom Limited
    IPFilterRule(*parse_ip('164.163.112.0'), 10), # Brazil - FNETCOM TELECOMUNICACAO E INFORMATICA LTDA
    IPFilterRule(*parse_ip('164.163.176.0'), 10), # Brazil - J M P M ALENCAR & A G F ALENCAR LTDA - ME
    IPFilterRule(*parse_ip('164.163.48.0'), 10), # Ecuador - ZOENETV S.A.
    IPFilterRule(*parse_ip('168.181.140.0'), 10), # Brazil - SYNDIGITAL TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('168.197.24.0'), 10), # Brazil - MUVNET TELECOM
    IPFilterRule(*parse_ip('168.228.20.0'), 10), # Brazil - Clesat Comunicação e Manutenção em Eletro.LDTA ME
    IPFilterRule(*parse_ip('170.150.208.0'), 10), # Brazil - IMUNIDADE DIGITAL SERVICOS EM COMUNICACAO LTDA
    IPFilterRule(*parse_ip('170.150.92.0'), 10), # Brazil - VOUE LTDA
    IPFilterRule(*parse_ip('170.231.84.0'), 10), # Brazil - BROSEGHINI LTDA EPP
    IPFilterRule(*parse_ip('170.238.176.0'), 10), # Brazil - SEMPRE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('170.244.100.0'), 10), # Brazil - Inova Fibra
    IPFilterRule(*parse_ip('170.244.36.0'), 10), # Brazil - INSTATEL SERVICOS ELETRONICOS LTDA
    IPFilterRule(*parse_ip('170.80.192.0'), 10), # Brazil - HLRC PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('170.81.164.0'), 10), # Brazil - SERVTEL EIRELI
    IPFilterRule(*parse_ip('170.82.206.0'), 9), # Brazil - GCOM NETWORKS LTDA ME
    IPFilterRule(*parse_ip('176.115.124.0'), 8), # Russia - JSC Elektrosvyaz
    IPFilterRule(*parse_ip('177.10.0.0'), 12), # Brazil - Clean Net Telecom Ltda
    IPFilterRule(*parse_ip('177.10.116.0'), 10), # Brazil - SPACE NET SERV. DE TELECOMUNICAÇÃO EM INF. LTDA-ME
    IPFilterRule(*parse_ip('177.107.176.0'), 12), # Brazil - PROVEDOR BRCENTRAL.NET LTDA
    IPFilterRule(*parse_ip('177.128.124.0'), 10), # Brazil - ISP PREMIUM TELECOM S/A
    IPFilterRule(*parse_ip('177.131.132.0'), 10), # Brazil - L2K Informatica LTDA
    IPFilterRule(*parse_ip('177.16.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.177.192.0'), 14), # Brazil - V tal
    IPFilterRule(*parse_ip('177.194.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.200.156.0'), 9), # Brazil - Kelvyn Sat Comércio e telecomunicações Ltda
    IPFilterRule(*parse_ip('177.221.96.0'), 12), # Brazil - Bi-Link Telecom
    IPFilterRule(*parse_ip('177.223.156.0'), 9), # Brazil - G NETWEB TELECOM LTDA - ME
    IPFilterRule(*parse_ip('177.228.0.0'), 16), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('177.242.152.0'), 11), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('177.38.104.0'), 11), # Brazil - Intermicro Ltda
    IPFilterRule(*parse_ip('177.71.24.0'), 11), # Brazil - Invista Net Provedor de Acesso Ltda
    IPFilterRule(*parse_ip('177.74.208.0'), 12), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('177.84.50.0'), 9), # Brazil - GE Network Provedor de Internet LTDA
    IPFilterRule(*parse_ip('178.218.16.0'), 12), # Russia - GigaLink Ltd.
    IPFilterRule(*parse_ip('178.219.168.22'), 1), # Russia - Ltd. "Cypher"
    IPFilterRule(*parse_ip('178.77.128.0'), 14), # Jordan - Al mouakhah lil khadamat al logesteih wa al itisalat
    IPFilterRule(*parse_ip('178.86.32.0'), 12), # Saudi Arabia - Saudi Telecom Company JSC
    IPFilterRule(*parse_ip('179.0.72.0'), 10), # Brazil - BTT TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('179.104.0.0'), 16), # Brazil - ALGAR TELECOM S/A
    IPFilterRule(*parse_ip('179.108.0.0'), 12), # Brazil - Desktop Sigmanet Comunicação Multimídia SA
    IPFilterRule(*parse_ip('179.127.64.0'), 11), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('179.2.0.0'), 16), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('179.63.112.0'), 10), # Brazil - EB FOX TELECOM LTDA
    IPFilterRule(*parse_ip('179.63.20.0'), 10), # Ecuador - DESPLIEGUE COMPUTACIONAL E INTERNET DCNET S.A.
    IPFilterRule(*parse_ip('179.63.80.0'), 10), # Brazil - VIPER TEC
    IPFilterRule(*parse_ip('179.98.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('180.241.0.0'), 16), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('181.117.224.0'), 13), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.164.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('181.174.158.0'), 8), # Argentina - AGUAS DEL COLORADO SAPEM
    IPFilterRule(*parse_ip('181.224.234.0'), 8), # Peru - INVERSIONES TELCOTEL SAC
    IPFilterRule(*parse_ip('181.224.235.0'), 8), # Peru - ECONOCABLE MEDIA SAC
    IPFilterRule(*parse_ip('181.51.128.0'), 14), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('181.72.0.0'), 18), # Chile - Telmex Servicios Empresariales S.A.
    IPFilterRule(*parse_ip('181.94.232.0'), 10), # Paraguay - Núcleo S.A.
    IPFilterRule(*parse_ip('181.97.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('182.176.0.0'), 19), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('182.190.192.0'), 13), # Pakistan - Wancom (Pvt) Ltd.
    IPFilterRule(*parse_ip('185.134.176.0'), 8), # Lebanon - Wave Net LLC
    IPFilterRule(*parse_ip('185.135.148.0'), 10), # Russia - MAXnet Systems Ltd.
    IPFilterRule(*parse_ip('185.181.108.0'), 10), # Iraq - I.Q Online for Internet Services and Communications LLC
    IPFilterRule(*parse_ip('185.30.40.0'), 10), # Russia - SerDi TeleCom, LTD
    IPFilterRule(*parse_ip('185.38.192.0'), 10), # Albania - APT CABLE SHPK
    IPFilterRule(*parse_ip('185.84.68.0'), 10), # Iraq - Korek Telecom Company for Communications LLC
    IPFilterRule(*parse_ip('186.104.0.0'), 18), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('186.11.0.0'), 15), # Chile - ENTEL CHILE S.A.
    IPFilterRule(*parse_ip('186.188.128.0'), 15), # Panama - Cable Onda
    IPFilterRule(*parse_ip('186.193.128.0'), 13), # Brazil - Telemidia Sistema de Telecomunicacao Ltda
    IPFilterRule(*parse_ip('186.193.192.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('186.250.204.0'), 10), # Brazil - G6 Internet
    IPFilterRule(*parse_ip('186.57.0.0'), 16), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('187.0.16.0'), 12), # Brazil - TERRA FIBER TELECOM LTDA-ME
    IPFilterRule(*parse_ip('187.108.112.0'), 12), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('187.110.224.0'), 12), # Brazil - DB3 SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('187.121.192.0'), 13), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('187.161.128.0'), 13), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('187.189.212.0'), 10), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.190.184.0'), 10), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.190.24.0'), 11), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.212.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.246.0.0'), 17), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('187.58.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.60.176.0'), 12), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('187.63.208.0'), 12), # Brazil - Superip Telecomunicações LTDA
    IPFilterRule(*parse_ip('187.87.16.0'), 11), # Brazil - Marinter Telecom Ltda.
    IPFilterRule(*parse_ip('189.110.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.126.208.0'), 12), # Brazil - NOVACIA TECNOLOGIA E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('189.164.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.168.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.176.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.199.32.0'), 12), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('189.203.182.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('189.203.228.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('189.203.88.0'), 11), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('189.216.16.0'), 12), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('189.217.192.0'), 13), # Mexico - Cablevisión, S.A. de C.V.
    IPFilterRule(*parse_ip('189.48.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('189.58.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.90.24.0'), 10), # Brazil - RBT Internet
    IPFilterRule(*parse_ip('190.104.116.0'), 8), # Guatemala - Servicios Innovadores de Comunicación y Entretenimiento, S.A.
    IPFilterRule(*parse_ip('190.212.128.0'), 15), # Nicaragua - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.226.128.0'), 14), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.52.72.0'), 10), # Brazil - BTT TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('190.57.192.0'), 13), # Argentina - Cooperativa Telefonica Del Viso
    IPFilterRule(*parse_ip('190.80.128.0'), 15), # Dominican Republic - Compañía Dominicana de Teléfonos S. A.
    IPFilterRule(*parse_ip('190.9.80.0'), 10), # Brazil - TOP NET SERVICOS DE PROVEDOR LTDA - ME
    IPFilterRule(*parse_ip('190.93.192.0'), 13), # Argentina - Davitel S.A.
    IPFilterRule(*parse_ip('191.124.0.0'), 18), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('191.253.40.0'), 11), # Brazil - SERRA GERAL SOLUCOES PARA INTERNET LTDA
    IPFilterRule(*parse_ip('191.37.16.0'), 11), # Brazil - RapeedoISP LTDA
    IPFilterRule(*parse_ip('191.52.240.0'), 11), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('191.6.0.0'), 10), # Brazil - BETINI NET TELECOM LTDA
    IPFilterRule(*parse_ip('191.8.0.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('192.140.40.0'), 10), # Brazil - Allfiber Telecom Serviços de Telecomunicações
    IPFilterRule(*parse_ip('192.141.244.0'), 10), # Mexico - ALTAN REDES, S.A.P.I. de C. V.
    IPFilterRule(*parse_ip('192.141.84.0'), 10), # Brazil - Espaço Link Telecomunicações LTDA - ME
    IPFilterRule(*parse_ip('194.28.180.0'), 10), # Ukraine - FOP Markovskiy Denis Vadimovich
    IPFilterRule(*parse_ip('197.144.0.0'), 18), # Morocco - Wana Corporate
    IPFilterRule(*parse_ip('197.254.0.0'), 15), # Kenya - ACCESSKENYA GROUP LTD is an ISP serving
    IPFilterRule(*parse_ip('197.89.72.0'), 10), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('2.48.0.0'), 18), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('200.117.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('200.124.224.0'), 13), # Ecuador - Ecuadortelecom S.A.
    IPFilterRule(*parse_ip('200.229.156.0'), 10), # Brazil - Emex Internet
    IPFilterRule(*parse_ip('200.24.64.0'), 11), # Brazil - NET INFINITO INTERNET FIBRA OPTICA
    IPFilterRule(*parse_ip('200.50.232.0'), 10), # Ecuador - Eliana Vanessa Morocho Oña
    IPFilterRule(*parse_ip('200.55.244.0'), 10), # Argentina - Servicios y Telecomunicaciones S.A.
    IPFilterRule(*parse_ip('200.87.128.0'), 14), # Bolivia - EMPRESA NACIONAL DE TELECOMUNICACIONES SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('200.87.0.0'), 15), # Bolivia - EMPRESA NACIONAL DE TELECOMUNICACIONES SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('200.91.32.0'), 11), # Argentina - Internet Para Todos - Gobierno de La Rioja
    IPFilterRule(*parse_ip('201.119.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('201.173.0.0'), 15), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('201.182.164.0'), 10), # Brazil - +Net & Telecom
    IPFilterRule(*parse_ip('201.186.0.0'), 16), # Chile - Telefonica del Sur S.A.
    IPFilterRule(*parse_ip('201.71.16.0'), 10), # Brazil - LX7 TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('202.65.224.0'), 12), # Indonesia - PT. NAP Info Lintas Nusa
    IPFilterRule(*parse_ip('203.148.84.0'), 9), # Indonesia - Indotrans Data, PT
    IPFilterRule(*parse_ip('205.164.144.0'), 12), # Pakistan - Optix Pakistan (Pvt.) Limited
    IPFilterRule(*parse_ip('209.101.24.0'), 9), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('212.146.160.0'), 11), # Oman - Oman Future Telecommunications Company SAOC
    IPFilterRule(*parse_ip('212.241.0.0'), 13), # Kyrgyzstan - OJSC Kyrgyztelecom
    IPFilterRule(*parse_ip('212.39.64.0'), 13), # Bulgaria - Vivacom Bulgaria EAD
    IPFilterRule(*parse_ip('212.60.160.0'), 13), # Austria - A1 Telekom Austria AG
    IPFilterRule(*parse_ip('216.234.208.0'), 9), # Brazil - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('222.255.36.0'), 9), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('222.255.48.0'), 12), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('223.123.104.0'), 11), # Pakistan - CMPak Limited
    IPFilterRule(*parse_ip('223.123.0.0'), 13), # Pakistan - CMPak Limited
    IPFilterRule(*parse_ip('31.131.128.0'), 11), # Ukraine - IE Parhomenko Aleksey Aleksandrovich
    IPFilterRule(*parse_ip('31.180.0.0'), 17), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('31.208.0.0'), 14), # Sweden - Bredband2 AB
    IPFilterRule(*parse_ip('31.24.252.0'), 8), # Iraq - prospective information technology ltd
    IPFilterRule(*parse_ip('36.64.0.0'), 17), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('36.80.0.0'), 20), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('37.111.210.0'), 9), # Bangladesh - GrameenPhone Ltd.
    IPFilterRule(*parse_ip('37.114.144.0'), 12), # Azerbaijan - Uninet LLC
    IPFilterRule(*parse_ip('37.186.50.0'), 9), # Qatar - Vodafone Qatar P.Q.S.C
    IPFilterRule(*parse_ip('37.236.128.0'), 14), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.236.64.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.239.192.0'), 14), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.40.64.0'), 14), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('38.171.0.0'), 16), # Venezuela - Airtek Solutions C.A.
    IPFilterRule(*parse_ip('38.196.192.0'), 10), # Venezuela - WLINK TELECOM CA
    IPFilterRule(*parse_ip('39.34.128.0'), 12), # Pakistan - Connect Communications
    IPFilterRule(*parse_ip('41.116.0.0'), 17), # South Africa - MTN SA
    IPFilterRule(*parse_ip('41.34.0.0'), 17), # Egypt - TE-AS
    IPFilterRule(*parse_ip('41.62.0.0'), 16), # Tunisia - TOPNET
    IPFilterRule(*parse_ip('41.71.0.0'), 15), # South Africa - RSAWEB (PTY) LTD
    IPFilterRule(*parse_ip('41.74.48.0'), 12), # Botswana - Orange Botswana (PTY) Ltd
    IPFilterRule(*parse_ip('45.117.62.0'), 9), # Bangladesh - Orange Communication
    IPFilterRule(*parse_ip('45.160.92.0'), 10), # Brazil - Net Sul LTDA - ME
    IPFilterRule(*parse_ip('45.167.84.0'), 10), # Brazil - BRASUL NETWORKS
    IPFilterRule(*parse_ip('45.175.16.0'), 10), # Brazil - ERNANE FAUAZE DOS ANJOS E CIA LTDA
    IPFilterRule(*parse_ip('45.178.248.0'), 10), # Brazil - UNIVERSO FIBER COMUNICACAO MULTIMIDIA
    IPFilterRule(*parse_ip('45.180.16.0'), 10), # Brazil - LINK BRASIL TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.180.35.0'), 8), # Brazil - AD TELECOM
    IPFilterRule(*parse_ip('45.183.16.0'), 10), # Brazil - SOL TELECOM LTDA
    IPFilterRule(*parse_ip('45.183.248.0'), 10), # Brazil - NETMITT IMP & MULTIMIDIA EIRELI
    IPFilterRule(*parse_ip('45.188.176.0'), 10), # Brazil - TEC PLUS TELECOMUNICAO LTDA
    IPFilterRule(*parse_ip('45.190.4.0'), 10), # Brazil - Malugainfor Comércio de Produtos de Informática Lt
    IPFilterRule(*parse_ip('45.191.252.0'), 10), # Brazil - LINAX SERVICOS DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.225.228.0'), 10), # Brazil - Provnet Internet Ltda
    IPFilterRule(*parse_ip('45.227.56.0'), 10), # Brazil - FIBERNET SERVICOS DE COMUNICACAO LTDA
    IPFilterRule(*parse_ip('45.230.152.0'), 10), # Brazil - NTEL SERVICOS DE COMUNICACAO MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('45.231.232.0'), 10), # Brazil - WN TELECOM LTDA - ME
    IPFilterRule(*parse_ip('45.234.86.0'), 8), # Paraguay - Masternet Telecomunicaciones
    IPFilterRule(*parse_ip('45.238.112.0'), 10), # Brazil - LINK BARATO.COM TELECOMUNICACOES EIRELI
    IPFilterRule(*parse_ip('45.238.136.0'), 10), # Brazil - CST - Cerentini Soluções em Tecnologia
    IPFilterRule(*parse_ip('45.70.236.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('5.107.0.0'), 16), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('5.144.72.0'), 11), # Russia - MTS PJSC
    IPFilterRule(*parse_ip('5.62.138.0'), 9), # Iraq - Al-Jazeera Al-Arabiya Company for Communication and Internet LTD
    IPFilterRule(*parse_ip('5.62.144.0'), 11), # Iraq - Al-Jazeera Al-Arabiya Company for Communication and Internet LTD
    IPFilterRule(*parse_ip('58.145.184.0'), 11), # Bangladesh - TM International Bangladesh Ltd.Internet service Provider,Gulshan-1,Dhaka-1212
    IPFilterRule(*parse_ip('59.103.216.0'), 11), # Pakistan - Connect Communication
    IPFilterRule(*parse_ip('59.152.96.0'), 10), # Bangladesh - EARTH TELECOMMUNICATION (Pvt) LTD.
    IPFilterRule(*parse_ip('72.255.0.0'), 13), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('72.27.144.0'), 12), # Jamaica - FLOW
    IPFilterRule(*parse_ip('77.137.0.0'), 15), # Israel - Hot-Net internet services Ltd.
    IPFilterRule(*parse_ip('8.243.15.0'), 8), # Argentina - Level 3 Parent, LLC
    IPFilterRule(*parse_ip('86.96.0.0'), 18), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('87.197.0.0'), 16), # Slovakia - Slovak Telekom, a.s.
    IPFilterRule(*parse_ip('91.90.8.0'), 11), # Ukraine - Comfo LTD
    IPFilterRule(*parse_ip('95.59.192.0'), 14), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('102.132.192.0'), 14), # South Africa - Cool Ideas Service Provider (Pty) Ltd
    IPFilterRule(*parse_ip('102.210.16.0'), 10), # Ivory Coast - Orange Côte d'Ivoire
    IPFilterRule(*parse_ip('102.212.236.0'), 10), # Kenya - Novia East Africa Ltd
    IPFilterRule(*parse_ip('102.213.92.0'), 10), # Kenya - FLINK TECHNOLOGIES LTD
    IPFilterRule(*parse_ip('102.40.0.0'), 19), # Egypt - TE-AS
    IPFilterRule(*parse_ip('103.109.95.0'), 8), # Bangladesh - Orange Communication
    IPFilterRule(*parse_ip('103.115.72.0'), 10), # Bangladesh - Net Matrix
    IPFilterRule(*parse_ip('103.121.178.0'), 9), # Pakistan - Dream Internet Services Pvt Ltd
    IPFilterRule(*parse_ip('103.121.60.0'), 10), # Bangladesh - Mohammad SAHIDUL ISLAM
    IPFilterRule(*parse_ip('103.123.85.0'), 8), # Indonesia - PT Desane Sinar Media
    IPFilterRule(*parse_ip('103.143.254.0'), 8), # Bangladesh - B.M IT and Cyber Place
    IPFilterRule(*parse_ip('103.152.104.0'), 9), # Bangladesh - Pan M Tech Limited
    IPFilterRule(*parse_ip('103.162.50.0'), 9), # Bangladesh - EXABYTE LTD
    IPFilterRule(*parse_ip('103.169.130.0'), 9), # Indonesia - PT Lancar Artha Media Data
    IPFilterRule(*parse_ip('103.176.96.0'), 9), # Indonesia - PT Global Sarana Elektronika
    IPFilterRule(*parse_ip('103.177.168.0'), 8), # Bangladesh - First n Fast IT Ltd
    IPFilterRule(*parse_ip('103.189.200.0'), 9), # Indonesia - PT INDONESIA COMNETS PLUS
    IPFilterRule(*parse_ip('103.19.108.0'), 10), # Indonesia - PT Netciti Persada
    IPFilterRule(*parse_ip('103.191.165.0'), 8), # Indonesia - PT Sakti Wijaya Network
    IPFilterRule(*parse_ip('103.196.4.0'), 10), # India - VAINAVI INDUSTIES LTD, INTERNET SERVICE PROVIDER, INDIA
    IPFilterRule(*parse_ip('103.199.108.0'), 10), # Bangladesh - Bijoy Online Ltd. Multihome Internet Service Provider
    IPFilterRule(*parse_ip('103.206.36.0'), 10), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('103.231.228.0'), 10), # Bangladesh - BD Networks
    IPFilterRule(*parse_ip('103.251.254.0'), 9), # Pakistan - New Pakistan Cable Network (Firm)
    IPFilterRule(*parse_ip('103.31.178.0'), 9), # Bangladesh - Vision Technologies Ltd.
    IPFilterRule(*parse_ip('103.35.212.0'), 9), # Pakistan - Riderz Network Broadband (Private) Limited
    IPFilterRule(*parse_ip('103.36.8.0'), 10), # Indonesia - PT Awinet Global Mandiri
    IPFilterRule(*parse_ip('103.70.171.0'), 8), # Bangladesh - First n Fast IT Ltd
    IPFilterRule(*parse_ip('104.28.243.218'), 1), # Brazil - Cloudflare, Inc.
    IPFilterRule(*parse_ip('105.212.0.0'), 18), # South Africa - MTN SA
    IPFilterRule(*parse_ip('105.216.0.0'), 19), # South Africa - MTN SA
    IPFilterRule(*parse_ip('105.224.0.0'), 18), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('106.210.224.0'), 13), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('109.252.0.0'), 16), # Russia - PJSC Moscow city telephone network
    IPFilterRule(*parse_ip('109.76.0.0'), 18), # Ireland - Vodafone Ireland Limited
    IPFilterRule(*parse_ip('111.119.32.0'), 11), # Nepal - Websurfer Nepal Internet Service Provider
    IPFilterRule(*parse_ip('119.156.0.0'), 15), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('129.122.128.0'), 15), # Angola - Finstar - Sociedade de Investimento e Participacoes S.A
    IPFilterRule(*parse_ip('131.108.150.0'), 9), # Brazil - Itop Internet e Servicos LTDA
    IPFilterRule(*parse_ip('131.108.188.0'), 10), # Brazil - totalweb - Provedor de Internet
    IPFilterRule(*parse_ip('131.196.40.0'), 10), # Brazil - Voafibra Comunicacao
    IPFilterRule(*parse_ip('131.221.252.0'), 10), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('131.255.44.0'), 10), # Brazil - RM dos Santos Informatica
    IPFilterRule(*parse_ip('132.255.36.0'), 10), # Brazil - STAR MAN NET PROVEDORA DE INTERNET LTDA - EPP
    IPFilterRule(*parse_ip('137.59.144.0'), 10), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('138.0.248.0'), 10), # Brazil - MASTER TECNOLOGIA
    IPFilterRule(*parse_ip('138.122.164.0'), 10), # Brazil - OS CONNECT INFORMATICA EIRELI - EPP
    IPFilterRule(*parse_ip('138.219.28.0'), 10), # Brazil - Vc de carvalho telecomunicações
    IPFilterRule(*parse_ip('138.255.84.0'), 10), # Brazil - speed telecom
    IPFilterRule(*parse_ip('138.94.84.0'), 10), # Brazil - ETECC FIBRA OPTICA TELECOM LTDA
    IPFilterRule(*parse_ip('138.97.24.0'), 10), # Brazil - SMA NETCOM LTDA ME
    IPFilterRule(*parse_ip('138.99.196.0'), 10), # Brazil - Fenix Wireless Internet Ltda
    IPFilterRule(*parse_ip('140.213.10.0'), 8), # Indonesia - PT XL Axiata Tbk
    IPFilterRule(*parse_ip('140.213.118.0'), 8), # Indonesia - PT XL Axiata Tbk
    IPFilterRule(*parse_ip('141.98.140.0'), 10), # Albania - Vodafone Albania Sh.A.
    IPFilterRule(*parse_ip('143.202.40.0'), 10), # Brazil - ContilNet Telecom - Staff Computer EIRELI
    IPFilterRule(*parse_ip('144.48.108.0'), 10), # Bangladesh - ICC Communication
    IPFilterRule(*parse_ip('152.231.128.0'), 15), # Costa Rica - Cable Tica
    IPFilterRule(*parse_ip('154.120.64.0'), 14), # Nigeria - SPECTRANET LIMITED
    IPFilterRule(*parse_ip('156.160.0.0'), 21), # Egypt - ETISALAT MISR
    IPFilterRule(*parse_ip('156.252.12.0'), 10), # Mexico - IENTC S DE RL DE CV
    IPFilterRule(*parse_ip('164.163.220.0'), 10), # Brazil - FIBRACOM TELECOMUNICACOES E SERVICOS EIRELI - ME
    IPFilterRule(*parse_ip('167.249.68.0'), 10), # Brazil - ULTRALINK TELECOM LTDA - ME
    IPFilterRule(*parse_ip('167.249.88.0'), 10), # Brazil - R&R TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('168.110.192.0'), 13), # Indonesia - Oracle Corporation
    IPFilterRule(*parse_ip('168.121.192.0'), 10), # Brazil - DTEL TELECOM
    IPFilterRule(*parse_ip('168.195.164.0'), 10), # Brazil - SS TELECOM LTDA
    IPFilterRule(*parse_ip('168.205.100.0'), 10), # Brazil - C-ComTelecom Servios Ltda-ME
    IPFilterRule(*parse_ip('168.205.136.0'), 10), # Brazil - GRUPO MEGA FLASH SERVICOS E COM LTDA - EPP
    IPFilterRule(*parse_ip('168.227.220.0'), 10), # Brazil - OPYT TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('168.227.224.0'), 10), # Brazil - SKYMAX TELECOMUNICAÇÕES LTDA ME
    IPFilterRule(*parse_ip('170.244.164.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('170.245.232.0'), 10), # Argentina - JR INTERCOM S.R.L
    IPFilterRule(*parse_ip('170.246.80.0'), 10), # Brazil - F.J.FANTINI AMPARO ME
    IPFilterRule(*parse_ip('170.82.180.0'), 10), # Brazil - SEA TELECOM LTDA
    IPFilterRule(*parse_ip('170.84.172.0'), 10), # Paraguay - SOL TELECOMUNICACIONES S.A.
    IPFilterRule(*parse_ip('176.65.96.0'), 13), # Russia - MTS PJSC
    IPFilterRule(*parse_ip('177.11.40.0'), 11), # Brazil - CROSS CONECTION PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.125.40.0'), 10), # Brazil - BRASILNETS COM. ATAC. DE EQ. INFORMATICA LTDA ME
    IPFilterRule(*parse_ip('177.126.216.0'), 11), # Brazil - LGNET SERVICOS DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.128.24.0'), 11), # Brazil - ISP PROVERNET INFORMATICA LTDA - ME
    IPFilterRule(*parse_ip('177.136.14.0'), 9), # Brazil - TASCOM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('177.196.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.201.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('177.212.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.223.240.0'), 12), # Brazil - THS Provider Serviços de Comunicação Multimídia LT
    IPFilterRule(*parse_ip('177.23.152.0'), 11), # Brazil - netstore tecnologia ltda
    IPFilterRule(*parse_ip('177.234.224.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('177.234.244.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('177.240.96.0'), 13), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('177.54.160.0'), 13), # Brazil - Tres Pontas Internet Ltda
    IPFilterRule(*parse_ip('177.67.136.0'), 11), # Brazil - Turbo BSB Tecnologias em Rede Ltda.
    IPFilterRule(*parse_ip('177.72.232.0'), 10), # Brazil - COPREL TELECOM LTDA
    IPFilterRule(*parse_ip('177.72.24.0'), 10), # Brazil - DUNET LTDA
    IPFilterRule(*parse_ip('177.73.8.0'), 11), # Brazil - HiperNET Servico de Comunicacao LTDA ME
    IPFilterRule(*parse_ip('177.85.136.0'), 11), # Brazil - tc conecta serviços de telecomunicações e provedor
    IPFilterRule(*parse_ip('177.86.0.0'), 11), # Brazil - MHNET TELECOM
    IPFilterRule(*parse_ip('177.87.12.0'), 10), # Brazil - L GONZAGA JUNIOR SERVICOS DE INTERNET - ME
    IPFilterRule(*parse_ip('178.176.136.0'), 10), # Russia - PJSC MegaFon
    IPFilterRule(*parse_ip('179.0.180.0'), 10), # Argentina - CORRIENTES TELECOMUNICACIONES S.A.P.E.M.
    IPFilterRule(*parse_ip('179.101.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.106.96.0'), 12), # Brazil - Speednet Telecomunicações Ltda ME
    IPFilterRule(*parse_ip('179.109.88.0'), 11), # Brazil - I4 Telecom LTDA -ME
    IPFilterRule(*parse_ip('179.125.28.0'), 10), # Brazil - G-LAB Telecom Informatica LTDA - ME
    IPFilterRule(*parse_ip('179.144.128.0'), 14), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.168.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.48.100.0'), 10), # Brazil - ULTRAFIBRA NET REPRESENTACOES TELECOM EIRELI
    IPFilterRule(*parse_ip('179.48.176.0'), 10), # Brazil - F.N DE JESUS SILVA
    IPFilterRule(*parse_ip('179.49.222.0'), 9), # Brazil - G4 Internet
    IPFilterRule(*parse_ip('179.51.156.0'), 10), # Brazil - SEGNET TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('180.242.0.0'), 17), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('180.248.0.0'), 18), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('181.117.160.0'), 12), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.177.0.0'), 14), # Argentina - TELESISTEMA S.R.L.
    IPFilterRule(*parse_ip('181.191.60.0'), 10), # Brazil - LEX TELECOM LTDA ME
    IPFilterRule(*parse_ip('181.232.180.0'), 10), # Venezuela - CONEXT VENEZUELA, C.A.
    IPFilterRule(*parse_ip('181.233.28.0'), 10), # Brazil - BIT CENTER INFORMATICA EIRELI
    IPFilterRule(*parse_ip('185.187.76.0'), 10), # Iraq - Kurdistan Net Company for Computer and Internet Ltd.
    IPFilterRule(*parse_ip('185.187.92.0'), 10), # Lebanon - C BEYOND s.a.l
    IPFilterRule(*parse_ip('185.229.84.0'), 10), # Kazakhstan - Tele2 Kazakhstan
    IPFilterRule(*parse_ip('185.24.60.0'), 10), # Iraq - Kurdistan Net Company for Computer and Internet Ltd.
    IPFilterRule(*parse_ip('185.50.56.0'), 10), # Bosnia and Herzegovina - NEON Solucije d.o.o. Kalesija
    IPFilterRule(*parse_ip('185.87.171.0'), 8), # Lebanon - Masco Group LLC
    IPFilterRule(*parse_ip('186.128.0.0'), 19), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('186.193.16.0'), 12), # Brazil - Acesse Comunicação Ltda
    IPFilterRule(*parse_ip('186.209.16.0'), 12), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('186.219.170.0'), 9), # Brazil - FLIX TELECOM
    IPFilterRule(*parse_ip('186.219.48.0'), 9), # Ecuador - SIGNAL-TELECOM TELECOMUNICACIONES & T.I CIA.LTDA.
    IPFilterRule(*parse_ip('186.225.128.0'), 13), # Brazil - Sinal Br Telecom Ltda
    IPFilterRule(*parse_ip('186.235.224.0'), 12), # Brazil - IBSOL TELECOM LTDA
    IPFilterRule(*parse_ip('186.237.224.0'), 12), # Brazil - INFRANET INTERNET LTDA.
    IPFilterRule(*parse_ip('186.251.12.0'), 10), # Brazil - RODRIGO BORGHI DA SILVA & CIA LTDA
    IPFilterRule(*parse_ip('186.5.0.0'), 15), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('186.68.0.0'), 18), # Ecuador - SERVICIOS DE TELECOMUNICACIONES SETEL S.A. (XTRIM EC)
    IPFilterRule(*parse_ip('186.76.0.0'), 17), # Nicaragua - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('186.78.0.0'), 17), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('186.92.0.0'), 16), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('186.93.64.0'), 14), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('187.102.104.0'), 10), # Brazil - Mikrocenter Informática Ltda.
    IPFilterRule(*parse_ip('187.103.224.0'), 13), # Brazil - Adylnet Telecom
    IPFilterRule(*parse_ip('187.110.64.0'), 14), # Brazil - PROVEDORA CMA INTERNET LTDA
    IPFilterRule(*parse_ip('187.17.176.0'), 12), # Brazil - ADLLink Provedor de Internet Via Radio LTDA
    IPFilterRule(*parse_ip('187.184.4.0'), 10), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('187.189.145.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.189.146.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.190.140.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.190.176.0'), 11), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.20.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.220.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.245.194.0'), 8), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('187.254.50.0'), 8), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('187.255.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.45.132.0'), 8), # Brazil - SPACnet - Projetos Avançados em Computação
    IPFilterRule(*parse_ip('187.57.128.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.61.112.0'), 11), # Brazil - Linkfull melhor fornecedor dos provedores
    IPFilterRule(*parse_ip('187.73.0.0'), 12), # Brazil - Companhia Itabirana Telecomunicações Ltda
    IPFilterRule(*parse_ip('187.84.144.0'), 10), # Brazil - HS TELECOMUNICACAO E TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('187.84.176.0'), 12), # Brazil - ALLREDE TELECOM LTDA
    IPFilterRule(*parse_ip('187.95.16.0'), 12), # Brazil - Netjacarei Telecon Ltda
    IPFilterRule(*parse_ip('188.113.192.0'), 12), # Uzbekistan - COSCOM Liability Limited Company
    IPFilterRule(*parse_ip('188.129.80.0'), 10), # Croatia - A1 Hrvatska d.o.o.
    IPFilterRule(*parse_ip('188.132.221.160'), 5), # Turkey - High Speed Telekomunikasyon ve Hab. Hiz. Ltd. Sti.
    IPFilterRule(*parse_ip('189.100.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.127.160.0'), 10), # Brazil - WEBNET GLOBAL TELEFONIA E COMUNICACAO EIRELI
    IPFilterRule(*parse_ip('189.127.48.0'), 12), # Brazil - I-CONECTA REDES DE TELECOMUNICACAO EIRELI EPP
    IPFilterRule(*parse_ip('189.12.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('189.151.192.0'), 14), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.167.192.0'), 14), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.188.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.194.160.0'), 13), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('189.21.0.0'), 16), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('189.217.64.0'), 13), # Mexico - Cablevisión, S.A. de C.V.
    IPFilterRule(*parse_ip('189.223.0.0'), 14), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.233.128.0'), 14), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.248.0.0'), 15), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.253.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.60.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.78.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.85.116.0'), 10), # Brazil - Via Fios - Via Fibra Ótica Service
    IPFilterRule(*parse_ip('190.110.104.0'), 11), # Chile - Silica Networks Argentina S.A.
    IPFilterRule(*parse_ip('190.112.136.0'), 10), # Argentina - C Y M INTERNET S.R.L.
    IPFilterRule(*parse_ip('190.115.0.0'), 12), # Guatemala - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('190.138.0.0'), 17), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.188.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.192.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.218.0.0'), 17), # Panama - Cable Onda
    IPFilterRule(*parse_ip('190.225.192.0'), 14), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.230.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.60.48.0'), 11), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('190.83.40.0'), 9), # Brazil - JOSE DAS GRACAS SOARES DE LIMA EIRELI
    IPFilterRule(*parse_ip('190.83.42.0'), 8), # Brazil - JOSE DAS GRACAS SOARES DE LIMA EIRELI
    IPFilterRule(*parse_ip('190.90.248.0'), 11), # Colombia - INTERNEXA S.A. E.S.P
    IPFilterRule(*parse_ip('190.93.120.0'), 10), # Dominican Republic - LAUAM MEGARED TELECOM, S.R.L.
    IPFilterRule(*parse_ip('190.96.96.0'), 11), # Ecuador - NECUSOFT CIA. LTDA. (NETTPLUS)
    IPFilterRule(*parse_ip('191.242.176.0'), 12), # Brazil - CONECT TELECOM
    IPFilterRule(*parse_ip('191.248.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.37.144.0'), 11), # Brazil - AZZA TELECOM SERVIÇOS EM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('191.5.0.0'), 13), # Brazil - RazaoInfo Internet Ltda
    IPFilterRule(*parse_ip('191.6.16.0'), 12), # Brazil - TURBONETT TELECOMUNICACOES LTDA. - ME
    IPFilterRule(*parse_ip('191.97.96.0'), 8), # Argentina - VISION NET
    IPFilterRule(*parse_ip('193.106.151.0'), 8), # Russia - UGTELECOM LLC
    IPFilterRule(*parse_ip('194.39.224.0'), 10), # Ukraine - New Information Systems PP
    IPFilterRule(*parse_ip('195.66.156.0'), 9), # Ukraine - PP Info-Center
    IPFilterRule(*parse_ip('196.189.128.0'), 15), # Ethiopia - Ethio Telecom
    IPFilterRule(*parse_ip('196.32.248.0'), 11), # South Africa - South African Digital Villages (Pty) Ltd
    IPFilterRule(*parse_ip('196.64.0.0'), 17), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('197.14.64.0'), 14), # Tunisia - Tunisia BackBone AS
    IPFilterRule(*parse_ip('197.248.0.0'), 16), # Kenya - Safaricom Limited
    IPFilterRule(*parse_ip('200.196.36.0'), 10), # Brazil - MZ NET FIBRA
    IPFilterRule(*parse_ip('200.8.0.0'), 16), # Venezuela - Corporación Telemic C.A.
    IPFilterRule(*parse_ip('201.13.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('201.139.184.0'), 11), # Brazil - DB3 SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('201.139.216.0'), 11), # Brazil - Enove Soluções em Comunicação Ltda
    IPFilterRule(*parse_ip('201.158.8.0'), 11), # Brazil - VIATEC TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('201.170.128.0'), 15), # Mexico - UNINET
    IPFilterRule(*parse_ip('201.190.248.0'), 11), # Argentina - ARLINK S.A.
    IPFilterRule(*parse_ip('201.58.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('205.169.39.0'), 8), # United States - Level 3 Parent, LLC
    IPFilterRule(*parse_ip('212.175.114.36'), 2), # Cyprus - Turk Telekomunikasyon Anonim Sirketi
    IPFilterRule(*parse_ip('212.34.0.0'), 13), # Jordan - Jordan Telecommunications PSC
    IPFilterRule(*parse_ip('213.139.32.0'), 13), # Jordan - Jordan Telecommunications PSC
    IPFilterRule(*parse_ip('213.24.96.0'), 13), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('216.98.212.0'), 10), # Brazil - LP PROVEDORA DE INTERNET E INSTALAÇÕES DE REDES TE
    IPFilterRule(*parse_ip('220.152.112.0'), 8), # Bangladesh - SkyTel Communications Limited
    IPFilterRule(*parse_ip('222.255.124.0'), 10), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('24.232.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('31.171.48.0'), 12), # Azerbaijan - SELNET LLC
    IPFilterRule(*parse_ip('36.68.0.0'), 18), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('37.150.0.0'), 17), # Kazakhstan - JSC Kazakhtelecom
    IPFilterRule(*parse_ip('37.186.40.0'), 11), # Qatar - Vodafone Qatar P.Q.S.C
    IPFilterRule(*parse_ip('37.236.224.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.237.128.0'), 13), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.237.176.0'), 11), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.238.96.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.238.0.0'), 13), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.34.128.0'), 15), # Kuwait - Mobile Telecommunications Company K.S.C.P.
    IPFilterRule(*parse_ip('37.40.128.0'), 15), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('37.61.0.0'), 15), # Azerbaijan - Baku Telephone Communication LLC
    IPFilterRule(*parse_ip('37.77.48.0'), 11), # Iraq - Al-Jazeera Al-Arabiya Company for Communication and Internet LTD
    IPFilterRule(*parse_ip('38.10.224.0'), 12), # Oman - Awaser Oman LLC
    IPFilterRule(*parse_ip('38.52.220.0'), 10), # Dominican Republic - TELECABLE DOMINICANO, S.A.
    IPFilterRule(*parse_ip('38.7.0.0'), 11), # Venezuela - GIGAPOP, C.A.
    IPFilterRule(*parse_ip('38.74.224.0'), 13), # Venezuela - GALAXY ENTERTAINMENT DE VENEZUELA, S.C.A.
    IPFilterRule(*parse_ip('39.34.144.0'), 12), # Pakistan - Wancom (Pvt) Ltd.
    IPFilterRule(*parse_ip('39.34.192.0'), 14), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('41.114.0.0'), 16), # South Africa - MTN SA
    IPFilterRule(*parse_ip('41.12.0.0'), 17), # South Africa - Vodacom
    IPFilterRule(*parse_ip('41.223.72.0'), 10), # Botswana - Mascom Wireless Ltd
    IPFilterRule(*parse_ip('41.36.0.0'), 18), # Egypt - TE-AS
    IPFilterRule(*parse_ip('45.160.236.0'), 10), # Brazil - QUADRI TELECOM LTDA - ME
    IPFilterRule(*parse_ip('45.161.56.0'), 10), # Brazil - Adalberto Gonçalves Nogueira Me
    IPFilterRule(*parse_ip('45.164.120.0'), 10), # Brazil - VTEK TELECOM LTDA - ME
    IPFilterRule(*parse_ip('45.164.180.0'), 10), # Brazil - Netway soluções em redes de acesso e comunicação l
    IPFilterRule(*parse_ip('45.164.41.0'), 8), # Brazil - ITANETBAHIA COMUNICAÇÃO MULTIMIDIA EIRELE
    IPFilterRule(*parse_ip('45.166.92.0'), 9), # Honduras - MULTICABLE DE HONDURAS
    IPFilterRule(*parse_ip('45.167.44.0'), 10), # Brazil - SUPRINET SOLUCOES EM INTERNET LTDA
    IPFilterRule(*parse_ip('45.167.48.0'), 10), # Brazil - Digitus Net Internet Ltda ME
    IPFilterRule(*parse_ip('45.168.140.0'), 10), # Brazil - REDE SMART SOLUCAO EM INTERNET EIRELI
    IPFilterRule(*parse_ip('45.173.88.0'), 10), # Brazil - Mimo Net Ltda
    IPFilterRule(*parse_ip('45.176.16.0'), 10), # Brazil - JACTOS INTERNET
    IPFilterRule(*parse_ip('45.181.168.0'), 10), # Brazil - P B Net Cursos Idiomas e Internet Ltda
    IPFilterRule(*parse_ip('45.181.252.0'), 10), # Brazil - RJ INTERNET
    IPFilterRule(*parse_ip('45.183.96.0'), 10), # Brazil - ARENA TELECOM COMERCIO DE EQUIPAMENTOS DE INFORMA
    IPFilterRule(*parse_ip('45.184.40.0'), 10), # Brazil - Novum Tecnologia Ltda
    IPFilterRule(*parse_ip('45.184.72.0'), 10), # Brazil - A2 TELECOM PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.185.84.0'), 10), # Brazil - Edmilson de Lima Araújo - me
    IPFilterRule(*parse_ip('45.187.32.0'), 10), # Brazil - Suprema Network Telecom LTDA
    IPFilterRule(*parse_ip('45.191.116.0'), 10), # Brazil - TCL Cortez Servicoes en telecominicacoes
    IPFilterRule(*parse_ip('45.224.0.0'), 9), # Brazil - MAIS IP LTDA
    IPFilterRule(*parse_ip('45.226.40.0'), 10), # Brazil - OLV BRASIL COMERCIO E SERVIÇOS LTDA
    IPFilterRule(*parse_ip('45.227.72.0'), 10), # Brazil - DUNAS TELECOM
    IPFilterRule(*parse_ip('45.228.240.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('45.236.200.0'), 10), # Brazil - LUXFIBRA TELECOM
    IPFilterRule(*parse_ip('45.71.200.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('46.11.0.0'), 16), # Malta - GO p.l.c.
    IPFilterRule(*parse_ip('46.138.0.0'), 16), # Russia - PJSC Moscow city telephone network
    IPFilterRule(*parse_ip('46.152.0.0'), 17), # Saudi Arabia - Etihad Etisalat, a joint stock company
    IPFilterRule(*parse_ip('46.161.193.72'), 2), # Syria - Valeen for General trading, Internet Services and Information Technology / Ltd
    IPFilterRule(*parse_ip('46.183.124.0'), 9), # Albania - MC NETWORKING Sh.p.k.
    IPFilterRule(*parse_ip('46.210.0.0'), 16), # Israel - Cellcom Fixed Line Communication L.P
    IPFilterRule(*parse_ip('46.32.174.0'), 8), # Azerbaijan - Flexnet LLC
    IPFilterRule(*parse_ip('5.165.240.0'), 12), # Russia - JSC "ER-Telecom Holding"
    IPFilterRule(*parse_ip('51.252.0.0'), 17), # Saudi Arabia - Saudi Telecom Company JSC
    IPFilterRule(*parse_ip('51.39.0.0'), 16), # Saudi Arabia - Mobile Telecommunication Company Saudi Arabia Joint-Stock company
    IPFilterRule(*parse_ip('62.201.239.0'), 8), # Iraq - I.Q Online for Internet Services and Communications LLC
    IPFilterRule(*parse_ip('66.167.147.0'), 8), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('77.239.160.0'), 11), # Ukraine - PrJSC VF UKRAINE
    IPFilterRule(*parse_ip('79.137.170.0'), 9), # Kazakhstan - Tele2 Kazakhstan
    IPFilterRule(*parse_ip('82.112.166.0'), 9), # Lebanon - IncoNet Data Management sal
    IPFilterRule(*parse_ip('82.205.0.0'), 15), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('82.86.160.0'), 11), # Venezuela - THUNDERNET, C.A.
    IPFilterRule(*parse_ip('83.171.206.0'), 9), # Iraq - SUPER CELL NETWORK FOR INTERNET SERVICES LTD
    IPFilterRule(*parse_ip('84.54.64.0'), 13), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('85.173.126.0'), 9), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('85.198.104.0'), 9), # Russia - Lovitel LLC
    IPFilterRule(*parse_ip('86.108.0.0'), 15), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('87.76.0.0'), 12), # Russia - Telecom.ru Ltd
    IPFilterRule(*parse_ip('89.23.128.0'), 14), # Russia - LLC POWERNET
    IPFilterRule(*parse_ip('90.156.160.0'), 11), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('91.207.114.128'), 7), # Ukraine - NOVOROS-TELECOM LLC
    IPFilterRule(*parse_ip('91.207.244.0'), 9), # Ukraine - FOP Samoylenko Oleksandr Volodymirovich
    IPFilterRule(*parse_ip('92.40.0.0'), 16), # United Kingdom - Hutchison 3G UK Limited
    IPFilterRule(*parse_ip('93.136.0.0'), 19), # Croatia - Hrvatski Telekom d.d.
    IPFilterRule(*parse_ip('94.236.192.0'), 10), # Bulgaria - OPTICCOM- BULGARIA Ltd.
    IPFilterRule(*parse_ip('94.56.0.0'), 18), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('95.24.0.0'), 16), # Russia - PJSC "Vimpelcom"
    IPFilterRule(*parse_ip('95.25.72.0'), 11), # Russia - PJSC "Vimpelcom"
    IPFilterRule(*parse_ip('103.12.172.0'), 10), # Bangladesh - SkyTel Communications Limited
    IPFilterRule(*parse_ip('103.178.72.0'), 9), # Bangladesh - E-JOGAJOG
    IPFilterRule(*parse_ip('170.82.60.0'), 10), # Brazil - Ired Internet Ltda
    IPFilterRule(*parse_ip('179.42.40.0'), 10), # Brazil - Ademir Ferreira
    IPFilterRule(*parse_ip('180.254.0.0'), 16), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('181.92.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('186.136.0.0'), 18), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('189.142.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('2.144.0.0'), 18), # Iran - Iran Cell Service and Communication Company
    IPFilterRule(*parse_ip('38.7.16.0'), 11), # Mexico - INTERNET TELEFONIA Y TV DE MICHOACAN SA DE CV
    IPFilterRule(*parse_ip('45.175.139.0'), 8), # Colombia - SERVYCOM COLOMBIA S.A.S
    IPFilterRule(*parse_ip('46.185.128.0'), 15), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('89.211.128.0'), 15), # Qatar - Ooredoo Q.S.C.
    IPFilterRule(*parse_ip('91.106.40.0'), 10), # Iraq - Hala Al Rafidain Company for Communications and Internet LTD.    IPFilterRule(*parse_ip('1.38.0.0'), 15), # India - Vodafone Idea Ltd
    IPFilterRule(*parse_ip('102.129.82.0'), 8), # Republic of the Congo - CONGO TELECOM
    IPFilterRule(*parse_ip('102.220.20.0'), 8), # Kenya - First Basics Technologies Limited
    IPFilterRule(*parse_ip('102.248.0.0'), 18), # South Africa - Telkom SA Ltd.
    IPFilterRule(*parse_ip('103.118.84.0'), 9), # Bangladesh - MD. Mokhlesur Rahman
    IPFilterRule(*parse_ip('103.123.60.0'), 9), # Nepal - DISH MEDIA NETWORK PUBLIC LIMITED
    IPFilterRule(*parse_ip('103.124.136.0'), 10), # Indonesia - PT.Global Media Data Prima
    IPFilterRule(*parse_ip('103.138.222.0'), 9), # Pakistan - WellNetworks (Private) Limited
    IPFilterRule(*parse_ip('103.146.16.0'), 9), # Bangladesh - STAR COMMUNICATION
    IPFilterRule(*parse_ip('103.148.154.0'), 9), # Pakistan - ConnectX
    IPFilterRule(*parse_ip('103.151.46.0'), 9), # Pakistan - Z COM NETWORKS
    IPFilterRule(*parse_ip('103.158.118.0'), 9), # Bangladesh - DELTA SOFTWARE AND COMMUNICATION LIMITED
    IPFilterRule(*parse_ip('103.161.152.0'), 9), # Bangladesh - Click Earth Online
    IPFilterRule(*parse_ip('103.198.132.0'), 8), # Bangladesh - Velocity Networks Limited
    IPFilterRule(*parse_ip('103.198.154.0'), 9), # Pakistan - PLAY BROADBAND (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('103.20.243.0'), 8), # Bangladesh - Plusnet Inc
    IPFilterRule(*parse_ip('103.245.96.0'), 9), # Bangladesh - Max Hub Limited
    IPFilterRule(*parse_ip('103.41.24.0'), 10), # India - Netplus Broadband Services Private Limited
    IPFilterRule(*parse_ip('103.51.53.0'), 8), # Bangladesh - X-LINK LIMITED
    IPFilterRule(*parse_ip('103.70.86.0'), 9), # Pakistan - Pace Telecom and Brodcasting Private Limited
    IPFilterRule(*parse_ip('103.73.100.0'), 10), # Pakistan - KK Networks (Pvt) Ltd.
    IPFilterRule(*parse_ip('104.28.237.72'), 2), # Vietnam - Cloudflare, Inc.
    IPFilterRule(*parse_ip('105.156.0.0'), 17), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('105.235.128.0'), 12), # Algeria - Wataniya Telecom Algerie
    IPFilterRule(*parse_ip('109.177.0.0'), 16), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('110.224.64.0'), 14), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('110.38.192.0'), 13), # Pakistan - National WiMAX/IMS environment
    IPFilterRule(*parse_ip('112.215.160.0'), 12), # Indonesia - PT XL Axiata
    IPFilterRule(*parse_ip('115.132.0.0'), 18), # Malaysia - TM TECHNOLOGY SERVICES SDN. BHD.
    IPFilterRule(*parse_ip('116.107.64.0'), 14), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('119.154.0.0'), 16), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('119.63.138.0'), 8), # Pakistan - Trans World Enterprise Services (Private) Limited
    IPFilterRule(*parse_ip('124.29.208.0'), 12), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('124.29.252.0'), 10), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('124.40.244.0'), 10), # India - Bangalore Broadband Network Pvt Ltd
    IPFilterRule(*parse_ip('128.192.0.0'), 16), # United States - University of Georgia
    IPFilterRule(*parse_ip('128.201.204.0'), 10), # Brazil - Objetivo Informatica Cachoeirinha Ltda-ME
    IPFilterRule(*parse_ip('128.201.80.0'), 10), # Argentina - GPS SANJUAN SRL.
    IPFilterRule(*parse_ip('129.205.96.0'), 13), # Nigeria - Globacom Limited
    IPFilterRule(*parse_ip('138.0.144.0'), 10), # Brazil - INTERNET O SUL COMÉRCIO E SERVIÇOS LTDA
    IPFilterRule(*parse_ip('138.0.244.0'), 10), # Brazil - AGE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('138.117.60.0'), 10), # Brazil - MULTIPLIC COMUNICACAO E TECNOLOGIA LTDA -ME
    IPFilterRule(*parse_ip('138.185.200.0'), 10), # Brazil - STAR NET - PROVEDOR E SERVICOS DE INTERNET LTDA -
    IPFilterRule(*parse_ip('138.255.228.0'), 10), # Brazil - LINK BRASIL LTDA
    IPFilterRule(*parse_ip('138.94.120.0'), 10), # Honduras - CABLECOLOR S.A.
    IPFilterRule(*parse_ip('143.208.108.0'), 10), # Brazil - OK ITAOCARA PROVEDOR INTERNET LTDA
    IPFilterRule(*parse_ip('147.135.220.0'), 10), # France - OVH SAS
    IPFilterRule(*parse_ip('147.235.223.128'), 7), # Israel - "Bezeq"- THE ISRAEL TELECOMMUNICATION CORP. LTD.
    IPFilterRule(*parse_ip('149.200.128.0'), 15), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('154.116.0.0'), 15), # Gabon - Gabon Telecom / Office of Posts and Telecommunications of Gabon
    IPFilterRule(*parse_ip('154.192.0.0'), 16), # Pakistan - Nayatel (Pvt) Ltd
    IPFilterRule(*parse_ip('157.48.0.0'), 18), # India - Reliance Jio Infocomm Limited
    IPFilterRule(*parse_ip('164.163.28.0'), 10), # Brazil - Alianca TecnoinfoLtda
    IPFilterRule(*parse_ip('168.0.16.0'), 10), # Brazil - DeltaAtiva Telecomunicacoes
    IPFilterRule(*parse_ip('168.0.76.0'), 10), # Brazil - Ricardo Adolfo Martins ME
    IPFilterRule(*parse_ip('168.181.120.0'), 10), # Honduras - ENRED S.DE.R.L
    IPFilterRule(*parse_ip('168.181.200.0'), 10), # Brazil - CURIO NET SERVICOS DE TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('168.196.196.0'), 10), # Brazil - Natal Conect Ltda
    IPFilterRule(*parse_ip('168.228.248.0'), 10), # Chile - HomeNet LTDA
    IPFilterRule(*parse_ip('168.232.20.0'), 10), # Brazil - MEGA PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('170.0.56.0'), 10), # Brazil - Panda Network
    IPFilterRule(*parse_ip('170.203.222.0'), 8), # Costa Rica - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('170.239.8.0'), 10), # Brazil - TURBONET TELECOM LTDA
    IPFilterRule(*parse_ip('170.239.68.0'), 10), # Brazil - Tche Turbo Provedor de Internet LTDA
    IPFilterRule(*parse_ip('170.245.64.0'), 10), # Brazil - Naveganet Comercio e Serviços Eirele
    IPFilterRule(*parse_ip('170.78.116.0'), 10), # Brazil - ALCANS TELECOM LTDA
    IPFilterRule(*parse_ip('170.78.56.0'), 10), # Brazil - ESTAR ON INTERNET FIBRA OPTICA LTDA
    IPFilterRule(*parse_ip('170.83.68.0'), 10), # Brazil - I3 Telecomunicacoes - EIRELI
    IPFilterRule(*parse_ip('170.84.216.0'), 10), # Brazil - FLEETNET TELECOMUNICACOES LTDA - ME
    IPFilterRule(*parse_ip('170.84.96.0'), 10), # Brazil - Visionet Fibra Ltda
    IPFilterRule(*parse_ip('175.107.235.0'), 8), # Singapore - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('176.105.236.0'), 10), # Iraq - Noor Al-Bedaya for General Trading, agricultural investments, Technical production and distribution, internet services, general services, Information technology and software Ltd
    IPFilterRule(*parse_ip('177.152.0.0'), 13), # Brazil - GLP Telecomunicações Ltda.
    IPFilterRule(*parse_ip('177.155.172.0'), 9), # Brazil - Vegas Telecom Informática Ltda.
    IPFilterRule(*parse_ip('177.184.212.0'), 10), # Brazil - NETDRP SERVIÇOS DE INTERNET LTDA.
    IPFilterRule(*parse_ip('177.223.64.0'), 12), # Brazil - Paranhananet Ltda.
    IPFilterRule(*parse_ip('177.47.160.0'), 12), # Brazil - WISP ICONECTA SERVICOS DE REDE LTDA
    IPFilterRule(*parse_ip('177.66.144.0'), 10), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('177.71.104.0'), 10), # Brazil - PLAY FIBRA SERVICOS DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.75.0.0'), 12), # Brazil - Networld Provedor e Servicos de Internet Ltda
    IPFilterRule(*parse_ip('177.75.48.0'), 12), # Brazil - EXPLORERNET INFOLINK TECNOLOGIA E TELECOMUNICACOES
    IPFilterRule(*parse_ip('177.84.92.0'), 10), # Brazil - Adriano Telecomunicacoes Ltda Me
    IPFilterRule(*parse_ip('177.91.248.0'), 11), # Peru - EMPRESA DE TELECOMUNICACIONES MULTIMEDIA ALFA
    IPFilterRule(*parse_ip('177.93.152.0'), 11), # Brazil - Work Banda Larga
    IPFilterRule(*parse_ip('178.204.0.0'), 18), # Russia - PJSC "TATTELECOM"
    IPFilterRule(*parse_ip('179.48.240.0'), 10), # Brazil - INOVAIP TELECOM LTDA
    IPFilterRule(*parse_ip('18.188.0.0'), 18), # United States - Amazon.com, Inc.
    IPFilterRule(*parse_ip('181.115.32.0'), 13), # Honduras - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('181.116.192.0'), 12), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.119.104.0'), 11), # Guatemala - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('181.196.12.0'), 9), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('181.224.174.0'), 8), # Ecuador - ALCIVAR ESPIN DANNY ALEXANDER (OptiCom)
    IPFilterRule(*parse_ip('181.40.0.0'), 16), # Paraguay - Telecel S.A.
    IPFilterRule(*parse_ip('181.95.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('182.184.0.0'), 18), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('182.253.112.0'), 12), # Indonesia - BIZNET NETWORKS
    IPFilterRule(*parse_ip('182.42.0.0'), 16), # China - CHINANET-BACKBONE
    IPFilterRule(*parse_ip('185.194.8.0'), 8), # Iraq - Horizon Scope Mobile Telecom WLL
    IPFilterRule(*parse_ip('185.253.162.0'), 8), # Romania - M247 Europe SRL
    IPFilterRule(*parse_ip('185.56.192.0'), 10), # Iraq - I.Q Online for Internet Services and Communications LLC
    IPFilterRule(*parse_ip('186.12.160.0'), 12), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.14.0.0'), 16), # Venezuela - Corporación Telemic C.A.
    IPFilterRule(*parse_ip('186.209.172.0'), 10), # Brazil - Ledyvanha Meneses Alencar
    IPFilterRule(*parse_ip('186.237.48.0'), 11), # Brazil - FORTE TELECOM LTDA.
    IPFilterRule(*parse_ip('186.26.80.0'), 10), # Brazil - Fibramar Telecomunicações Ltda
    IPFilterRule(*parse_ip('186.86.110.0'), 8), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('187.102.80.0'), 12), # Brazil - Bnet Telecomunicações Ltda
    IPFilterRule(*parse_ip('187.103.96.0'), 13), # Brazil - BR.Digital Provider
    IPFilterRule(*parse_ip('187.16.144.0'), 12), # Brazil - Wtl Telecomunicacoes do Brasil Ltda
    IPFilterRule(*parse_ip('187.189.136.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.190.192.0'), 10), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.49.184.0'), 10), # Brazil - Nw3 telecomunicações Ltda
    IPFilterRule(*parse_ip('187.62.96.0'), 10), # Brazil - AMD TELECOM LTDA
    IPFilterRule(*parse_ip('188.18.128.0'), 15), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('188.72.56.0'), 9), # Iraq - Tarik Al-thuraya Company For Communications Service Ltd.
    IPFilterRule(*parse_ip('189.126.168.0'), 11), # Brazil - CABONNET INTERNET LTDA
    IPFilterRule(*parse_ip('189.126.92.0'), 10), # Brazil - ViaNet _Telecom
    IPFilterRule(*parse_ip('189.146.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.152.0.0'), 19), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.18.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.186.0.0'), 17), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.201.248.0'), 10), # Brazil - jms-telecom ltda
    IPFilterRule(*parse_ip('189.217.96.0'), 12), # Mexico - Cablevisión, S.A. de C.V.
    IPFilterRule(*parse_ip('189.218.192.0'), 14), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('189.219.184.0'), 11), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('189.51.40.0'), 10), # Brazil - INOVE TELECOMUNICAÇÕES E SERVIÇOS LTDA
    IPFilterRule(*parse_ip('189.8.120.0'), 10), # Brazil - ALLREDE TELECOM LTDA
    IPFilterRule(*parse_ip('190.108.224.0'), 13), # Argentina - Neunet S.A.
    IPFilterRule(*parse_ip('190.115.64.0'), 10), # Brazil - FIBER WEB SERVICES LTDA
    IPFilterRule(*parse_ip('190.130.128.0'), 15), # Ecuador - Ecuadortelecom S.A.
    IPFilterRule(*parse_ip('190.140.0.0'), 15), # Panama - Cable Onda
    IPFilterRule(*parse_ip('190.22.0.0'), 16), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('190.70.0.0'), 16), # Colombia - UNE EPM TELECOMUNICACIONES S.A.
    IPFilterRule(*parse_ip('190.83.88.0'), 10), # Brazil - TELECOMSHOP COMERCIO E SERVICOS DE TELECOMUNICACOE
    IPFilterRule(*parse_ip('190.89.156.0'), 10), # Brazil - CONNECT TELECOM LTDA
    IPFilterRule(*parse_ip('191.187.224.0'), 12), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('191.19.192.0'), 13), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.243.96.0'), 12), # Brazil - INFORTECLINE TELECOM
    IPFilterRule(*parse_ip('191.24.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.6.80.0'), 10), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('192.140.144.0'), 11), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('192.141.120.0'), 10), # Brazil - MVF NETWORK
    IPFilterRule(*parse_ip('192.141.172.0'), 10), # Brazil - C e B do Amaral Comunicacao - ME
    IPFilterRule(*parse_ip('194.127.137.0'), 8), # Iraq - Dar Al-Salam Co. for Internet Services and Information Technology Ltd
    IPFilterRule(*parse_ip('194.28.16.0'), 10), # Ukraine - PIK Ltd
    IPFilterRule(*parse_ip('194.49.87.0'), 8), # Iraq - SUPER CELL NETWORK FOR INTERNET SERVICES LTD
    IPFilterRule(*parse_ip('196.189.0.0'), 14), # Ethiopia - Ethio Telecom
    IPFilterRule(*parse_ip('197.112.0.0'), 19), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('197.200.0.0'), 19), # Algeria - Telecom Algeria
    IPFilterRule(*parse_ip('197.237.0.0'), 15), # Kenya - Wananchi Group (Kenya) Limited
    IPFilterRule(*parse_ip('200.110.204.0'), 10), # Brazil - SICONECT TELECOMUNICACOES EIRELI
    IPFilterRule(*parse_ip('200.12.36.0'), 10), # Guatemala - Navega.com S.A.
    IPFilterRule(*parse_ip('200.142.176.0'), 11), # Brazil - FACILITI TELECOM
    IPFilterRule(*parse_ip('200.152.16.0'), 9), # Brazil - Directnet Prestacao de Servicos Ltda.
    IPFilterRule(*parse_ip('200.153.128.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('200.163.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('200.225.140.0'), 10), # Brazil - CHECK-UP NET TELECOM
    IPFilterRule(*parse_ip('200.7.112.0'), 12), # Brazil - SUNWAY TELECOM LTDA
    IPFilterRule(*parse_ip('201.14.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.248.0.0'), 14), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('201.76.112.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('202.56.164.0'), 10), # Indonesia - Lintas Data Prima, PT
    IPFilterRule(*parse_ip('202.59.12.0'), 10), # Pakistan - FIBERISH (PVT) LTD
    IPFilterRule(*parse_ip('202.59.208.0'), 10), # Bangladesh - Sustainable Development Networking Program
    IPFilterRule(*parse_ip('202.71.180.0'), 9), # Bangladesh - Spark IT
    IPFilterRule(*parse_ip('203.96.168.0'), 10), # Pakistan - Ebone Network (PVT.) Limited
    IPFilterRule(*parse_ip('213.196.96.0'), 12), # Serbia - TELEKOM SRBIJA a.d.
    IPFilterRule(*parse_ip('213.204.64.0'), 13), # Lebanon - TerraNet sal
    IPFilterRule(*parse_ip('213.80.128.0'), 15), # Russia - Joint Stock Company TransTeleCom
    IPFilterRule(*parse_ip('23.178.112.0'), 8), # United States - Cloudflare London, LLC
    IPFilterRule(*parse_ip('27.60.16.0'), 11), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('31.148.160.0'), 11), # Uzbekistan - Inform-Service TV Ltd.
    IPFilterRule(*parse_ip('31.148.224.0'), 12), # Russia - Intercity Ltd.
    IPFilterRule(*parse_ip('31.215.0.0'), 16), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('35.80.0.0'), 20), # United States - Amazon.com, Inc.
    IPFilterRule(*parse_ip('37.111.144.0'), 12), # Pakistan - Telenor Pakistan
    IPFilterRule(*parse_ip('37.131.0.0'), 15), # Bahrain - STC BAHRAIN B.S.C CLOSED
    IPFilterRule(*parse_ip('37.238.192.0'), 13), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.238.32.0'), 11), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.52.0.0'), 18), # Ukraine - JSC "Ukrtelecom"
    IPFilterRule(*parse_ip('38.3.134.0'), 8), # Brazil - SMARSUL CONECT FREY LTDA
    IPFilterRule(*parse_ip('41.220.144.0'), 12), # Algeria - Optimum Telecom Algeria
    IPFilterRule(*parse_ip('41.73.96.0'), 13), # Mali - Orange Mali SA
    IPFilterRule(*parse_ip('45.161.96.0'), 10), # Brazil - LOG INFORMATICA LTDA
    IPFilterRule(*parse_ip('45.162.52.0'), 10), # Brazil - COMPLETA Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('45.173.116.0'), 10), # Brazil - BAIANA NET TELECOM LTDA
    IPFilterRule(*parse_ip('45.176.4.0'), 10), # Brazil - TELLCORP - TELECOMUNICACOES CORPORATIVAS LTDA
    IPFilterRule(*parse_ip('45.176.76.0'), 10), # Brazil - EXPERT INTERNET LTDA
    IPFilterRule(*parse_ip('45.180.96.0'), 10), # Brazil - Leilane de Vasconcelos Pereira
    IPFilterRule(*parse_ip('45.184.60.0'), 10), # Brazil - MM TELECOM
    IPFilterRule(*parse_ip('45.187.128.0'), 10), # Brazil - DW TELECOM LTDA
    IPFilterRule(*parse_ip('45.187.192.0'), 10), # Brazil - CN-TELECOM LTDA
    IPFilterRule(*parse_ip('45.188.148.0'), 10), # Brazil - PLANETA NET TELECOM
    IPFilterRule(*parse_ip('45.188.156.0'), 10), # Brazil - Marcelo & Renato Digital Net LTDA
    IPFilterRule(*parse_ip('45.188.240.0'), 10), # Brazil - M.M. Brito da Silva - Multimidia
    IPFilterRule(*parse_ip('45.189.248.0'), 10), # Brazil - MM Telecomunicações LTDA.
    IPFilterRule(*parse_ip('45.224.40.0'), 10), # Brazil - DK Telecom
    IPFilterRule(*parse_ip('45.224.72.0'), 10), # Brazil - Gigaweb Tecnologia
    IPFilterRule(*parse_ip('45.226.140.0'), 10), # Brazil - XZoom Telecom
    IPFilterRule(*parse_ip('45.228.20.0'), 10), # Brazil - GEE SOLUÇÕES EM INFORMÁTICA LTDA
    IPFilterRule(*parse_ip('45.233.184.0'), 10), # Brazil - MICROLINK INFORMATICA COMERCIO E SERVICOS LTDA ME
    IPFilterRule(*parse_ip('45.235.152.0'), 10), # Brazil - AZAT INTERNET LTDA
    IPFilterRule(*parse_ip('45.4.108.0'), 10), # Brazil - Chapnet Serviços de Comunicação Ltda
    IPFilterRule(*parse_ip('45.4.136.0'), 10), # Honduras - CABLECOLOR S.A.
    IPFilterRule(*parse_ip('45.4.164.0'), 10), # Argentina - RED WOLF SRL
    IPFilterRule(*parse_ip('45.5.195.0'), 8), # Brazil - RPNET TELECOM
    IPFilterRule(*parse_ip('45.65.212.0'), 10), # Brazil - Eurocorp Vialux Internet Eireli
    IPFilterRule(*parse_ip('45.71.42.0'), 9), # Brazil - E-TECH TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('46.61.0.0'), 15), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('46.72.0.0'), 17), # Russia - PJSC MegaFon
    IPFilterRule(*parse_ip('49.205.32.0'), 11), # India - Atria Convergence Technologies Pvt. Ltd. Broadband Internet Service Provider INDIA
    IPFilterRule(*parse_ip('5.0.0.0'), 16), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('5.192.0.0'), 17), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('5.206.232.0'), 11), # Kosovo - TelKos L.L.C
    IPFilterRule(*parse_ip('51.36.0.0'), 16), # Saudi Arabia - Mobile Telecommunication Company Saudi Arabia Joint-Stock company
    IPFilterRule(*parse_ip('56.228.0.0'), 16), # Sweden - Amazon.com, Inc.
    IPFilterRule(*parse_ip('58.65.212.0'), 10), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('77.91.160.0'), 13), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('79.173.192.0'), 14), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('82.115.44.0'), 10), # Kazakhstan - JSC Transtelecom
    IPFilterRule(*parse_ip('82.180.192.0'), 14), # Iran - Mobile Communication Company of Iran PLC
    IPFilterRule(*parse_ip('85.154.0.0'), 16), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('85.93.32.0'), 13), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('90.188.128.0'), 15), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('91.72.0.0'), 18), # United Arab Emirates - Emirates Integrated Telecommunications Company PJSC
    IPFilterRule(*parse_ip('92.253.0.0'), 15), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('93.170.122.0'), 8), # Ukraine - ITTak LLC
    IPFilterRule(*parse_ip('94.187.0.0'), 14), # Lebanon - OGERO
    IPFilterRule(*parse_ip('94.202.0.0'), 17), # United Arab Emirates - Emirates Integrated Telecommunications Company PJSC
    IPFilterRule(*parse_ip('94.204.0.0'), 17), # United Arab Emirates - Emirates Integrated Telecommunications Company PJSC
    IPFilterRule(*parse_ip('95.170.192.0'), 13), # Iraq - Allay Nawroz Telecom Company for Communication/Ltd.
    IPFilterRule(*parse_ip('95.182.104.0'), 10), # Kazakhstan - TOO Kainar-Media
    IPFilterRule(*parse_ip('95.82.124.0'), 10), # Kazakhstan - Kar-Tel LLC
    IPFilterRule(*parse_ip('95.82.80.0'), 11), # Kazakhstan - Kar-Tel LLC
    IPFilterRule(*parse_ip('1.38.0.0'), 15), # India - Vodafone Idea Ltd
    IPFilterRule(*parse_ip('102.129.72.0'), 11), # Republic of the Congo - CONGO TELECOM
    IPFilterRule(*parse_ip('102.182.0.0'), 16), # South Africa - AFRIHOST SP (PTY) LTD
    IPFilterRule(*parse_ip('102.217.184.0'), 10), # South Africa - MikroTikSA Networks CC
    IPFilterRule(*parse_ip('102.217.240.0'), 10), # South Africa - NET99 (PTY) LTD
    IPFilterRule(*parse_ip('102.219.148.0'), 10), # South Africa - WirelessONE
    IPFilterRule(*parse_ip('102.24.0.0'), 19), # Tunisia - SOCIETE NATIONALE DES TELECOMMUNICATIONS (Tunisie Telecom)
    IPFilterRule(*parse_ip('102.88.0.0'), 17), # Nigeria - MTN NIGERIA Communication limited
    IPFilterRule(*parse_ip('102.90.64.0'), 14), # Nigeria - MTN NIGERIA Communication limited
    IPFilterRule(*parse_ip('102.91.0.0'), 16), # Nigeria - MTN NIGERIA Communication limited
    IPFilterRule(*parse_ip('103.134.43.0'), 8), # Bangladesh - Friends Cable Net
    IPFilterRule(*parse_ip('103.148.22.0'), 9), # Nepal - Fiberworld Communication Pvt.ltd
    IPFilterRule(*parse_ip('103.154.170.0'), 9), # Indonesia - PT Irama Media FlashNet
    IPFilterRule(*parse_ip('103.167.232.0'), 9), # Nepal - TECHMINDS NETWORKS PVT. LTD.
    IPFilterRule(*parse_ip('103.172.17.0'), 8), # Indonesia - PT Media Access Telematika
    IPFilterRule(*parse_ip('103.191.130.0'), 9), # Nepal - DISH MEDIA NETWORK PUBLIC LIMITED
    IPFilterRule(*parse_ip('103.229.84.0'), 10), # Bangladesh - Comilla Online
    IPFilterRule(*parse_ip('103.234.118.0'), 9), # Bangladesh - Dewan Enterprise
    IPFilterRule(*parse_ip('103.240.68.0'), 9), # Indonesia - PT Parsaoran Global Datatrans
    IPFilterRule(*parse_ip('103.68.4.0'), 10), # Bangladesh - Sharmin Akter Shilpi t/a M/S. Saiba International
    IPFilterRule(*parse_ip('103.7.120.0'), 9), # Bangladesh - EXABYTE LTD
    IPFilterRule(*parse_ip('103.89.24.0'), 9), # Bangladesh - Aalok IT Limited
    IPFilterRule(*parse_ip('104.152.236.0'), 10), # Jamaica - FLOW
    IPFilterRule(*parse_ip('106.222.208.0'), 12), # India - Bharti Airtel Ltd., Telemedia Services
    IPFilterRule(*parse_ip('109.201.32.0'), 13), # Kazakhstan - Kar-Tel LLC
    IPFilterRule(*parse_ip('112.196.0.0'), 15), # India - Quadrant Televentures Limited
    IPFilterRule(*parse_ip('114.96.64.0'), 14), # China - China Telecom
    IPFilterRule(*parse_ip('117.96.16.0'), 11), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('119.160.128.0'), 13), # Brunei - Unified National Networks
    IPFilterRule(*parse_ip('122.152.48.0'), 11), # Bangladesh - Innovative Online Limited
    IPFilterRule(*parse_ip('123.136.29.0'), 8), # Bangladesh - Royal Green Communication Limited
    IPFilterRule(*parse_ip('123.200.0.0'), 13), # Bangladesh - Link3 Technologies Ltd.
    IPFilterRule(*parse_ip('128.201.192.0'), 10), # Brazil - Universo Digital Telecomunicações LTDA ME
    IPFilterRule(*parse_ip('128.201.228.0'), 10), # Brazil - NETVIS TELECOM
    IPFilterRule(*parse_ip('131.0.196.0'), 10), # Bolivia - Telefónica Celular de Bolivia S.A.
    IPFilterRule(*parse_ip('138.118.28.0'), 10), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('138.118.60.0'), 10), # Brazil - Bandeiranet Telecomunicações Ltda ME
    IPFilterRule(*parse_ip('138.204.224.0'), 10), # Brazil - Connectronic Servicos Ltda
    IPFilterRule(*parse_ip('138.255.144.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('138.36.48.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('138.84.62.0'), 9), # Argentina - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('138.99.80.0'), 9), # Brazil - MaxNet Telecom
    IPFilterRule(*parse_ip('139.135.32.0'), 12), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('143.137.52.0'), 10), # Brazil - FCPI PROVEDORES DE INTERNET EIRELI
    IPFilterRule(*parse_ip('143.202.10.0'), 9), # Brazil - D.V Comercio em Telecomunicacoes de Rede LTDA-ME
    IPFilterRule(*parse_ip('143.202.108.0'), 10), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('143.202.48.0'), 10), # Brazil - NetCintra Telecomunicações Ltda.
    IPFilterRule(*parse_ip('143.208.228.0'), 10), # Brazil - Cassiano Zanon - CZNET Provedor de Internet
    IPFilterRule(*parse_ip('148.227.72.0'), 10), # Argentina - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('149.107.224.0'), 13), # Argentina - FIBRAZUL INTERNET S.R.L.
    IPFilterRule(*parse_ip('149.19.168.0'), 10), # Mexico - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('152.0.0.0'), 16), # Dominican Republic - Compañía Dominicana de Teléfonos S. A.
    IPFilterRule(*parse_ip('154.128.0.0'), 20), # Egypt - The Egyptian Company for Mobile Services (Mobinil)
    IPFilterRule(*parse_ip('154.152.0.0'), 19), # Kenya - Airtel Networks Kenya Limited
    IPFilterRule(*parse_ip('154.198.60.0'), 9), # Colombia - SERVYCOM COLOMBIA S.A.S
    IPFilterRule(*parse_ip('154.47.29.0'), 8), # Croatia - Datacamp Limited
    IPFilterRule(*parse_ip('157.100.68.0'), 9), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('157.119.200.0'), 10), # India - Fast 4 Technologies
    IPFilterRule(*parse_ip('157.15.58.0'), 9), # Nepal - Global Trading And IT Solution Pvt. Ltd.
    IPFilterRule(*parse_ip('158.140.190.0'), 9), # Indonesia - PT. Eka Mas Republik
    IPFilterRule(*parse_ip('160.30.175.0'), 8), # Pakistan - Wavecomm (Private) Limited
    IPFilterRule(*parse_ip('167.108.0.0'), 16), # Uruguay - Administracion Nacional de Telecomunicaciones
    IPFilterRule(*parse_ip('167.249.144.0'), 10), # Brazil - F. A. ROCHA E COMERCIO
    IPFilterRule(*parse_ip('168.181.124.0'), 10), # Brazil - NET PLANETY INFOTELECOM LTDA ME
    IPFilterRule(*parse_ip('168.197.216.0'), 10), # Argentina - OBERCOM S.R.L.
    IPFilterRule(*parse_ip('168.227.16.0'), 10), # Brazil - G3 Telecom EIRELI
    IPFilterRule(*parse_ip('168.228.200.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('170.150.132.0'), 10), # Brazil - NETWISE INFORMATICA LTDA
    IPFilterRule(*parse_ip('170.231.128.0'), 11), # Brazil - JUPITER PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('170.239.200.0'), 10), # Brazil - NORTE TELECOM PROVEDOR DE INTERNET EIRELI
    IPFilterRule(*parse_ip('170.246.208.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('170.254.152.0'), 10), # Brazil - RazaoInfo Internet Ltda
    IPFilterRule(*parse_ip('170.79.220.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('171.242.16.0'), 12), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('176.222.60.0'), 10), # Iraq - I.Q Online for Internet Services and Communications LLC
    IPFilterRule(*parse_ip('176.74.64.0'), 14), # Georgia - System Net Ltd
    IPFilterRule(*parse_ip('177.105.246.0'), 9), # Brazil - REDE WORKS TELECOM
    IPFilterRule(*parse_ip('177.11.192.0'), 12), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('177.116.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.12.152.0'), 11), # Brazil - Pronto Net Ltda.
    IPFilterRule(*parse_ip('177.124.188.0'), 10), # Brazil - BRNet Telecomunicações LTDA
    IPFilterRule(*parse_ip('177.125.124.0'), 10), # Brazil - TINASNET SERVICOS E ACESSOS A INTERNET LTDA
    IPFilterRule(*parse_ip('177.152.88.0'), 11), # Brazil - Elonet Provedor de Internet Ltda
    IPFilterRule(*parse_ip('177.155.224.0'), 11), # Brazil - INTERMICRO INFORMATICA DE ITAPERUNA LTDA
    IPFilterRule(*parse_ip('177.18.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.185.240.0'), 12), # Brazil - GOX S.A.
    IPFilterRule(*parse_ip('177.195.128.0'), 14), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.23.52.0'), 10), # Brazil - Digi Fibra
    IPFilterRule(*parse_ip('177.27.192.0'), 14), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.28.0.0'), 18), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('177.47.224.0'), 12), # Brazil - TEN INTERNET Ltda
    IPFilterRule(*parse_ip('177.55.176.0'), 12), # Brazil - BTT TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('177.63.0.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.66.248.0'), 11), # Brazil - e.serv informatica e tecnologia ltda.
    IPFilterRule(*parse_ip('177.72.184.0'), 11), # Brazil - NEWLINE TELECOM
    IPFilterRule(*parse_ip('177.84.76.0'), 10), # Brazil - QUATRO IRMAOS COMERCIO E SERVICOS EM INFORMATICA E
    IPFilterRule(*parse_ip('177.93.168.0'), 11), # Brazil - AVANCAR INTERNET
    IPFilterRule(*parse_ip('178.186.0.0'), 17), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('178.222.0.0'), 16), # Serbia - TELEKOM SRBIJA a.d.
    IPFilterRule(*parse_ip('178.223.128.0'), 14), # Serbia - TELEKOM SRBIJA a.d.
    IPFilterRule(*parse_ip('178.223.192.0'), 13), # Serbia - TELEKOM SRBIJA a.d.
    IPFilterRule(*parse_ip('179.100.0.0'), 15), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.106.72.0'), 11), # Brazil - EGR NET TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('179.108.16.0'), 11), # Brazil - G6 Internet
    IPFilterRule(*parse_ip('179.109.128.0'), 13), # Brazil - DIGITAL NET RJ TELECOM EIRELI
    IPFilterRule(*parse_ip('179.12.0.0'), 18), # Colombia - Colombia Móvil
    IPFilterRule(*parse_ip('179.130.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.164.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('179.191.192.0'), 13), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('179.210.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.218.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.42.140.0'), 10), # Brazil - BRUNO SAVI GONCALVES
    IPFilterRule(*parse_ip('179.62.128.0'), 12), # Argentina - Red Intercable Digital S.A.
    IPFilterRule(*parse_ip('179.92.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('180.72.0.0'), 18), # Malaysia - TM TECHNOLOGY SERVICES SDN. BHD.
    IPFilterRule(*parse_ip('181.116.248.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.117.136.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.16.160.0'), 13), # Argentina - Colsecor Cooperativa Limitada
    IPFilterRule(*parse_ip('181.174.104.0'), 10), # Guatemala - Servicios Innovadores de Comunicación y Entretenimiento, S.A.
    IPFilterRule(*parse_ip('181.191.168.0'), 10), # Brazil - GRAFNET TELECOM
    IPFilterRule(*parse_ip('181.192.0.0'), 13), # Argentina - Coop Telefonica Villa Gesell Ltda
    IPFilterRule(*parse_ip('181.209.128.0'), 15), # Guatemala - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('181.37.0.0'), 16), # Dominican Republic - ALTICE DOMINICANA S.A.
    IPFilterRule(*parse_ip('181.53.96.0'), 8), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('181.86.0.0'), 17), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('185.171.144.0'), 10), # Albania - ONE ALBANIA SH.A.
    IPFilterRule(*parse_ip('185.183.183.0'), 8), # Oman - Awaser Oman LLC
    IPFilterRule(*parse_ip('185.221.252.0'), 10), # Albania - FASTNET ALBANIA Sh.p.k
    IPFilterRule(*parse_ip('185.33.32.0'), 10), # Albania - Starnet Sh.p.k.
    IPFilterRule(*parse_ip('186.188.0.0'), 15), # Venezuela - Corporación Telemic C.A.
    IPFilterRule(*parse_ip('186.208.208.0'), 11), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('186.216.240.0'), 12), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('186.224.128.0'), 14), # Brazil - Cilnet Comunicação e Informática S.A.
    IPFilterRule(*parse_ip('186.235.92.0'), 10), # Brazil - ATK Telecomunicações Ltda.
    IPFilterRule(*parse_ip('186.33.64.0'), 14), # Dominican Republic - WIND Telecom S.A.
    IPFilterRule(*parse_ip('187.107.64.0'), 13), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.184.176.0'), 12), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('187.189.40.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.57.96.0'), 13), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.84.0.0'), 12), # Brazil - Cilnet Comunicação e Informática S.A.
    IPFilterRule(*parse_ip('188.190.64.0'), 13), # Ukraine - ISP Shtorm LTD
    IPFilterRule(*parse_ip('188.253.32.0'), 13), # Iran - Pishgaman Toseeh Ertebatat Company (Private Joint Stock)
    IPFilterRule(*parse_ip('188.64.8.0'), 11), # Azerbaijan - "AZERONLINE LTD" JOINT ENTERPRISE
    IPFilterRule(*parse_ip('188.72.46.0'), 8), # Iraq - Steps Telecom For Internet Ltd.
    IPFilterRule(*parse_ip('189.113.48.0'), 11), # Brazil - Opcao Telecom
    IPFilterRule(*parse_ip('189.114.192.0'), 14), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('189.127.132.0'), 10), # Brazil - NEXCESS Soluções de Redes Ltda.
    IPFilterRule(*parse_ip('189.203.46.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('189.28.192.0'), 13), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('189.55.152.0'), 11), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.84.160.0'), 13), # Brazil - S. O. do Brasil Telecomunicações LTDA ME
    IPFilterRule(*parse_ip('189.90.232.0'), 10), # Brazil - NaveNet servicos de internet ltda
    IPFilterRule(*parse_ip('190.108.76.0'), 10), # Colombia - CELSIA INTERNET S.A.S.
    IPFilterRule(*parse_ip('190.2.96.0'), 13), # Argentina - Teledifusora S.A.
    IPFilterRule(*parse_ip('190.201.0.0'), 15), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('190.44.0.0'), 18), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('190.5.252.0'), 10), # Panama - Cable Onda
    IPFilterRule(*parse_ip('190.52.96.0'), 11), # Venezuela - GOLD DATA USA INC
    IPFilterRule(*parse_ip('190.57.36.0'), 10), # Panama - Cable Onda
    IPFilterRule(*parse_ip('190.60.63.0'), 8), # Colombia - COLOMBIA MAS TV S.A.S
    IPFilterRule(*parse_ip('190.84.116.0'), 10), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('190.9.70.0'), 9), # Argentina - TORRES SERGIO HERNAN (ITEQ INTERNET)
    IPFilterRule(*parse_ip('191.186.0.0'), 14), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('191.242.48.0'), 11), # Brazil - WAY.COM PROVEDOR BANDA LARGA EIRELI
    IPFilterRule(*parse_ip('191.243.112.0'), 12), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('191.253.96.0'), 13), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('191.6.96.0'), 13), # Brazil - VOCE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('193.43.159.0'), 8), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('194.124.36.104'), 3), # Syria - High Speed Telekomunikasyon ve Hab. Hiz. Ltd. Sti.
    IPFilterRule(*parse_ip('195.8.50.0'), 9), # Armenia - Diananet LLC
    IPFilterRule(*parse_ip('196.207.128.0'), 14), # Kenya - Wananchi Group (Kenya) Limited
    IPFilterRule(*parse_ip('197.232.0.0'), 16), # Kenya - Jamii Telecommunications Limited
    IPFilterRule(*parse_ip('2.79.0.0'), 16), # Kazakhstan - Kcell JSC
    IPFilterRule(*parse_ip('200.107.64.0'), 10), # Brazil - ZIONTECH TECNOLOGIA E SERVICOS
    IPFilterRule(*parse_ip('200.14.56.0'), 10), # Brazil - CONNECT PEDREIRAS SERVIÇOS DE INFORMATICA LTDA
    IPFilterRule(*parse_ip('200.155.128.0'), 14), # Brazil - Telium Telecomunicações Ltda
    IPFilterRule(*parse_ip('200.203.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('200.225.112.0'), 10), # Brazil - RVT SERVICOS DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('200.46.234.0'), 9), # Panama - Cable Onda
    IPFilterRule(*parse_ip('200.74.0.0'), 15), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('200.84.0.0'), 15), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('201.16.120.0'), 9), # Brazil - BR.Digital Provider
    IPFilterRule(*parse_ip('201.183.0.0'), 16), # Ecuador - Ecuadortelecom S.A.
    IPFilterRule(*parse_ip('201.192.0.0'), 20), # Costa Rica - Instituto Costarricense de Electricidad y Telecom.
    IPFilterRule(*parse_ip('201.216.92.0'), 10), # Brazil - Tecnonet Servicos Provedor De Internet Ltda
    IPFilterRule(*parse_ip('201.218.208.0'), 8), # Panama - Cable Onda
    IPFilterRule(*parse_ip('201.254.0.0'), 15), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('201.49.236.0'), 10), # Brazil - Speednet Telecomunicações Ltda ME
    IPFilterRule(*parse_ip('201.66.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('203.81.238.0'), 8), # Pakistan - Special Communication Organization
    IPFilterRule(*parse_ip('204.157.182.0'), 9), # Iraq - Horizon Scope Mobile Telecom WLL
    IPFilterRule(*parse_ip('210.211.56.0'), 11), # Ecuador - TELEALFACOM S.A.S.
    IPFilterRule(*parse_ip('212.11.192.0'), 13), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('212.68.59.0'), 7), # Syria - Guneydogu Telekom int.bil. ve ilt. hiz. tic. ltd. sti.
    IPFilterRule(*parse_ip('212.95.152.0'), 10), # Iraq - ASIACELL COMMUNICATIONS PJSC
    IPFilterRule(*parse_ip('213.206.60.0'), 10), # Uzbekistan - Uzbektelekom Joint Stock Company
    IPFilterRule(*parse_ip('213.6.0.0'), 16), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('24.41.132.0'), 10), # Puerto Rico - Liberty Communications of Puerto Rico LLC
    IPFilterRule(*parse_ip('27.60.0.0'), 12), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('27.97.176.0'), 12), # India - Vodafone Idea Ltd
    IPFilterRule(*parse_ip('36.72.0.0'), 19), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('37.104.0.0'), 18), # Saudi Arabia - Saudi Telecom Company JSC
    IPFilterRule(*parse_ip('37.202.64.0'), 14), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('37.237.160.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('38.3.140.0'), 10), # Brazil - BRX TELECOMUNICACOES LTDA - EPP
    IPFilterRule(*parse_ip('38.3.186.0'), 8), # Brazil - H2A TELECOM
    IPFilterRule(*parse_ip('38.41.32.0'), 10), # Venezuela - SISPROT GLOBAL FIBER, C.A.
    IPFilterRule(*parse_ip('41.208.128.0'), 14), # Senegal - SONATEL-AS Autonomous System
    IPFilterRule(*parse_ip('41.249.0.0'), 15), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('41.87.192.0'), 13), # South Africa - Cipherwave
    IPFilterRule(*parse_ip('43.245.120.0'), 10), # Bangladesh - Banglalink Digital Communications Ltd
    IPFilterRule(*parse_ip('45.112.48.0'), 10), # India - Pioneer Elabs Ltd.
    IPFilterRule(*parse_ip('45.160.88.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('45.162.196.0'), 10), # Brazil - Conecta Network Telecom LTDA
    IPFilterRule(*parse_ip('45.162.236.0'), 10), # Brazil - REDE RALPNET TELECOMUNICACOES EIRELI
    IPFilterRule(*parse_ip('45.162.252.0'), 10), # Brazil - GiroNet Provedor de Internet e Telecom
    IPFilterRule(*parse_ip('45.164.68.0'), 10), # Brazil - REDE SUL SP LTDA - ME
    IPFilterRule(*parse_ip('45.165.248.0'), 10), # Brazil - I A TORRES PROVEDORES ME
    IPFilterRule(*parse_ip('45.167.116.0'), 10), # Brazil - INFORTEC COMERCIO VAREJISTA DE MAQUINAS, EQUIPAMEN
    IPFilterRule(*parse_ip('45.168.184.0'), 9), # Brazil - GRUPO TDKOM
    IPFilterRule(*parse_ip('45.169.240.0'), 10), # Brazil - Topetex Telecom LTDA
    IPFilterRule(*parse_ip('45.170.96.0'), 10), # Brazil - ELEVAR TELECOM LTDA
    IPFilterRule(*parse_ip('45.172.64.0'), 10), # Brazil - AREA 51 PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.173.212.0'), 10), # Argentina - ISP GROUP SRL
    IPFilterRule(*parse_ip('45.177.104.0'), 10), # Brazil - NOXY COMUNICAÇÃO E TELECOMUNICAÇÃO LTDA.
    IPFilterRule(*parse_ip('45.178.100.0'), 10), # Brazil - M. da Silveira Ferreira ME
    IPFilterRule(*parse_ip('45.181.60.0'), 10), # Brazil - Sp-link Telecom Comunicacao Multimidia - Scm LTDA
    IPFilterRule(*parse_ip('45.182.12.0'), 10), # Brazil - ULTRAXX SERVICOS DE CONECTIVIDADE LTDA
    IPFilterRule(*parse_ip('45.183.192.0'), 10), # Brazil - PAULO HENRIQUE SOARES DE SOUZA
    IPFilterRule(*parse_ip('45.184.16.0'), 10), # Brazil - ORBI TELECOM
    IPFilterRule(*parse_ip('45.185.12.0'), 10), # Brazil - NETCENTER TELECOM
    IPFilterRule(*parse_ip('45.185.167.0'), 8), # Brazil - TurboNet Telecom
    IPFilterRule(*parse_ip('45.185.44.0'), 10), # Brazil - DELTA TELECOM
    IPFilterRule(*parse_ip('45.187.240.0'), 10), # Brazil - SYNCNET TELECOM
    IPFilterRule(*parse_ip('45.191.148.0'), 10), # Brazil - FORCA E ACAO SERVICOS DE TELECOMUNICACAO EIRELI
    IPFilterRule(*parse_ip('45.229.120.0'), 10), # Brazil - LINK NET BANDA LARGA EIRELI - ME
    IPFilterRule(*parse_ip('45.230.144.0'), 10), # Brazil - IDEALNET FIBRA
    IPFilterRule(*parse_ip('45.231.88.0'), 10), # Brazil - JOTAZO TELECOM
    IPFilterRule(*parse_ip('45.232.248.0'), 10), # Brazil - NETUNO DO BRASIL TELECOM LTDA
    IPFilterRule(*parse_ip('45.237.196.0'), 10), # Brazil - NovoLink Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('45.4.44.0'), 10), # Brazil - ITANET PONTO COM LTDA
    IPFilterRule(*parse_ip('45.4.56.0'), 10), # Brazil - VN TELECOM PROVEDORES A.R.C EIRELI
    IPFilterRule(*parse_ip('45.6.180.0'), 10), # Brazil - Artinet Telecom
    IPFilterRule(*parse_ip('45.7.116.0'), 10), # Brazil - Conect- Provedor de Internet Ltda EPP
    IPFilterRule(*parse_ip('45.70.164.0'), 10), # Brazil - WILLIAN MENDES DE OLIVEIRA ­ ME
    IPFilterRule(*parse_ip('46.143.160.0'), 11), # Saudi Arabia - ITC AS number
    IPFilterRule(*parse_ip('46.184.128.0'), 15), # Bahrain - STC BAHRAIN B.S.C CLOSED
    IPFilterRule(*parse_ip('47.11.0.0'), 16), # India - Reliance Jio Infocomm Limited
    IPFilterRule(*parse_ip('47.8.0.0'), 17), # India - Reliance Jio Infocomm Limited
    IPFilterRule(*parse_ip('5.1.104.0'), 11), # Iraq - Optimal Solutions Technology Company for information Technology and software solutions Ltd
    IPFilterRule(*parse_ip('5.175.146.0'), 9), # Iraq - SUPER CELL NETWORK FOR INTERNET SERVICES LTD
    IPFilterRule(*parse_ip('5.194.0.0'), 15), # United Arab Emirates - Emirates Internet
    IPFilterRule(*parse_ip('5.62.140.0'), 10), # Iraq - Al-Jazeera Al-Arabiya Company for Communication and Internet LTD
    IPFilterRule(*parse_ip('78.108.168.0'), 10), # Lebanon - TerraNet sal
    IPFilterRule(*parse_ip('80.233.32.0'), 13), # Ireland - Three Ireland (Hutchison) limited
    IPFilterRule(*parse_ip('80.246.81.0'), 8), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('80.72.215.0'), 8), # Russia - Truenetwork LLC
    IPFilterRule(*parse_ip('84.203.0.0'), 16), # Ireland - Digiweb ltd
    IPFilterRule(*parse_ip('84.47.208.0'), 9), # Iran - Iran Telecommunication Company PJS
    IPFilterRule(*parse_ip('87.225.32.0'), 11), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('87.241.128.0'), 14), # Armenia - Telecom Armenia AS
    IPFilterRule(*parse_ip('89.109.0.0'), 14), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('89.147.128.0'), 14), # Oman - Awaser Oman LLC
    IPFilterRule(*parse_ip('89.223.32.0'), 13), # Russia - Nevalink, LLC
    IPFilterRule(*parse_ip('90.154.152.0'), 10), # Bulgaria - Geo BG Net SPLtd.
    IPFilterRule(*parse_ip('91.142.224.0'), 12), # Ireland - Rapid Broadband Ltd
    IPFilterRule(*parse_ip('91.186.224.0'), 13), # Jordan - Batelco Jordan
    IPFilterRule(*parse_ip('91.243.96.0'), 12), # Russia - Special Engineering and Design Bureau "Orbita" JSC
    IPFilterRule(*parse_ip('94.241.192.0'), 14), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('94.44.0.0'), 16), # Hungary - One Hungary Ltd.
    IPFilterRule(*parse_ip('95.25.128.0'), 15), # Russia - PJSC "Vimpelcom"
    IPFilterRule(*parse_ip('102.0.16.0'), 11), # Kenya - Airtel Networks Kenya Limited
    IPFilterRule(*parse_ip('102.142.0.0'), 16), # Gabon - GVA Cote d'Ivoire SAS
    IPFilterRule(*parse_ip('102.207.0.0'), 10), # Ivory Coast - Atlantique Telecom (Cote d'Ivoire)
    IPFilterRule(*parse_ip('102.207.8.0'), 11), # Ivory Coast - Orange Côte d'Ivoire
    IPFilterRule(*parse_ip('102.213.200.0'), 10), # South Africa - MUBVUMELA CORPORATION PTY LTD
    IPFilterRule(*parse_ip('102.214.176.0'), 10), # South Africa - Wifiza Telecoms cc
    IPFilterRule(*parse_ip('102.217.120.0'), 10), # Kenya - Click Fiber Communications Limited
    IPFilterRule(*parse_ip('102.218.92.0'), 10), # Angola - Finstar - Sociedade de Investimento e Participacoes S.A
    IPFilterRule(*parse_ip('102.219.24.0'), 10), # South Africa - Vox Telecom Ltd
    IPFilterRule(*parse_ip('103.10.28.0'), 10), # Nepal - VIA NET COMMUNICATION LTD.
    IPFilterRule(*parse_ip('103.103.32.0'), 10), # Bangladesh - X-LINK LIMITED
    IPFilterRule(*parse_ip('103.104.87.0'), 8), # Pakistan - Orbit Internet Service Provider Pvt Ltd
    IPFilterRule(*parse_ip('103.110.34.0'), 9), # Indonesia - PT RECONET SEMESTA INDONESIA
    IPFilterRule(*parse_ip('103.113.172.0'), 10), # Bangladesh - SKY SYSTEMS LTD
    IPFilterRule(*parse_ip('103.113.192.0'), 10), # Bangladesh - Noakhali Broadband Network
    IPFilterRule(*parse_ip('103.124.96.0'), 10), # Nepal - Pokhara Internet Pvt. Ltd.
    IPFilterRule(*parse_ip('103.129.32.0'), 9), # Bangladesh - Jahid Communication
    IPFilterRule(*parse_ip('103.129.92.0'), 10), # Indonesia - PT. Eka Mas Republik
    IPFilterRule(*parse_ip('103.133.246.0'), 9), # Bangladesh - M. S. Adiba Online
    IPFilterRule(*parse_ip('103.139.10.0'), 9), # Indonesia - PT. Cemerlang Multimedia
    IPFilterRule(*parse_ip('103.140.26.0'), 9), # India - Shrisai Shavenk Technotronics Private Limited
    IPFilterRule(*parse_ip('103.155.151.0'), 8), # Bangladesh - WINK NETWORK
    IPFilterRule(*parse_ip('103.156.218.0'), 9), # Indonesia - PT. Eka Mas Republik
    IPFilterRule(*parse_ip('103.156.86.0'), 8), # Indonesia - PT Chacha Networking System
    IPFilterRule(*parse_ip('103.159.170.0'), 8), # Bangladesh - A S ONLINE
    IPFilterRule(*parse_ip('103.161.128.0'), 8), # Indonesia - PT Sandya Sistem Indonesia
    IPFilterRule(*parse_ip('103.169.65.0'), 8), # Pakistan - KCN
    IPFilterRule(*parse_ip('103.174.4.0'), 9), # Pakistan - FASTTEL BROADBAND (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('103.177.220.0'), 9), # Bangladesh - Duranto Broadband Network
    IPFilterRule(*parse_ip('103.184.18.0'), 9), # Indonesia - PT Garuda Lintas Cakrawala
    IPFilterRule(*parse_ip('103.190.136.0'), 9), # Bangladesh - Maruf Online BD
    IPFilterRule(*parse_ip('103.198.133.0'), 8), # Bangladesh - Digi Jadoo Broadband Ltd
    IPFilterRule(*parse_ip('103.205.132.0'), 8), # Bangladesh - ICC Communication
    IPFilterRule(*parse_ip('103.209.198.0'), 8), # Bangladesh - Sustainable Development Networking Program
    IPFilterRule(*parse_ip('103.222.20.0'), 10), # Bangladesh - Kazi Mohammad Shoabe T/A Explore Online
    IPFilterRule(*parse_ip('103.225.244.0'), 10), # Nepal - Websurfer Nepal Internet Service Provider
    IPFilterRule(*parse_ip('103.23.224.0'), 10), # Indonesia - Universitas Sebelas Maret
    IPFilterRule(*parse_ip('103.23.252.0'), 9), # Pakistan - MultiCity Broad Band Pvt Ltd
    IPFilterRule(*parse_ip('103.230.245.0'), 8), # Bangladesh - Ms Online
    IPFilterRule(*parse_ip('103.253.246.0'), 9), # Bangladesh - Innovative Online Limited
    IPFilterRule(*parse_ip('103.255.132.0'), 9), # Indonesia - PT Sarana Kawan Setia
    IPFilterRule(*parse_ip('103.255.72.0'), 10), # India - U.P. COMMUNICATION SERVICES PVT LTD
    IPFilterRule(*parse_ip('103.26.80.0'), 9), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('103.35.156.0'), 8), # Bangladesh - IP Communications Limited
    IPFilterRule(*parse_ip('103.46.8.0'), 9), # Indonesia - PT JARINGANKU SARANA NUSANTARA
    IPFilterRule(*parse_ip('103.58.72.0'), 10), # Bangladesh - Business Network
    IPFilterRule(*parse_ip('103.60.204.0'), 9), # Bangladesh - Ms Online
    IPFilterRule(*parse_ip('103.66.168.0'), 8), # Bangladesh - DELTA SOFTWARE AND COMMUNICATION LIMITED
    IPFilterRule(*parse_ip('103.76.44.0'), 10), # Bangladesh - U-Turn Technologies
    IPFilterRule(*parse_ip('103.78.226.0'), 9), # Bangladesh - Digicon Telecommunication Ltd
    IPFilterRule(*parse_ip('103.80.0.0'), 10), # Bangladesh - SS Online
    IPFilterRule(*parse_ip('103.89.26.0'), 8), # Bangladesh - Gmax
    IPFilterRule(*parse_ip('103.91.228.0'), 10), # Bangladesh - NetExpress Online
    IPFilterRule(*parse_ip('103.93.93.0'), 8), # Indonesia - PT Jinde Grup Indonesia
    IPFilterRule(*parse_ip('105.112.0.0'), 20), # Nigeria - Airtel Networks Limited
    IPFilterRule(*parse_ip('105.154.0.0'), 16), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('105.159.192.0'), 13), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('105.160.0.0'), 19), # Kenya - Safaricom Limited
    IPFilterRule(*parse_ip('106.200.0.0'), 13), # India - Bharti Airtel Ltd., Telemedia Services
    IPFilterRule(*parse_ip('106.206.192.0'), 14), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('106.219.144.0'), 12), # India - Bharti Airtel Ltd., Telemedia Services
    IPFilterRule(*parse_ip('106.219.192.0'), 14), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('106.76.70.0'), 9), # India - Vodafone Idea Ltd
    IPFilterRule(*parse_ip('109.175.0.0'), 15), # Bosnia and Herzegovina - BIHNET Autonomus System
    IPFilterRule(*parse_ip('109.186.0.0'), 16), # Israel - Cellcom Fixed Line Communication L.P
    IPFilterRule(*parse_ip('109.225.0.0'), 13), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('109.236.32.0'), 12), # Albania - Abissnet sh.a.
    IPFilterRule(*parse_ip('110.38.240.0'), 12), # Pakistan - Galaxy Broadband
    IPFilterRule(*parse_ip('110.39.63.0'), 8), # Pakistan - National WiMAX/IMS environment
    IPFilterRule(*parse_ip('113.210.0.0'), 17), # Malaysia - Binariang Berhad
    IPFilterRule(*parse_ip('114.10.40.0'), 11), # Indonesia - INDOSAT Internet Network Provider
    IPFilterRule(*parse_ip('114.31.136.0'), 11), # India - Vodafone Idea Ltd
    IPFilterRule(*parse_ip('116.204.148.0'), 10), # Bangladesh - Digicon Telecommunication Ltd
    IPFilterRule(*parse_ip('117.192.0.0'), 22), # India - National Internet Backbone
    IPFilterRule(*parse_ip('118.96.0.0'), 17), # Indonesia - PT Telekomunikasi Indonesia
    IPFilterRule(*parse_ip('118.99.80.0'), 10), # Indonesia - BIZNET NETWORKS
    IPFilterRule(*parse_ip('119.73.112.0'), 10), # Pakistan - Trans World Enterprise Services (Private) Limited
    IPFilterRule(*parse_ip('119.73.120.0'), 9), # Pakistan - Trans World Enterprise Services (Private) Limited
    IPFilterRule(*parse_ip('122.129.68.0'), 8), # Pakistan - FALCON BROADBAND (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('122.171.128.0'), 15), # India - Bharti Airtel Ltd., Telemedia Services
    IPFilterRule(*parse_ip('122.201.24.0'), 11), # Mongolia - Univision LLC
    IPFilterRule(*parse_ip('123.255.200.0'), 11), # Indonesia - PT. DATA Utama Dinamika
    IPFilterRule(*parse_ip('131.0.164.0'), 10), # Brazil - WINQ ULTRANET
    IPFilterRule(*parse_ip('131.0.92.0'), 10), # Brazil - SiqueiraLink Internet Banda Larga
    IPFilterRule(*parse_ip('131.161.64.0'), 10), # Brazil - IOL REDE DE PROVEDORES LTDA
    IPFilterRule(*parse_ip('131.196.100.0'), 10), # Brazil - NV7 TELECOM LTDA
    IPFilterRule(*parse_ip('131.221.172.0'), 10), # Brazil - DIGITAL WAVE DE MERITI PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('131.221.192.0'), 10), # Brazil - Tamar Comercio e Equipamentos para Informática Ltd
    IPFilterRule(*parse_ip('131.221.52.0'), 10), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('131.221.56.0'), 10), # Brazil - Net Fácil Sistemas Eletrônicos Ltda ME
    IPFilterRule(*parse_ip('138.0.168.0'), 10), # Brazil - FRANCISCO MARQUES VIEIRA GONCALVES ME
    IPFilterRule(*parse_ip('138.0.68.0'), 10), # Brazil - DIRETRIX COMÉRCIO INFORMATICA LTDA.
    IPFilterRule(*parse_ip('138.117.116.0'), 10), # Brazil - WF -TELECOM SERVIÇOS DE TELECOMUNICAÇOES EIRELE ME
    IPFilterRule(*parse_ip('138.118.168.0'), 10), # Brazil - DIRECT INTERNET LTDA
    IPFilterRule(*parse_ip('138.121.104.0'), 10), # Argentina - RED POWER INTERNET SRL
    IPFilterRule(*parse_ip('138.121.64.0'), 10), # Brazil - Companhia Itabirana Telecomunicações Ltda
    IPFilterRule(*parse_ip('138.186.116.0'), 10), # Brazil - MHNET TELECOM
    IPFilterRule(*parse_ip('138.204.36.0'), 10), # Brazil - AW Fibra
    IPFilterRule(*parse_ip('138.219.160.0'), 10), # Argentina - GLOBAL TECHNOLOGY SRL
    IPFilterRule(*parse_ip('138.219.192.0'), 10), # Brazil - BRASIL NET EMPREENDIMENTOS LTDA - ME
    IPFilterRule(*parse_ip('138.255.232.0'), 10), # Brazil - POWERNET SOLUTIONS LTDA
    IPFilterRule(*parse_ip('138.36.80.0'), 10), # Brazil - Netfar Informatica Ltda
    IPFilterRule(*parse_ip('138.84.32.0'), 10), # Chile - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('138.84.38.0'), 9), # Peru - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('141.101.229.0'), 8), # Russia - AirLink Ltd.
    IPFilterRule(*parse_ip('143.0.184.0'), 10), # Brazil - CONNECTA TELECOM INTERNET LTDA - EPP
    IPFilterRule(*parse_ip('143.105.128.0'), 9), # Guyana - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('143.137.176.0'), 8), # Brazil - Une Telecom Ltda
    IPFilterRule(*parse_ip('143.137.68.0'), 10), # Brazil - ok virtual provedor de internet ltda
    IPFilterRule(*parse_ip('143.202.120.0'), 10), # Brazil - Butzen e Mentges Ltda
    IPFilterRule(*parse_ip('143.255.100.0'), 10), # Brazil - MHNET TELECOM
    IPFilterRule(*parse_ip('143.255.96.0'), 10), # Brazil - Sul Online Telecom Ltda - EPP
    IPFilterRule(*parse_ip('144.48.128.0'), 11), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('146.120.97.0'), 8), # Ukraine - Khozinskyi Vadym
    IPFilterRule(*parse_ip('148.222.230.0'), 9), # Peru - MORENO YANOC NEMIAS BERNARDO
    IPFilterRule(*parse_ip('148.227.88.0'), 10), # Brazil - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('149.107.208.0'), 12), # Argentina - ESTABLECIMIENTO CASCADA BLANCA S.A
    IPFilterRule(*parse_ip('150.129.128.0'), 10), # India - Gazon Communications India Limited
    IPFilterRule(*parse_ip('150.228.4.0'), 9), # Ukraine - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('152.166.128.0'), 15), # Dominican Republic - ALTICE DOMINICANA S.A.
    IPFilterRule(*parse_ip('152.167.0.0'), 16), # Dominican Republic - ALTICE DOMINICANA S.A.
    IPFilterRule(*parse_ip('154.112.0.0'), 16), # Gabon - Gabon Telecom / Office of Posts and Telecommunications of Gabon
    IPFilterRule(*parse_ip('154.208.40.0'), 11), # Pakistan - IN CABLE INTERNET (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('154.68.176.0'), 12), # South Africa - FIRSTNET TECHNOLOGY SERVICES (PTY) LTD
    IPFilterRule(*parse_ip('154.80.0.0'), 15), # Pakistan - PMCL /LDI IP TRANSIT
    IPFilterRule(*parse_ip('157.10.184.0'), 8), # Indonesia - PT Internet Tjepat Indonesia
    IPFilterRule(*parse_ip('157.10.28.0'), 8), # Bangladesh - One Touch Online
    IPFilterRule(*parse_ip('157.100.0.0'), 13), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('157.15.172.0'), 8), # Indonesia - PT Mitra Telekomunikasi Nusantara
    IPFilterRule(*parse_ip('159.48.8.0'), 10), # Oman - Awaser Oman LLC
    IPFilterRule(*parse_ip('160.113.0.0'), 16), # Republic of the Congo - MTN CONGO
    IPFilterRule(*parse_ip('160.154.0.0'), 17), # Ivory Coast - Orange Côte d'Ivoire
    IPFilterRule(*parse_ip('160.19.174.0'), 9), # Brazil - MUSSEL NET TELECOMUNICAÇÕES EIRELE ME
    IPFilterRule(*parse_ip('160.250.254.0'), 9), # Nepal - DISH MEDIA NETWORK PUBLIC LIMITED
    IPFilterRule(*parse_ip('161.22.56.0'), 11), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('161.8.64.0'), 14), # Oman - Awaser Oman LLC
    IPFilterRule(*parse_ip('163.227.62.0'), 9), # Bangladesh - ZERO 4 COMMUNICATION
    IPFilterRule(*parse_ip('164.163.36.0'), 10), # Brazil - SUPRANET TELECOM INFORMATICA LTDA
    IPFilterRule(*parse_ip('167.249.240.0'), 10), # Brazil - E. C. E. Telecomunicações LTDA
    IPFilterRule(*parse_ip('168.194.192.0'), 10), # Brazil - PAINSONLINE Macal Internet Info
    IPFilterRule(*parse_ip('168.195.196.0'), 10), # Brazil - Taionet Telecomunicações Ltda. ME
    IPFilterRule(*parse_ip('168.195.0.0'), 10), # Brazil - JL INFORMATICA E TELECOM LTDA - ME
    IPFilterRule(*parse_ip('168.196.224.0'), 10), # Argentina - VANET TELECOMUNICACIONES S.R.L.
    IPFilterRule(*parse_ip('168.197.228.0'), 10), # Brazil - GIGASAT SERVIÇOS DE PROCESSAMENTOS DE DADOS LTDA
    IPFilterRule(*parse_ip('168.205.164.0'), 10), # Brazil - G G Tecnologia de Informação LTDA ME
    IPFilterRule(*parse_ip('168.226.80.0'), 12), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('168.228.188.0'), 8), # Brazil - FIBRANET TELECOM
    IPFilterRule(*parse_ip('170.150.55.0'), 8), # Brazil - Star Telecomunicações LTDA
    IPFilterRule(*parse_ip('170.203.196.0'), 9), # Brazil - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('170.231.180.0'), 10), # Brazil - MICRON LINE SERVICOS DE INFORMATICA LTDA - ME
    IPFilterRule(*parse_ip('170.239.52.0'), 10), # Brazil - SILVA MORAES SERV DE COMUN MULTIMIDIA-SCM EIRELI
    IPFilterRule(*parse_ip('170.246.168.0'), 10), # Brazil - Goldweb Barretos serviços de Telecomunicações Ltda
    IPFilterRule(*parse_ip('170.247.12.0'), 10), # Brazil - Firemicro Informática
    IPFilterRule(*parse_ip('170.247.68.0'), 10), # Brazil - Une Telecom Ltda
    IPFilterRule(*parse_ip('170.247.80.0'), 10), # Brazil - Emex Internet
    IPFilterRule(*parse_ip('170.254.20.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('170.78.244.0'), 10), # Brazil - VEXNET TELECON INFORMÁTICA LTDA
    IPFilterRule(*parse_ip('170.79.176.0'), 10), # Brazil - TOP NET LTDA
    IPFilterRule(*parse_ip('170.80.12.0'), 10), # Brazil - Athena Telecomunicão Ltda
    IPFilterRule(*parse_ip('170.81.108.0'), 10), # Brazil - L3 NETWORKS E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('170.81.12.0'), 10), # Brazil - UNINET TELECOM E INFORMÁTICA - EIRELLI - ME
    IPFilterRule(*parse_ip('170.81.216.0'), 11), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('170.82.104.0'), 10), # Brazil - RZ NET LTDA.
    IPFilterRule(*parse_ip('170.82.152.0'), 10), # Brazil - LINK10 BR
    IPFilterRule(*parse_ip('170.83.136.0'), 10), # Brazil - Connecta Comercio e Serviços Ltda - EPP
    IPFilterRule(*parse_ip('170.83.160.0'), 10), # Brazil - CAMON PROVEDOR
    IPFilterRule(*parse_ip('170.83.64.0'), 10), # Brazil - isabella magalhães silveira mello me
    IPFilterRule(*parse_ip('170.84.224.0'), 10), # Brazil - Henet Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('173.225.240.0'), 11), # Jamaica - Digicel Jamaica
    IPFilterRule(*parse_ip('175.107.224.0'), 10), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('175.144.0.0'), 17), # Malaysia - TM TECHNOLOGY SERVICES SDN. BHD.
    IPFilterRule(*parse_ip('175.157.0.0'), 16), # Sri Lanka - Dialog Axiata PLC.
    IPFilterRule(*parse_ip('175.6.216.0'), 10), # China - Hengyang
    IPFilterRule(*parse_ip('176.114.192.0'), 13), # Russia - Annet Ltd.
    IPFilterRule(*parse_ip('176.122.48.0'), 12), # Russia - IP Gasanov Farhad Urujbekovich
    IPFilterRule(*parse_ip('177.10.128.0'), 10), # Brazil - NDC PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.10.160.0'), 11), # Brazil - Chapeco Tecnologia em Telecomunicações Ltda.
    IPFilterRule(*parse_ip('177.10.216.0'), 10), # Brazil - Fox Conect Provedor de Internet LTDA
    IPFilterRule(*parse_ip('177.10.248.0'), 11), # Brazil - ORLA TELECOM
    IPFilterRule(*parse_ip('177.10.92.0'), 10), # Brazil - NOVANET TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.104.16.0'), 12), # Brazil - INETSAFE COMERCIO DE EQUIPAMENTOS ELETRONICOS LTDA
    IPFilterRule(*parse_ip('177.118.128.0'), 14), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.12.0.0'), 14), # Brazil - Predlink Rede de Telecomunicções Ltda
    IPFilterRule(*parse_ip('177.124.96.0'), 10), # Brazil - BANDA TURBO PROVEDORES DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.128.182.0'), 8), # Brazil - CLICKIP PROVEDORES DE ACESSO LTDA
    IPFilterRule(*parse_ip('177.128.48.0'), 10), # Brazil - REVNET TELECOMUNICACOES E SERVICOS LTDA
    IPFilterRule(*parse_ip('177.129.184.0'), 11), # Brazil - Link Sete Servicos de Internet e Redes Ltda
    IPFilterRule(*parse_ip('177.129.28.0'), 10), # Brazil - AMARO & AMARO COMUNICAO LTDA - ME
    IPFilterRule(*parse_ip('177.129.48.0'), 11), # Brazil - VSAT- TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('177.143.0.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.154.160.0'), 12), # Brazil - Go In Tecnologia
    IPFilterRule(*parse_ip('177.155.176.0'), 12), # Brazil - RIO CABLE TELECOM LTDA
    IPFilterRule(*parse_ip('177.160.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.184.96.0'), 13), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('177.184.220.0'), 10), # Brazil - HELP NET TELECOM E INFORMÁTICA LTDA - ME
    IPFilterRule(*parse_ip('177.200.140.0'), 10), # Brazil - Redfiber Telecomunicações Ltda.
    IPFilterRule(*parse_ip('177.202.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('177.222.32.0'), 13), # Bolivia - Telefónica Celular de Bolivia S.A.
    IPFilterRule(*parse_ip('177.223.224.0'), 12), # Brazil - NOVATEC TELECOM LTDA
    IPFilterRule(*parse_ip('177.226.128.0'), 15), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('177.226.64.0'), 12), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('177.234.211.0'), 8), # Ecuador - VUELATECHNOLOGY S.A.S.
    IPFilterRule(*parse_ip('177.241.32.0'), 13), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('177.249.168.0'), 11), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('177.38.240.0'), 11), # Brazil - Henet Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.39.112.0'), 11), # Brazil - PARAISONET LTDA
    IPFilterRule(*parse_ip('177.39.240.0'), 12), # Brazil - BRASIL TECPAR | AMIGO | AVATO
    IPFilterRule(*parse_ip('177.44.220.0'), 10), # Brazil - Dataware Telecomunicações LTDA. - EPP
    IPFilterRule(*parse_ip('177.52.104.0'), 11), # Brazil - XTURBO PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('177.53.40.0'), 11), # Brazil - ALLREDE TELECOM LTDA
    IPFilterRule(*parse_ip('177.54.112.0'), 12), # Brazil - Friburgo Online LTDA ME
    IPFilterRule(*parse_ip('177.55.192.0'), 12), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('177.62.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.67.172.0'), 10), # Brazil - SPACE NET SERV. DE TELECOMUNICAÇÃO EM INF. LTDA-ME
    IPFilterRule(*parse_ip('177.71.32.0'), 12), # Brazil - BROSEGHINI LTDA EPP
    IPFilterRule(*parse_ip('177.72.80.0'), 11), # Brazil - BRMOM CONSTRUINDO CONEXOES LTDA
    IPFilterRule(*parse_ip('177.73.216.0'), 10), # Brazil - INFINITY FIBRA TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.74.184.0'), 11), # Brazil - ALCANS TELECOM LTDA
    IPFilterRule(*parse_ip('177.8.112.0'), 12), # Brazil - Roveri Opção Provedor de Acesso a Internet Ltda ME
    IPFilterRule(*parse_ip('177.84.56.0'), 10), # Brazil - w de c canto junior
    IPFilterRule(*parse_ip('177.91.140.0'), 10), # Brazil - Seta Micros Ltda
    IPFilterRule(*parse_ip('177.92.164.0'), 10), # Brazil - RALUEL COMERCIO LTDA ME
    IPFilterRule(*parse_ip('178.131.128.0'), 14), # Iran - Mobin Net Communication Company (Private Joint Stock)
    IPFilterRule(*parse_ip('178.134.0.0'), 16), # Georgia - JSC "Silknet"
    IPFilterRule(*parse_ip('178.137.0.0'), 16), # Ukraine - Kyivstar PJSC
    IPFilterRule(*parse_ip('178.168.0.0'), 15), # Moldova - StarNet Solutii SRL
    IPFilterRule(*parse_ip('178.210.224.0'), 10), # Iraq - Al-Sabah Technical Company for Trading and General Contracting Ltd.
    IPFilterRule(*parse_ip('178.218.96.0'), 12), # Russia - MTS PJSC
    IPFilterRule(*parse_ip('178.220.0.0'), 17), # Serbia - TELEKOM SRBIJA a.d.
    IPFilterRule(*parse_ip('179.0.112.0'), 10), # Brazil - F ROMARIO GOMES DA SILVA
    IPFilterRule(*parse_ip('179.108.192.0'), 13), # Brazil - CONECTA LTDA.
    IPFilterRule(*parse_ip('179.157.16.0'), 11), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.191.128.0'), 13), # Brazil - Videomar Rede Nordeste S/A
    IPFilterRule(*parse_ip('179.215.0.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('179.48.180.0'), 9), # Brazil - Soluti Fibra Telecomunicações Ltda
    IPFilterRule(*parse_ip('179.60.112.0'), 12), # Bolivia - Digital TV CABLE DE EDMUND S.R.L.
    IPFilterRule(*parse_ip('179.60.174.0'), 8), # Costa Rica - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('179.63.64.0'), 10), # Brazil - NOVA UNIAO TELECOM LTDA
    IPFilterRule(*parse_ip('179.96.240.0'), 12), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('181.113.100.0'), 8), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('181.116.176.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('181.175.0.0'), 16), # Ecuador - SERVICIOS DE TELECOMUNICACIONES SETEL S.A. (XTRIM EC)
    IPFilterRule(*parse_ip('181.188.128.0'), 14), # Bolivia - Telefónica Celular de Bolivia S.A.
    IPFilterRule(*parse_ip('181.192.64.0'), 12), # Argentina - CESOP
    IPFilterRule(*parse_ip('181.198.0.0'), 16), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('181.208.0.0'), 16), # Venezuela - Corporación Telemic C.A.
    IPFilterRule(*parse_ip('181.211.216.0'), 10), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('181.214.29.0'), 8), # Dominican Republic - TELERY NETWORKS, S.R.L
    IPFilterRule(*parse_ip('181.224.223.0'), 8), # Argentina - ALDERETE RIVAS JORDAN TOMAS SEBASTIAN (COMUNICATE INTERNET)
    IPFilterRule(*parse_ip('181.226.0.0'), 16), # Chile - Telefonica del Sur S.A.
    IPFilterRule(*parse_ip('181.32.0.0'), 16), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('181.55.112.0'), 12), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('181.78.64.0'), 11), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('185.103.88.0'), 10), # Lebanon - CHAWICH GROUP LTD
    IPFilterRule(*parse_ip('185.106.28.0'), 10), # Iraq - Kurdistan Net Company for Computer and Internet Ltd.
    IPFilterRule(*parse_ip('185.114.88.0'), 10), # Lebanon - BITAR NET SARL
    IPFilterRule(*parse_ip('185.122.252.0'), 10), # Iraq - Light Luster
    IPFilterRule(*parse_ip('185.139.136.0'), 10), # Uzbekistan - "Uzbektelekom" Joint Stock Company
    IPFilterRule(*parse_ip('185.15.60.0'), 10), # Russia - Dagomys Telecom LLC
    IPFilterRule(*parse_ip('185.156.152.0'), 10), # Serbia - Sat-Trakt D.O.O.
    IPFilterRule(*parse_ip('185.185.124.0'), 9), # Oman - Awaser Oman LLC
    IPFilterRule(*parse_ip('185.186.80.0'), 10), # Kosovo - TelKos L.L.C
    IPFilterRule(*parse_ip('185.206.124.0'), 10), # Iraq - Steps Telecom For Internet Ltd.
    IPFilterRule(*parse_ip('185.213.154.0'), 8), # Sweden - 31173 Services AB
    IPFilterRule(*parse_ip('185.225.40.0'), 10), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('185.239.120.0'), 10), # Ukraine - Alexey Geiner
    IPFilterRule(*parse_ip('185.30.144.0'), 10), # Albania - Mobitel sh.p.k.
    IPFilterRule(*parse_ip('185.64.208.0'), 10), # Russia - Svyazist LLC
    IPFilterRule(*parse_ip('185.79.2.0'), 9), # Armenia - House Net LLC
    IPFilterRule(*parse_ip('185.92.139.72'), 2), # Ukraine - K-telekom LLC
    IPFilterRule(*parse_ip('185.97.94.0'), 8), # Lebanon - My ISP SARL
    IPFilterRule(*parse_ip('186.0.195.0'), 3), # Argentina - Silica Networks Argentina S.A.
    IPFilterRule(*parse_ip('186.12.204.0'), 10), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.122.88.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.13.96.0'), 13), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.13.208.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.151.92.0'), 9), # Guatemala - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('186.158.0.0'), 11), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.158.32.0'), 13), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.192.96.0'), 13), # Brazil - ELETRODATA LTDA
    IPFilterRule(*parse_ip('186.193.0.0'), 12), # Brazil - BRXNQT Telecomunicações Ltda
    IPFilterRule(*parse_ip('186.219.144.0'), 12), # Brazil - CONEXAO SERVICOS DE COMUNICACAO MULTIMIDIA LTDA-ME
    IPFilterRule(*parse_ip('186.226.160.0'), 12), # Brazil - INFORTEL COMUNICACOES LTDA
    IPFilterRule(*parse_ip('186.226.176.0'), 12), # Brazil - IVI TECNOLOGIA E COMUNICAÇÃO LTDA
    IPFilterRule(*parse_ip('186.40.128.0'), 15), # Chile - CTC. CORP S.A. (TELEFONICA EMPRESAS)
    IPFilterRule(*parse_ip('186.47.176.0'), 11), # Ecuador - CORPORACION NACIONAL DE TELECOMUNICACIONES - CNT EP
    IPFilterRule(*parse_ip('186.82.64.0'), 13), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.85.240.0'), 9), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('186.96.208.0'), 12), # Trinidad and Tobago - AMPLIA COMMUNICATIONS LTD.
    IPFilterRule(*parse_ip('187.103.216.0'), 10), # Brazil - G2G INTERNET E SERVICOS DE TELECOM LTDA
    IPFilterRule(*parse_ip('187.112.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.120.48.0'), 12), # Brazil - DB3 SERVICOS DE TELECOMUNICACOES S.A
    IPFilterRule(*parse_ip('187.126.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('187.189.216.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.19.80.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('187.190.146.0'), 9), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.36.0.0'), 18), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('187.48.0.0'), 16), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('187.56.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('187.61.104.0'), 11), # Brazil - CINTE Telecom Comercio e Servicos Ltda.
    IPFilterRule(*parse_ip('187.63.144.0'), 10), # Brazil - NEOPRINT INTERNET LTDA
    IPFilterRule(*parse_ip('187.84.160.0'), 12), # Brazil - Beltrãonet Telecomunicações LTDA - EPP
    IPFilterRule(*parse_ip('187.87.240.0'), 12), # Brazil - Netwave Telecomunicações Ltda.
    IPFilterRule(*parse_ip('188.113.216.0'), 10), # Uzbekistan - COSCOM Liability Limited Company
    IPFilterRule(*parse_ip('188.163.0.0'), 16), # Ukraine - Kyivstar PJSC
    IPFilterRule(*parse_ip('188.19.0.0'), 16), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('188.225.128.0'), 15), # Palestinian Territory - Coolnet New Communication Provider
    IPFilterRule(*parse_ip('188.229.128.0'), 15), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('189.124.128.0'), 15), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('189.145.160.0'), 13), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.216.136.0'), 11), # Mexico - Cablevisión, S.A. de C.V.
    IPFilterRule(*parse_ip('189.232.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.241.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.33.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('189.36.128.0'), 10), # Brazil - BL PROVEDOR DE ACESSO A INTERNET LTDA
    IPFilterRule(*parse_ip('189.76.208.0'), 12), # Brazil - WKVE Assessoria em Serv. de Inf. e Telecom Ltda
    IPFilterRule(*parse_ip('189.84.56.0'), 10), # Brazil - STEC GUAIBA
    IPFilterRule(*parse_ip('189.89.246.0'), 9), # Brazil - ALMEIDA SERVICOS DE MULTIMIDIA E COMUNICACOES LTDA
    IPFilterRule(*parse_ip('190.108.208.0'), 11), # Guyana - E-Networks Inc.
    IPFilterRule(*parse_ip('190.110.99.0'), 6), # Chile - Silica Networks Argentina S.A.
    IPFilterRule(*parse_ip('190.115.212.0'), 10), # Brazil - VALMIR LOPES DE SOUZA
    IPFilterRule(*parse_ip('190.123.72.0'), 10), # Brazil - P3 SERVIÇOS DE TELECOMUNICAÇÃO LTDA
    IPFilterRule(*parse_ip('190.137.176.0'), 12), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.2.68.0'), 10), # Brazil - FIBER CONNECT LTDA
    IPFilterRule(*parse_ip('190.200.0.0'), 15), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('190.226.64.0'), 14), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('190.227.13.0'), 8), # Argentina - DELCO IMAGEN S.A.
    IPFilterRule(*parse_ip('190.4.112.0'), 12), # Argentina - Interface
    IPFilterRule(*parse_ip('190.5.160.0'), 13), # Argentina - MERCO COMUNICACIONES
    IPFilterRule(*parse_ip('190.53.248.0'), 9), # Honduras - Telefónica Celular S.A
    IPFilterRule(*parse_ip('190.56.0.0'), 16), # Guatemala - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.6.0.0'), 9), # Venezuela - Net Uno, C.A.
    IPFilterRule(*parse_ip('190.62.88.0'), 9), # El Salvador - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.83.128.0'), 15), # Trinidad and Tobago - Columbus Communications Trinidad Limited.
    IPFilterRule(*parse_ip('190.83.56.0'), 10), # Brazil - SSC TELECOM & CIA LTDA
    IPFilterRule(*parse_ip('190.89.30.0'), 9), # Venezuela - CORPORACION FIBEX TELECOM, C.A.
    IPFilterRule(*parse_ip('190.97.120.0'), 11), # Argentina - COOPERATIVA ELECTRICA DE MONTE LTDA
    IPFilterRule(*parse_ip('191.204.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.241.128.0'), 11), # Brazil - MINAS INFO LTDA-ME
    IPFilterRule(*parse_ip('191.241.144.0'), 12), # Brazil - SATURNO COMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('191.242.160.0'), 12), # Brazil - Cyber Info Provedor de Acesso LTDA ME
    IPFilterRule(*parse_ip('191.243.44.0'), 10), # Brazil - MICROTURBO TELECOMUNICACOES LTDA-ME
    IPFilterRule(*parse_ip('191.253.48.0'), 11), # Brazil - ENEVE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('191.30.0.0'), 17), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('191.36.192.0'), 12), # Brazil - 3WLINK INTERNET LTDA
    IPFilterRule(*parse_ip('191.37.216.0'), 11), # Brazil - UNI TELECOM LTDA
    IPFilterRule(*parse_ip('191.9.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('192.141.188.0'), 10), # Brazil - DNL NETWORK TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('193.188.96.0'), 13), # Bahrain - BEYON B.S.C.
    IPFilterRule(*parse_ip('193.34.225.0'), 8), # Kyrgyzstan - Extra Line LLC
    IPFilterRule(*parse_ip('193.43.140.0'), 8), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('193.43.145.0'), 8), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('193.77.128.0'), 15), # Slovenia - Telekom Slovenije, d.d.
    IPFilterRule(*parse_ip('195.178.110.200'), 2), # The Netherlands - TECHOFF SRV LIMITED
    IPFilterRule(*parse_ip('195.68.240.0'), 9), # Russia - Kompanon LLC.
    IPFilterRule(*parse_ip('196.130.0.0'), 17), # Egypt - Vodafone Data
    IPFilterRule(*parse_ip('196.154.0.0'), 14), # Egypt - Vodafone Data
    IPFilterRule(*parse_ip('196.210.0.0'), 16), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('196.70.240.0'), 11), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('197.160.0.0'), 19), # Egypt - Link Egypt (Link.NET)
    IPFilterRule(*parse_ip('197.238.0.0'), 16), # Tunisia - TOPNET
    IPFilterRule(*parse_ip('197.94.248.0'), 10), # South Africa - Dimension Data
    IPFilterRule(*parse_ip('198.12.44.0'), 10), # Argentina - ARLINK S.A.
    IPFilterRule(*parse_ip('2.57.96.0'), 10), # Kazakhstan - JSC Transtelecom
    IPFilterRule(*parse_ip('200.0.8.0'), 11), # Brazil - CONNECT WIRELESS LTDA
    IPFilterRule(*parse_ip('200.100.0.0'), 16), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('200.104.0.0'), 16), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('200.160.64.0'), 13), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('200.188.96.0'), 13), # Mexico - Alestra, S. de R.L. de C.V.
    IPFilterRule(*parse_ip('200.189.20.0'), 9), # Brazil - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('200.202.96.0'), 12), # Brazil - LESTE FLU SERVIÇOS DE TELECOM LTDA
    IPFilterRule(*parse_ip('200.26.248.0'), 10), # Brazil - DATA LINK COMUNICAÇÃO LTDA ME
    IPFilterRule(*parse_ip('200.39.150.0'), 9), # Brazil - CITYNET COM. DE PROD. DE INFORMATICA LTDA
    IPFilterRule(*parse_ip('200.4.116.0'), 10), # Brazil - DIRECT INTERNET LTDA
    IPFilterRule(*parse_ip('200.44.192.0'), 14), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('200.59.32.0'), 12), # Argentina - VELOCOM
    IPFilterRule(*parse_ip('200.80.160.0'), 13), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('200.88.0.0'), 16), # Dominican Republic - Compañía Dominicana de Teléfonos S. A.
    IPFilterRule(*parse_ip('200.96.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('201.106.0.0'), 15), # Mexico - UNINET
    IPFilterRule(*parse_ip('201.108.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('201.143.128.0'), 15), # Mexico - UNINET
    IPFilterRule(*parse_ip('201.148.240.0'), 10), # Brazil - VIA SUL TELECOMUNICAÇOES LTDA ME
    IPFilterRule(*parse_ip('201.159.164.0'), 9), # Brazil - Tuddo Telecom Ltda.
    IPFilterRule(*parse_ip('201.159.184.0'), 11), # Brazil - Patrimônio Monitoramento Eletrônico LTDA.
    IPFilterRule(*parse_ip('201.164.144.0'), 11), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('201.17.0.0'), 16), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('201.182.120.0'), 10), # Brazil - AVIAnet Telecom
    IPFilterRule(*parse_ip('201.182.32.0'), 10), # Brazil - ADM INTERNET EIRELI
    IPFilterRule(*parse_ip('201.182.48.0'), 10), # Brazil - ULTRANET NETWORK
    IPFilterRule(*parse_ip('201.188.0.0'), 17), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('201.21.128.0'), 15), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('201.229.128.0'), 15), # Dominican Republic - Compañía Dominicana de Teléfonos S. A.
    IPFilterRule(*parse_ip('201.24.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.241.0.0'), 16), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('201.247.0.0'), 15), # El Salvador - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('201.252.0.0'), 15), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('201.40.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.88.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('201.94.144.0'), 10), # Brazil - FIBRACONN SERVIÇOS DE TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('202.142.155.0'), 8), # Pakistan - Dotcom International Pvt. Limited
    IPFilterRule(*parse_ip('202.142.95.0'), 8), # India - INDINET SERVICE PRIVATE LIMITED
    IPFilterRule(*parse_ip('202.165.232.0'), 9), # Pakistan - Optix Pakistan (Pvt.) Limited
    IPFilterRule(*parse_ip('202.22.192.0'), 12), # Bangladesh - Access Telecom (BD) Ltd.
    IPFilterRule(*parse_ip('202.56.0.0'), 10), # Cambodia - SMART AXIATA Co., Ltd.
    IPFilterRule(*parse_ip('203.189.236.0'), 10), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('203.190.8.0'), 11), # Bangladesh - Daffodil Online Ltd.
    IPFilterRule(*parse_ip('203.94.64.0'), 13), # Sri Lanka - Sri Lanka Telecom Internet
    IPFilterRule(*parse_ip('203.99.144.0'), 9), # Bangladesh - Orange Communication
    IPFilterRule(*parse_ip('206.0.204.0'), 9), # Pakistan - Optix Pakistan (Pvt.) Limited
    IPFilterRule(*parse_ip('206.221.80.0'), 12), # Argentina - Cablenet S.A.
    IPFilterRule(*parse_ip('207.248.192.0'), 12), # Chile - Pacifico Cable SPA.
    IPFilterRule(*parse_ip('217.199.144.0'), 12), # Kenya - MTN SA
    IPFilterRule(*parse_ip('223.186.192.0'), 14), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('24.152.24.0'), 10), # Brazil - HORUS TELECOMUNICACOES EIRELI
    IPFilterRule(*parse_ip('27.124.88.0'), 11), # Indonesia - PT INDONESIA COMNETS PLUS
    IPFilterRule(*parse_ip('27.125.224.0'), 13), # Malaysia - U Mobile Sdn Bhd
    IPFilterRule(*parse_ip('27.57.128.0'), 14), # India - Bharti Airtel Ltd., Telemedia Services
    IPFilterRule(*parse_ip('27.61.32.0'), 13), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('31.5.0.0'), 16), # Romania - Vodafone Romania S.A.
    IPFilterRule(*parse_ip('34.23.0.0'), 16), # United States - Google LLC
    IPFilterRule(*parse_ip('36.50.179.0'), 8), # Bangladesh - Orange Communication
    IPFilterRule(*parse_ip('37.17.240.0'), 10), # Ukraine - Best ISP
    IPFilterRule(*parse_ip('37.242.32.0'), 13), # Saudi Arabia - Etihad Etisalat, a joint stock company
    IPFilterRule(*parse_ip('37.252.221.0'), 8), # Albania - KORABI-NET SHPK
    IPFilterRule(*parse_ip('37.28.0.0'), 15), # Oman - Omani Qatari Telecommunication Company SAOC
    IPFilterRule(*parse_ip('37.36.0.0'), 18), # Kuwait - Mobile Telecommunications Company K.S.C.P.
    IPFilterRule(*parse_ip('38.156.228.0'), 10), # Colombia - SOMOS NETWORKS COLOMBIA S.A.S. BIC
    IPFilterRule(*parse_ip('38.159.184.0'), 10), # Brazil - INNOVA NET TELECOM EIRELI
    IPFilterRule(*parse_ip('38.187.0.0'), 13), # Peru - NEXTNET SAC
    IPFilterRule(*parse_ip('38.190.126.0'), 9), # Peru - CTV CHICLIN E.I.R.L.
    IPFilterRule(*parse_ip('38.196.152.0'), 10), # Venezuela - Cogent Communications, LLC
    IPFilterRule(*parse_ip('38.196.229.0'), 8), # Brazil - Conectanet Telecom e Informatica Ltda.
    IPFilterRule(*parse_ip('38.210.125.0'), 8), # Brazil - ULTRA INTERNET LTDA
    IPFilterRule(*parse_ip('38.22.164.0'), 10), # Mexico - Cogent Communications, LLC
    IPFilterRule(*parse_ip('38.226.246.0'), 8), # Peru - CABLE ANDINA S.A.C
    IPFilterRule(*parse_ip('38.25.128.0'), 15), # Venezuela - Airtek Solutions C.A.
    IPFilterRule(*parse_ip('38.51.192.0'), 13), # Venezuela - TECNOVEN SERVICES CA
    IPFilterRule(*parse_ip('39.36.0.0'), 18), # Pakistan - Pakistan Telecommunication Company Limited
    IPFilterRule(*parse_ip('43.153.0.0'), 15), # United States - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('43.165.128.0'), 14), # Japan - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('45.96.0.0'), 20), # Egypt - The Egyptian Company for Mobile Services (Mobinil)
    IPFilterRule(*parse_ip('45.144.32.0'), 10), # Moldova - INTERDNESTRKOM, Sovmestnoe Zakrytoe Aktsionernoe Obshchestvo
    IPFilterRule(*parse_ip('45.160.240.0'), 10), # Brazil - Gurisat Gurinet Ltda Me
    IPFilterRule(*parse_ip('45.161.176.0'), 10), # Brazil - CONECTAR TELECOM BANDA LARGA LTDA
    IPFilterRule(*parse_ip('45.161.80.0'), 10), # Brazil - Sinal do Ceu Telecom Comercio e Servicos Ltda
    IPFilterRule(*parse_ip('45.164.76.0'), 10), # Brazil - BCM SERVICOS DE COMUNICACAO E MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('45.165.124.0'), 10), # Brazil - FLL - NETPLACE TELECOM
    IPFilterRule(*parse_ip('45.165.60.0'), 10), # Brazil - ROCHA FIBER FIBRA OPTICA LTDA. - ME
    IPFilterRule(*parse_ip('45.165.96.0'), 10), # Brazil - Conexao Bahia Sul
    IPFilterRule(*parse_ip('45.166.172.0'), 10), # Brazil - J&C PROVEDOR DE INTERNET BANDA LARGA LTDA
    IPFilterRule(*parse_ip('45.166.180.0'), 10), # Brazil - M & R NETWORK LTDA - ME
    IPFilterRule(*parse_ip('45.167.126.0'), 8), # Colombia - SEPCOM COMUNICACIONES SAS
    IPFilterRule(*parse_ip('45.168.228.0'), 10), # Brazil - FRANCONETFIBRA LTDA
    IPFilterRule(*parse_ip('45.169.136.0'), 10), # Brazil - RAFAEL FERNANDES DE MEDEIROS
    IPFilterRule(*parse_ip('45.169.32.0'), 10), # Brazil - NETSTORE TELECOM
    IPFilterRule(*parse_ip('45.170.144.0'), 10), # Brazil - Globalcom Com. e Serv. de Inf. ltda
    IPFilterRule(*parse_ip('45.172.116.0'), 10), # Brazil - NetCaster Solutions
    IPFilterRule(*parse_ip('45.173.104.0'), 10), # Brazil - BRIDGENET LTDA ME
    IPFilterRule(*parse_ip('45.174.152.0'), 10), # Brazil - ROLIM NET TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('45.175.120.0'), 10), # Brazil - ESMILENE GOIS FRANCA - ME
    IPFilterRule(*parse_ip('45.176.44.0'), 10), # Brazil - Ilhas Net LTDA - ME
    IPFilterRule(*parse_ip('45.177.152.0'), 10), # Brazil - VEM PRA UNO PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.177.76.0'), 10), # Brazil - Weclix Telecom S/A
    IPFilterRule(*parse_ip('45.178.200.0'), 10), # Brazil - L 2 COMERCIO E SERVICOS DE INFORMATICA LTDA ME
    IPFilterRule(*parse_ip('45.180.236.0'), 10), # Brazil - Conecte Telecom
    IPFilterRule(*parse_ip('45.182.252.0'), 10), # Brazil - WAGNER JOSE RIBEIRO
    IPFilterRule(*parse_ip('45.184.232.0'), 10), # Brazil - REDES METRO
    IPFilterRule(*parse_ip('45.184.80.0'), 10), # Brazil - D M Gianini & Cia Ltda
    IPFilterRule(*parse_ip('45.186.156.0'), 10), # Brazil - FIBRALINK INTERNET E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.186.0.0'), 10), # Brazil - TECHNET COMUNICACAO MULTIMIDIA LTDA
    IPFilterRule(*parse_ip('45.187.64.0'), 8), # Brazil - T. DE S. ALENCAR
    IPFilterRule(*parse_ip('45.189.68.0'), 10), # Brazil - SPEED JET TELECOM LTDA
    IPFilterRule(*parse_ip('45.190.104.0'), 10), # Brazil - Via Internet Telecomunicacoes LTDA
    IPFilterRule(*parse_ip('45.190.108.0'), 10), # Brazil - Indaiafibra Networking Eireli
    IPFilterRule(*parse_ip('45.190.140.0'), 10), # Brazil - BRASIL DIGITAL SERVIÇOS DE INFORMATICA E COMERCIO
    IPFilterRule(*parse_ip('45.190.68.0'), 10), # Brazil - NETCITY TELECOM LTDA
    IPFilterRule(*parse_ip('45.190.86.0'), 8), # Colombia - NETWORK CONNEXIONS SAS
    IPFilterRule(*parse_ip('45.195.12.0'), 9), # Venezuela - TELECOMUNICACIONES SILVERDATA, C.A.
    IPFilterRule(*parse_ip('45.225.192.0'), 10), # Brazil - IBIUNET MULTIPLAY
    IPFilterRule(*parse_ip('45.226.20.0'), 10), # Brazil - TURBONET WIFI LTDA - ME
    IPFilterRule(*parse_ip('45.228.248.0'), 10), # Brazil - SHIELD TELECOM LTDA
    IPFilterRule(*parse_ip('45.229.144.0'), 10), # Brazil - VOE INTERNET
    IPFilterRule(*parse_ip('45.231.200.0'), 10), # Brazil - Good Net Provedor de Internet Ltda - EPP
    IPFilterRule(*parse_ip('45.233.176.0'), 10), # Brazil - USBINF INFORMATICA LTDA - ME
    IPFilterRule(*parse_ip('45.233.42.0'), 9), # Brazil - live.connection me ltda
    IPFilterRule(*parse_ip('45.234.128.0'), 10), # Brazil - Giga Tecnologia em Redes e Internet LTDA
    IPFilterRule(*parse_ip('45.235.204.0'), 10), # Brazil - CARLA ANDREIA ARAUJO DE OLIVEIRA EIRELI - ME
    IPFilterRule(*parse_ip('45.235.68.0'), 10), # Brazil - FENIX TELECOM
    IPFilterRule(*parse_ip('45.237.24.0'), 10), # Brazil - INNOVA TECNOLOGIA LTDA ME
    IPFilterRule(*parse_ip('45.239.234.0'), 8), # Brazil - SOUSA & RAMOS PRESTADORA DE SERVICOS LTDA
    IPFilterRule(*parse_ip('45.239.44.0'), 10), # Paraguay - SOL TELECOMUNICACIONES S.A.
    IPFilterRule(*parse_ip('45.4.179.0'), 8), # Brazil - YUHOO NET
    IPFilterRule(*parse_ip('45.4.200.0'), 10), # Ecuador - Eliana Vanessa Morocho Oña
    IPFilterRule(*parse_ip('45.5.248.0'), 10), # Brazil - GM Telecom LTDA
    IPFilterRule(*parse_ip('45.5.4.0'), 10), # Brazil - VTX NET TELECOM LTDA
    IPFilterRule(*parse_ip('45.6.140.0'), 10), # Mexico - LUMENET COMUNICACIONES S. DE R.L. DE C.V.
    IPFilterRule(*parse_ip('45.7.0.0'), 10), # Brazil - Voafibra Comunicacao
    IPFilterRule(*parse_ip('45.7.192.0'), 10), # Brazil - REELU NET COMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('45.70.76.0'), 10), # Brazil - HOMENET PROVEDOR
    IPFilterRule(*parse_ip('45.71.12.0'), 10), # Brazil - MILANIN NET
    IPFilterRule(*parse_ip('45.71.28.0'), 10), # Brazil - M3 Net Fibra LTDA - ME
    IPFilterRule(*parse_ip('45.71.44.0'), 10), # Chile - FULL CONECTION LTDA
    IPFilterRule(*parse_ip('46.116.0.0'), 17), # Israel - Cellcom Fixed Line Communication L.P
    IPFilterRule(*parse_ip('46.251.192.0'), 13), # Kyrgyzstan - Alfa Telecom CJSC
    IPFilterRule(*parse_ip('46.29.29.0'), 8), # Venezuela - NETWORK SPEED C.A
    IPFilterRule(*parse_ip('46.55.64.0'), 14), # Moldova - Moldtelecom SA
    IPFilterRule(*parse_ip('46.61.245.0'), 8), # Russia - Miranda-Media Ltd
    IPFilterRule(*parse_ip('49.51.160.0'), 12), # Germany - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('5.141.192.0'), 13), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('5.206.0.0'), 15), # Russia - Intersvyaz-2 JSC
    IPFilterRule(*parse_ip('5.208.0.0'), 19), # Iran - Mobile Communication Company of Iran PLC
    IPFilterRule(*parse_ip('5.32.192.0'), 14), # Oman - OmanTel NAP
    IPFilterRule(*parse_ip('50.46.0.0'), 17), # United States - Wholesail networks LLC
    IPFilterRule(*parse_ip('58.65.216.0'), 11), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('63.143.116.0'), 9), # Jamaica - Digicel Jamaica
    IPFilterRule(*parse_ip('66.102.120.0'), 11), # Pakistan - MTCL (Mansoorah Telecommunications Company Pvt Ltd)
    IPFilterRule(*parse_ip('66.231.68.0'), 8), # Ecuador - SERVICIOS DE TELECOMUNICACIONES ATVCABLE CIA. LTDA.
    IPFilterRule(*parse_ip('72.252.128.0'), 15), # Jamaica - Columbus Networks USA, Inc.
    IPFilterRule(*parse_ip('77.222.96.0'), 13), # Russia - Intersvyaz-2 JSC
    IPFilterRule(*parse_ip('77.69.192.0'), 13), # Bahrain - BEYON B.S.C.
    IPFilterRule(*parse_ip('78.92.0.0'), 15), # Hungary - Magyar Telekom Plc.
    IPFilterRule(*parse_ip('78.96.0.0'), 17), # Romania - Vodafone Romania S.A.
    IPFilterRule(*parse_ip('80.76.63.0'), 8), # Russia - MCS LLC
    IPFilterRule(*parse_ip('80.91.160.0'), 10), # Ukraine - Datagroup PJSC
    IPFilterRule(*parse_ip('82.114.78.0'), 8), # Kosovo - Kujtesa Net Sh.p.k.
    IPFilterRule(*parse_ip('82.76.0.0'), 18), # Romania - DIGI ROMANIA S.A.
    IPFilterRule(*parse_ip('83.137.48.0'), 11), # Russia - Altagen JSC
    IPFilterRule(*parse_ip('83.142.104.0'), 11), # Ukraine - LLC Global-City-Net
    IPFilterRule(*parse_ip('84.1.0.0'), 13), # Hungary - Magyar Telekom Plc.
    IPFilterRule(*parse_ip('84.112.0.0'), 18), # Austria - T-Mobile Austria GmbH
    IPFilterRule(*parse_ip('85.113.208.0'), 12), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('87.238.128.0'), 11), # Jordan - Jordanian mobile phone services Ltd
    IPFilterRule(*parse_ip('89.138.0.0'), 17), # Israel - Cellcom Fixed Line Communication L.P
    IPFilterRule(*parse_ip('89.164.128.0'), 15), # Croatia - Hrvatski Telekom d.d.
    IPFilterRule(*parse_ip('89.238.156.0'), 8), # Canada - M247 Europe SRL
    IPFilterRule(*parse_ip('89.34.68.0'), 10), # Moldova - Moldtelecom SA
    IPFilterRule(*parse_ip('89.43.132.0'), 9), # Syria - High Speed For Internet Services L.L.C
    IPFilterRule(*parse_ip('91.192.180.0'), 10), # Ukraine - Information Technologies private company
    IPFilterRule(*parse_ip('91.198.101.0'), 8), # Kazakhstan - NLS Kazakhstan LLC
    IPFilterRule(*parse_ip('91.220.41.0'), 8), # Iraq - Iraq Al-wataniyah Co. for Telecom Services Ltd.
    IPFilterRule(*parse_ip('91.241.148.0'), 10), # Russia - NEO-TELEKOM Ltd
    IPFilterRule(*parse_ip('92.100.0.0'), 17), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('93.175.32.0'), 13), # Israel - K.M.A ADVANCED TECHNOLOGIES LTD
    IPFilterRule(*parse_ip('94.249.0.0'), 15), # Jordan - Jordan Data Communications Company LLC
    IPFilterRule(*parse_ip('95.139.128.0'), 15), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('95.153.64.0'), 14), # Moldova - INTERDNESTRKOM, Sovmestnoe Zakrytoe Aktsionernoe Obshchestvo
    IPFilterRule(*parse_ip('95.158.0.0'), 14), # Ukraine - Best ISP
    IPFilterRule(*parse_ip('95.159.64.0'), 14), # Iraq - Shabaka Sfn Al-Haditha for General Trading & Information Technology LTD.
    IPFilterRule(*parse_ip('95.167.128.0'), 15), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('95.215.104.0'), 10), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('95.220.0.0'), 17), # Russia - PJSC MegaFon
    IPFilterRule(*parse_ip('95.46.197.0'), 8), # Russia - Technologii svyazi Ltd.
    IPFilterRule(*parse_ip('1.178.208.0'), 12), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('1.22.216.0'), 11), # India - Tikona Infinet Ltd.
    IPFilterRule(*parse_ip('102.140.224.0'), 13), # Kenya - Wananchi Group (Kenya) Limited
    IPFilterRule(*parse_ip('102.206.120.0'), 10), # Ivory Coast - Atlantique Telecom (Cote d'Ivoire)
    IPFilterRule(*parse_ip('102.207.160.0'), 12), # Kenya - Wavex Internet Service Provider LTD
    IPFilterRule(*parse_ip('102.213.132.0'), 10), # South Africa - NET99 (PTY) LTD
    IPFilterRule(*parse_ip('102.36.152.0'), 10), # South Africa - OCTOPI SMART SOLUTIONS (PTY) LTD
    IPFilterRule(*parse_ip('103.106.164.0'), 9), # Bangladesh - Md. Zakir Hossain
    IPFilterRule(*parse_ip('103.111.164.0'), 9), # Bangladesh - REAL STATION BROADBAND
    IPFilterRule(*parse_ip('103.114.166.0'), 8), # Bangladesh - BROTHERS ONLINE
    IPFilterRule(*parse_ip('103.114.20.0'), 10), # Bangladesh - BOL System
    IPFilterRule(*parse_ip('103.121.240.0'), 10), # India - Genstar Network Solutions Pvt Ltd.
    IPFilterRule(*parse_ip('103.127.4.0'), 10), # Bangladesh - Triangle Services Limited.
    IPFilterRule(*parse_ip('103.131.18.0'), 9), # Indonesia - PT.Global Media Data Prima
    IPFilterRule(*parse_ip('103.134.36.0'), 8), # Bangladesh - Internet Factory
    IPFilterRule(*parse_ip('103.135.138.0'), 8), # Bangladesh - EXABYTE LTD
    IPFilterRule(*parse_ip('103.148.108.0'), 8), # Bangladesh - Skyinfo Online
    IPFilterRule(*parse_ip('103.148.74.0'), 9), # Bangladesh - Sinthia Telecom
    IPFilterRule(*parse_ip('103.161.68.0'), 9), # Bangladesh - Digicon Telecommunication Ltd
    IPFilterRule(*parse_ip('103.177.54.0'), 9), # Bangladesh - Quantum Broadband
    IPFilterRule(*parse_ip('103.191.163.0'), 8), # Bangladesh - AKNetworks
    IPFilterRule(*parse_ip('103.202.222.0'), 8), # Bangladesh - Sustainable Development Networking Program
    IPFilterRule(*parse_ip('103.222.255.0'), 8), # Indonesia - PT Iktiar Doa Tawakal
    IPFilterRule(*parse_ip('103.234.200.0'), 10), # Bangladesh - ADN Telecom Ltd.
    IPFilterRule(*parse_ip('103.49.115.0'), 8), # Bangladesh - EARTH TELECOMMUNICATION (Pvt) LTD.
    IPFilterRule(*parse_ip('103.53.162.0'), 9), # Pakistan - FASTTEL BROADBAND (PRIVATE) LIMITED
    IPFilterRule(*parse_ip('103.58.92.0'), 10), # Bangladesh - Metaphor Digital Media
    IPFilterRule(*parse_ip('103.80.80.0'), 10), # Indonesia - PT JARINGANKU SARANA NUSANTARA
    IPFilterRule(*parse_ip('103.82.10.0'), 8), # Bangladesh - EXABYTE LTD
    IPFilterRule(*parse_ip('109.195.16.0'), 12), # Russia - JSC "ER-Telecom Holding"
    IPFilterRule(*parse_ip('109.196.64.0'), 12), # Russia - Trytek LLC
    IPFilterRule(*parse_ip('111.88.84.0'), 10), # Pakistan - Connect Communications
    IPFilterRule(*parse_ip('112.134.0.0'), 17), # Sri Lanka - Sri Lanka Telecom Internet
    IPFilterRule(*parse_ip('114.130.71.0'), 8), # Bangladesh - Mango Teleservices Limited (ISP)
    IPFilterRule(*parse_ip('116.98.224.0'), 13), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('119.160.215.0'), 8), # Pakistan - TELECOMMUNICATION AND TECHNOLOGY MASTERS (PVT.) LIMITED
    IPFilterRule(*parse_ip('119.42.152.0'), 11), # India - GEOCITY NETWORK SOLUTIONS PVT LTD
    IPFilterRule(*parse_ip('124.123.160.0'), 13), # India - Atria Convergence Technologies Ltd.,
    IPFilterRule(*parse_ip('125.212.128.0'), 13), # Vietnam - Viettel Group
    IPFilterRule(*parse_ip('128.201.140.0'), 10), # Brazil - Enoki & Ruiz Ltda - ME
    IPFilterRule(*parse_ip('131.108.76.0'), 10), # Brazil - GLOBOINFO LTDA
    IPFilterRule(*parse_ip('131.72.92.0'), 10), # Brazil - PROVALE SCM LTDA
    IPFilterRule(*parse_ip('138.0.80.0'), 10), # Brazil - NET SET TELECOMUNICAÇÕES LTDA - ME
    IPFilterRule(*parse_ip('138.121.244.0'), 10), # Brazil - OXMAN TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('138.122.88.0'), 10), # Brazil - RazaoInfo Internet Ltda
    IPFilterRule(*parse_ip('138.185.144.0'), 10), # Brazil - CONECTA PROVEDOR DE INTERNET LTDA. - ME
    IPFilterRule(*parse_ip('138.185.172.0'), 10), # Brazil - PROVEDOR DE INTERNET DE ANAPU LTDA - ME
    IPFilterRule(*parse_ip('138.185.16.0'), 10), # Brazil - JN TECNOLOGIA LTDA-ME
    IPFilterRule(*parse_ip('138.185.67.0'), 8), # Venezuela - GALAXY ENTERTAINMENT DE VENEZUELA, S.C.A.
    IPFilterRule(*parse_ip('138.204.8.0'), 10), # Brazil - MEGA PROVEDORES DE INTERNET E COM. DE INFO LTDA ME
    IPFilterRule(*parse_ip('138.255.136.0'), 10), # Brazil - Eagle Redes de Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('138.255.212.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('138.59.120.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('142.147.160.0'), 13), # United States - Web2Objects LLC
    IPFilterRule(*parse_ip('143.202.60.0'), 10), # Brazil - SPEED TURBO TELECOM
    IPFilterRule(*parse_ip('143.255.244.0'), 10), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('148.227.68.0'), 10), # Argentina - Space Exploration Technologies Corporation
    IPFilterRule(*parse_ip('149.255.192.0'), 14), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('149.50.192.0'), 12), # Ecuador - PUNTONET S.A.
    IPFilterRule(*parse_ip('149.78.48.0'), 10), # Argentina - FIBRAZUL INTERNET S.R.L.
    IPFilterRule(*parse_ip('152.172.0.0'), 18), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('152.237.0.0'), 16), # Brazil - V tal
    IPFilterRule(*parse_ip('154.118.192.0'), 13), # Angola - Finstar - Sociedade de Investimento e Participacoes S.A
    IPFilterRule(*parse_ip('154.57.222.0'), 9), # Pakistan - Trans World Enterprise Services (Private) Limited
    IPFilterRule(*parse_ip('156.255.192.0'), 14), # Venezuela - Airtek Solutions C.A.
    IPFilterRule(*parse_ip('157.100.200.0'), 10), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('160.191.83.0'), 8), # Bangladesh - Kloud Technologies Limited
    IPFilterRule(*parse_ip('167.249.188.0'), 10), # Brazil - Henet Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('167.249.64.0'), 10), # Brazil - INET TELECOM E INFORMATICA LTDA
    IPFilterRule(*parse_ip('167.250.44.0'), 10), # Brazil - Inova Fibra
    IPFilterRule(*parse_ip('168.0.80.0'), 10), # Brazil - XINGU TELECOM LTDA
    IPFilterRule(*parse_ip('168.121.96.0'), 10), # Brazil - TRIXNET SERVIÇOS DE TELEINFORMATICA LTDA
    IPFilterRule(*parse_ip('168.195.184.0'), 8), # Argentina - ERGON CABLE S.R.L
    IPFilterRule(*parse_ip('168.195.244.0'), 10), # Brazil - MALTA E CARVALHO LTDA - EPP
    IPFilterRule(*parse_ip('168.197.104.0'), 10), # Brazil - GTBA TELECOM LTDA ME
    IPFilterRule(*parse_ip('168.205.176.0'), 10), # Brazil - Osirnet Info Telecom Ltda.
    IPFilterRule(*parse_ip('170.0.11.0'), 8), # Colombia - GUAJIRANET ISP S.A.S.
    IPFilterRule(*parse_ip('170.231.252.0'), 10), # Brazil - Weclix Telecom S/A
    IPFilterRule(*parse_ip('170.238.172.0'), 10), # Brazil - S.C. RIO TELECOMUNICACOES E INFORMATICA LTDA
    IPFilterRule(*parse_ip('170.238.36.0'), 10), # Brazil - Hilink Comunicações
    IPFilterRule(*parse_ip('170.239.192.0'), 10), # Brazil - Companhia Itabirana Telecomunicações Ltda
    IPFilterRule(*parse_ip('170.239.252.0'), 10), # Brazil - UTOPIANET INFORMATICA E TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('170.246.196.0'), 10), # Brazil - Henet Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('170.246.212.0'), 10), # Brazil - rede banda larga
    IPFilterRule(*parse_ip('170.247.78.0'), 8), # Argentina - CH Sistemas Videla S.R.L.
    IPFilterRule(*parse_ip('170.80.236.0'), 10), # Brazil - RJNET Telecomunicacoes Ltda ME
    IPFilterRule(*parse_ip('170.80.64.0'), 10), # Brazil - BTT TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('170.81.200.0'), 10), # Brazil - Victor.net Telecom Ltda ME
    IPFilterRule(*parse_ip('170.83.152.0'), 10), # Brazil - GSM BAHIA PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('176.122.112.0'), 12), # Ukraine - Ukrainian Telecommunication Group LLC
    IPFilterRule(*parse_ip('177.11.96.0'), 10), # Brazil - IP AMERICA TELECOM LTDA
    IPFilterRule(*parse_ip('177.12.128.0'), 10), # Brazil - G20 Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.137.24.0'), 10), # Brazil - IPGLOBE INTERNET LTDA
    IPFilterRule(*parse_ip('177.137.64.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('177.140.0.0'), 17), # Brazil - Claro NXT Telecomunicacoes Ltda
    IPFilterRule(*parse_ip('177.190.144.0'), 10), # Brazil - MKNETWORK TELECOM LTDA ME
    IPFilterRule(*parse_ip('177.23.32.0'), 11), # Brazil - LPRINT TELECOMUNICAÇÕES E ENGENHARIA LTDA
    IPFilterRule(*parse_ip('177.239.80.0'), 12), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('177.39.160.0'), 11), # Brazil - Defferrari Solucoes em Internet Ltda
    IPFilterRule(*parse_ip('177.40.0.0'), 18), # Brazil - TELEFÔNICA BRASIL S.A
    IPFilterRule(*parse_ip('177.55.128.0'), 12), # Brazil - EVOLUNET PROVEDORA DE INTERNET LTDA PE
    IPFilterRule(*parse_ip('177.70.208.0'), 12), # Brazil - INFRANET INTERNET LTDA.
    IPFilterRule(*parse_ip('177.8.132.0'), 10), # Brazil - JET NETWORK TELECOMUNICAÇÃO LTDA
    IPFilterRule(*parse_ip('177.8.224.0'), 12), # Brazil - ITS TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.84.31.0'), 8), # Brazil - RRNET TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('177.86.48.0'), 11), # Brazil - Fenix Wireless Internet Ltda
    IPFilterRule(*parse_ip('178.165.128.0'), 15), # Austria - ==> TELE2 AUSTRIA <==
    IPFilterRule(*parse_ip('179.0.160.0'), 10), # Brazil - K C TELECOM LTDA
    IPFilterRule(*parse_ip('179.1.192.0'), 14), # Colombia - INTERNEXA S.A. E.S.P
    IPFilterRule(*parse_ip('179.41.0.0'), 16), # Argentina - Telefonica de Argentina
    IPFilterRule(*parse_ip('179.49.202.0'), 9), # Dominican Republic - TELECABLE DOMINICANO, S.A.
    IPFilterRule(*parse_ip('179.50.128.0'), 15), # Costa Rica - Cable Tica
    IPFilterRule(*parse_ip('179.63.12.0'), 10), # Brazil - NEW LINK CONNECT
    IPFilterRule(*parse_ip('181.188.220.0'), 10), # Ecuador - Otecel S.A.
    IPFilterRule(*parse_ip('181.232.160.0'), 10), # Argentina - LUMINET S.A.
    IPFilterRule(*parse_ip('181.232.176.0'), 10), # Brazil - UNAFIBER TELECOM LTDA
    IPFilterRule(*parse_ip('181.237.0.0'), 15), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('181.50.216.0'), 11), # Colombia - Telmex Colombia S.A.
    IPFilterRule(*parse_ip('181.78.0.0'), 12), # Colombia - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('182.252.64.0'), 12), # Bangladesh - Agni Systems Limited
    IPFilterRule(*parse_ip('185.110.104.0'), 10), # Syria - STE PDN Internal AS
    IPFilterRule(*parse_ip('185.128.36.0'), 9), # Iraq - Nawafeth Al-hadhara for Internet and Information Systems Co.,Ltd
    IPFilterRule(*parse_ip('185.217.84.0'), 10), # Lebanon - Smart City SARL
    IPFilterRule(*parse_ip('185.75.224.0'), 10), # Iraq - I.Q Online for Internet Services and Communications LLC
    IPFilterRule(*parse_ip('185.90.100.0'), 10), # Russia - CityLink Ltd
    IPFilterRule(*parse_ip('186.1.160.0'), 13), # Colombia - Dialnet de Colombia S.A. E.S.P.
    IPFilterRule(*parse_ip('186.12.188.0'), 10), # Argentina - Techtel LMDS Comunicaciones Interactivas S.A.
    IPFilterRule(*parse_ip('186.156.0.0'), 16), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('186.169.128.0'), 15), # Colombia - COLOMBIA TELECOMUNICACIONES S.A. ESP BIC
    IPFilterRule(*parse_ip('186.208.64.0'), 12), # Brazil - VELOO NET LTDA
    IPFilterRule(*parse_ip('186.224.48.0'), 12), # Brazil - CONECTA LTDA.
    IPFilterRule(*parse_ip('186.226.112.0'), 12), # Brazil - SCNet Equipamentos de Informática Ltda
    IPFilterRule(*parse_ip('186.227.72.0'), 10), # Brazil - Seanet Telecom Carazinho Eireli
    IPFilterRule(*parse_ip('186.232.192.0'), 11), # Brazil - PROXXIMA TELECOMUNICACOES SA
    IPFilterRule(*parse_ip('186.26.112.0'), 12), # Costa Rica - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('186.96.96.0'), 13), # Colombia - TV AZTECA SUCURSAL COLOMBIA
    IPFilterRule(*parse_ip('187.109.192.0'), 12), # Brazil - ISPX Solucoes em Telecomunicacoes SPE Ltda
    IPFilterRule(*parse_ip('187.153.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.16.176.0'), 12), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('187.168.0.0'), 18), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.184.8.0'), 10), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('187.190.21.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.190.223.0'), 8), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('187.228.128.0'), 15), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.250.224.0'), 13), # Mexico - UNINET
    IPFilterRule(*parse_ip('187.252.248.0'), 10), # Mexico - Cablemas Telecomunicaciones SA de CV
    IPFilterRule(*parse_ip('187.40.0.0'), 15), # Brazil - V tal
    IPFilterRule(*parse_ip('187.44.0.0'), 14), # Brazil - MASTER S/A
    IPFilterRule(*parse_ip('187.61.128.0'), 15), # Brazil - Alares Cabo Servicos de Telecomunicacoes S.A.
    IPFilterRule(*parse_ip('187.62.80.0'), 10), # Brazil - vipfiber telecom LTDA
    IPFilterRule(*parse_ip('188.161.0.0'), 16), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('188.186.64.0'), 14), # Russia - JSC "ER-Telecom Holding"
    IPFilterRule(*parse_ip('188.53.96.0'), 13), # Saudi Arabia - Saudi Telecom Company JSC
    IPFilterRule(*parse_ip('189.106.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('189.133.0.0'), 16), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.138.0.0'), 14), # Mexico - UNINET
    IPFilterRule(*parse_ip('189.194.208.0'), 12), # Mexico - Mega Cable, S.A. de C.V.
    IPFilterRule(*parse_ip('189.203.96.0'), 11), # Mexico - TOTAL PLAY TELECOMUNICACIONES SA DE CV
    IPFilterRule(*parse_ip('189.219.208.0'), 12), # Mexico - Television Internacional, S.A. de C.V.
    IPFilterRule(*parse_ip('189.249.0.0'), 16), # Mexico - unknown
    IPFilterRule(*parse_ip('189.36.244.0'), 10), # Brazil - LD telecom
    IPFilterRule(*parse_ip('189.39.96.0'), 12), # Brazil - PERSIS INTERNET LTDA
    IPFilterRule(*parse_ip('190.108.80.0'), 10), # Peru - INTERNEXA PERU S.A
    IPFilterRule(*parse_ip('190.109.96.0'), 10), # Brazil - SIAT TELECOM INTERNET DEDICADA LTDA
    IPFilterRule(*parse_ip('190.113.96.0'), 13), # Costa Rica - Telecable Economico S.A.
    IPFilterRule(*parse_ip('190.120.244.0'), 10), # Argentina - Cable Televisora Color
    IPFilterRule(*parse_ip('190.154.0.0'), 17), # Ecuador - SERVICIOS DE TELECOMUNICACIONES SETEL S.A. (XTRIM EC)
    IPFilterRule(*parse_ip('190.202.0.0'), 15), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('190.206.0.0'), 15), # Venezuela - CANTV Servicios, Venezuela
    IPFilterRule(*parse_ip('190.40.0.0'), 18), # Peru - Telefonica del Peru S.A.A.
    IPFilterRule(*parse_ip('190.87.160.0'), 10), # El Salvador - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('190.89.29.0'), 8), # Venezuela - CORPORACION FIBEX TELECOM, C.A.
    IPFilterRule(*parse_ip('190.92.192.0'), 13), # Singapore - HUAWEI CLOUDS
    IPFilterRule(*parse_ip('190.95.128.0'), 15), # Ecuador - Telconet S.A
    IPFilterRule(*parse_ip('190.97.0.0'), 14), # Argentina - BVNET S.A.
    IPFilterRule(*parse_ip('190.99.192.0'), 14), # Colombia - EMPRESAS MUNICIPALES DE CALI E.I.C.E. E.S.P.
    IPFilterRule(*parse_ip('191.0.64.0'), 14), # Brazil - V tal
    IPFilterRule(*parse_ip('191.116.0.0'), 16), # Chile - VTR BANDA ANCHA S.A.
    IPFilterRule(*parse_ip('191.120.0.0'), 18), # Brazil - TIM S/A
    IPFilterRule(*parse_ip('191.243.88.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('191.37.172.0'), 10), # Brazil - UNIFIQUE TELECOMUNICACOES S/A
    IPFilterRule(*parse_ip('191.56.0.0'), 19), # Brazil - CLARO S.A.
    IPFilterRule(*parse_ip('192.141.144.0'), 10), # Brazil - NETFLESH TELECOM E COM DE PROD DE INFORMAT LTDA-ME
    IPFilterRule(*parse_ip('193.107.168.0'), 10), # Ukraine - PE UAinet
    IPFilterRule(*parse_ip('195.184.214.28'), 2), # Russia - Timer, LLC
    IPFilterRule(*parse_ip('196.217.0.0'), 15), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('196.250.240.0'), 11), # South Africa - Mitsol (Pty) Ltd
    IPFilterRule(*parse_ip('197.153.0.0'), 16), # Morocco - MEDITELECOM
    IPFilterRule(*parse_ip('197.214.128.0'), 15), # Republic of the Congo - Airtel Congo S.A
    IPFilterRule(*parse_ip('198.12.40.0'), 9), # Argentina - ARLINK S.A.
    IPFilterRule(*parse_ip('2.190.0.0'), 17), # Iran - Iran Telecommunication Company PJS
    IPFilterRule(*parse_ip('200.112.0.0'), 15), # Chile - TELEFÓNICA CHILE S.A.
    IPFilterRule(*parse_ip('200.180.0.0'), 17), # Brazil - V tal
    IPFilterRule(*parse_ip('200.219.64.0'), 14), # Brazil - V tal
    IPFilterRule(*parse_ip('200.225.160.0'), 13), # Brazil - V tal
    IPFilterRule(*parse_ip('200.233.40.0'), 10), # Argentina - TELESMART S.A
    IPFilterRule(*parse_ip('200.24.133.0'), 8), # Ecuador - SERVITRACTOR S.A.
    IPFilterRule(*parse_ip('200.6.192.0'), 14), # Guatemala - TELECOMUNICACIONES DE GUATEMALA, SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('200.71.120.0'), 10), # Brazil - Forza Telecomunicações LTDA
    IPFilterRule(*parse_ip('200.82.128.0'), 15), # Venezuela - Corporación Telemic C.A.
    IPFilterRule(*parse_ip('201.148.0.0'), 14), # Mexico - Operbes, S.A. de C.V.
    IPFilterRule(*parse_ip('201.157.252.0'), 10), # Brazil - TASCOM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('201.159.116.0'), 10), # Brazil - Flash Net Brasil Telecom Ltda - EPP
    IPFilterRule(*parse_ip('201.190.174.0'), 9), # Argentina - ARLINK S.A.
    IPFilterRule(*parse_ip('201.221.112.0'), 10), # Venezuela - CABLE NORTE CA.
    IPFilterRule(*parse_ip('201.222.28.0'), 10), # Brazil - NETWISE INFORMATICA LTDA
    IPFilterRule(*parse_ip('201.240.0.0'), 16), # Peru - Telefonica del Peru S.A.A.
    IPFilterRule(*parse_ip('201.253.0.0'), 16), # Argentina - Telecom Argentina S.A.
    IPFilterRule(*parse_ip('201.49.64.0'), 13), # Brazil - VERO S.A
    IPFilterRule(*parse_ip('202.12.123.0'), 8), # Bangladesh - Seven Stars Hospital & Diagnostic Center
    IPFilterRule(*parse_ip('203.78.144.0'), 10), # Bangladesh - SPEED TECH ONLINE
    IPFilterRule(*parse_ip('205.164.248.0'), 10), # Brazil - mega ip connect
    IPFilterRule(*parse_ip('206.85.1.0'), 8), # Dominican Republic - LAUAM MEGARED TELECOM, S.R.L.
    IPFilterRule(*parse_ip('212.49.64.0'), 13), # Kenya - Kenyan Post & Telecommunications Company / Telkom Kenya Ltd
    IPFilterRule(*parse_ip('213.142.96.0'), 13), # Austria - T-Mobile Austria GmbH
    IPFilterRule(*parse_ip('213.204.112.0'), 12), # Lebanon - TerraNet sal
    IPFilterRule(*parse_ip('213.244.64.0'), 13), # Palestinian Territory - PALTEL Autonomous System
    IPFilterRule(*parse_ip('222.255.224.0'), 11), # Vietnam - VNPT Corp
    IPFilterRule(*parse_ip('223.184.128.0'), 15), # India - Bharti Airtel Ltd. AS for GPRS Service
    IPFilterRule(*parse_ip('31.28.192.0'), 13), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('37.111.216.0'), 11), # Bangladesh - GrameenPhone Ltd.
    IPFilterRule(*parse_ip('37.237.248.0'), 11), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.237.64.0'), 14), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.239.160.0'), 12), # Iraq - Hulum Almustakbal Company for Communication Engineering and Services Ltd
    IPFilterRule(*parse_ip('37.46.96.0'), 10), # Kazakhstan - X-COMMUNICATION LLP
    IPFilterRule(*parse_ip('38.154.143.0'), 8), # United States - B2 Net Solutions Inc.
    IPFilterRule(*parse_ip('38.172.160.0'), 12), # Venezuela - RED SERVITEL, CA
    IPFilterRule(*parse_ip('38.183.0.0'), 14), # India - Netplus Broadband Services Private Limited
    IPFilterRule(*parse_ip('38.25.0.0'), 15), # Peru - WI-NET TELECOM S.A.C.
    IPFilterRule(*parse_ip('38.41.196.0'), 10), # Brazil - Nicnet S.A.
    IPFilterRule(*parse_ip('38.43.104.0'), 10), # Brazil - OLLA COMUNICACAO LTDA
    IPFilterRule(*parse_ip('38.43.192.0'), 14), # Venezuela - FULL DATA COMUNICACIONES C.A.
    IPFilterRule(*parse_ip('38.51.232.0'), 10), # Colombia - SP SISTEMAS PALACIOS LTDA
    IPFilterRule(*parse_ip('38.80.12.0'), 9), # Dominican Republic - ANTHONELY TECNOLOGY SYSTEM SRL
    IPFilterRule(*parse_ip('41.10.0.0'), 16), # South Africa - Vodacom
    IPFilterRule(*parse_ip('41.121.0.0'), 15), # South Africa - MTN SA
    IPFilterRule(*parse_ip('41.142.0.0'), 15), # Morocco - Office National des Postes et Telecommunications ONPT (Maroc Telecom) / IAM
    IPFilterRule(*parse_ip('41.220.112.0'), 12), # Kenya - ACCESSKENYA GROUP LTD is an ISP serving
    IPFilterRule(*parse_ip('41.90.8.0'), 11), # Kenya - Safaricom Limited
    IPFilterRule(*parse_ip('43.130.128.0'), 14), # United States - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('43.135.128.0'), 14), # United States - Tencent Building, Kejizhongyi Avenue
    IPFilterRule(*parse_ip('45.130.244.0'), 10), # Ukraine - BREEZE NETWORK
    IPFilterRule(*parse_ip('45.132.99.0'), 8), # Indonesia - Elisteka UAB
    IPFilterRule(*parse_ip('45.161.52.0'), 10), # Brazil - AC TELECOM - PROVEDOR DE INTERNET
    IPFilterRule(*parse_ip('45.161.72.0'), 10), # Brazil - SL Telecomunicações EIRELI
    IPFilterRule(*parse_ip('45.163.0.0'), 10), # Brazil - DBUG TELECOM LTDA
    IPFilterRule(*parse_ip('45.163.204.0'), 10), # Ecuador - VISIONMAGICA SOCIEDAD ANONIMA
    IPFilterRule(*parse_ip('45.170.196.0'), 10), # Brazil - Meganet Tecnologia LTDA
    IPFilterRule(*parse_ip('45.171.4.0'), 10), # Brazil - AIRMAR TELECOM
    IPFilterRule(*parse_ip('45.172.184.0'), 9), # Colombia - BETEL SOLUCIONES S.A.S
    IPFilterRule(*parse_ip('45.172.40.0'), 10), # Brazil - cinthia cristina da silva
    IPFilterRule(*parse_ip('45.173.136.0'), 10), # Brazil - Freitas Sistema de Comunicação Internet Eireli-ME
    IPFilterRule(*parse_ip('45.175.232.0'), 10), # Mexico - INBTEL SA DE CV
    IPFilterRule(*parse_ip('45.182.176.0'), 10), # Brazil - EVOLUCAO TELECOM LTDA
    IPFilterRule(*parse_ip('45.184.68.0'), 10), # Brazil - CANAA TELECOMUNICAÇÕES LTDA - ME
    IPFilterRule(*parse_ip('45.186.88.0'), 10), # Brazil - PONTOCOM SOLUÇÕES EM TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('45.187.224.0'), 10), # Brazil - BRLOGNET TELECOMUNICACOES LTDA
    IPFilterRule(*parse_ip('45.188.76.0'), 10), # Mexico - ONT NETWORKS SA de CV
    IPFilterRule(*parse_ip('45.190.200.0'), 10), # Brazil - ARK TELECOM LTDA - ME
    IPFilterRule(*parse_ip('45.224.96.0'), 10), # Ecuador - UFINET PANAMA S.A.
    IPFilterRule(*parse_ip('45.225.236.0'), 10), # Brazil - DIRECT INTERNET LTDA
    IPFilterRule(*parse_ip('45.226.116.0'), 10), # Brazil - GIGA MAIS FIBRA TELECOMUNICACOES S.A.
    IPFilterRule(*parse_ip('45.227.116.0'), 10), # Brazil - Virtual Internet
    IPFilterRule(*parse_ip('45.227.43.0'), 8), # Brazil - CONEXT TELECOMUNICAÇOES LTDA
    IPFilterRule(*parse_ip('45.229.132.0'), 10), # Brazil - NET FORT Telecom
    IPFilterRule(*parse_ip('45.232.88.0'), 10), # Brazil - AZZA TELECOM SERVIÇOS EM TELECOMUNICAÇÕES LTDA
    IPFilterRule(*parse_ip('45.234.104.0'), 10), # Brazil - Livenet telecom
    IPFilterRule(*parse_ip('45.234.28.0'), 10), # Brazil - BRASILIANET PROVEDOR DE INTERNET LTDA
    IPFilterRule(*parse_ip('45.236.152.0'), 10), # Brazil - FIBRANET BRASIL
    IPFilterRule(*parse_ip('45.239.252.0'), 10), # Brazil - LM SISTEMAS LTDA
    IPFilterRule(*parse_ip('45.65.204.0'), 10), # Brazil - GLINK TECNOLOGIA LTDA
    IPFilterRule(*parse_ip('45.70.224.0'), 10), # Brazil - FIBRATECH INTERNET DE ALTA VELOCIDADE LTDA ME
    IPFilterRule(*parse_ip('45.71.216.0'), 10), # Brazil - SGV TI E TELECOM LTDA
    IPFilterRule(*parse_ip('46.174.112.0'), 11), # Russia - Kvartal Plus Ltd
    IPFilterRule(*parse_ip('46.20.100.0'), 8), # Lebanon - Elie Achkar trading as FiberSkynet
    IPFilterRule(*parse_ip('46.53.224.0'), 13), # Belarus - Unitary enterprise A1
    IPFilterRule(*parse_ip('46.60.0.0'), 12), # Palestinian Territory - AL Zaytona Company For Communication Ltd.
    IPFilterRule(*parse_ip('5.74.0.0'), 16), # Iran - Iran Telecommunication Company PJS
    IPFilterRule(*parse_ip('5.79.128.0'), 15), # Russia - Intersvyaz-2 JSC
    IPFilterRule(*parse_ip('5.8.128.0'), 13), # Lebanon - SODETEL S.A.L.
    IPFilterRule(*parse_ip('54.254.0.0'), 17), # Singapore - Amazon.com, Inc.
    IPFilterRule(*parse_ip('59.152.0.0'), 11), # Bangladesh - Banglalink Digital Communications Ltd
    IPFilterRule(*parse_ip('62.201.240.0'), 11), # Iraq - IQ Networks for Data and Internet Services Ltd
    IPFilterRule(*parse_ip('63.143.88.0'), 11), # Jamaica - Digicel Jamaica
    IPFilterRule(*parse_ip('72.255.58.0'), 9), # Pakistan - Cyber Internet Services (Pvt) Ltd.
    IPFilterRule(*parse_ip('77.222.152.0'), 11), # Ukraine - Datagroup Retail
    IPFilterRule(*parse_ip('77.235.128.0'), 13), # Lebanon - Broadband Plus S.a.l.
    IPFilterRule(*parse_ip('77.28.0.0'), 17), # North Macedonia - Makedonski Telekom AD-Skopje
    IPFilterRule(*parse_ip('77.77.0.0'), 13), # Bulgaria - UltraNET Ltd
    IPFilterRule(*parse_ip('81.196.128.0'), 15), # Romania - DIGI ROMANIA S.A.
    IPFilterRule(*parse_ip('81.88.144.0'), 12), # Kazakhstan - JSC Alma Telecommunications
    IPFilterRule(*parse_ip('82.208.64.0'), 14), # Russia - PJSC Rostelecom
    IPFilterRule(*parse_ip('82.215.96.0'), 12), # Uzbekistan - Turon Media XK
    IPFilterRule(*parse_ip('82.86.128.0'), 13), # Venezuela - THUNDERNET, C.A.
    IPFilterRule(*parse_ip('85.250.0.0'), 16), # Israel - Cellcom Fixed Line Communication L.P
    IPFilterRule(*parse_ip('87.200.0.0'), 17), # United Arab Emirates - Emirates Integrated Telecommunications Company PJSC
    IPFilterRule(*parse_ip('89.232.4.0'), 10), # Georgia - Georgianairlink LLC
    IPFilterRule(*parse_ip('91.106.48.0'), 12), # Iraq - Hala Al Rafidain Company for Communications and Internet LTD.
    IPFilterRule(*parse_ip('91.188.128.0'), 13), # Uzbekistan - ARS-INFORM LLC
    IPFilterRule(*parse_ip('92.241.32.0'), 13), # Jordan - Batelco Jordan
    IPFilterRule(*parse_ip('92.53.0.0'), 14), # North Macedonia - Company for communications services A1 Makedonija DOOEL Skopje
    IPFilterRule(*parse_ip('93.118.128.0'), 13), # Iran - Iran Telecommunication Company PJS
    IPFilterRule(*parse_ip('94.178.0.0'), 17), # Ukraine - JSC "Ukrtelecom"
    IPFilterRule(*parse_ip('95.87.64.0'), 11), # Kyrgyzstan - NUR Telecom LLC

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
