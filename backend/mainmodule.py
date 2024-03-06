import multiprocessing
import time
from backend.modulebase import Module
from .server import run
from . import screenlock
class MainModule(Module):
    def run(self, webui_queue, module_queue):
        webuiproc = multiprocessing.Process(target=run, args=(webui_queue,))
        webuiproc.start()

        try:
            while True:
                if not module_queue.empty():
                    msg = module_queue.get()
                    if msg == 'KEYBOARD':
                        raise KeyboardInterrupt
                webui_queue.put({'locked': screenlock.is_screen_locked()})
                time.sleep(0.2)
        except KeyboardInterrupt:
            webuiproc.join()
            print("Service ended with keyboard.")
        except Exception as e:
            webuiproc.join()
            print(f"Error: {e}")
