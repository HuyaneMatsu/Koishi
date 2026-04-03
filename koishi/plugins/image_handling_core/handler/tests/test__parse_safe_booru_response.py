import vampytest

from ...image_detail import ImageDetailProvided

from ..safe_booru import PROVIDER_SAFE_BOORU, parse_safe_booru_response


def _iter_options():
    yield (
        '',
        (
            0,
            None,
        ),
    )
    
    yield (
        (
            '<posts count="29173" offset="0">\n'
                '<post '
                    'height="3508" '
                    'score="" '
                    'file_url="https://orindance.party/integer/hash.png" '
                    'parent_id="" '
                    'sample_url="https://orindance.party/samples/sample_hash.jpg" '
                    'sample_width="850" '
                    'sample_height="1202" '
                    'preview_url="https://orindance.party/thumbnails/thumbnail_hash.jpg" '
                    'rating="q" '
                    'tags=" black_hat green_skirt touhou vest white_background " '
                    'id="6025228" '
                    'width="2480" '
                    'change="1755912622" '
                    'md5="61818d29617c398b5a7f95a9404ad65d" '
                    'creator_id="168" '
                    'has_children="false" '
                    'created_at="Sat Aug 23 03:30:21 +0200 2025" '
                    'status="active" '
                    'source="https://orindance.party/miau" '
                    'has_notes="false" '
                    'has_comments="false" '
                    'preview_width="176" '
                    'preview_height="250"/>'
            '</posts>'
        ),
        (
            29173,
            [
                ImageDetailProvided(
                    "https://orindance.party/integer/hash.png",
                ).with_provider(
                    PROVIDER_SAFE_BOORU,
                ).with_tags(
                    frozenset(('black_hat', 'green_skirt', 'touhou', 'vest', 'white_background',))
                ),
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_safe_booru_response(data):
    """
    Tests whether ``parse_safe_booru_response`` works as intended.
    
    Parameters
    ----------
    data : `bytes`
        Data to parse.
    
    Returns
    -------
    output : ``(int, None | list<ImageDetailProvided>)``
    """
    output = parse_safe_booru_response(data)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], int)
    vampytest.assert_instance(output[1], list, nullable = True)
    if (output[1] is not None):
        for element in output[1]:
            vampytest.assert_instance(element, ImageDetailProvided)
    
    return output
