__all__ = ()

from hata import ButtonStyle, Emoji, InteractionForm, create_button, create_row, create_text_input


MESSAGE_MOVER_CONTEXT_TIMEOUT = 600.0

MESSAGE_MOVER_CONTEXTS = {}


CUSTOM_ID_MESSAGE_MOVER_SUBMIT = 'message_mover.submit'
CUSTOM_ID_MESSAGE_MOVER_CANCEL = 'message_mover.cancel'
CUSTOM_ID_MESSAGE_MOVER_CLOSE = 'message_mover.close'
CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID = 'message_mover.add_by_id'


MESSAGE_MOVER_SUBMITTING_EMOJI = Emoji.precreate(704393708467912875)


BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED = create_button(
    'Submit',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_SUBMIT,
    style = ButtonStyle.green,
)

BUTTON_MESSAGE_MOVE_SUBMIT_DISABLED = BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED.copy_with(
    enabled = False,
)

BUTTON_MESSAGE_MOVE_ADD_BY_ID = create_button(
    'Enter message id',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID,
    style = ButtonStyle.blue,
)

BUTTON_MESSAGE_MOVE_CANCEL = create_button(
    'Cancel',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_CANCEL,
    style = ButtonStyle.red,
)

BUTTON_MESSAGE_MOVE_CLOSE = create_button(
    'Close',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_CLOSE,
    style = ButtonStyle.red,
)

MESSAGE_MOVER_COMPONENTS_ENABLED = create_row(
    BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED,
    BUTTON_MESSAGE_MOVE_ADD_BY_ID,
    BUTTON_MESSAGE_MOVE_CANCEL,
)

MESSAGE_MOVER_COMPONENTS_DISABLED = create_row(
    BUTTON_MESSAGE_MOVE_SUBMIT_DISABLED,
    BUTTON_MESSAGE_MOVE_ADD_BY_ID,
    BUTTON_MESSAGE_MOVE_CANCEL,
)

MESSAGE_MOVER_COMPONENTS_AFTERLIFE = create_row(
    BUTTON_MESSAGE_MOVE_CLOSE,
)

MESSAGE_MOVER_ADD_BY_ID_FORM = InteractionForm(
    'Add message by id to move group',
    [
        create_text_input(
            'message\'s id',
            min_length = 7,
            max_length = 21,
            custom_id = 'message_id',
        )
    ],
    custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID,
)
