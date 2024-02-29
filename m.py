from backend import sys_comms_refresh, min_on_lock, screenlock
import multiprocessing
import server as webui
import time
from config.mol import WINDOWS2MIN
# List to store module functions and their arguments
modules = []
processes = []
def add_module(module_function, *args, **kwargs):
    modules.append((module_function, args, kwargs))

def run_modules():
    
    for module, args, kwargs in modules:
        
        process = multiprocessing.Process(target=module, args=args, kwargs=kwargs)
        processes.append(process)
        process.start()
def join_modules():
    for process in processes:
        process.join()

# Add modules to the list with their respective arguments

cmsq=multiprocessing.Queue()
add_module(sys_comms_refresh.reset_interface, 0.1, cmsq)
add_module(min_on_lock.check_screen_lock_and_minimize, WINDOWS2MIN, cmsq)
webuiq=multiprocessing.Queue()


if __name__ == '__main__':
    webuiproc=multiprocessing.Process(target=webui.run, args=(webuiq,))
    webuiproc.start()
    print("Service started")
    try:
        run_modules()
        while True:
            if not cmsq.empty():
                pass
            webuiq.put({'locked':screenlock.is_screen_locked()})
            time.sleep(.2)
            
        
        print("Service ended")
    except KeyboardInterrupt:
        webuiproc.join()
        join_modules()
        print("Service ended with keyboard.")
        
    except Exception as e:
        webuiproc.join()
        
        join_modules()
        print(f"Error: {e}")
