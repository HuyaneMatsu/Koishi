from html import escape as html_escape
from scarletio.web_common import quote

class HttpText:
    __slots__ = ('value', )
    
    def __new__(cls, value):
        self = object.__new__(cls)
        self.value = value
        return self
    
    def render(self):
        return html_escape(self.value)

class HttpUrl:
    __slots__ = ('value', 'url')
    
    def __new__(cls, value, url):
        self = object.__new__(cls)
        self.value = value
        self.url = url
        return self
    
    def render(self):
        url = quote(self.url, safe=':@', protected='/')
        value = html_escape(self.value)
        
        return f'<a href="{url}">{value}</a>'


class HttpContent:
    __slots__ = ('parts',)
    def __new__(cls, *parts):
        self = object.__new__(cls)
        self.parts = parts
        return self
    
    def render(self):
        return ''.join(part.render() for part in self.parts)
