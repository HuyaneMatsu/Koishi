# -*- coding: utf-8 -*-
import re
from threading import Lock as SyncLock

from collections import deque

from hata import Embed, Lock, Task, alchemy_incendiary, KOKORO
from hata.ext.commands import Pagination, wait_for_message
from hata.backend.futures import _ignore_frame

_ignore_frame(__spec__.origin, '__call__',
    'await client.loop.run_in_executor(alchemy_incendiary(exec,(code_object,self.locals),),)')


#emulates a file
class InterpreterPrinter(object):
    __slots__=('lock','buffer',)
    def __init__(self):
        self.lock=SyncLock()
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
            raise ValueError('wrap start and wrap end are longer than the limit-ignore itself')
        
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

class InterpreterInputter(object):
    def __init__(self,owner):
        self.owner=owner
        self.client=None
        self.channel=None
        
    def __call__(self,promt=None):
        client=self.client
        channel=self.channel
        if (client is None) or (channel is None):
            raise RuntimeError(f'{self.__class__.__name__} has no linked `.client` or `.channel`')
        
        printer=self.owner.printer
        if promt is not None:
            if not isinstance(promt,str):
                promt=str(promt)
            printer.write(promt)
        
        if printer:
            pages=[]
            while printer:
                pages.append(Embed('Waiting for input (timeout 5 min):',printer.get_value()))
            
            amount=len(pages)
            for index,embed in enumerate(pages,1):
                embed.add_footer(f'page {index}/{amount}')
        
        else:
            pages=[Embed('Waiting for input (timeout 5 min):')]
        
        with client.loop.enter():
            task=Task(Pagination(client,channel,pages,300.),client.loop)
            future=wait_for_message(client,channel,self.check_is_owner,300.)
        
        task.syncwrap().wait()
        try:
            message=future.syncwrap().wait()
        except TimeoutError:
            raise SystemExit from None
        
        return message.content
    
    def set(self,client,channel):
        self.client=client
        self.channel=channel
    
    def check_is_owner(self,message):
        return self.client.is_owner(message.author)
    
LINE_START=re.compile('[ \t]*')
BLOCK_START=re.compile('(```|`|)(.*?)?(```|`|)')
PYTHON_RP=re.compile('(?:python|py|)[ \t]*',re.I)
ENDER_1_RP=re.compile('[^\\\]`')
ENDER_3_RP=re.compile('[^\\\]```')

def parse_code_content(content1, content2, no_code_output=None):
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
            return no_code_output,True
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
        return no_code_output,True
    
    return '\n'.join(lines), False

class Interpreter(object):
    __slots__=('inputter', 'locals', 'lock', 'printer',)
    def __init__(self,locals_):
        self.lock=Lock(KOKORO)
        
        printer=InterpreterPrinter()
        locals_['print']=printer
        self.printer=printer
        
        inputter=InterpreterInputter(self)
        locals_['input']=inputter
        self.inputter=inputter
        
        self.locals=locals_
        
    async def __call__(self,client,message,content):
        if not client.is_owner(message.author):
            await client.message_create(message.channel,'You are not my boss!')
            return
        
        if self.lock.locked():
            await client.message_create(message.channel,'An execution is already running.')
            return
        
        self.inputter.set(client,message.channel)
        
        async with self.lock:
            result, is_exception = parse_code_content(content, message.content, 'No code to execute.')
            if is_exception:
                await client.message_create(message.channel, embed=Embed('Parsing error',result))
                return
            
            printer=self.printer
            
            try:
                code_object=compile(result,'online_interpreter','exec')
            except SyntaxError as err:
                printer.write(f'{err.__class__.__name__} at line {err.lineno}: {err.msg}\n{result[err.lineno-1]}\n{" "*(err.offset-1)}^')
            else:
                try:
                    await client.loop.run_in_executor(alchemy_incendiary(exec,(code_object,self.locals),),)
                except BaseException as err:
                    await client.loop.render_exc_async(err,file=printer)
            
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


del re
del _ignore_frame
