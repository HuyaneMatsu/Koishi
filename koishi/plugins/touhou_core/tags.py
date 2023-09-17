__all__ = ('parse_touhou_characters_from_tags', )

from scarletio import call

from .safe_booru_tags import TOUHOU_SAFE_BOORU_TAGS


TAG_TO_CHARACTER = {}


@call
def populate_tag_map():
    """
    Populates ``TAG_TO_CHARACTER``.
    """
    for character, tags in TOUHOU_SAFE_BOORU_TAGS.items():
        for tag in tags:
            TAG_TO_CHARACTER[tag] = character


def parse_touhou_characters_from_tags(image_detail):
    """
    Parses out the touhou characters from the given image detail's tags.
    
    Parameters
    ----------
    image_detail : ``ImageDetail``
        The image detail to parse its tag of.
    
    Returns
    -------
    characters : `set<TouhouCharacter>`
        The parsed out characters.
    """
    characters = set()
    
    tags = image_detail.tags
    if (tags is not None):
        for tag in tags:
            try:
                character = TAG_TO_CHARACTER[tag]
            except KeyError:
                pass
            else:
                characters.add(character)
    
    return characters
