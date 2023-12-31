__all__ = ('add_embed_provider',)


def add_embed_provider(embed, image_detail):
    """
    Adds the provider of the given image detail to the embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to add the provider to.
    image_detail : ``ImageDetail``
        The respective image detail.
    
    Returns
    -------
    embed : ``Embed``
    """
    provider = image_detail.provider
    if (provider is not None):
        embed.add_footer(
            f'Image provided by {provider}'
        )

    return embed
