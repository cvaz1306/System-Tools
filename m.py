import sys_comms_refresh

import multiprocessing
if __name__=='__main__':
    
    print("Service started")
    try:
        p = multiprocessing.Process(target=sys_comms_refresh.reset_interface, args=(0.1,))
        p.start()
        p.join()
    except KeyboardInterrupt:
        print("Service ended with keyboard.")
    except Exception as e:
        print(f"Error: {e}")