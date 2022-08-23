__all__ = ()

from hata.ext.slash import Button, ButtonStyle, Form, Row, TextInput

from .constants import (
    CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID, CUSTOM_ID_MESSAGE_MOVER_CANCEL, CUSTOM_ID_MESSAGE_MOVER_CLOSE,
    CUSTOM_ID_MESSAGE_MOVER_SUBMIT
)


BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED = Button(
    'Submit',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_SUBMIT,
    style = ButtonStyle.green,
)

BUTTON_MESSAGE_MOVE_SUBMIT_DISABLED = BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED.copy_with(
    enabled = False,
)

BUTTON_MESSAGE_MOVE_ADD_BY_ID = Button(
    'Enter message id',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID,
    style = ButtonStyle.blue,
)

BUTTON_MESSAGE_MOVE_CANCEL = Button(
    'Cancel',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_CANCEL,
    style = ButtonStyle.red,
)

BUTTON_MESSAGE_MOVE_CLOSE = Button(
    'Close',
    custom_id = CUSTOM_ID_MESSAGE_MOVER_CLOSE,
    style = ButtonStyle.red,
)

MESSAGE_MOVER_COMPONENTS_ENABLED = Row(
    BUTTON_MESSAGE_MOVE_SUBMIT_ENABLED,
    BUTTON_MESSAGE_MOVE_ADD_BY_ID,
    BUTTON_MESSAGE_MOVE_CANCEL,
)

MESSAGE_MOVER_COMPONENTS_DISABLED = Row(
    BUTTON_MESSAGE_MOVE_SUBMIT_DISABLED,
    BUTTON_MESSAGE_MOVE_ADD_BY_ID,
    BUTTON_MESSAGE_MOVE_CANCEL,
)

MESSAGE_MOVER_COMPONENTS_AFTERLIFE = Row(
    BUTTON_MESSAGE_MOVE_CLOSE,
)

MESSAGE_MOVER_ADD_BY_ID_FORM = Form(
    'Add message by id to move group',
    [
        TextInput(
            'message\'s id',
            min_length = 7,
            max_length = 21,
            custom_id = 'message_id',
        )
    ],
    custom_id = CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID,
)
