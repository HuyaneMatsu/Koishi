import vampytest

from hata import InteractionForm, TextInputStyle, create_label, create_text_input

from ..component_building import build_to_do_create_form


def _iter_options():
    yield (
        InteractionForm(
            'Add todo entry',
            [
                create_label(
                    'Name',
                    component = create_text_input(
                        custom_id = 'name',
                        max_length = 128,
                        min_length = 2,
                    ),
                ),
                create_label(
                    'Description',
                    component = create_text_input(
                        custom_id = 'description',
                        max_length = 1000,
                        min_length = 0,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            custom_id = 'to_do.create',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_to_do_create_form():
    """
    Tests whether ``build_to_do_create_form`` works as intended.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_to_do_create_form()
    vampytest.assert_instance(output, InteractionForm)
    return output
