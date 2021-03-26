# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime

from hata import Client, LOOP_TIME, Lock, imultidict, KOKORO, istr, Future, Embed
from hata.discord.http import LIB_USER_AGENT
from hata.backend.headers import USER_AGENT, DATE
from hata.discord.rate_limit import parse_date_to_datetime
from hata.backend.quote import quote
from hata.ext.slash import abort

from bot_utils.shared import GUILD__NEKO_DUNGEON

SLASH_CLIENT : Client

GITHUB_HEADERS = imultidict()
GITHUB_HEADERS[USER_AGENT] = LIB_USER_AGENT

GITHUB_HEADER_RATE_LIMIT_REMAINING = istr('x-ratelimit-remaining')
GITHUB_HEADER_RATE_LIMIT_RESET_AT = istr('x-ratelimit-reset')

class GitHubQueryLimit(object):
    __slots__ = ('rate_limit_reset_at', 'lock')
    def __init__(self):
        self.rate_limit_reset_at = 0.0
        self.lock = Lock(KOKORO)
    
    def is_active(self):
        return (self.rate_limit_reset_at > LOOP_TIME())
    
    def set(self, headers):
        if headers.get(GITHUB_HEADER_RATE_LIMIT_REMAINING, '') == '0':
            now = parse_date_to_datetime(headers[DATE]).timestamp()
            reset = int(headers[GITHUB_HEADER_RATE_LIMIT_RESET_AT])
            self.rate_limit_reset_at = LOOP_TIME() + float(reset-now)

class GitHubQuery(object):
    __slots__ = ('active', 'limit', 'http', 'query_builder', 'cache', 'object_type')
    def __new__(cls, query_builder, http, object_type, limit=None):
        if limit is None:
            limit = GitHubQueryLimit()
        
        self = object.__new__(cls)
        self.active = {}
        self.limit = limit
        self.query_builder = query_builder
        self.http = http
        self.cache = OrderedDict()
        self.object_type = object_type
        return self
    
    async def __call__(self, key):
        cache = self.cache
        try:
            result = cache[key]
        except KeyError:
            pass
        else:
            cache.move_to_end(key)
            return result, False
        
        if self.limit.is_active():
            return None, True
        
        quoted_key = quote(key)
        
        active = self.active
        try:
            waiters = active[key]
        except KeyError:
            pass
        else:
            waiter = Future(KOKORO)
            waiters.append(waiter)
            return await waiter
        
        waiters = []
        active[key] = waiters
        
        try:
            async with self.limit.lock:
                # Check time again, because we may become limited when we get here.
                if self.limit.is_active():
                    result = None
                    limited = True
                else:
                    
                    url = self.query_builder(quoted_key)
                    async with self.http.get(url, headers=GITHUB_HEADERS) as response:
                        self.limit.set(response.headers)
                        if response.status in (200, 404):
                            result_data = await response.json()
                        else:
                            result_data = None
                    
                    result = self.object_type(result_data)
                    if len(cache) == 1000:
                        del cache[next(iter(cache))]
                    
                    cache[key] = result
                    limited = False
        
        except BaseException as err:
            try:
                del active[key]
            except KeyError:
                pass
            else:
                for waiter in waiters:
                    waiter.set_exception_if_pending(err)
            
            raise err
        
        else:
            try:
                del active[key]
            except KeyError:
                pass
            else:
                for waiter in waiters:
                    waiter.set_result_if_pending((result, limited))
            
            return result, limited


def build_search_user_url(key):
    return f'https://api.github.com/search/users?q={key}&per_page=20'

def build_get_user_url(key):
    return f'https://api.github.com/users/{key}'

def build_get_organizations_url(key):
    return f'https://api.github.com/users/{key}/orgs'


