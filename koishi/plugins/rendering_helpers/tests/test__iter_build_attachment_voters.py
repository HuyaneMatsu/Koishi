import vampytest
from hata import User

from ..attachment_builders import iter_build_attachment_voters


def test__iter_build_attachment_voters__no_voters():
    """
    Tests whether ``iter_build_attachment_voters`` works as intended.
    
    Case: No voters.
    """
    down_voters = set()
    up_voters = set()
    guild = None
    
    output = [*iter_build_attachment_voters(down_voters, up_voters, guild)]
    vampytest.assert_eq(len(output), 0)


def test__iter_build_attachment_voters__with_voters():
    """
    Tests whether ``iter_build_attachment_voters`` works as intended.
    
    Case: With voters.
    """
    user_id_0 = 202402010005
    user_name_0 = 'koishi'
    
    user_id_1 = 202402010006
    user_name_1 = 'satori'
    
    user_id_2 = 202402010007
    user_name_2 = 'orin'
    
    user_id_3 = 202402010008
    user_name_3 = 'okuu'
        
    
    down_voters = {
        User.precreate(user_id_0, name = user_name_0),
        User.precreate(user_id_1, name = user_name_1),
    }
    up_voters = {
        User.precreate(user_id_2, name = user_name_2),
        User.precreate(user_id_3, name = user_name_3),
    }
    guild = None
    
    output = [*iter_build_attachment_voters(down_voters, up_voters, guild)]
    vampytest.assert_eq(len(output), 1)
    
    vampytest.assert_eq(
        output[0],
        (
            'voters.txt',
            (
                f'### Down voters\n'
                f'\n'
                f'1.: {user_name_0!s} ({user_id_0!s})\n'
                f'2.: {user_name_1!s} ({user_id_1!s})\n'
                f'\n'
                f'### Up voters\n'
                f'\n'
                f'1.: {user_name_2!s} ({user_id_2!s})\n'
                f'2.: {user_name_3!s} ({user_id_3!s})\n'
            ),
        ),
    )
