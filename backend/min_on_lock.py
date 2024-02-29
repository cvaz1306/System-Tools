import pygetwindow as gw
import time
from .screenlock import *

def minimize_windows(titles):
    for title_start in titles:
        # Get all windows starting with the specified prefix
        windows = [window for window in gw.getAllTitles() if window.startswith(title_start)]
        
        # Iterate over the windows and minimize each one
        for window_title in windows:
            window = gw.getWindowsWithTitle(window_title)[0]
            window.minimize()

def check_screen_lock_and_minimize(titles, cq):
    while True:
        #print(is_screen_locked())
        if is_screen_locked():
            cq.put({'locked': True})
            minimize_windows(titles)
        else:
            cq.put({'locked': False})
        time.sleep(0.3)
