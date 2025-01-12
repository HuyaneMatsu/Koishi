import vampytest
from hata import Embed

from ..embed_builders import build_failure_embed_insufficient_relationship_slots


def _iter_options():
    yield (
        5,
        2,
        7,
        Embed(
            'Insufficient relationship slots',
            (
                f'You do not have enough available relationship slots.\n'
                f'You have 7 relationship slots from which '
                f'5 is occupied by relationships and '
                f'2 is occupied by relationship requests.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_relationship_slots(
    relationship_count, relationship_request_count, relationship_slots
):
    """
    Tests whether ``build_failure_embed_insufficient_relationship_slots`` works as intended.
    
    Parameters
    ----------
    relationship_count : `int`
        How much relationships the user has.
    
    relationship_request_count : `int`
        How much relationship requests the user has.
    
    relationship_slots : `int`
        How much relationships the user can have.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_relationship_slots(
        relationship_count, relationship_request_count, relationship_slots
    )
    vampytest.assert_instance(output, Embed)
    return output
