import vampytest
from hata import User
from ..interactions import make_response
from hata.ext.slash import InteractionResponse, Row, Button
from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..constants import STYLE_HEARTS, STYLE_NAME, STYLE_NUMBER, STYLE_RESET, \
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, CUSTOM_ID_PAGE_BASE, \
    EMOJI_PAGE_PREVIOUS, PAGE_SIZE



async def test__make_response():
    """
    Tests whether ``make_response`` works as intended.
    """
    page_index = 19
    
    user_0 = User.precreate(202308230016, name = 'okuu')
    user_1 = User.precreate(202308230017, name = 'orin')
    
    async def get_top_list_entries(page_index_parameter):
        nonlocal page_index
        vampytest.assert_eq(page_index, page_index_parameter)
        
        return [
            (user_0.id, 1111),
            (user_1.id, 1112),
        ]
    
    
    async def get_user(user_id):
        vampytest.assert_in(user_id, (user_0.id, user_1.id))
        
        return User.precreate(user_id)
    
    
    mocked = vampytest.mock_globals(
        make_response,
        get_top_list_entries = get_top_list_entries,
        get_user = get_user,
    )
    
    output = await mocked(page_index)
    
    vampytest.assert_eq(
        output,
        InteractionResponse(
            content = (
                f'{EMOJI__HEART_CURRENCY} **Top-list** {EMOJI__HEART_CURRENCY} *[Page {page_index + 1!s}]*\n'
                f'```ansi\n'
                f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 1!s}{STYLE_RESET}.: {STYLE_HEARTS}{1111!s} {STYLE_NAME}okuu\n'
                f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 2!s}{STYLE_RESET}.: {STYLE_HEARTS}{1112!s} {STYLE_NAME}orin\n'
                f'```'
            
            ),
            components = Row(
                Button(
                    emoji = EMOJI_PAGE_PREVIOUS,
                    custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index - 1!s}',
                ),
                BUTTON_PAGE_NEXT_DISABLED,
                BUTTON_CLOSE,
            ),
        ),
    )
