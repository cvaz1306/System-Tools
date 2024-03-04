import multiprocessing
import time
import server as webui
from backend import sys_comms_refresh, min_on_lock, screenlock
from config.mol import WINDOWS2MIN

class ModuleManager:
    def __init__(self):
        self.modules = []

    def add_module(self, module_function, *args, **kwargs):
        self.modules.append((module_function, args, kwargs))

    def run_modules(self):
        processes = []
        cmsq = multiprocessing.Queue()
        webuiq = multiprocessing.Queue()
        
        for module, args, kwargs in self.modules:
            process = multiprocessing.Process(target=module, args=args, kwargs=kwargs)
            processes.append(process)
            process.start()

        webuiproc = multiprocessing.Process(target=webui.run, args=(webuiq,))
        webuiproc.start()

        try:
            while True:
                if not cmsq.empty():
                    msg = cmsq.get()
                    if msg == 'KEYBOARD':
                        raise KeyboardInterrupt
                webuiq.put({'locked': screenlock.is_screen_locked()})
                time.sleep(0.2)
        except KeyboardInterrupt:
            webuiproc.join()
            for process in processes:
                process.join()
            print("Service ended with keyboard.")
        except Exception as e:
            webuiproc.join()
            for process in processes:
                process.join()
            print(f"Error: {e}")

