__all__ = ()

import re

from hata import Permission
from hata.ext.slash import abort, InteractionResponse

from ..bot_utils.constants import GUILD__SUPPORT
from ..bots import FEATURE_CLIENTS


SPACE_RP = re.compile('[ \t]+')
IDENTIFIER_RP = re.compile('[_a-zA-Z][_a-zA-Z0-9]*')

OPERATOR_ESCAPE = '\\'
OPERATOR_PARENTHESES_OPEN = '('
OPERATOR_PARENTHESES_CLOSE = ')'
OPERATOR_ATTRIBUTE_ACCESS = '.'
OPERATOR_LINE_BREAK = '\n'
OPERATOR_COMMA = ','
OPERATOR_STAR = '*'

TOKEN_TYPE_SPACE = 0
TOKEN_TYPE_ESCAPE = 1
TOKEN_TYPE_PARENTHESES_OPEN = 2
TOKEN_TYPE_PARENTHESES_CLOSE = 3
TOKEN_TYPE_ATTRIBUTE_ACCESS = 4
TOKEN_TYPE_LINE_BREAK = 5
TOKEN_TYPE_EOF = 6
TOKEN_TYPE_IDENTIFIER = 7
TOKEN_TYPE_KEYWORD_FROM = 8
TOKEN_TYPE_KEYWORD_IMPORT = 9
TOKEN_TYPE_KEYWORD_AS = 10
TOKEN_TYPE_THE_UNKNOWN = 11
TOKEN_TYPE_COMMA = 12
TOKEN_TYPE_STAR = 13

LINE_LENGTH_MAX = 120
INDENT_LENGTH = 4
INDENT = ' ' * INDENT_LENGTH


KEYWORD_MAP = {
    'from': TOKEN_TYPE_KEYWORD_FROM,
    'import': TOKEN_TYPE_KEYWORD_IMPORT,
    'as': TOKEN_TYPE_KEYWORD_AS,
}

TOKEN_GROUP_TYPE_IDENTIFIER = 101
TOKEN_GROUP_TYPE_LISTING = 102
TOKEN_GROUP_TYPE_KEYWORD_AS = 103
TOKEN_GROUP_TYPE_LISTING_ELEMENT = 104

class TokenBase:
    __slots__ = ('type',)
    
    def __new__(cls, type_):
        self = object.__new__(cls)
        self.type = type_
        return self
    
    def get_start(self):
        return 0
    
    def get_end(self):
        return 0
    
    def _cursed_repr_builder(self):
        repr_parts = ['<', self.__class__.__name__, ' type = ', repr(get_token_name(self.type))]
        yield repr_parts
        repr_parts.append('>')
    
    
    def __repr__(self):
        for repr_parts in self._cursed_repr_builder():
            pass
        
        return ''.join(repr_parts)


class Token(TokenBase):
    __slots__ = ('start_position', 'length')
    
    def __new__(cls, type_, start_position, length):
        self = TokenBase.__new__(cls, type_)
        self.start_position = start_position
        self.length = length
        return self
    
    def get_start(self):
        return self.start_position
    
    def get_end(self):
        return self.start_position + self.length
    
    def __repr__(self):
        for repr_parts in self._cursed_repr_builder():
            repr_parts.append(', start_position = ')
            repr_parts.append(repr(self.start_position))
            
            repr_parts.append(', length = ')
            repr_parts.append(repr(self.length))
        
        return ''.join(repr_parts)


class TokenGroup(TokenBase):
    __slots__ = ('tokens',)
    
    def __new__(cls, type_, tokens):
        self = TokenBase.__new__(cls, type_)
        self.tokens = tokens
        return self
    
    def get_start(self):
        start = -1
        for token in self.tokens:
            token_start = token.get_start()
            if start == -1:
                start = token_start
            else:
                if token_start < start:
                    start = token_start
        
        if start == -1:
            start = 0
        
        return start
    
    def get_end(self):
        end = -1
        for token in self.tokens:
            token_end = token.get_end()
            if end == -1:
                end = token_end
            else:
                if token_end > end:
                    end = token_end
        
        if end == -1:
            end = 0
        
        return end
    
    def __repr__(self):
        for repr_parts in self._cursed_repr_builder():
            repr_parts.append(', tokens = ')
            repr_parts.append(repr(self.tokens))
        
        return ''.join(repr_parts)


class IdentifierPartBase:
    def __new__(cls):
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the identifier part's representation."""
        return ''.join(['<', type(self).__name__, '>'])
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return False
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return False
    
    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return False
    
    
    def get_length(self):
        return 0
    
    
    def render_into(self, into):
        pass


class IdentifierPartStar(IdentifierPartBase):
    __slots__ = ()
    
    def __new__(cls):
        return object.__new__(cls)
    
    def __eq__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return False
        
        if other_type is IdentifierPartString:
            return False
        
        if other_type is IdentifierPartStar:
            return True
        
        return NotImplemented
    
    def __gt__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return False
        
        if other_type is IdentifierPartString:
            return False
        
        if other_type is IdentifierPartStar:
            return False
        
        return NotImplemented
    
    def __lt__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return True
        
        if other_type is IdentifierPartString:
            return True
        
        if other_type is IdentifierPartStar:
            return False
        
        return NotImplemented
    
    
    def get_length(self):
        return 1
    
    
    def render_into(self, into):
        into.append('*')


IDENTIFIER_STAR = IdentifierPartStar()


