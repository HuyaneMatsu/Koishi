import vampytest

from ...tile_bit_masks import (
    BIT_MASK_CHARACTER, BIT_MASK_FLOOR, BIT_FLAG_NORTH, BIT_MASK_OBSTACLE
)

from ..history_element import (
    JSON_KEY_HISTORY_ELEMENT_CHANGES, JSON_KEY_HISTORY_ELEMENT_POSITION, JSON_KEY_HISTORY_ELEMENT_WAS_SKILL,
    HistoryElement
)

def _assert_fields_set(history_element):
    """
    Asserts whether the given history element has all of its fields set.
    
    Parameters
    ----------
    history_element : ``HistoryElement``
        The history element to check.
    """
    vampytest.assert_instance(history_element, HistoryElement)
    vampytest.assert_instance(history_element.changes, tuple)
    vampytest.assert_instance(history_element.position, int)
    vampytest.assert_instance(history_element.was_skill, bool)


def test__HistoryElement__new():
    """
    Tests whether ``HistoryElement.__new__`` works as intended.
    """
    position = 10
    was_skill = True
    changes = (
        (10, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
        (10, BIT_MASK_OBSTACLE),
    )
    
    history_element = HistoryElement(
        position,
        was_skill,
        changes,
    )
    _assert_fields_set(history_element)
    
    vampytest.assert_eq(history_element.changes, changes)
    vampytest.assert_eq(history_element.was_skill, was_skill)
    vampytest.assert_eq(history_element.changes, changes)


def test__HistoryElement__repr():
    """
    Tests whether ``HistoryElement.__repr__`` works as intended.
    """
    position = 10
    was_skill = 10
    changes = (
        (10, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
        (11, BIT_MASK_OBSTACLE),
    )
    
    history_element = HistoryElement(
        position,
        was_skill,
        changes,
    )
    
    output = repr(history_element)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    position = 10
    was_skill = True
    changes = (
        (10, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
        (11, BIT_MASK_OBSTACLE),
    )
    
    keyword_parameters = {
        'position': position,
        'was_skill': was_skill,
        'changes': changes,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'position': 11,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'was_skill': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'changes': (
                (11, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
                (12, BIT_MASK_OBSTACLE),
            )
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__HistoryElement__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``HistoryElement.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    history_element_0 = HistoryElement(**keyword_parameters_0)
    history_element_1 = HistoryElement(**keyword_parameters_1)
    
    output = history_element_0 == history_element_1
    vampytest.assert_instance(output, bool)
    return output


def test__HistoryElement__from_data():
    """
    Tests whether ``HistoryElement.from_data`` works as intended.
    """
    position = 10
    was_skill = True
    changes = (
        (10, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
        (10, BIT_MASK_OBSTACLE),
    )
    
    data = {
        JSON_KEY_HISTORY_ELEMENT_POSITION: position,
        JSON_KEY_HISTORY_ELEMENT_WAS_SKILL: was_skill,
        JSON_KEY_HISTORY_ELEMENT_CHANGES: [[*change] for change in changes],
    }
    
    history_element = HistoryElement.from_data(data)
    _assert_fields_set(history_element)
    
    vampytest.assert_eq(history_element.changes, changes)
    vampytest.assert_eq(history_element.was_skill, was_skill)
    vampytest.assert_eq(history_element.changes, changes)


def test__HistoryElement__to_data():
    """
    Tests whether ``HistoryElement.from_data`` works as intended.
    """
    position = 10
    was_skill = True
    changes = (
        (10, BIT_MASK_FLOOR | BIT_MASK_CHARACTER | BIT_FLAG_NORTH),
        (10, BIT_MASK_OBSTACLE),
    )
    
    history_element = HistoryElement(
        position,
        was_skill,
        changes,
    )
    
    vampytest.assert_eq(
        history_element.to_data(),
        {
            JSON_KEY_HISTORY_ELEMENT_POSITION: position,
            JSON_KEY_HISTORY_ELEMENT_WAS_SKILL: was_skill,
            JSON_KEY_HISTORY_ELEMENT_CHANGES: changes,
        },
    )
