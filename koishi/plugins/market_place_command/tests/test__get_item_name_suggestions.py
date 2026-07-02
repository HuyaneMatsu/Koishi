import vampytest

from ...item_core import ITEM_FLAG_COSTUME, ITEM_FLAG_EDIBLE, ITEM_ID_PEACH, get_item

from ..item_name_auto_completion import get_item_name_suggestions


def _iter_options():
    yield (
        0,
        None,
        [
            ('all', '0'),
            ('Aching affection\'s Heart-piercer', '2c'),
            ('Angelroot', '15'),
            ('Bamboo shoot', '1f'),
            ('Blood sausage', '6d'),
            ('Blueberries', '3'),
            ('Bluefrankish', '7'),
            ('Broom', '2e'),
            ('Bunny suit', '25'),
            ('Carrot', '8'),
            ('Chief maid\'s Elegant dress', '23'),
            ('Corpse voyager\'s Roguish dress', '29'),
            ('Dango', '40'),
            ('Devilcart oyster', '4'),
            ('Electrostatical discharge protective coat', '26'),
            ('Fishing rod', '6'),
            ('Flykiller amanita', '5'),
            ('Garlic', '9'),
            ('Gothic attire', '31'),
            ('Hand fan', '2f'),
            ('Hell cat\'s Big braids', '27'),
            ('Hiking set', '32'),
            ('Human Eye', '47'),
            ('Human Muscle', '46'),
            ('Human arm', '5d'),
        ],
    )
    
    yield (
        0,
        'peach',
        [
            (get_item(ITEM_ID_PEACH).name, format(ITEM_ID_PEACH, 'x')),
        ],
    )
    
    yield (
        0,
        format(ITEM_ID_PEACH, 'x'),
        [
            (get_item(ITEM_ID_PEACH).name, format(ITEM_ID_PEACH, 'x')),
        ],
    )
    
    yield (
        ITEM_FLAG_EDIBLE,
        None,
        [
            ('all', '0'),
            ('Angelroot', '15'),
            ('Bamboo shoot', '1f'),
            ('Blood sausage', '6d'),
            ('Blueberries', '3'),
            ('Bluefrankish', '7'),
            ('Carrot', '8'),
            ('Dango', '40'),
            ('Devilcart oyster', '4'),
            ('Flykiller amanita', '5'),
            ('Garlic', '9'),
            ('Human Eye', '47'),
            ('Human Muscle', '46'),
            ('Human blood', '51'),
            ('Human brain', '48'),
            ('Human cartilage', '52'),
            ('Human ear', '5a'),
            ('Human fat', '53'),
            ('Human heart', '4a'),
            ('Human intestines', '4c'),
            ('Human kidney', '50'),
            ('Human liver', '4b'),
            ('Human lung', '49'),
            ('Human nervous tissue', '56'),
            ('Human pancreas', '4e'),
        ],
    )
    
    yield (
        ITEM_FLAG_EDIBLE,
        'peach',
        [
            (get_item(ITEM_ID_PEACH).name, format(ITEM_ID_PEACH, 'x')),
        ],
    )
    
    yield (
        ITEM_FLAG_EDIBLE,
        format(ITEM_ID_PEACH, 'x'),
        [
            (get_item(ITEM_ID_PEACH).name, format(ITEM_ID_PEACH, 'x')),
        ],
    )
    
    yield (
        ITEM_FLAG_COSTUME,
        None,
        [
            ('all', '0'),
            ('Bunny suit', '25'),
            ('Chief maid\'s Elegant dress', '23'),
            ('Corpse voyager\'s Roguish dress', '29'),
            ('Electrostatical discharge protective coat', '26'),
            ('Gothic attire', '31'),
            ('Hiking set', '32'),
            ('Kimono', '33'),
            ('King\'s new clothes', '21'),
            ('Maid dress', '22'),
        ],
    )
    
    yield (
        ITEM_FLAG_COSTUME,
        'peach',
        None,
    )
    
    yield (
        ITEM_FLAG_COSTUME,
        format(ITEM_ID_PEACH, 'x'),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_item_name_suggestions(required_flags, value):
    """
    Tests whether ``get_item_name_suggestions`` works as intended.
    
    Parameters
    ----------
    required_flags : `int`
        Flags the item should have.
    
    value : `None | str`
        Value the user typed.
    
    Returns
    -------
    output : ``None | list<(str, str)>``
    """
    output = get_item_name_suggestions(required_flags, value)
    vampytest.assert_instance(output, list, nullable = True)
    return output
