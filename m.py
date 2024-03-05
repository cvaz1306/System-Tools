from backend.modulebase import *
from config.mol import WINDOWS2MIN

if __name__ == '__main__':
    minimize_windows_module = MinimizeWindows(WINDOWS2MIN, multiprocessing.Queue())
    reset_interface_module = ResetInterface(0.1, multiprocessing.Queue())
    main_module = MainModule(multiprocessing.Queue(), multiprocessing.Queue())

    print("Service started")
    try:
        minimize_windows_module.start()
        reset_interface_module.start()
        main_module.start()
    except KeyboardInterrupt:
        print("Service ended with keyboard.")
        minimize_windows_module.stop()
        reset_interface_module.stop()
        main_module.stop()
        
    except Exception as e:
        minimize_windows_module.stop()
        reset_interface_module.stop()
        main_module.stop()
        print(f"Error: {e}")