class SearchUserType(object):
    __slots__ = ('names', 'total_count')
    def __new__(cls, data):
        names = []
        for partial_user_data in data['items']:
            name = partial_user_data['login']
            
            names.append(name)
        
        total_count = data['total_count']
        
        self = object.__new__(cls)
        self.names = names
        self.total_count = total_count
        return self
    
    def render_description_to(self, extend):
        names = self.names
        limit = len(names)
        if limit:
            index = 0
            while True:
                name = names[index]
                index += 1
                extend.append(repr(index))
                extend.append('.: [')
                extend.append(name)
                extend.append('](https://github.com/')
                extend.append(quote(name))
                extend.append(')')
                
                if index == limit:
                    break
                
                extend.append('\n')
        
        return extend

class UserType(object):
    __slots__ = ('user_name', 'nick_name', 'avatar_url', 'created_at', 'reference_url', 'follower_count',
        'repo_count', 'gist_count', 'bio', 'following_count', 'company', 'location', 'twitter_user_name', 'blog_name',
        'blog_link', 'has_extra_fields', )
    
    def __new__(cls, data):
        user_name = data['login']
        nick_name = data['name']
        avatar_url = data['avatar_url']
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        reference_url = data['html_url']
        follower_count = data['followers']
        repo_count = data['public_repos']
        gist_count = data['public_gists']
        bio = data['bio']
        following_count = data['following']
        
        company = data['company']
        location = data['location']
        twitter_user_name = data['twitter_username']
        blog_name = data['blog']
        if blog_name.startswith('http'):
            blog_link = blog_name
        elif blog_name:
            blog_link = f'https://{blog_name}'
        else:
            blog_link = None
            blog_name = None
        
        if (company is not None) or (location is not None) or (twitter_user_name is not None) \
                or (blog_name is not None):
            has_extra_fields = True
        else:
            has_extra_fields = False
        
        self = object.__new__(cls)
        self.nick_name = nick_name
        self.user_name = user_name
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.reference_url = reference_url
        self.follower_count = follower_count
        self.repo_count = repo_count
        self.gist_count = gist_count
        self.bio = bio
        self.following_count = following_count
        
        self.company = company
        self.location = location
        self.twitter_user_name = twitter_user_name
        self.blog_name = blog_name
        self.blog_link = blog_link
        self.has_extra_fields = has_extra_fields
        
        return self
    
    def render_title_to(self, extend):
        nick_name = self.nick_name
        user_name = self.user_name
        
        if nick_name is None:
            extend.append(user_name)
        else:
            extend.append(nick_name)
            extend.append(' (')
            extend.append(user_name)
            extend.append(')')
        
        return extend
    
    def render_description_to(self, extend):
        bio = self.bio
        if (bio is not None):
            extend.append('```\n')
            extend.append(bio)
            extend.append('\n```\n')
        
        quoted_name = quote(self.user_name)
        
        extend.append('Followers: [')
        extend.append(repr(self.follower_count))
        extend.append('](https://github.com/')
        extend.append(quoted_name)
        extend.append('?tab=followers)\n'
                      'Following: [')
        extend.append(repr(self.following_count))
        extend.append('](https://github.com/')
        extend.append(quoted_name)
        extend.append('?tab=following)\n'
                      'Repositories: [')
        extend.append(repr(self.repo_count))
        extend.append('](https://github.com/')
        extend.append(quoted_name)
        extend.append('?tab=following)\n'
                                 'Gists: [')
        extend.append(repr(self.gist_count))
        extend.append('](https://gist.github.com/')
        extend.append(quoted_name)
        extend.append(')')
        
        if self.has_extra_fields:
            extend.append('\n')
            company = self.company
            if (company is not None):
                extend.append('\nCompany: ')
                extend.append(company)
            
            location = self.location
            if (location is not None):
                extend.append('\nLocation: ')
                extend.append(location)
            
            twitter_user_name = self.twitter_user_name
            if (twitter_user_name is not None):
                extend.append('\nTwitter: @')
                extend.append(twitter_user_name)
            
            blog_name = self.blog_name
            if (blog_name is not None):
                blog_link = self.blog_link
                extend.append('\nBlog: [')
                extend.append(blog_name)
                extend.append('](')
                extend.append(blog_link)
                extend.append(')')
        
        return extend
    
