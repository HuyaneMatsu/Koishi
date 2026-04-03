from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import get_to_do_match_rate_for_value
from ..to_do import ToDo


def _iter_options():
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409180000
    description = 'nyan orin'
    name = 'miau'
    
    entry_id = 127
    
    to_do = ToDo(name, description, created_at, creator_id)
    to_do.entry_id = entry_id
    
    yield to_do, 'nyan', (1, 0, entry_id)
    yield to_do, 'miau', (0, 0, entry_id)
    yield to_do, 'orin', (1, 5, entry_id)
    yield to_do, 'au', (0, 2, entry_id)
    yield to_do, 'mister', None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_to_do_match_rate_for_value(to_do, value):
    """
    Tests whether ``get_to_do_match_rate_for_value`` works as intended.
    
    Parameters
    ----------
    to_do : ``ToDo``
        To-do to get match rate for.
    
    value : `str`
        The value to match. Should be `.casefold()`-ed before passing.
    
    Returns
    -------
    output : `None | (int, int, int)`
    """
    output = get_to_do_match_rate_for_value(to_do, value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
