from base64 import b64encode as base64_encode
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata.ext.slash import Button, Row

from ..constants import (
    CUSTOM_ID_TO_DO_LIST_CLOSE, EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT, create_custom_id_to_do_change_page
)
from ..helpers import create_to_do_page_components
from ..to_do import ToDo


def test__create_to_do_page_components():
    """
    Tests whether ``create_to_do_page_components`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 20240919021
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id_0 = 143
    entry_id_1 = 144
    entry_id_2 = 145
    
    to_do_0 = ToDo(name, description, created_at, creator_id)    
    to_do_0.entry_id = entry_id_0
    to_do_1 = ToDo(name, description, created_at, creator_id)    
    to_do_1.entry_id = entry_id_1
    to_do_2 = ToDo(name, description, created_at, creator_id)    
    to_do_2.entry_id = entry_id_2
    
    value = 'hey mister'
    query = "" if value is None else base64_encode(value.encode()).decode()
    
    
    output = create_to_do_page_components([to_do_0, to_do_1, to_do_2], 1, value)
    vampytest.assert_instance(output, list)
    
    expected_output = [
        Row(
            Button(
                'Page 0',
                EMOJI_LEFT,
                custom_id = create_custom_id_to_do_change_page(query, 0),
                enabled = False,
            ),
            Button(
                'Page 2',
                EMOJI_RIGHT,
                custom_id = create_custom_id_to_do_change_page(query, 2),
                enabled = False,
            ),
            Button(
                None,
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_TO_DO_LIST_CLOSE,
            ),
        ),
    ]
    
    vampytest.assert_eq(output, expected_output)
