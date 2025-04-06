import vampytest
from hata import Embed

from ...item_core import ITEM_FLAG_HEAD

from ..embed_builders import build_failure_embed_no_equipment_like 


def _iter_options():
    yield (
        ITEM_FLAG_HEAD,
        'pudding',
        Embed(
            'Oh no',
            'Cannot equip pudding as head accessory.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_no_equipment_like(item_flag, value):
    """
    Tests whether ``build_failure_embed_no_equipment_like`` works as intended.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    value : `str`
        The item's name to select.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_no_equipment_like(item_flag, value)
    vampytest.assert_instance(output, Embed)
    return output
