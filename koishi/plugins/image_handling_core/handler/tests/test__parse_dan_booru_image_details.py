import vampytest

from ...image_detail import ImageDetailProvided

from ..dan_booru import PROVIDER_DAN_BOORU, parse_dan_booru_image_details


def _iter_options():
    yield (
        None,
        None,
        None,
        None,
    )
    
    yield (
        [
            {
                'file_url': 'https://orindance.party/integer/hash.png',
                'tag_string': 'black_hat green_skirt touhou vest white_background',
            },
        ],
        None,
        None,
        [
            ImageDetailProvided(
                "https://orindance.party/integer/hash.png",
            ).with_provider(
                PROVIDER_DAN_BOORU,
            ).with_tags(
                frozenset(('black_hat', 'green_skirt', 'touhou', 'vest', 'white_background',))
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_dan_booru_image_details(data, tags_required, tags_banned):
    """
    Tests whether ``parse_dan_booru_image_details`` works as intended.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Data to parse from.
    
    tags_required : `None | frozenset<str>`
        Tags to enable.
    
    tags_banned : `None | frozenset<str>`
        Tags to disable.
    
    Returns
    -------
    output : ``None | list<ImageDetailProvided>``
    """
    output = parse_dan_booru_image_details(data, tags_required, tags_banned)
    
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ImageDetailProvided)
    
    return output
