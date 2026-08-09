import vampytest
from hata import User

from ..queries import process_entries


def _iter_options():
    yield (
        10,
        [
            (202608090000, 1112),
            (202608090001, 1111),
        ],
        20,
        (
            [
                (User.precreate(202608090000), 1112),
                (User.precreate(202608090001), 1111),
            ],
            False,
        ),
    )
    
    yield (
        10,
        [
            (202608090002, 1113),
            (202608090003, 1112),
            (202608090004, 1111),
        ],
        2,
        (
            [
                (User.precreate(202608090002), 1113),
                (User.precreate(202608090003), 1112),
            ],
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__process_entries(page_index, entries, page_size):
    """
    Tests whether ``process_entries`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    
    entries : `list<sqlalchemy.engine.result.RowProxy>`
        Raw entries to process.
    
    page_size : `int`
        Custom page site to use.
    
    Returns
    -------
    output : ``(list<(ClientUserBase, int)>, bool)``
    """
    async def get_user(user_id):
        return User.precreate(user_id)
    
    mocked = vampytest.mock_globals(process_entries, get_user = get_user, PAGE_SIZE = page_size)
    
    output = await mocked(page_index, entries)
    
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    processed_entries, has_more = output
    vampytest.assert_instance(processed_entries, list)
    vampytest.assert_instance(has_more, bool)
    
    return output
