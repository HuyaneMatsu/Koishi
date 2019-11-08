from collections import deque
from code import InteractiveConsole
from hata.embed import Embed
from hata.futures import render_exc_to_list
from hata.events import Pagination
from hata.dereaddons_local import alchemy_incendiary
from threading import Lock
import re

from help_handler import KOISHI_HELP_COLOR, KOISHI_HELPER

#emulates a file
class InterpreterPrinter(object):
    __slots__=('lock','buffer',)
    def __init__(self):
        self.lock=Lock()
        self.buffer=deque()

    def write(self,value):
        with self.lock:
            self.buffer.append(value)

    def writelines(self,lines):
        with self.lock:
            self.buffer.extend(lines)

    def __bool__(self):
        with self.lock:
            if self.buffer:
                return True
            return False

    def __len__(self):
        with self.lock:
            ln=0
            for value in self.buffer:
                ln+=value.__len__()
            return ln

    def __call__(self,*args,**kwargs):
        kwargs['file']=self
        print(*args,**kwargs)

    def get_value(self,wrap_start='```',wrap_end='```',limit=2000,ignore=50):
        limit=limit-len(wrap_start)-len(wrap_end)-2 #allocate 2 more for linebreaks
        if limit<=ignore:
            raise ValueError('wrap start and wrap end are longer than the limir-ignore itself')

        result=[wrap_start,'\n']
        buffer=self.buffer

        with self.lock:
            while buffer:
                value=buffer[0]
                if value=='\n':
                    del buffer[0]
                    continue
                break

            while buffer:
                value=buffer[0]
                ln=len(value)

                if not value:
                    del buffer[0]
                    continue

                if ln<limit:
                    del buffer[0]
                    result.append(value)
                    limit-=ln
                    continue

                if limit<ignore:
                    while result:
                        value=result[-1]
                        if value=='\n':
                            del result[-1]
                            continue
                        break
                    if limit>ignore:
                        continue
                    break

                lines=value.split('\n')
                if len(lines)>1:
                    index=len(lines)-1
                    del buffer[0]
                    while True:
                        buffer.appendleft(lines[index])
                        if index:
                            buffer.appendleft('\n')
                            index-=1
                            continue
                        break
                    continue

                limit=limit-20
                if limit<ignore:
                    while result:
                        value=result[-1]
                        if value=='\n':
                            del result[-1]
                            continue
                        break
                    if limit>ignore:
                        continue
                    break

                result.append(value[:limit])
                buffer[0]=value[limit:]
                result.append('\n*line truncated*...')
                break

        if result[-1][-1]!='\n':
            result.append('\n')
        result.append(wrap_end)

        return ''.join(result)

LINE_START=re.compile('[ \t]*')
BLOCK_START=re.compile('(```|`|)(.*?)?(```|`|)')
PYTHON_RP=re.compile('(?:python|py|)[ \t]*',re.I)
ENDER_1_RP=re.compile('[^\\\]`')
ENDER_3_RP=re.compile('[^\\\]```')

def parse_content(content1,content2):
    #if second line is set we ignore the 1st
    line_break_index=content2.find('\n')
    if line_break_index==-1:
        if content1:
            starter,center,ender=BLOCK_START.fullmatch(content1).groups()
            if starter:
                if ender:
                    if starter!=ender:
                        return 'inlined 1 code line starter should be same long as it\'s ender.',True
                    else:
                        lines=[center]
                else:
                    return 'Inlined 1 code line, but has no ender.',True
            else:
                if ender:
                    return 'Inlined 1 code line with ender, but it has no starter.',True
                else:
                    lines=[center]
        else:
            return 'No code to execute.',True
    else:
        lines=content2.splitlines()
        del lines[0]
        line=lines[0]
        starter,center,ender=BLOCK_START.fullmatch(line).groups()
        if starter:
            if ender:
                if starter!=ender:
                    return '1 code line starter should be same long as it\'s ender.',True
                else:
                    lines=[center]
            else:
                lang_match=PYTHON_RP.fullmatch(center)
                if lang_match is None:
                    return 'Invalid langauge',True
                else:
                    del lines[0]
                    if len(starter)==1:
                        pattern=ENDER_1_RP
                    else: #3
                        pattern=ENDER_3_RP
                    index=0
                    ln=len(lines)
                    while index<ln:
                        line=lines[index]
                        if line.startswith(starter):
                            del lines[index:]
                            break
                        matched=pattern.search(line)
                        if matched is None:
                            index=index+1
                            continue
                        line=line[:matched.start()+1]
                        lines[index]=line
                        index+=1
                        del lines[index:]
                        break
                    else:
                        return 'Code block was never ended.',True
                    
    index=len(lines)
    while index:
        index=index-1
        line=lines[index]
        start=LINE_START.match(line).end()
        if start!=len(line) and line[0]!='#':
            continue

        del lines[index]

    if not lines:
        return 'No code to execute.',True

    parts=['try:']

    ln=len(lines)
    while index<ln:
        line=lines[index]
        parts.append('\n  ')
        parts.append(line)
        index+=1

    parts.append('\nexcept BaseException:\n  import traceback\n  traceback.print_exc(file=print)\n')

    return ''.join(parts),False

class Interpreter(object):
    __slots__=('console','printer',)
    def __init__(self,locals_):
        printer=InterpreterPrinter()
        locals_['print']=printer
        self.printer=printer
        self.console=InteractiveConsole(locals_)

    async def __call__(self,client,message,content):
        if not client.is_owner(message.author):
            await client.message_create(message.channel,'You are not my boss!')
            return

        code_block,except_=parse_content(content,message.content)
        if except_:
            await client.message_create(message.channel,embed=Embed('Parsing error',code_block))
            return

        printer=self.printer

        try:
            code_object=compile(code_block,'online_interpreter','exec')
            await client.loop.run_in_executor(alchemy_incendiary(self.console.runcode,(code_object,),),)
        except BaseException as err:
            extracted=[
                'Exception occured at ',
                self.__class__.__name__,
                '.__call__\nTraceback (most recent call last):\n',
                    ]
            render_exc_to_list(err,extend=extracted)
            printer.write(''.join(extracted))

        if printer:
            pages=[]
            while printer:
                pages.append(Embed('Output:',printer.get_value()))

            amount=len(pages)
            for index,embed in enumerate(pages,1):
                embed.add_footer(f'page {index}/{amount}')

        else:
            pages=[Embed('No output')]
        await Pagination(client,message.channel,pages,240.)


async def _help_execute(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('execute',(
        'Use an interpreter trough me :3\n'
        'Usages:\n'
        f'{prefix}execute #code here\n'
        '*not code*\n'
        '\n'
        f'{prefix}execute\n'
        '#code goes here\n'
        '#code goes here\n'
        '\n'
        f'{prefix}execute\n'
        '```\n'
        '#code goes here\n'
        '#code goes here\n'
        '```\n'
        '*not code*'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('execute',_help_execute,KOISHI_HELPER.check_is_owner)


del re
