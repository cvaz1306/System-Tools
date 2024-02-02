import sys_comms_refresh

import multiprocessing
print("Service started")
try:
    p = multiprocessing.Process(target=sys_comms_refresh.reset_interface, args=(0.1,))
except KeyboardInterrupt:
    print("Service ended with keyboard.")
except:
    print("Error")