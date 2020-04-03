from hata import eventlist, Future
from hata.ext.commands import Command, ChooseMenu

TEST_COMMANDS=eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(TEST_COMMANDS)
    
def teardown(lib):
    Koishi.commands.unextend(TEST_COMMANDS)

@TEST_COMMANDS(category='TEST COMMANDS')
async def test_choose_menu_repr(client, message):
    '''
    Creates a ChooseMenu and returns it's repr.
    '''
    choices = ['nice', 'cat']
    choose_menu = await ChooseMenu(client, message.channel, choices, lambda *args:Future(client.loop))
    await client.message_create(message.channel,repr(choose_menu))
