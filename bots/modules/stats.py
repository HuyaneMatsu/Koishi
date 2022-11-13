__all__ = ()

import os, sys
IS_PYPY = (sys.implementation.name == 'pypy')

if IS_PYPY:
    from gc import get_stats as get_gc_stats

from datetime import datetime
from threading import enumerate as list_threads, _MainThread as MainThreadType

from scarletio import EventThread, ExecutorThread
from hata import Client, Embed, Color, elapsed_time
from hata.ext.commands_v2 import checks

from bot_utils.models import DB_ENGINE
from bot_utils.cpu_info import CpuUsage, psutil, PROCESS, PROCESS_PID, CPU_MAX_FREQUENCY

STAT_COLOR = Color.from_rgb(61, 255, 249)

COMMAND_CLIENT: Client
COMMAND_CLIENT.command_processor.create_category('STATS', checks=checks.owner_only())


def thread_count_type_item_sort_key(item):
    return item[1]

@COMMAND_CLIENT.commands.from_class
class threads:
    async def command(client, message):
        thread_count_by_type = {}
        thread_count = 0
        
        for thread in list_threads():
            thread_count += 1
            thread_type = thread.__class__
            thread_count_by_type[thread_type] = thread_count_by_type.get(thread_type,0) + 1
        
        description = []
        
        main_thread_count = thread_count_by_type.pop(MainThreadType, 0)
        event_thread_count = thread_count_by_type.pop(EventThread, 0)
        
        event_loop_executor_count = 0
        
        add_space = False
        
        if main_thread_count or event_thread_count:
            add_space = True
            description.append('**Main threads**:\n')
            
            if main_thread_count:
                description.append('Main threads: ')
                description.append(repr(main_thread_count))
                description.append('\n')
            
            if event_thread_count:
                description.append('Event threads: ')
                description.append(repr(event_thread_count))
                description.append('\n')
                
                for thread in list_threads():
                    if type(thread) is EventThread:
                        event_loop_executor_count += thread.used_executor_count + thread.free_executor_count
            
            description.append(
                f'--------------------\n'
                f'Total: {main_thread_count + event_thread_count}'
            )
        
        
        executor_thread_count = thread_count_by_type.pop(ExecutorThread, 0)
        if executor_thread_count:
            if add_space:
                description.append('\n\n')
            else:
                add_space = True
            
            other_executors = executor_thread_count
            
            description.append('**Executors:**\n')
            
            if event_loop_executor_count:
                other_executors -=event_loop_executor_count
                description.append('Event thread executors: ')
                description.append(repr(event_loop_executor_count))
                description.append('\n')
            
            if DB_ENGINE.uses_single_worker:
                other_executors -=1
                description.append('Database engine worker: 1\n')
            
            if other_executors>0:
                description.append('Other executors: ')
                description.append(repr(other_executors))
                description.append('\n')
            
            description.append(
                f'--------------------\n'
                f'Total: {executor_thread_count}'
            )
        
        if thread_count_by_type:
            if add_space:
                description.append('\n\n')
            else:
                add_space = True
            
            description.append('**Other thread types**:\n')
            
            thread_count_by_type = sorted(thread_count_by_type.items(), key = thread_count_type_item_sort_key)
            
            total_leftover = 0
            for item in thread_count_by_type:
                total_leftover +=item[1]
            
            displayed_thread_types_count = 0
            non_displayed_thread_count = total_leftover
            
            while True:
                if non_displayed_thread_count == 0:
                    break
                
                if displayed_thread_types_count == 10:
                    description.append('Other: ')
                    description.append(repr(non_displayed_thread_count))
                    description.append('\n')
                    break
                
                type_, count = thread_count_by_type.pop()
                non_displayed_thread_count-=count
                
                thread_type_name = type_.__name__
                if len(thread_type_name) > 32:
                    thread_type_name = thread_type_name[:32]+'...'
                
                description.append(thread_type_name)
                description.append(': ')
                description.append(repr(count))
                description.append('\n')
            
            description.append('--------------------\nTotal: ')
            description.append(repr(total_leftover))
        
        if add_space:
            description.append('\n\n**--------------------**\n')
        
        description.append('**Total**: ')
        description.append(repr(thread_count))
        
        embed = Embed('Threads', ''.join(description), color = STAT_COLOR)
        
        await client.message_create(message.channel, embed = embed)
    
    category = 'STATS'
    
    async def description(command_context):
        return Embed('threads',(
            'Just shows how my threads are doing.\n'
            f'Usage: `{command_context.prefix}threads`'
            ), color = STAT_COLOR).add_footer(
                'Owner only!')

if IS_PYPY:
    @COMMAND_CLIENT.commands.from_class
    class gc_stats:
        async def command(client, message):
            stats = get_gc_stats()
            
            embed = Embed(None,
                '**Total memory consumed:**\n'
                f'GC used: {stats.total_gc_memory} (peak: {stats.peak_memory})\n'
                f'In arenas: {stats.total_arena_memory}\n'
                f'Rawmalloced: {stats.total_rawmalloced_memory}\n'
                f'Nursery: {stats.nursery_size}\n'
                f'Jit backend used: {stats.jit_backend_used}\n'
                '----------------------------\n'
                f'Total: {stats.memory_used_sum}\n'
                '\n'
                f'**Total memory allocated:**\n'
                f'GC allocated: {stats.total_allocated_memory} (peak: {stats.peak_allocated_memory})\n'
                f'In arenas: {stats.peak_arena_memory}\n'
                f'Rawmalloced: {stats.peak_rawmalloced_memory}\n'
                f'Nursery: {stats.nursery_size}\n'
                f'Jit backend allocated: {stats.jit_backend_allocated}\n'
                '----------------------------\n'
                f'Total: {stats.memory_allocated_sum}\n'
                '\n'
                f'Total time spent in GC: {stats.total_gc_time / 1000.0:.3f}',
                  color = STAT_COLOR)
            
            await client.message_create(message.channel, embed = embed)
        
        aliases = ['gc', 'gc-info',]
        category = 'STATS'
        
        async def description(command_context):
            return Embed('gc-stats',(
                'Garbage collector info to check memory usage.\n'
                f'Usage: `{command_context}gc-stats`'
                ), color = STAT_COLOR).add_footer(
                    'Owner only!')


