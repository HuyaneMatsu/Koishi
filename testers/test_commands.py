from hata import eventlist
from hata.events import Command, checks

TEST_COMMANDS=eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(TEST_COMMANDS)
    
def teardown(lib):
    Koishi.commands.unextend(TEST_COMMANDS)
    
