import vampytest

from ...relationships_core import (
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_WAIFU
)

from ..relationship_listing_rendering_long import produce_relationships_listing_page_long


def _iter_options():
    yield (
        'single section',
        [
            (
                RELATIONSHIP_TYPE_WAIFU,
                RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                [
                    'Reisen',
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
                RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                [
                    'Aya',
                    'Reisen',
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
                RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                [
                    'Aya',
                ],
            ),
            (
                RELATIONSHIP_TYPE_WAIFU,
                RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                [
                    'Reisen',
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
                RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
                [
                    'Reisen',
                ],
            ),
        ],
        (
            '### Mama (in law)\n'
            '- Reisen'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__produce_relationships_listing_page_long(page):
    """
    Tests whether ``produce_relationships_listing_page_long``
    
    Parameters
    ----------
    page : `list<(int, int, list<(str)>)>`
        The page to render.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_relationships_listing_page_long(page)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
