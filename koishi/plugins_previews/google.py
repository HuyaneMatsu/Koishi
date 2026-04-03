from time import monotonic


from hata import KOKORO, Embed, Color
from hata.ext.plugin_loader import require
from hata.ext.slash.menus import Pagination
from scarletio import Lock

from config import GOOGLE_API_KEYS

from ..bot_utils.constants import GUILD__SUPPORT
from ..bots import FEATURE_CLIENTS, MAIN_CLIENT


require(GOOGLE_API_KEYS = list)


GOOGLE_FAVICON = 'https://image.flaticon.com/teams/slug/google.jpg'
API_URL = 'https://www.googleapis.com/customsearch/v1'

HTTP_CLIENT = MAIN_CLIENT.http

class ApiKeyTracker:
    __slots__ = ('api_key', 'lock', 'rate_limited', 'reset_at', )
    def __init__(self, api_key):
        self.api_key = api_key
        self.reset_at = 0.0
        self.rate_limited = False
        self.lock = Lock(KOKORO)
        
    def request_done(self, rate_limited):
        now = monotonic()
        if now < self.reset_at:
            self.reset_at = now + 86400.0
        
        if rate_limited:
            self.rate_limited = rate_limited
    
    def can_do_request(self):
        now = monotonic()
        if now < self.reset_at:
            return False
        
        if self.rate_limited:
            self.rate_limited = False
        
        return True


API_KEY_TRACKERS = [ApiKeyTracker(api_key) for api_key in GOOGLE_API_KEYS]

async def search(query, safe_search = True, image_search = False):
    for api_key_tracker in API_KEY_TRACKERS:
        if api_key_tracker.can_do_request():
            async with api_key_tracker.lock:
                query = {
                    'key': api_key_tracker.api_key,
                    'cx': '015786823554162166929:szgrbbrrox0' if image_search else '015786823554162166929:mywctwj8es4',
                    'q': query,
                    'safe': 'active' if safe_search else 'off',
                }
                if image_search:
                    query['searchType'] = 'image'
                
                async with HTTP_CLIENT.get(API_URL, query = query) as response:
                    response_data = await response.json()
                
                api_error = response_data.get('error', None)
                if api_error is None:
                    result = create_search_results(response_data, image_search)
                    rate_limited = False
                else:
                    result = None
                    
                    api_errors = api_error.get('errors', None)
                    if (api_errors is None) or (not api_errors):
                        error_message = 'Unknown api error occurred.'
                        rate_limited = False
                    else:
                        first_error_message = api_errors[0]
                        first_error_message_domain = first_error_message.get('domain', None)
                        if (first_error_message_domain is not None) and (first_error_message_domain == 'usageLimits'):
                            error_message = None
                            rate_limited = True
                        else:
                            error_message = ', '.join(sub_api_error['message'] for sub_api_error in api_errors)
                            rate_limited = False
                
                api_key_tracker.request_done(rate_limited)
                
                if (result is None):
                    return False, error_message
                else:
                    return True, result
        
        
        return False, 'Rate limited, please try again later.'

class SearchResult:
    def __new__(cls, title, description, url, image_url):
        self = object.__new__(cls)
        self.title = title
        self.description = description
        self.url = url
        self.image_url = image_url
        return self

def create_search_results(data, image_search):
    results = []
    
    try:
        items = data['items']
    except KeyError:
        pass
    else:
        for item in items:
            title = item.get('title', None)
            description = item.get('snippet', None)
            if (description is not None):
                description = description.replace('\n', '')
            
            if image_search:
                image_url = item['link']
                try:
                    url = item['image']['contextLink']
                except KeyError:
                    url = image_url
            else:
                url = item['link']
                page_map = item.get('pagemap', None)
                if (page_map is None):
                    image_url = GOOGLE_FAVICON
                else:
                    while True:
                        image_datas = page_map.get('cse_image', None)
                        
                        if (image_datas is not None) and image_datas:
                            image_data = image_datas[0]
                            try:
                                image_url = image_data['src']
                            except KeyError:
                                pass
                            else:
                                if not image_url.startswith('x-raw-image'):
                                    break
                        
                        thumbnail_datas = page_map.get('cse_thumbnail', None)
                        if (thumbnail_datas is not None) and thumbnail_datas:
                            thumbnail_data = thumbnail_datas[0]
                            try:
                                image_url = thumbnail_data['src']
                            except KeyError:
                                pass
                            else:
                                break
                        
                        image_url = GOOGLE_FAVICON
                        break
            
            result = SearchResult(title, description, url, image_url)
            results.append(result)
    
    return results


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT)
async def google(client, event, query:(str, 'query')):
    yield
    
    success, result_or_error_message = await search(query)
    if not success:
        yield result_or_error_message
    
    pages = []
    
    limit = len(result_or_error_message)
    if limit:
        index = 0
        
        while index < limit:
            result = result_or_error_message[index]
            index += 1
            
            page_embed = Embed(
                result.title,
                result.description,
                color = Color.random(),
                url = result.url,
            ).add_footer(
                f'Page {index}/{limit}',
                client.avatar_url,
            )
            
            image_url = result.image_url
            if (image_url is not None):
                page_embed.add_thumbnail(image_url)
            
            pages.append(page_embed)
    else:
        embed = Embed(query, '*no result*')
        pages.append(embed)
    
    await Pagination(client, event, pages)
