import vampytest

from ...relationships_core import (
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_WAIFU
)

from ..relationship_listing_rendering_wide import produce_relationships_listing_page_wide


def _iter_options():
    yield (
        'single section',
        [
            (
                (
                    (
                        1,
                        RELATIONSHIP_TYPE_WAIFU,
                        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                    ),
                ),
                'Reisen',
            ),
        ],
        (
            '- Reisen - Waifu'
        ),
    )
    
    yield (
        'Single relationship type with 2 items',
        [
            (
                (
                    (
                        1,
                        RELATIONSHIP_TYPE_WAIFU,
                        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                    ),
                ),
                'Aya',
            ),
            (
                (
                    (
                        1,
                        RELATIONSHIP_TYPE_WAIFU,
                        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                    ),
                ),
                'Reisen',
            ),
        ],
        (
            '- Aya - Waifu\n'
            '- Reisen - Waifu'
        ),
    )
    
    yield (
        'multiple relationships',
        [
            (
                (
                    (
                        1,
                        RELATIONSHIP_TYPE_WAIFU,
                        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                    ),
                    (
                        3,
                        RELATIONSHIP_TYPE_MAMA,
                        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
                    ),
                ),
                'Reisen',
            ),
        ],
        (
            '- Reisen - Waifu & Mama (in law)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__produce_relationships_listing_page_wide(page):
    """
    Tests whether ``produce_relationships_listing_page_wide``
    
    Parameters
    ----------
    page : `list<(tuple<(int, int, int)>, str)>`
        The page to render.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_relationships_listing_page_wide(page)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
