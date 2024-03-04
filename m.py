from backend.modules import *


if __name__ == '__main__':
    module_manager = ModuleManager()
    cmsq=multiprocessing.Queue()
    module_manager.add_module(sys_comms_refresh.reset_interface, 0.1, cmsq)
    module_manager.add_module(min_on_lock.check_screen_lock_and_minimize, WINDOWS2MIN, cmsq)
    
    print("Service started")
    module_manager.run_modules()
