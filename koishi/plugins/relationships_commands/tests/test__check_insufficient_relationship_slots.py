import vampytest
from hata import Component, create_button, create_row, create_text_display

from ..checks import check_insufficient_relationship_slots


def _iter_options():
    yield (
        0,
        0,
        1,
        False,
        None,
    )
    
    yield (
        5,
        0,
        6,
        False,
        None,
    )
    
    yield (
        0,
        5,
        6,
        False,
        None,
    )
    
    yield (
        5,
        5,
        11,
        False,
        None,
    )
    
    yield (
        6,
        0,
        6,
        False,
        [
            create_text_display(
                f'You do not have enough available relationship slots.\n'
                f'You have 6 relationship slots from which '
                f'6 is occupied by relationships and '
                f'0 is occupied by relationship requests.'
            ),
            create_row(
                create_button(
                    'I want some More! More!',
                    custom_id = f'user.buy_relationship_slots.invoke.{0:x}',
                ),
            )
        ],
    )
    
    yield (
        6,
        0,
        6,
        True,
        None,
    )
    
    yield (
        0,
        6,
        6,
        False,
        [
            create_text_display(
                f'You do not have enough available relationship slots.\n'
                f'You have 6 relationship slots from which '
                f'0 is occupied by relationships and '
                f'6 is occupied by relationship requests.'
            ),
            create_row(
                create_button(
                    'I want some More! More!',
                    custom_id = f'user.buy_relationship_slots.invoke.{0:x}',
                ),
            )
        ],
    )
    
    yield (
        5,
        6,
        11,
        False,
        [
            create_text_display(
                f'You do not have enough available relationship slots.\n'
                f'You have 11 relationship slots from which '
                f'5 is occupied by relationships and '
                f'6 is occupied by relationship requests.'
            ),
            create_row(
                create_button(
                    'I want some More! More!',
                    custom_id = f'user.buy_relationship_slots.invoke.{0:x}',
                ),
            )
        ],
    )
    
    yield (
        6,
        5,
        11,
        False,
        [
            create_text_display(
                f'You do not have enough available relationship slots.\n'
                f'You have 11 relationship slots from which '
                f'6 is occupied by relationships and '
                f'5 is occupied by relationship requests.'
            ),
            create_row(
                create_button(
                    'I want some More! More!',
                    custom_id = f'user.buy_relationship_slots.invoke.{0:x}',
                ),
            )
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_insufficient_relationship_slots(
    relationship_count, relationship_request_count, relationship_slots, already_related
):
    """
    Tests whether ``check_insufficient_relationship_slots`` works as intended.
    
    Parameters
    ----------
    relationship_count : `int`
        How much relationships the user has.
    
    relationship_request_count : `int`
        How much relationship requests the user has.
    
    relationship_slots : `int`
        How much relationships the user can have.
    
    already_related : `bool`
        Whether the two users are already related.
    
    Returns
    -------
    output : ``None | list<Component>``
    """
    output = check_insufficient_relationship_slots(
        relationship_count, relationship_request_count, already_related, relationship_slots
    )
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Component)
    
    return output
