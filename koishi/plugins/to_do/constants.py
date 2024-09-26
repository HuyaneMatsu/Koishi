__all__ = ()

from re import compile as re_compile

from hata import BUILTIN_EMOJIS
from hata.ext.slash import Button, ButtonStyle, Form, P, TextInput, TextInputStyle


TO_DOS = {}


CUSTOM_ID_TO_DO_ADD = 'to_do.add.form'
CUSTOM_ID_TO_DO_DELETE_BASE = 'to_do.del'
CUSTOM_ID_TO_DO_EDIT_BASE = 'to_do.edit'

CUSTOM_ID_TO_DO_EDIT_RP = re_compile('to_do\\.edit\\.(\\d+)\\.form')
CUSTOM_ID_TO_DO_DELETE_RP = re_compile('to_do\\.del\\.(\\d+)\\.([01])')
ENTRY_BY_ID_RP = re_compile('#(\\d*)\\:?\s*')

PAGE_SIZE = 20

EMOJI_LEFT = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT = BUILTIN_EMOJIS['arrow_forward']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']

CUSTOM_ID_TO_DO_LIST_CLOSE = 'to-do.page.close'
create_custom_id_to_do_change_page = lambda query, page: f'to-do.page.{query}.{page}'
CUSTOM_ID_TO_DO_CHANGE_PAGE_RP = re_compile('to-do\\.page\\.([A-Za-z0-9\\+\\/\\=]+)?\\.(\\d+)')


TEXT_INPUT_NAME = TextInput(
    'Name',
    min_length = 2,
    max_length = 128,
    custom_id = 'name',
)

TEXT_INPUT_DESCRIPTION = TextInput(
    'Description',
    style = TextInputStyle.paragraph,
    min_length = 2,
    max_length = 1000,
    custom_id = 'description',
)


ADD_TO_DO_FORM = Form(
    'Add todo entry',
    [
        TEXT_INPUT_NAME,
        TEXT_INPUT_DESCRIPTION,
    ],
    custom_id = CUSTOM_ID_TO_DO_ADD,
)


DELETE_TO_DO_APPROVE = Button(
    'FATALITY',
    style = ButtonStyle.red,
    custom_id = f'{CUSTOM_ID_TO_DO_DELETE_BASE}.0',
)

DELETE_TO_DO_CANCEL = Button(
    'Nah.',
    style = ButtonStyle.blue,
    custom_id = f'{CUSTOM_ID_TO_DO_DELETE_BASE}.0',
)
