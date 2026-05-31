from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import InteractionForm, TextInputStyle, create_label, create_text_input

from ..component_building import build_to_do_edit_form
from ..to_do import ToDo


def _iter_options():
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605270000,
    )
    to_do.entry_id = 100
    
    yield (
        to_do,
        InteractionForm(
            'Edit todo entry',
            [
                create_label(
                    'Name',
                    component = create_text_input(
                        custom_id = 'name',
                        max_length = 128,
                        min_length = 2,
                        value = 'shrimp',
                    ),
                ),
                create_label(
                    'Description',
                    component = create_text_input(
                        custom_id = 'description',
                        max_length = 1000,
                        min_length = 0,
                        style = TextInputStyle.paragraph,
                        value = None,
                    ),
                ),
            ],
            custom_id = f'to_do.edit.{100:x}',
        ),
    )
    
    to_do = ToDo(
        'shrimp',
        'fry',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605270001,
    )
    to_do.entry_id = 100
    
    yield (
        to_do,
        InteractionForm(
            'Edit todo entry',
            [
                create_label(
                    'Name',
                    component = create_text_input(
                        custom_id = 'name',
                        max_length = 128,
                        min_length = 2,
                        value = 'shrimp',
                    ),
                ),
                create_label(
                    'Description',
                    component = create_text_input(
                        custom_id = 'description',
                        max_length = 1000,
                        min_length = 0,
                        style = TextInputStyle.paragraph,
                        value = 'fry',
                    ),
                ),
            ],
            custom_id = f'to_do.edit.{100:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_to_do_edit_form(to_do):
    """
    Tests whether ``build_to_do_edit_form`` works as intended.
    
    Parameters
    ----------
    to_do : ``ToDo``
        Todo entry to edit.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_to_do_edit_form(to_do)
    vampytest.assert_instance(output, InteractionForm)
    return output
