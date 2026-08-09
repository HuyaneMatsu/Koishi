import vampytest
from hata import GuildProfile, User

from ..constants import PAGE_SIZE, STYLE_VALUE, STYLE_NAME, STYLE_NUMBER
from ..content_building import produce_top_list_description


def _iter_options():
    page_index = 20
    guild_id = 202503070003
    
    processed_entries = [
        (User.precreate(202308230004, name = 'okuu'), 1112),
        (User.precreate(202308230005, name = 'orin'), 1111),
    ]
    processed_entries[1][0].guild_profiles[guild_id] = GuildProfile(nick = 'rin rin')
    
    
    yield (
        page_index,
        processed_entries,
        guild_id,
        (
            f'```ansi\n'
            f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 1!s}.: {STYLE_VALUE}{1112!s} {STYLE_NAME}okuu\n'
            f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 2!s}.: {STYLE_VALUE}{1111!s} {STYLE_NAME}rin rin\n'
            f'```'
        ),
    )
    
    
    yield (
        0,
        [],
        0,
        (
            f'```ansi\n'
            f'```'
        ),
    )
    
    
    processed_entries = [
        (User.precreate(202308230006, name =   'okuu'),  1111),
        (User.precreate(202308230007, name =   'orin'),  1112),
        (User.precreate(202308230008, name =  'yuuka'),  1113),
        (User.precreate(202308230009, name = 'koishi'),   555),
        (User.precreate(202308230010, name = 'satori'), 12222),
        (User.precreate(202308230011, name =  'yuuma'),    56),
        (User.precreate(202308230012, name =    'ran'),    75),
        (User.precreate(202308230013, name =   'chen'),    12),
        (User.precreate(202308230014, name =  'biten'),     1),
        (User.precreate(202308230015, name = 'hisami'),  6969),
    ]
    
    yield (
        0,
        processed_entries,
        0,
        (
            f'```ansi\n'
            f'{STYLE_NUMBER} 1.: {STYLE_VALUE} 1111 {STYLE_NAME}okuu\n'
            f'{STYLE_NUMBER} 2.: {STYLE_VALUE} 1112 {STYLE_NAME}orin\n'
            f'{STYLE_NUMBER} 3.: {STYLE_VALUE} 1113 {STYLE_NAME}yuuka\n'
            f'{STYLE_NUMBER} 4.: {STYLE_VALUE}  555 {STYLE_NAME}koishi\n'
            f'{STYLE_NUMBER} 5.: {STYLE_VALUE}12222 {STYLE_NAME}satori\n'
            f'{STYLE_NUMBER} 6.: {STYLE_VALUE}   56 {STYLE_NAME}yuuma\n'
            f'{STYLE_NUMBER} 7.: {STYLE_VALUE}   75 {STYLE_NAME}ran\n'
            f'{STYLE_NUMBER} 8.: {STYLE_VALUE}   12 {STYLE_NAME}chen\n'
            f'{STYLE_NUMBER} 9.: {STYLE_VALUE}    1 {STYLE_NAME}biten\n'
            f'{STYLE_NUMBER}10.: {STYLE_VALUE} 6969 {STYLE_NAME}hisami\n'
            f'```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_top_list_description(page_index, processed_entries, guild_id):
    """
    Tests whether ``produce_top_list_description`` works as intended.
    
    Parameters
    ----------
    page_index : `int`
        Page index.
    
    processed_entries : ``list<(ClientUserBase int>)``
        Professed entries.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_top_list_description(page_index, processed_entries, guild_id)]
    
    for part in parts:
        vampytest.assert_instance(part, str)
    
    return ''.join(parts)
