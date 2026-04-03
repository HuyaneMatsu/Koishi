import vampytest

from ..move_directions import MOVE_DIRECTION_EAST, MOVE_DIRECTION_NORTH, MOVE_DIRECTION_SOUTH, MoveDirections


def _assert_fields_set(move_directions):
    """
    Asserts whether the given move directions has all of tis fields set.
    
    Parameters
    ----------
    move_directions : ``MoveDirections``
    """
    vampytest.assert_instance(move_directions, MoveDirections)
    vampytest.assert_instance(move_directions.directions, set)


def test__MoveDirections__new():
    """
    Tests whether ``MoveDirections.__new__`` works as intended.
    """
    move_directions = MoveDirections()
    _assert_fields_set(move_directions)


def test__MoveDirections__repr():
    """
    Tests whether ``MoveDirections.__repr__`` works as intended.
    """
    move_directions = MoveDirections()
    
    output = repr(move_directions)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        [],
        [],
        True,
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
        ],
        [],
        False,
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
        ],
        [
            (MOVE_DIRECTION_EAST, True),
        ],
        False,
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
        ],
        [
            (MOVE_DIRECTION_NORTH, True),
        ],
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__MoveDirections__eq(items_0, items_1):
    """
    Tests whether ``MoveDirections.__eq__`` works as intended.
    
    Parameters
    ----------
    items_0 : `list<(int, bool)>`
        Direction items to set.
    
    items_1 : `list<(int, bool)>`
        Direction items to set.
    
    Returns
    -------
    output : `bool`
    """
    move_directions_0 = MoveDirections()
    for direction, value in items_0:
        move_directions_0.set(direction, value)
    
    move_directions_1 = MoveDirections()
    for direction, value in items_1:
        move_directions_1.set(direction, value)
    
    output = move_directions_0 == move_directions_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__set():
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
            (MOVE_DIRECTION_EAST, True),
        ],
        {
            MOVE_DIRECTION_NORTH,
            MOVE_DIRECTION_EAST,
        },
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
            (MOVE_DIRECTION_NORTH, False),
        ],
        set(),
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
            (MOVE_DIRECTION_NORTH, False),
            (MOVE_DIRECTION_NORTH, True),
        ],
        {
            MOVE_DIRECTION_NORTH,
        },
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, False),
        ],
        set(),
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
            (MOVE_DIRECTION_EAST, False),
        ],
        {
            MOVE_DIRECTION_NORTH,
        },
    )


@vampytest._(vampytest.call_from(_iter_options__set()).returning_last())
def test__MoveDirections__set(items):
    """
    Tests whether ``MoveDirections.set`` works as intended.
    
    Parameters
    ----------
    items : `list<(int, bool)>`
        Direction items to set.
    
    Returns
    -------
    output : `set<int>`
    """
    move_directions = MoveDirections()
    
    for direction, value in items:
        move_directions.set(direction, value)
    
    return move_directions.directions


def _iter_options__get():
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
            (MOVE_DIRECTION_EAST, True),
        ],
        MOVE_DIRECTION_NORTH,
        True,
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
            (MOVE_DIRECTION_EAST, True),
        ],
        MOVE_DIRECTION_EAST,
        True,
    )
    
    yield (
        [
            (MOVE_DIRECTION_NORTH, True),
            (MOVE_DIRECTION_EAST, True),
        ],
        MOVE_DIRECTION_SOUTH,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__get()).returning_last())
def test__MoveDirections__get(items, direction_to_get):
    """
    Tests whether ``MoveDirections.get`` works as intended.
    
    Parameters
    ----------
    items : `list<(int, bool)>`
        Direction items to get.
    
    direction_to_get : `int`
        Direction to get.
    
    Returns
    -------
    output : `bool`
    """
    move_directions = MoveDirections()
    
    for direction, value in items:
        move_directions.set(direction, value)
    
    output = move_directions.get(direction_to_get)
    vampytest.assert_instance(output, bool)
    return output
