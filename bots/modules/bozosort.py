import re
from collections import namedtuple

SPACE_RP = re.compile('[ \t]+')
IDENTIFIER_RP = re.compile('[_a-zA-Z][_a-zA-Z0-9]*')

OPERATOR_ESCAPE = '\\'
OPERATOR_PARENTHESES_OPEN = '('
OPERATOR_PARENTHESES_CLOSE = ')'
OPERATOR_ATTRIBUTE_ACCESS = '.'
OPERATOR_LINE_BREAK = '\n'
OPERATOR_COMMA = ','

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

LINE_LENGTH = 120

KEYWORD_MAP = {
    'from': TOKEN_TYPE_KEYWORD_FROM,
    'import': TOKEN_TYPE_KEYWORD_IMPORT,
    'as': TOKEN_TYPE_KEYWORD_AS,
}

TOKEN_GROUP_TYPE_IDENTIFIER = 101
TOKEN_GROUP_TYPE_LISTING = 102
TOKEN_GROUP_TYPE_KEYWORD_AS = 103
TOKEN_GROUP_TYPE_LISTING_ELEMENT = 104

Token = namedtuple('Token', ('type', 'start_position', 'length'))

TokenGroup = namedtuple('Token', ('type', 'tokens'))

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
))

NO_IDS = frozenset(())

TOKEN_FOLLOWING_IDS = {
    # TOKEN_TYPE_SPACE: NO_IDS # Already all removed
    # TOKEN_TYPE_ESCAPE: NO_IDS # Already all removed
    TOKEN_TYPE_PARENTHESES_OPEN: frozenset((
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
        TOKEN_TYPE_IDENTIFIER,
    )),
    TOKEN_TYPE_PARENTHESES_CLOSE: frozenset((
        TOKEN_TYPE_KEYWORD_IMPORT,
        TOKEN_TYPE_KEYWORD_AS,
        TOKEN_TYPE_COMMA,
    )),
    TOKEN_TYPE_ATTRIBUTE_ACCESS: frozenset((
        TOKEN_TYPE_ATTRIBUTE_ACCESS,
        TOKEN_TYPE_IDENTIFIER,
    )),
    # TOKEN_TYPE_LINE_BREAK: NO_IDS # Already all removed
    # TOKEN_TYPE_EOF: NO_IDS # Already all removed
    TOKEN_TYPE_IDENTIFIER: frozenset((
        TOKEN_TYPE_KEYWORD_IMPORT,
        TOKEN_TYPE_KEYWORD_AS,
        TOKEN_TYPE_COMMA,
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
    )),
}

class EvaluationError(Exception):
    pass

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
        
        match = SPACE_RP.match(text, start_position)
        if (match is not None):
            token_type = TOKEN_TYPE_SPACE
            length = match.end()-match.start()
            break
        
        match = IDENTIFIER_RP.match(text, start_position)
        if (match is not None):
            token_value = match.group(0)
            print(token_value)
            token_type = KEYWORD_MAP.get(token_value, TOKEN_TYPE_IDENTIFIER)
            print(get_token_name(token_type))
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
    
    
    for index in range(len(tokens)-1):
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
    for index in range(len(tokens)):
        
        token = tokens[identifier_since]
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
                tokens.append(tokens[identifier_since])
            else:
                token_group = TokenGroup(TOKEN_GROUP_TYPE_IDENTIFIER, [tokens[identifier_since:index]])
                tokens.append(token_group)
        
        tokens.append(token)
    
    else:
        index = 0
    
    if identifier_since != -1:
        if identifier_since == index:
            tokens.append(tokens[identifier_since])
        else:
            token_group = TokenGroup(TOKEN_GROUP_TYPE_IDENTIFIER, [tokens[identifier_since:index+1]])
            tokens.append(token_group)
    
    
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
            new_tokens, index = build_parentheses_recursive(tokens, index + 1)
            if len(new_tokens) == 1:
                new_tokens = new_tokens[0]
            else:
                new_tokens = maybe_build_listing(new_tokens)
            new_tokens.extend(new_tokens)
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
        if (index < 2) or (index >= len(tokens) - 1):
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
    
    if tokens_length < 4:
        return
    
    index = 1
    tokens_length -= 1
    
    new_tokens = [tokens[0]]
    
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
            if (index < 1) or (index >= len(tokens) - 1):
                index += 1
            else:
            
                if (
                    token_type != TOKEN_TYPE_IDENTIFIER and
                    token_type != TOKEN_GROUP_TYPE_IDENTIFIER
                ):
                    index += 1
                else:
                    after_token = tokens[index+1]
                    if after_token.type == TOKEN_TYPE_KEYWORD_AS:
                        token = TokenGroup(
                            TOKEN_GROUP_TYPE_KEYWORD_AS,
                            [token, after_token, tokens[index+2]],
                        )
                        index += 3
                    
                    else:
                        token = tokens[index]
                        index += 1
        
        new_tokens.append(token)
            
        continue
    
    return new_tokens


def bozosort_group(token_group):
    check_group_followance(token_group)
    token_group = merge_identifiers(token_group)
    token_group = build_parentheses(token_group)
    check_keyword_as_recursive(token_group)
    token_group = build_keyword_as_recursively(token_group)
    print(token_group)


def bozosort(text):
    tokens = read_tokens(text)
    tokens = remove_escapes(tokens)
    check_parentheses(tokens)
    token_groups = build_token_groups(tokens)
    
    new_token_groups = []
    
    for token_group in token_groups:
        token_group = bozosort_group(token_group)
        new_token_groups.append(token_group)


def test():
    string = (
        'from bozo import sort\n'
        'from ..folder import ayaya\n'
        'import cake, ..noice\n'
        'import cake as cookie\n'
        'from (bozo) import oh_no, more_import\n'
        'from (..bozo) import cake as cookie import keyword\n'
        'from ..bozo.nova import (keyword, element)\n'
    )
    bozosort(string)

if __name__ == '__main__':
    test()
