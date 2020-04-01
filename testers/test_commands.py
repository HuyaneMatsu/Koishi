from hata import eventlist
from hata.ext.commands import Command

TEST_COMMANDS=eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(TEST_COMMANDS)
    
def teardown(lib):
    Koishi.commands.unextend(TEST_COMMANDS)