if (CpuUsage is not None):
    @COMMAND_CLIENT.commands.from_class
    class system_stats:
        aliases = ['system', 'process', 'process-stats']
        
        async def command(client, message):
            await client.typing(message.channel)
            
            process_cpu_usage = await CpuUsage()
            
            description = []
            
            description.append('**System info**:\n' \
                               'Platform: ')
            description.append(sys.platform)
            description.append('\n' \
                               'Cores: ')
            description.append(repr(psutil.cpu_count(logical=False)))
            description.append('\n' \
                               'Threads: ')
            description.append(repr(psutil.cpu_count(logical=True)))
            description.append('\n' \
                               'Max CPU frequency: ')
            description.append(CPU_MAX_FREQUENCY.__format__('.2f'))
            description.append('MHz\n\n' \
                               '**Memory and swap**:\n' \
                               'Memory total: ')
            memory = psutil.virtual_memory()
            description.append((memory.total / (1 << 20)).__format__('.2f'))
            description.append('MB\n' \
                               'Memory used: ')
            description.append((memory.used / (1 << 20)).__format__('.2f'))
            description.append('MB\n' \
                               'Memory percent: ')
            description.append(memory.percent.__format__('.2f'))
            description.append('%\n' \
                               'Swap total: ')
            swap = psutil.swap_memory()
            description.append((swap.total / (1 << 20)).__format__('.2f'))
            description.append('MB\n' \
                               'Swap used: ')
            description.append((swap.used / (1 << 20)).__format__('.2f'))
            description.append('MB\n' \
                               'Swap percent: ')
            description.append(swap.percent.__format__('.2f'))
            description.append('%\n' \
                               '\n' \
                               '**Process info**:\n' \
                               'Name: ')
            description.append(PROCESS.name())
            description.append('\n' \
                               'PID: ')
            description.append(repr(PROCESS_PID))
            description.append('\n' \
                               'File descriptor count: ')
            description.append(repr(PROCESS.num_fds()))
            description.append('\n' \
                               'Thread count: ')
            description.append(repr(PROCESS.num_threads()))
            description.append('\n' \
                               'Created: ')
            description.append(elapsed_time(datetime.utcfromtimestamp(PROCESS.create_time())))
            description.append(' ago\n' \
                               '\n' \
                               '**CPU times:**\n' \
                               'User: ')
            cpu_times = PROCESS.cpu_times()
            cpu_time_user = cpu_times.user
            cpu_time_total = cpu_time_user
            description.append(cpu_time_user.__format__('.2f'))
            cpu_time_system = cpu_times.system
            cpu_time_total +=cpu_time_system
            description.append('\n' \
                               'System: ')
            description.append(cpu_time_system.__format__('.2f'))
            description.append('\n' \
                               'Children User: ')
            cpu_times = PROCESS.cpu_times()
            cpu_time_children_user = cpu_times.children_user
            cpu_time_total += cpu_time_children_user
            description.append(cpu_time_children_user.__format__('.2f'))
            description.append('\n' \
                               'Children system: ')
            cpu_time_children_system = cpu_times.children_system
            cpu_time_total +=cpu_time_children_system
            description.append(cpu_time_children_system.__format__('.2f'))
            description.append('\n' \
                               'IO wait: ')
            cpu_time_io_wait = cpu_times.iowait
            cpu_time_total += cpu_time_io_wait
            description.append(cpu_time_io_wait.__format__('.2f'))
            description.append('\n' \
                               '--------------------\n' \
                               'Total: ')
            description.append(cpu_time_total.__format__('.2f'))
            description.append('\n' \
                               '\n' \
                               '**CPU usage:**\n' \
                               'CPU usage percent: ')
            description.append(process_cpu_usage.cpu_percent.__format__('.2f'))
            description.append('%\n' \
                               'CPU usage with max frequency: ')
            description.append(process_cpu_usage.cpu_percent_with_max_frequency.__format__('.2f'))
            description.append('%\n' \
                               'CPU usage over all cores: ')
            description.append(process_cpu_usage.cpu_percent_total.__format__('.2f'))
            description.append('%\n' \
                               '\n' \
                               '**RAM usage**:\n' \
                               'Total: ')
            description.append((PROCESS.memory_info().rss / (1 << 20)).__format__('.2f'))
            description.append('MB\n' \
                               'Percent: ')
            description.append(PROCESS.memory_percent().__format__('.2f'))
            description.append('%')
            
            embed = Embed('System and Process stats:', ''.join(description), color = STAT_COLOR)
            
            await client.message_create(message.channel, embed = embed)
        
        category = 'STATS'
        
        async def description(command_context):
            return Embed('system-stats',(
                'Shows my system\s and processes\'s stats.\n'
                f'Usage: `{command_context.prefix}system-stats`'
                ), color = STAT_COLOR).add_footer(
                    'Owner only!')

