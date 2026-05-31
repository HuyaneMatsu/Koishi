from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import InteractionForm, create_text_display

from ..component_building import build_to_do_delete_form
from ..to_do import ToDo


def _iter_options():
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605270002,
    )
    to_do.entry_id = 100
    
    yield (
        to_do,
        InteractionForm(
            'Are you sure to delete the following to-do?',
            [
                create_text_display(
                    f'## \\#100: shrimp',
                ),
            ],
            custom_id = f'to_do.delete.{100:x}',
        ),
    )
    
    to_do = ToDo(
        'shrimp',
        'fry',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605270003,
    )
    to_do.entry_id = 100
    
    yield (
        to_do,
        InteractionForm(
            'Are you sure to delete the following to-do?',
            [
                create_text_display(
                    f'## \\#100: shrimp',
                ),
                create_text_display(
                    'fry',
                ),
            ],
            custom_id = f'to_do.delete.{100:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_to_do_delete_form(to_do):
    """
    Tests whether ``build_to_do_delete_form`` works as intended.
    
    Parameters
    to_do : ``ToDo``
        Todo entry to delete.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_to_do_delete_form(to_do)
    vampytest.assert_instance(output, InteractionForm)
    return output