class IdentifierPartDot(IdentifierPartBase):
    __slots__ = ()
    
    def __new__(cls):
        return object.__new__(cls)
    
    def __eq__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return True
        
        if other_type is IdentifierPartString:
            return False
        
        if other_type is IdentifierPartStar:
            return False
        
        return NotImplemented
    
    def __gt__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return False
        
        if other_type is IdentifierPartString:
            return True
        
        if other_type is IdentifierPartStar:
            return True
        
        return NotImplemented
    
    def __lt__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return False
        
        if other_type is IdentifierPartString:
            return False
        
        if other_type is IdentifierPartStar:
            return False
        
        return NotImplemented
    
    
    def get_length(self):
        return 1
    
    
    def render_into(self, into):
        into.append('.')


IDENTIFIER_DOT = IdentifierPartDot()


class IdentifierPartString(IdentifierPartBase):
    __slots__ = ('value',)

    def __new__(cls, value):
        self = object.__new__(cls)
        self.value = value
        return self
    
    
    def __repr__(self):
        """Returns the identifier part's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # value
        repr_parts.append(' value = ')
        repr_parts.append(repr(self.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return False
        
        if other_type is IdentifierPartString:
            if self.value == other.value:
                return True
            
            return False
        
        if other_type is IdentifierPartStar:
            return False
        
        return NotImplemented
    
    def __gt__(self, other):
        other_type = type(other)
        if other_type is IdentifierPartDot:
            return False
        
        if other_type is IdentifierPartString:
            if self.value > other.value:
                return True
            
            return False
        
        if other_type is IdentifierPartStar:
            return True
        
        return NotImplemented
    
    def __lt__(self, other):
        other_type = type(other)
        
        if other_type is IdentifierPartDot:
            return True
        
        if other_type is IdentifierPartString:
            if self.value < other.value:
                return True
            
            return False
        
        if other_type is IdentifierPartStar:
            return False
        
        return NotImplemented
    
    
    def get_length(self):
        return len(self.value)
    
    
    def render_into(self, into):
        into.append(self.value)


def create_identifier_part(token, text):
    token_type = token.type
    if token_type == TOKEN_TYPE_IDENTIFIER:
        value = text[token.get_start():token.get_end()]
        part = IdentifierPartString(value)
    elif token_type == TOKEN_TYPE_STAR:
        part = IDENTIFIER_STAR
    else:
        part = IDENTIFIER_DOT
    
    return part


class Identifier:
    __slots__ = ('before_parts', 'after_part')
    
    def __new__(cls, token, text):
        if token.type == TOKEN_GROUP_TYPE_KEYWORD_AS:
            before_token = token.tokens[0]
            after_token = token.tokens[2]
        else:
            before_token = token
            after_token = None
        
        if before_token.type in (
            TOKEN_TYPE_IDENTIFIER,
            TOKEN_TYPE_STAR,
        ):
            before_parts = [create_identifier_part(before_token, text)]
        else:
            before_parts = [create_identifier_part(sub_token, text) for sub_token in before_token.tokens]
        
        if after_token is None:
            after_part = None
        else:
            after_part = create_identifier_part(after_token, text)
        
        self = object.__new__(cls)
        self.before_parts = before_parts
        self.after_part = after_part
        return self
    
    
    def __repr__(self):
        """Returns the identifier's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # before_parts
        repr_parts.append(' before_parts = ')
        repr_parts.append(repr(self.before_parts))
        
        # after_part
        repr_parts.append(', after_part = ')
        repr_parts.append(repr(self.after_part))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_group_level(self):
        before_parts = self.before_parts
        first_part = before_parts[0]
        if type(first_part) is IdentifierPartString:
            value = first_part.value
            if value in BUILTIN_MODULES:
                return (GROUP_LEVEL_SORT_KEY_PACKAGE, GROUP_LEVEL_BUILTIN)
            
            if value in PACKAGE_MODULES:
                return (GROUP_LEVEL_SORT_KEY_PACKAGE, GROUP_LEVEL_PACKAGE)
            
            return (GROUP_LEVEL_SORT_KEY_LOCAL, 0)
        
        
        index = 1
        length = len(before_parts)
        while True:
            if index >= length:
                break
            
            part = before_parts[index]
            if part is not IDENTIFIER_DOT:
                break
            
            index += 1
            continue
        
        return (GROUP_LEVEL_SORT_KEY_LOCAL, -index)
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.before_parts != other.before_parts:
            return False
        
        if self.after_part != other.after_part:
            return False
        
        return True
    
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_before_parts = self.before_parts
        other_before_parts = other.before_parts
        
        if self_before_parts > other_before_parts:
            return True
        
        if self_before_parts < other_before_parts:
            return False
        
        self_after_part = self.after_part
        other_after_part = other.after_part
        
        if self_after_part is None:
            return False
        
        if other_after_part is None:
            return True
        
        if self_after_part > other_after_part:
            return True
        
        return False
    
    
    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_before_parts = self.before_parts
        other_before_parts = other.before_parts
        
        if self_before_parts < other_before_parts:
            return True
        
        if self_before_parts > other_before_parts:
            return False
        
        self_after_part = self.after_part
        other_after_part = other.after_part
        
        
        if other_after_part is None:
            return False
        
        if self_after_part is None:
            return True
        
        if self_after_part < other_after_part:
            return True
        
        return False
    
    
    def get_length(self):
        length = 0
        
        for part in self.before_parts:
            length += part.get_length()
        
        after_part = self.after_part
        if (after_part is not None):
            length += 4
            length += after_part.get_length()
        
        return length
    
    
    def render_into(self, into):
        for part in self.before_parts:
            part.render_into(into)
        
        after_part = self.after_part
        if (after_part is not None):
            into.append(' as ')
            after_part.render_into(into)



