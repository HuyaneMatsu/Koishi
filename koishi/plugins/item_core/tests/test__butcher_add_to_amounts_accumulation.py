import vampytest

from ..logic_butcher import butcher_add_to_amounts_accumulation


def _iter_options():
   item_id_0 = 8
   item_id_1 = 10
   
   yield (
       None,
       item_id_0,
       8,
       [
           (item_id_0, 8),
       ],
   )
   
   yield (
       [
           (item_id_0, 8),
           (item_id_1, 9),
       ],
       item_id_0,
       11,
       [
           (item_id_0, 19),
           (item_id_1, 9),
       ],
   )
   
   yield (
       [
           (item_id_0, 8),
           (item_id_1, 9),
       ],
       item_id_1,
       11,
       [
           (item_id_0, 8),
           (item_id_1, 20),
       ],
   )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__butcher_add_to_amounts_accumulation(butcher_amounts_accumulated, item_id, amount):
    """
    Tests whether ``butcher_add_to_amounts_accumulation`` works as intended.
    
    Parameters
    ----------
    butcher_amounts_accumulated : `None | list<(int, int)>`
        Already accumulated butchered items.
    
    item_id : `int`
        Item identifier to add.
    
    amount : `int`
        Amount to add.
    
    Returns
    -------
    output : `list<(int, int)>`
    """
    if (butcher_amounts_accumulated is not None):
        butcher_amounts_accumulated = butcher_amounts_accumulated.copy()
    
    output = butcher_add_to_amounts_accumulation(butcher_amounts_accumulated, item_id, amount)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 2)
        item_id, amount = element
        vampytest.assert_instance(item_id, int)
        vampytest.assert_instance(amount, int)
    
    return output
