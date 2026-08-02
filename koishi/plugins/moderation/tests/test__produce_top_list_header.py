import vampytest
from hata import Guild

from ..constants import ACTION_TYPE_BAN
from ..content_building import produce_top_list_header


def _iter_options():
    guild = Guild.precreate(202607290000, name = 'Moriya shrine')
    
    yield (
        guild,
        2000,
        ACTION_TYPE_BAN,
        40,
        (
            '# Moriya shrine\'s mod top-list\n'
            '\n'
            'Sort by: ban\n'
            'Days: 40\n'
            'Page: 2001'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_top_list_header(guild, page_index, sort_by, days):
    """
    Tests whether ``produce_top_list_header`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The local guild.
    
    page_index : `int`
        The page to show. Used to calculate entry index.
    
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    
    days : `int`
        The amount of days to request.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_top_list_header(guild, page_index, sort_by, days)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