GROUP_LEVEL_SORT_KEY_PACKAGE = 0
GROUP_LEVEL_SORT_KEY_LOCAL = 1

GROUP_LEVEL_BUILTIN = 1
GROUP_LEVEL_PACKAGE = 2

# We cheat
BUILTIN_MODULES = frozenset((
    'warnings',
    'datetime',
    'sys',
    'os',
    're',
    'collections',
    'time',
    'weakref',
    '_weakref',
    'math',
    'base64',
    'binascii',
    'reprlib',
    'json',
    'threading',
    'itertools',
    'functools',
    'types',
    'importlib',
    'py_compile',
    'ast',
    'pathlib',
    'subprocess',
    'shlex',
    'ctypes',
    'audioop',
    'socket',
    'random',
    'threading',
    'heapq',
    'ssl',
    'stat',
    'io',
    'http',
    'codecs',
    'hashlib',
    'uuid',
    'ntpath',
    'difflib',
    'zlib',
    'struct',
    'mimetypes',
    'urllib',
    'string',
    'ipaddress',
    'email',
    'tempfile',
    'setuptools',
    'errno',
    'selectors',
    'linecache',
    'platform',
    'code',
    'contextlib',
    'enum',
    'csv',
    'colorsys',
))

# We cheat more
PACKAGE_MODULES = frozenset((
    'hata',
    'scarletio',
    'chardet',
    'cchardet',
    'nacl',
    'dotenv',
    'brotli',
    'sqlalchemy',
    'dateutil',
    'vampytest',
    'PIL',
    'matplotlib',
    'numpy',
    'seaborn',
    'scipy',
))

