import vampytest

from ..table_building import build_table_into


def _iter_options():
    yield (
        ('name', 'value'),
        [
            ('none', 'koishi', 'satori'),
            ('0', '1', '2'),
        ],
        (
            '+--------+-------+\n'
            '| name   | value |\n'
            '+========+=======+\n'
            '| none   | 0     |\n'
            '+--------+-------+\n'
            '| koishi | 1     |\n'
            '+--------+-------+\n'
            '| satori | 2     |\n'
            '+--------+-------+'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_table_into(headers, columns):
    """
    Tests whether ``build_table_into`` works as intended.
    
    Parameters
    ----------
    headers : `tuple<str>`
        Table headers.
    
    columns : `tuple<list<str>>`
        Table columns.
    
    Returns
    -------
    output : `str`
    """
    into = build_table_into([], headers, columns)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