ORGANIZATION_LIMIT = 6

class Organization(object):
    __slots__ = ('name', 'description')
    def __new__(cls, data):
        name = data['login']
        description = data['description']
        if len(description) > 100:
            description = description[:100] + ' ...'
        
        self = object.__new__(cls)
        self.name = name
        self.description = description
        
        return self

class OrganizationContainerType(object):
    __slots__ = ('organizations', 'truncated')
    def __new__(cls, data):
        if (data is None) or (not data):
            organizations = None
            truncated = None
        else:
            organization_count = len(data)
            if organization_count > 6:
                truncated = 6-organization_count
                data = data[:6]
            else:
                truncated = 0
            
            organizations = []
            for organization_data in data:
                organizations.append(Organization(organization_data))
        
        self = object.__new__(cls)
        self.organizations = organizations
        self.truncated = truncated
        return self
    
    def render_description_to(self, extend):
        organizations = self.organizations
        if organizations is None:
            return
        
        extend.append('\n\n**Organizations:**\n')
        for organization in organizations:
            organization_name = organization.name
            extend.append('[')
            extend.append(organization_name)
            extend.append('](https://github.com/')
            extend.append(quote(organization_name))
            extend.append(')')
            
            organization_description = organization.description
            if (organization_description is not None):
                if len(organization_description) > 100:
                    organization_description = organization_description[:100] + ' ...'
                
                extend.append(': ')
                extend.append(organization_description)
            
            extend.append('\n')
        
        truncated = self.truncated
        if truncated:
            extend.append('*')
            extend.append(repr(truncated))
            extend.append(' truncated*')
        else:
            del extend[-1]
        
        return extend

GET_USER_AND_ORGANIZATIONS_LIMIT = GitHubQueryLimit()
SEARCH_USER_NAME = GitHubQuery(build_search_user_url, SLASH_CLIENT.http, SearchUserType)
GET_USER = GitHubQuery(build_get_user_url, SLASH_CLIENT.http, UserType, limit=GET_USER_AND_ORGANIZATIONS_LIMIT)
GET_ORGANIZATIONS = GitHubQuery(build_get_organizations_url, SLASH_CLIENT.http, OrganizationContainerType,
    limit=GET_USER_AND_ORGANIZATIONS_LIMIT)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def github_profile(client, event,
        user: ('str', 'The user\'s name to get'),
            ):
    """Gets the user's guild profile."""
    guild = event.guild
    if (guild is None) or (guild not in client.guild_profiles):
        abort('The command unavailable in guilds, where the application\'s bot is not in.')
    
    if not user:
        abort('User parameter cannot be empty.')
    
    yield
    
    # Was the user requested recently?
    user_search, rate_limited = await SEARCH_USER_NAME(user)
    if rate_limited:
        abort('We are being rate limited, please try again later!')
    
    names = user_search.names
    if not names:
        abort('No user matched the given name.')
    
    if user == names[0]:
        name = user
    elif len(names) == 1:
        name = names[0]
    else:
        yield Embed('Multiple matches', ''.join(user_search.render_description_to([]))) \
            .add_footer(f'Total: {user_search.total_count}')
        return
    
    user_object, rate_limited = await GET_USER(name)
    if rate_limited:
        abort('We are being rate limited, please try again later!')
    
    organization_container, rate_limited = await GET_ORGANIZATIONS(name)
    if rate_limited:
        abort('We are being rate limited, please try again later!')
    
    description_parts = []
    user_object.render_description_to(description_parts)
    organization_container.render_description_to(description_parts)
    description = ''.join(description_parts)
    
    title = ''.join(user_object.render_title_to([]))
    yield Embed(title, description).add_thumbnail(user_object.avatar_url)
    
    return
