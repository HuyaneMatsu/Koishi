import vampytest
from hata import Embed

from ...item_core import ITEM_FLAG_HEAD

from ..embed_builders import build_failure_embed_empty_equipment_slot 


def _iter_options():
    yield (
        ITEM_FLAG_HEAD,
        Embed(
            'Oh no',
            f'You do not have any item equipped as head accessory.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_empty_equipment_slot(item_flag):
    """
    Tests whether ``build_failure_embed_empty_equipment_slot`` works as intended.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_empty_equipment_slot(item_flag)
    vampytest.assert_instance(output, Embed)
    return output
