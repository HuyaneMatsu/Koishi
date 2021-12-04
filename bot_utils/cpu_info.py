import sys
from os import getpid as get_process_identifier
from hata import KOKORO
from scarletio import Future, sleep

try:
    import psutil
except ModuleNotFoundError:
    psutil = None

# We always use turbo
CPU_MODEL_TO_FREQUENCY = {
    b'Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz': 3500.0,
    b'Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz': 3500.0,
}

if (psutil is None) or (sys.platform != 'linux'):
    CpuUsage = None
    PROCESS_PID = 0
    PROCESS = None
    CPU_MAX_FREQUENCY = 0
else:
    PROCESS_PID = get_process_identifier()
    
    try:
        PROCESS = psutil.Process(PROCESS_PID)
    except (AttributeError, psutil.NoSuchProcess):
        CpuUsage = None
        CPU_MAX_FREQUENCY = 0
        PROCESS = None
    else:
        def get_max_cpu_frequency():
            
            cpu_frequency = psutil.cpu_freq()
            CPU_MAX_FREQUENCY = cpu_frequency.max
            
            import subprocess
            
            CPU_MODEL = None
            
            try:
                lscpu_output = subprocess.check_output('lscpu', shell=False)
            except subprocess.CalledProcessError:
                pass
            else:
                for line in lscpu_output.splitlines():
                    if line.startswith(b'CPU max MHz:'):
                        CPU_MAX_FREQUENCY = float(line[len(b'CPU max MHz:'):].strip())
                        continue
                    
                    if line.startswith(b'Model name:'):
                        CPU_MODEL = line[len(b'Model name:'):].strip()
                        continue
            
            while True:
                if CPU_MAX_FREQUENCY == 0.0:
                    if (CPU_MODEL is not None):
                        try:
                            CPU_MAX_FREQUENCY = CPU_MODEL_TO_FREQUENCY[CPU_MODEL]
                        except KeyError:
                            sys.stdout.write(f'Unknown CPU model: {CPU_MODEL!r}.')
                        else:
                            break
                    
                    CPU_MAX_FREQUENCY = cpu_frequency.current
                    break
            
            return CPU_MAX_FREQUENCY
        
        CPU_MAX_FREQUENCY = get_max_cpu_frequency()
        del get_max_cpu_frequency
        
        class CpuUsage:
            
            __slots__ = ('average_cpu_frequency', 'cpu_percent',)
            
            waiter = None
            
            async def __new__(cls):
                waiter = cls.waiter
                if waiter is None:
                    average_cpu_frequency = psutil.cpu_freq().current
                    PROCESS.cpu_percent()
                    cls.waiter = waiter = Future(KOKORO)
                    await sleep(0.8, KOKORO)
                    cpu_percent = PROCESS.cpu_percent()
                    cpu_frequency = psutil.cpu_freq()
                    average_cpu_frequency = (average_cpu_frequency + cpu_frequency.current) * 0.5
                    
                    result = object.__new__(cls)
                    result.cpu_percent = cpu_percent
                    result.average_cpu_frequency = average_cpu_frequency
                    waiter.set_result(result)
                    cls.waiter = None
                else:
                    result = await waiter
                
                return result
            
            @property
            def cpu_percent_with_max_frequency(self):
                return (self.average_cpu_frequency / CPU_MAX_FREQUENCY * self.cpu_percent)
            
            @property
            def cpu_percent_total(self):
                return self.cpu_percent_with_max_frequency / psutil.cpu_count(logical=False)
