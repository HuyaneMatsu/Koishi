import vampytest

from ...relationships_core import (
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_WAIFU
)

from ..relationship_listing_rendering_legacy import produce_relationships_listing_page_legacy


def _iter_options():
    yield (
        'single section',
        [
            (
                RELATIONSHIP_TYPE_WAIFU,
                [
                    (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                ],
            ),
        ],
        (
            '### Waifu\n'
            '- Reisen'
        ),
    )
    
    yield (
        'single section, more elements',
        [
            (
                RELATIONSHIP_TYPE_WAIFU,
                [
                    (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Aya'),
                    (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                ],
            ),
        ],
        (
            '### Waifus\n'
            '- Aya\n'
            '- Reisen'
        ),
    )
    
    yield (
        'Multiple section',
        [
            (
                RELATIONSHIP_TYPE_MAMA,
                [
                    (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Aya'),
                ],
            ),
            (
                RELATIONSHIP_TYPE_WAIFU,
                [
                    (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                ],
            ),
        ],
        (
            '### Mama\n'
            '- Aya\n'
            '### Waifu\n'
            '- Reisen'
        ),
    )

    yield (
        'single section with modifier',
        [
            (
                RELATIONSHIP_TYPE_MAMA,
                [
                    (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW, 'Reisen'),
                ],
            ),
        ],
        (
            '### Mama\n'
            '- Reisen (in law)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__produce_relationships_listing_page_legacy(page):
    """
    Tests whether ``produce_relationships_listing_page_legacy``
    
    Parameters
    ----------
    page : `list<(int, list<(int, str)>)>`
        The page to render.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_relationships_listing_page_legacy(page)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