class ImportStatement:
    __slots__ = ('import_from', 'import_what',)
    
    def __new__(cls, tokens, text):
        if len(tokens) == 2:
            # import a
            
            import_from_token = None
            import_what_token = tokens[1]
        
        else:
            # from a import b
            import_from_token = tokens[1]
            import_what_token = tokens[3]
        
        
        if import_from_token is None:
            import_from = None
        else:
            import_from = Identifier(import_from_token, text)
        
        if import_what_token.type == TOKEN_GROUP_TYPE_LISTING:
            import_what = [Identifier(token_group.tokens[0], text) for token_group in import_what_token.tokens]
            import_what.sort()
        else:
            import_what = [Identifier(import_what_token, text)]
        
        self = object.__new__(cls)
        self.import_from = import_from
        self.import_what = import_what
        return self
    
    
    def __repr__(self):
        """Returns the import statement's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # import_from
        repr_parts.append(' import_from = ')
        repr_parts.append(repr(self.import_from))
    
        # import_what
        repr_parts.append(' import_what = ')
        repr_parts.append(repr(self.import_what))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_group_level(self):
        import_from = self.import_from
        if (import_from is None):
            level_identifier = self.import_what[0]
        else:
            level_identifier = import_from
        
        return level_identifier.get_group_level()
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.import_from != other.import_from:
            return False
        
        if self.import_what != other.import_what:
            return False
    
        return True
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_import_from = self.import_from
        other_import_from = other.import_from
        
        if self_import_from is None:
            if other_import_from is not None:
                return False
        else:
            if other_import_from is None:
                return True
        
        if (self_import_from is not None):
            if self_import_from > other_import_from:
                return True
            
            if self_import_from < other_import_from:
                return False
        
        
        if self.import_what > other.import_what:
            return True
        
        return False
    
    
    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_import_from = self.import_from
        other_import_from = other.import_from
        
        if self_import_from is None:
            if other_import_from is not None:
                return True
        else:
            if other_import_from is None:
                return False
        
        if (self_import_from is not None):
            if self_import_from < other_import_from:
                return True
            
            if self_import_from > other_import_from:
                return False
        
        if self.import_what < other.import_what:
            return True
        
        return False
    
    
    def get_single_line_length(self):
        length = len('import ')
        
        import_from = self.import_from
        if (import_from is not None):
            length += len('from  ')
            length += import_from.get_length()
        
        import_what = self.import_what
        length += len(', ') * (len(import_what) - 1)
        for identifier in import_what:
            length += identifier.get_length()
        
        return length
    
    
    def render_into(self, into):
        length = self.get_single_line_length()
        if length < LINE_LENGTH_MAX:
            self.render_single_line_into(into)
        else:
            self.render_multi_line_into(into)
    
    
    def render_single_line_into(self, into):
        import_from = self.import_from
        if (import_from is not None):
            into.append('from ')
            import_from.render_into(into)
            into.append(' ')
        
        into.append('import ')
        
        import_what = self.import_what
        index = 0
        length = len(import_what)
        while True:
            identifier = import_what[index]
            identifier.render_into(into)
            
            index += 1
            if index == length:
                break
            
            into.append(', ')
    
    
    def render_multi_line_into(self, into):
        import_from = self.import_from
        if (import_from is not None):
            into.append('from ')
            import_from.render_into(into)
            into.append(' ')
        
        into.append('import (\n')
        
        line_length = 0
        line_length_max = LINE_LENGTH_MAX - INDENT_LENGTH - 1
        
        into.append(INDENT)
        
        import_what = self.import_what
        index = 0
        length = len(import_what)
        
        while import_what:
            identifier = import_what[index]
            identifier_length = identifier.get_length()
            
            line_length += identifier_length
            
            if index:
                line_length += 1
            
            if line_length > line_length_max:
                into.append('\n')
                into.append(INDENT)
                line_length = identifier_length
                identifier.render_into(into)
            else:
                if index:
                    into.append(' ')
                
                identifier.render_into(into)
            
            index += 1
            if index == length:
                break
            
            into.append(',')
            line_length += 1
        
        into.append('\n)')


def build_statement_groups(statements):
    groups_by_key = {}
    
    for statement in statements:
        group_level = statement.get_group_level()
        
        try:
            group = groups_by_key[group_level]
        except KeyError:
            group = []
            groups_by_key[group_level] = group
        
        group.append(statement)
    
    groups_and_keys = sorted(groups_by_key.items())
    groups = [item[1] for item in groups_and_keys]
    
    for group in groups:
        group.sort()
    
    return groups


def render_statement_group_into(statement_group, into):
    index = 0
    length = len(statement_group)
    
    while True:
        statement = statement_group[index]
        statement.render_into(into)
        
        index += 1
        if index == length:
            break
        
        into.append('\n')
        continue


def render_statement_groups(statement_groups):
    into = []
    length = len(statement_groups)
    if length:
        index = 0
        
        while True:
            statement_group = statement_groups[index]
            render_statement_group_into(statement_group, into)
            
            index += 1
            if index == length:
                break
            
            into.append('\n\n')
            continue
    
    return ''.join(into)



TOKEN_NAME_DEFAULT = 'flandre'

TOKEN_TYPE_TO_NAME = {
    TOKEN_TYPE_SPACE: 'space',
    TOKEN_TYPE_ESCAPE: 'escape',
    TOKEN_TYPE_PARENTHESES_OPEN: 'parentheses open',
    TOKEN_TYPE_PARENTHESES_CLOSE: 'parentheses close',
    TOKEN_TYPE_ATTRIBUTE_ACCESS: 'dot',
    TOKEN_TYPE_LINE_BREAK: 'line break',
    TOKEN_TYPE_EOF: 'eof',
    TOKEN_TYPE_IDENTIFIER: 'identifier',
    TOKEN_TYPE_KEYWORD_FROM: 'from keyword',
    TOKEN_TYPE_KEYWORD_IMPORT: 'import keyword',
    TOKEN_TYPE_KEYWORD_AS: 'as keyword',
    TOKEN_TYPE_THE_UNKNOWN: TOKEN_NAME_DEFAULT,
    TOKEN_TYPE_COMMA: 'comma',
    TOKEN_TYPE_STAR: 'star',
    
    TOKEN_GROUP_TYPE_IDENTIFIER: 'dotted identifier',
    TOKEN_GROUP_TYPE_LISTING: 'listing',
    TOKEN_GROUP_TYPE_KEYWORD_AS: 'keyword as',
    TOKEN_GROUP_TYPE_LISTING_ELEMENT : 'listing element',
}

def get_token_name(token_type):
    return TOKEN_TYPE_TO_NAME.get(token_type, TOKEN_NAME_DEFAULT)


TOKEN_STARTING_IDS = frozenset((
    TOKEN_TYPE_KEYWORD_FROM,
    TOKEN_TYPE_KEYWORD_IMPORT,
))


TOKEN_ENDING_IDS = frozenset((
    TOKEN_TYPE_IDENTIFIER,
    TOKEN_TYPE_PARENTHESES_CLOSE,
    TOKEN_TYPE_STAR,
))

NO_IDS = frozenset(())

TOKEN_FOLLOWING_IDS = {
    # TOKEN_TYPE_SPACE: NO_IDS # Already all removed
    # TOKEN_TYPE_ESCAPE: NO_IDS # Already all removed
    TOKEN_TYPE_PARENTHESES_OPEN: frozenset((
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
        TOKEN_TYPE_IDENTIFIER,
        TOKEN_TYPE_STAR,
    )),
    TOKEN_TYPE_PARENTHESES_CLOSE: frozenset((
        TOKEN_TYPE_KEYWORD_IMPORT,
        TOKEN_TYPE_KEYWORD_AS,
        TOKEN_TYPE_COMMA,
    )),
    TOKEN_TYPE_ATTRIBUTE_ACCESS: frozenset((
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
        TOKEN_TYPE_IDENTIFIER,
        TOKEN_TYPE_KEYWORD_IMPORT,
    )),
    # TOKEN_TYPE_LINE_BREAK: NO_IDS # Already all removed
    # TOKEN_TYPE_EOF: NO_IDS # Already all removed
    TOKEN_TYPE_IDENTIFIER: frozenset((
        TOKEN_TYPE_KEYWORD_IMPORT,
        TOKEN_TYPE_KEYWORD_AS,
        TOKEN_TYPE_COMMA,
        TOKEN_TYPE_PARENTHESES_CLOSE,
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
    )),
    TOKEN_TYPE_KEYWORD_FROM: frozenset((
        TOKEN_TYPE_PARENTHESES_OPEN,
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
        TOKEN_TYPE_IDENTIFIER,
    )),
    TOKEN_TYPE_KEYWORD_IMPORT: frozenset((
        TOKEN_TYPE_PARENTHESES_OPEN,
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
        TOKEN_TYPE_IDENTIFIER,
        TOKEN_TYPE_STAR,
    )),
    TOKEN_TYPE_KEYWORD_AS: frozenset((
        TOKEN_TYPE_PARENTHESES_OPEN,
        TOKEN_TYPE_IDENTIFIER,
    )),
    # TOKEN_TYPE_THE_UNKNOWN: NO_IDS # Already all removed
    TOKEN_TYPE_COMMA: frozenset((
        TOKEN_TYPE_PARENTHESES_OPEN,
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
        TOKEN_TYPE_IDENTIFIER,
        TOKEN_TYPE_PARENTHESES_CLOSE,
        TOKEN_TYPE_STAR,
    )),
    TOKEN_TYPE_STAR: frozenset((
        TOKEN_TYPE_COMMA,
        TOKEN_TYPE_PARENTHESES_CLOSE,
    )),
}

class EvaluationError(Exception):
    def __init__(self, tokens, error_message):
        self.tokens = tokens
        self.error_message = error_message
        Exception.__init__(self, tokens, error_message)
    
    
    def get_pretty_repr_on(self, text):
        repr_parts = []
        
        for token in self.tokens:
            token_start = token.get_start()
            token_end = token.get_end()
            
            text_start = text.rfind('\n', token_start-20, token_start)
            if text_start == -1:
                text_start = token_start-20
                if text_start < 0:
                    text_start_cropped = False
                    text_start = 0
                elif text_start > 0:
                    text_start_cropped = True
                else:
                    text_start_cropped = False
            
            else:
                text_start += 1
                text_start_cropped = False
            
            text_end = text.find('\n', token_end, token_end+20)
            if text_end == -1:
                text_end = token_end+20
                if text_end > len(text):
                    text_end_cropped = False
                    text_end = len(text)
                elif text_end < len(text):
                    text_end_cropped = True
                else:
                    text_end_cropped = False
            else:
                text_end_cropped = False
            
            if text_start_cropped:
                repr_parts.append('...')
            
            repr_parts.append(text[text_start:text_end])
            
            if text_end_cropped:
                repr_parts.append('...')
            
            repr_parts.append('\n')
            
            add_space_count = text_start_cropped * 3 + token_start-text_start
            repr_parts.append(' '*add_space_count)
            
            add_arrow_count = token_end-token_start
            repr_parts.append('^'*add_arrow_count)
            
            repr_parts.append('\n')
        
        repr_parts.append('\n')
        repr_parts.append(self.error_message)
        
        return ''.join(repr_parts)


def read_token(text, start_position):
    while True:
        if len(text) == start_position:
            token_type = TOKEN_TYPE_EOF
            length = 0
            break
    
        start_character = text[start_position]
        if start_character == OPERATOR_ESCAPE:
            token_type = TOKEN_TYPE_ESCAPE
            length = 1
            break
        
        if start_character == OPERATOR_PARENTHESES_OPEN:
            token_type = TOKEN_TYPE_PARENTHESES_OPEN
            length = 1
            break
        
        if start_character == OPERATOR_PARENTHESES_CLOSE:
            token_type = TOKEN_TYPE_PARENTHESES_CLOSE
            length = 1
            break
        
        if start_character == OPERATOR_ATTRIBUTE_ACCESS:
            token_type = TOKEN_TYPE_ATTRIBUTE_ACCESS
            length = 1
            break
        
        if start_character == OPERATOR_LINE_BREAK:
            token_type = TOKEN_TYPE_LINE_BREAK
            length = 1
            break
        
        if start_character == OPERATOR_COMMA:
            token_type = TOKEN_TYPE_COMMA
            length = 1
            break
        
        if start_character == OPERATOR_STAR:
            token_type = TOKEN_TYPE_STAR
            length = 1
            break
        
        match = SPACE_RP.match(text, start_position)
        if (match is not None):
            token_type = TOKEN_TYPE_SPACE
            length = match.end()-match.start()
            break
        
        match = IDENTIFIER_RP.match(text, start_position)
        if (match is not None):
            token_value = match.group(0)
            token_type = KEYWORD_MAP.get(token_value, TOKEN_TYPE_IDENTIFIER)
            length = match.end()-match.start()
            break
        
        token_type = TOKEN_TYPE_THE_UNKNOWN
        length = 1
        break
    
    return Token(token_type, start_position, length)


def read_tokens(text):
    tokens = []
    
    start_position = 0
    
    while True:
        token = read_token(text, start_position)
        start_position += token.length
        token_type = token.type
        
        # skip spaces
        if token_type == TOKEN_TYPE_SPACE:
            continue
        
        # end at eof
        if token_type == TOKEN_TYPE_EOF:
            break
        
        # raise at unknown
        if token_type == TOKEN_TYPE_THE_UNKNOWN:
            raise EvaluationError([token], 'unexpected character')
        
        tokens.append(token)
    
    return tokens


def remove_escapes(tokens):
    new_tokens = []
    
    last_token_escape = False
    
    
    for index in range(len(tokens)):
        token = tokens[index]
        
        if last_token_escape:
            if token.type == TOKEN_TYPE_LINE_BREAK:
                last_token_escape = False
            else:
                raise EvaluationError([tokens[-1], token], 'escape should be followed by linebreak')
        
        else:
            if token.type == TOKEN_TYPE_ESCAPE:
                last_token_escape = True
            else:
                new_tokens.append(token)
    
    return new_tokens


def check_parentheses(tokens):
    parentheses_stack = []
    for token in tokens:
        token_type = token.type
        if token_type == TOKEN_TYPE_PARENTHESES_OPEN:
            parentheses_stack.append(token)
            
        elif token_type == TOKEN_TYPE_PARENTHESES_CLOSE:
            if parentheses_stack:
                del parentheses_stack[-1]
            else:
                raise EvaluationError([token], 'parentheses never opened')
    
    if parentheses_stack:
        raise EvaluationError([parentheses_stack[-1]], 'parentheses never closed')



def build_token_groups(tokens):
    token_groups = []
    new_token_group = None
    
    parentheses_stack_size = 0
    
    for token in tokens:
        token_type = token.type
        if token_type == TOKEN_TYPE_LINE_BREAK:
            if parentheses_stack_size:
                continue
            
            if (new_token_group is None):
                continue
            
            token_groups.append(new_token_group)
            new_token_group = None
            continue
        
        if token_type == TOKEN_TYPE_PARENTHESES_OPEN:
            parentheses_stack_size += 1
        elif token_type == TOKEN_TYPE_PARENTHESES_CLOSE:
            parentheses_stack_size -= 1
        
        if (new_token_group is None):
            new_token_group = []
        
        new_token_group.append(token)
        continue
    
    
    if (new_token_group is not None):
        token_groups.append(new_token_group)
        new_token_group = None
    
    return token_groups


def check_group_followance(tokens):
    token = tokens[0]
    token_type = token.type
    if token_type not in TOKEN_STARTING_IDS:
        raise EvaluationError([token], f'expression cannot start with {get_token_name(token_type)}')
    
    last_token_type = token_type
    
    token = tokens[-1]
    token_type = token.type
    if token_type not in TOKEN_ENDING_IDS:
        raise EvaluationError([token], f'expression cannot end with {get_token_name(token_type)}')
    
    for index in range(1, len(tokens)):
        token = tokens[index]
        token_type = token.type
        if token_type not in TOKEN_FOLLOWING_IDS.get(last_token_type, NO_IDS):
            raise EvaluationError(
                [tokens[index - 1], token],
                f'{get_token_name(last_token_type)} cannot be followed by {get_token_name(token_type)}',
            )
        
        last_token_type = token_type


def merge_identifiers(tokens):
    new_tokens = []
    
    identifier_since = -1
    
    index = 0
    for index in range(len(tokens)):
        
        token = tokens[index]
        token_type = token.type
        if (
            token_type == TOKEN_TYPE_IDENTIFIER or
            token_type == TOKEN_TYPE_ATTRIBUTE_ACCESS
        ):
            if identifier_since == -1:
                identifier_since = index
            
            continue
        
        if identifier_since != -1:
            if identifier_since == index - 1:
                before_token = tokens[identifier_since]
                if before_token.type == TOKEN_TYPE_ATTRIBUTE_ACCESS:
                    before_token = TokenGroup(TOKEN_GROUP_TYPE_IDENTIFIER, [before_token])
                
                new_tokens.append(before_token)
            else:
                token_group = TokenGroup(TOKEN_GROUP_TYPE_IDENTIFIER, tokens[identifier_since:index])
                new_tokens.append(token_group)
            
            identifier_since = -1
        
        new_tokens.append(token)
        continue
    
    
    if identifier_since != -1:
        if identifier_since == index:
            before_token = tokens[identifier_since]
            if before_token.type == TOKEN_TYPE_ATTRIBUTE_ACCESS:
                before_token = TokenGroup(TOKEN_GROUP_TYPE_IDENTIFIER, [before_token])
            
            new_tokens.append(before_token)
        else:
            token_group = TokenGroup(TOKEN_GROUP_TYPE_IDENTIFIER, tokens[identifier_since:index + 1])
            new_tokens.append(token_group)
    
    
    return new_tokens


def split_by_comma(tokens):
    collected_tokens = None
    for token in tokens:
        if token.type == TOKEN_TYPE_COMMA:
            if (collected_tokens is not None):
                yield collected_tokens
                collected_tokens = None
        
        else:
            if (collected_tokens is None):
                collected_tokens = []
            
            collected_tokens.append(token)
    
    if (collected_tokens is not None):
        yield collected_tokens


def maybe_build_listing(tokens):
    token_groups = list(split_by_comma(tokens))
    if len(token_groups) == 1:
        new_tokens = token_groups[0]
    
    else:
        new_tokens = [
            TokenGroup(
                TOKEN_GROUP_TYPE_LISTING,
                [
                    TokenGroup(TOKEN_GROUP_TYPE_LISTING_ELEMENT, token_group)
                    for token_group in token_groups
                ],
            )
        ]
    
    return new_tokens


def build_parentheses_recursive(tokens, index):
    new_tokens = []
    
    length = len(tokens)
    while True:
        if index == length:
            break
        
        token = tokens[index]
        
        token_type = token.type
        if token_type == TOKEN_TYPE_PARENTHESES_OPEN:
            token_group, index = build_parentheses_recursive(tokens, index + 1)
            token_group = maybe_build_listing(token_group)
            new_tokens.extend(token_group)
            continue
        
        if token_type == TOKEN_TYPE_PARENTHESES_CLOSE:
            index += 1
            break
        
        new_tokens.append(token)
        index += 1
        continue
    
    return new_tokens, index


def build_parentheses(tokens):
    new_tokens, index = build_parentheses_recursive(tokens, 0)
    return new_tokens


def check_multiple_keyword_import_recursive(tokens, import_token):
    for token in tokens:
        token_type = token.type
        if token_type == TOKEN_TYPE_KEYWORD_IMPORT:
            if import_token is None:
                import_token = token
            else:
                raise EvaluationError([import_token, token], 'multiple import keywords inside of a single statement.')
        
        elif token_type == TOKEN_GROUP_TYPE_LISTING:
            for token_group in token.tokens:
                import_token = check_multiple_keyword_import_recursive(token_group.tokens, import_token)
    
    return import_token


def check_multiple_keyword_import(tokens):
    check_multiple_keyword_import_recursive(tokens, None)
    

def check_keyword_as_recursive(tokens):
    tokens_length = len(tokens)
    
    index = 0
    
    while True:
        if index >= tokens_length:
            break
        
        token = tokens[index]
        token_type = token.type
        if token_type == TOKEN_GROUP_TYPE_LISTING:
            for token_group in token.tokens:
                check_keyword_as_recursive(token_group.tokens)
            
            index += 1
            continue
            
        if token_type != TOKEN_TYPE_KEYWORD_AS:
            index += 1
            continue
        
        # should not happen
        if (index < 1) or (index >= len(tokens) - 1):
            raise EvaluationError(
                [token],
                f'{get_token_name(token_type)} at invalid position',
            )
        
        # check bad `as identifier as`
        if index >= 4:
            way_before_token = tokens[index - 2]
            way_before_token_type = way_before_token.type
            if way_before_token_type == TOKEN_TYPE_KEYWORD_AS:
                raise EvaluationError(
                    [way_before_token, token],
                    f'chaining {get_token_name(token_type)}-s is forbidden',
                )
        
        # check good `identifier as`
        before_token = tokens[index - 1]
        before_token_type = before_token.type
        if (
            before_token_type != TOKEN_TYPE_IDENTIFIER and
            before_token_type != TOKEN_GROUP_TYPE_IDENTIFIER
        ):
            raise EvaluationError(
                [before_token, token],
                f'{get_token_name(before_token_type)} cannot be followed by {get_token_name(token_type)}',
            )

        # check good `as identifier`
        after_token = tokens[index + 1]
        after_token_type = before_token.type
        if (
            after_token_type != TOKEN_TYPE_IDENTIFIER and
            after_token_type != TOKEN_GROUP_TYPE_IDENTIFIER
        ):
            raise EvaluationError(
                [token, after_token],
                f'{get_token_name(token_type)} cannot be followed by {get_token_name(after_token_type)}',
            )
        
        index += 2
        continue


def build_keyword_as_recursively(tokens):
    tokens_length = len(tokens)
    index = 0
    
    new_tokens = []
    
    while True:
        if index >= tokens_length:
            break
        
        token = tokens[index]
        token_type = token.type
        
        if token_type == TOKEN_GROUP_TYPE_LISTING:
            for token_group in token.tokens:
                token_group.tokens = build_keyword_as_recursively(token_group.tokens)
            
            index += 1
        
        else:
            if (index >= tokens_length - 1):
                index += 1
                
            else:
                if (
                    token_type != TOKEN_TYPE_IDENTIFIER and
                    token_type != TOKEN_GROUP_TYPE_IDENTIFIER
                ):
                    index += 1
                
                else:
                    after_token = tokens[index + 1]
                    if after_token.type == TOKEN_TYPE_KEYWORD_AS:
                        token = TokenGroup(
                            TOKEN_GROUP_TYPE_KEYWORD_AS,
                            [token, after_token, tokens[index + 2]],
                        )
                        index += 3
                    
                    else:
                        index += 1
        
        new_tokens.append(token)
        
        continue
    
    return new_tokens


def merge_lazy_parentheses(tokens):
    comma_indexes = []
    
    index = 0
    length = len(tokens)
    
    while index < length:
        token = tokens[index]
        if token.type == TOKEN_TYPE_COMMA:
            comma_indexes.append(index)
        
        index += 1
        continue
    
    if not comma_indexes:
        return tokens
    
    comma_groups = []
    comma_group = None
    
    last_comma_index = -1
    
    for comma_index in comma_indexes:
        if comma_group is None:
            comma_group = [comma_index]
        else:
            if comma_index == last_comma_index+2:
                comma_group.append(comma_index)
            else:
                comma_groups.append(comma_group)
                comma_group = [comma_index]
        
        last_comma_index = comma_index
    
    comma_groups.append(comma_group)
    
    
    comma_part_end_last = 0
    new_tokens = []
    
    for comma_group in comma_groups:
        comma_part_start = comma_group[0] - 1
        comma_part_end = comma_group[-1] + 2
        new_tokens.extend(tokens[comma_part_end_last:comma_part_start])
        
        new_tokens.append(
            TokenGroup(
                TOKEN_GROUP_TYPE_LISTING,
                [
                    TokenGroup(TOKEN_GROUP_TYPE_LISTING_ELEMENT, [token])
                    for token in tokens[comma_part_start:comma_part_end:2]
                ],
            )
        )
        comma_part_end_last = comma_part_end
    
    new_tokens.extend(tokens[comma_part_end_last:])
    
    return new_tokens


def check_for_nested_listings(tokens):
    for token in tokens:
        if token.type == TOKEN_GROUP_TYPE_LISTING:
            for token_group in token.tokens:
                for token in token_group.tokens:
                    if token.type == TOKEN_GROUP_TYPE_LISTING:
                        raise EvaluationError([token], 'nested listing disallowed')


def check_as_before_listing(tokens):
    # from bozo as nova import sort
    #      ^^^^^^^^^^^^
    # This cannot have `as` in it
    length = len(tokens)
    if length == 4:
        token = tokens[1]
        if token.type == TOKEN_GROUP_TYPE_KEYWORD_AS:
            raise EvaluationError([token], 'in `from a import b` part `a` cannot contain `as`')


def check_listing_before_import(tokens):
    # from bozo, nova import sort
    #      ^^^^^^^^^^
    # This cannot be a listing
    length = len(tokens)
    if length == 4:
        token = tokens[1]
        if token.type == TOKEN_GROUP_TYPE_LISTING:
            raise EvaluationError([token], 'in `from a import b` part `a` cannot be multiple values')


def check_dots_after_as(tokens):
    # import bozo as ..nova
    #                ^^^^^^
    # after `as` we cannot have an identifier with dots in it.
    for token in tokens:
        token_type = token.type
        if token_type == TOKEN_GROUP_TYPE_LISTING:
            for token_group in token.tokens:
                check_dots_after_as(token_group.tokens)
        
        elif token_type == TOKEN_GROUP_TYPE_KEYWORD_AS:
            token = token.tokens[2]
            if token.type == TOKEN_GROUP_TYPE_IDENTIFIER:
                raise EvaluationError([token], 'in `a as b` part `b` cannot have dots in it')


def check_for_no_dots(token):
    token_type = token.type
    if (
        (token_type == TOKEN_GROUP_TYPE_IDENTIFIER) or
        (
            (token_type == TOKEN_GROUP_TYPE_KEYWORD_AS) and
            (token.tokens[0].type == TOKEN_GROUP_TYPE_IDENTIFIER)
        )
    ):
        raise EvaluationError([token], 'in `from a import b` part `b` cannot have dots in it')
    
def check_dots_after_from_import(tokens):
    # from bozo import ..nova, .bozo as nova
    #                  ^^^^^^  ^^^^^
    # These cannot have dots in them either
    length = len(tokens)
    if length == 4:
        token = tokens[3]
        if token.type == TOKEN_GROUP_TYPE_LISTING:
            for token_group in token.tokens:
                for token in token_group.tokens:
                    check_for_no_dots(token)
        else:
            check_for_no_dots(token)


def check_from_import_positions(tokens):
    # Valid expressions:
    #
    # from a import b
    # import b
    length = len(tokens)
    if tokens[0].type == TOKEN_TYPE_KEYWORD_IMPORT:
        if length > 2:
            raise EvaluationError([tokens[2]], 'extra part after `import a`')
    
    else:
        # Since a line can start only with `form` and `import`, we do not need to do a second check.
        if length < 4:
            raise EvaluationError([tokens[0]], '`from a import b` not complete (not enough tokens)')
        
        token = tokens[2]
        if token.type != TOKEN_TYPE_KEYWORD_IMPORT:
            raise EvaluationError([token], 'in `from a import b` the `import` part is missing or is at a bad position')
        
        if length > 4:
            raise EvaluationError([tokens[4]], 'extra part after `from a import b`')


def bozosort_group(tokens, text):
    check_group_followance(tokens)
    tokens = merge_identifiers(tokens)
    tokens = build_parentheses(tokens)
    check_multiple_keyword_import(tokens)
    check_keyword_as_recursive(tokens)
    tokens = build_keyword_as_recursively(tokens)
    tokens = merge_lazy_parentheses(tokens)
    check_for_nested_listings(tokens)
    check_from_import_positions(tokens)
    check_as_before_listing(tokens)
    check_listing_before_import(tokens)
    check_dots_after_as(tokens)
    check_dots_after_from_import(tokens)
    return ImportStatement(tokens, text)


def bozosort(text):
    try:
        tokens = read_tokens(text)
        tokens = remove_escapes(tokens)
        check_parentheses(tokens)
        token_groups = build_token_groups(tokens)
        
        statements = []
        
        for token_group in token_groups:
            statement = bozosort_group(token_group, text)
            statements.append(statement)
    
    except EvaluationError as err:
        output = err.get_pretty_repr_on(text)
    
    else:
        statement_groups = build_statement_groups(statements)
        
        output = render_statement_groups(statement_groups)
    
    return output


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    target = 'message',
    required_permissions = Permission().update_by_keys(manage_messages = True),
)
async def bozosort_(
    client,
    event,
    message,
):
    if (not event.user_permissions.can_manage_messages):
        abort('You need to have manage messages to invoke this command.')
    
    content = message.content
    if content is None:
        attachments = message.attachments
        if (attachments is not None):
            for attachment in attachments:
                content_type = attachment.content_type
                if (content_type is not None) and content_type.startswith('text/plain'):
                    yield # ack the event before downloading the attachment
                    content = await client.download_attachment(attachment)
                    content = content.decode('utf-8')
                    break
        
        if (content is None):
            abort('No content detected')
            
    output = bozosort(content)
    
    if not output:
        content = '*no output*'
        file = None
    
    elif len(output) < 1900:
        content = f'```py\n{output}\n```'
        file = None
    
    else:
        content = None
        file = ('output.py', output)
    
    yield InteractionResponse(content, allowed_mentions = None, file = file)
