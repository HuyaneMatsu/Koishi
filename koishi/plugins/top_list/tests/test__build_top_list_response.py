import vampytest
from hata import Embed, User
from hata.ext.slash import Button, InteractionResponse, Row

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..constants import (
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, CUSTOM_ID_PAGE_BASE, EMOJI_PAGE_PREVIOUS, PAGE_SIZE, STYLE_HEARTS,
    STYLE_NAME, STYLE_NUMBER
)
from ..interactions import build_top_list_response


def test__build_top_list_response():
    """
    Tests whether ``build_top_list_response`` works as intended.
    """
    page_index = 19
    
    user_0 = User.precreate(202309010000, name = 'okuu')
    user_1 = User.precreate(202309010001, name = 'orin')
    guild_id = 0
    
    entries = [
        (page_index * PAGE_SIZE + 1, 1111, user_0),
        (page_index * PAGE_SIZE + 2, 1112, user_1),
    ]
    
    output = build_top_list_response(page_index, entries, guild_id)
    
    
    vampytest.assert_eq(
        output,
        InteractionResponse(
            embed = Embed(
                f'{EMOJI__HEART_CURRENCY} Top-list {EMOJI__HEART_CURRENCY}',
                (
                    f'```ansi\n'
                    f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 1!s}.: {STYLE_HEARTS}{1111!s} {STYLE_NAME}okuu\n'
                    f'{STYLE_NUMBER}{page_index * PAGE_SIZE + 2!s}.: {STYLE_HEARTS}{1112!s} {STYLE_NAME}orin\n'
                    f'```'
                ),
            ).add_field(
                'Page',
                (
                    f'```\n'
                    f'{page_index + 1}\n'
                    f'```'
                ),
                True,
            ).add_field(
                'Sort order',
                (
                    f'```\n'
                    f'decreasing\n'
                    f'```'
                ),
                True,
            ),
            components = Row(
                Button(
                    f'Page {page_index}',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index - 1!s}',
                ),
                BUTTON_PAGE_NEXT_DISABLED.copy_with(
                    label = f'Page {page_index + 2}',
                ),
                BUTTON_CLOSE,
            ),
        ),
    )
