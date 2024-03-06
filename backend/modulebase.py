import multiprocessing
import time
from . import server as webui
from backend import screenlock
import pygetwindow as gw
import ctypes
from time import sleep

class Module:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.process = None

    def start(self):
        self.process = multiprocessing.Process(target=self.run, args=self.args, kwargs=self.kwargs)
        self.process.start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.join()

    def run(self):
        raise NotImplementedError("Subclasses must implement the run method.")

class MinimizeWindows(Module):
    def run(self, titles, cq):
        while True:
            if screenlock.is_screen_locked():
                cq.put({'locked': True})
                self.minimize_windows(titles)
            else:
                cq.put({'locked': False})
            time.sleep(0.3)

    def minimize_windows(self, titles):
        for title_start in titles:
            windows = [window for window in gw.getAllTitles() if window.startswith(title_start)]
            for window_title in windows:
                window = gw.getWindowsWithTitle(window_title)[0]
                window.minimize()

class ResetInterface(Module):
    def run(self, interval, cq):
        try:
            while True:
                self.reset_interface()
                sleep(interval)
        except KeyboardInterrupt:
            print("Service sys_comms_refresh() interrupted.")
            cq.put("KEYBOARD")

    def reset_interface(self):
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0214, 0, 0)