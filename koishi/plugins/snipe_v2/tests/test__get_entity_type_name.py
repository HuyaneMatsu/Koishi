import vampytest
from hata import Emoji, SoundboardSound, Sticker

from ..content_building import get_entity_type_name


def _iter_options():
    yield (
        Emoji,
        'emoji',
    )
    
    yield (
        Sticker,
        'sticker',
    )
    
    yield (
        SoundboardSound,
        'sound',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_entity_type_name(entity_type):
    """
    Tests whether ``get_entity_type_name`` works as intended.
    
    Parameters
    ----------
    entity_type : ``type<Emoji | Sticker | SoundboardSound>``
        The type of the entity.
    
    Returns
    -------
    output : `str`
    """
    output = get_entity_type_name(entity_type)
    vampytest.assert_instance(output, str)
    return output
