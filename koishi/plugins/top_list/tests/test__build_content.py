import vampytest
from hata import User

from ..builders import build_content
from ..constants import PAGE_SIZE, STYLE_HEARTS, STYLE_NAME, STYLE_NUMBER


def test__build_content():
    """
    Tests whether ``build_content`` works as intended.
    """
    page_index = 20
    processed_entries = [
        (page_index * PAGE_SIZE + 1, 1111, User.precreate(202308230004, name = 'okuu')),
        (page_index * PAGE_SIZE + 2, 1112, User.precreate(202308230005, name = 'orin')),
    ]
    
    output = build_content(page_index, processed_entries)
    
    vampytest.assert_eq(
        output,
        (
            f'```ansi\n'
            f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 1!s}.: {STYLE_HEARTS}{1111!s} {STYLE_NAME}okuu\n'
            f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 2!s}.: {STYLE_HEARTS}{1112!s} {STYLE_NAME}orin\n'
            f'```'
        ),
    )


def test__build_content__empty():
    """
    Tests whether ``build_content`` works as intended.
    
    Case: empty.
    """
    page_index = 20
    processed_entries = []
    
    output = build_content(page_index, processed_entries)
    
    vampytest.assert_eq(
        output,
        (
            f'```\n'
            f'no result\n'
            f'```'
        ),
    )


def test__build_content__shifted():
    """
    Tests whether ``build_content`` works as intended.
    
    Case: values shifted.
    """
    processed_entries = [
        ( 1,  1111, User.precreate(202308230006, name = 'okuu')),
        ( 2,  1112, User.precreate(202308230007, name = 'orin')),
        ( 3,  1113, User.precreate(202308230008, name = 'yuuka')),
        ( 4,   555, User.precreate(202308230009, name = 'koishi')),
        ( 5, 12222, User.precreate(202308230010, name = 'satori')),
        ( 6,    56, User.precreate(202308230011, name = 'yuuma')),
        ( 7,    75, User.precreate(202308230012, name = 'ran')),
        ( 8,    12, User.precreate(202308230013, name = 'chen')),
        ( 9,     1, User.precreate(202308230014, name = 'biten')),
        (10,  6969, User.precreate(202308230015, name = 'hisami')),
    ]
    
    output = build_content(0, processed_entries)
    
    vampytest.assert_eq(
        output,
        (
            f'```ansi\n'
            f'{STYLE_NUMBER} 1.: {STYLE_HEARTS} 1111 {STYLE_NAME}okuu\n'
            f'{STYLE_NUMBER} 2.: {STYLE_HEARTS} 1112 {STYLE_NAME}orin\n'
            f'{STYLE_NUMBER} 3.: {STYLE_HEARTS} 1113 {STYLE_NAME}yuuka\n'
            f'{STYLE_NUMBER} 4.: {STYLE_HEARTS}  555 {STYLE_NAME}koishi\n'
            f'{STYLE_NUMBER} 5.: {STYLE_HEARTS}12222 {STYLE_NAME}satori\n'
            f'{STYLE_NUMBER} 6.: {STYLE_HEARTS}   56 {STYLE_NAME}yuuma\n'
            f'{STYLE_NUMBER} 7.: {STYLE_HEARTS}   75 {STYLE_NAME}ran\n'
            f'{STYLE_NUMBER} 8.: {STYLE_HEARTS}   12 {STYLE_NAME}chen\n'
            f'{STYLE_NUMBER} 9.: {STYLE_HEARTS}    1 {STYLE_NAME}biten\n'
            f'{STYLE_NUMBER}10.: {STYLE_HEARTS} 6969 {STYLE_NAME}hisami\n'
            f'```'
        ),
    )
