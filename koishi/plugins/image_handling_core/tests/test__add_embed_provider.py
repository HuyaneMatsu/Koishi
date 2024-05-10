import vampytest
from hata import Embed

from ...image_handling_core import ImageDetailBase, ImageDetailProvided, ImageDetailStatic

from ..embed_building_helpers import add_embed_provider


def _iter_options():
    yield (
        ImageDetailBase(
            'https://orindance.party/',
        ),
        Embed()
    )
    
    yield (
        ImageDetailProvided(
            'https://orindance.party/',
        ).with_provider(
            'miau'
        ),
        Embed().add_footer(
            f'Image provided by miau.'
        )
    )
    
    yield (
        ImageDetailStatic(
            'https://orindance.party/',
        ).with_creator(
            'miau'
        ),
        Embed().add_footer(
            'By miau.'
        ),
    )
    
    yield (
        ImageDetailStatic(
            'https://orindance.party/',
        ).with_creators(
            'miau', 'meow'
        ),
        Embed().add_footer(
            'By meow & miau.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_embed_provider(image_detail):
    """
    Adds the provider of the given image detail to the embed.
    
    Parameters
    ----------
    image_detail : ``ImageDetailBase``
        Image detail to work with.
    
    Returns
    -------
    output : ``Embed``
    """
    embed = Embed()
    output = add_embed_provider(embed, image_detail)
    vampytest.assert_instance(output, Embed)
    return output
