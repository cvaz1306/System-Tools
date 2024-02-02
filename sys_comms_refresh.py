import ctypes
from time import sleep
def reset_interface(interval):
    try:
        while True:
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0214, 0, 0)
            sleep(interval)
    except:
        print("Service sys_comms_refresh interrupted.")