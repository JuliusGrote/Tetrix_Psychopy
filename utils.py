# import libraries
import ctypes, time
import pygame

# checks whether a specific window is created
def is_window_open(window_title):        
    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    if hwnd == 0: # window not found
        return False  
    else:
        return True 


# define function to bring the window with a specific title to the foreground
def Get_on_top(window_title):
    active_window = None
    HWND_TOPMOST = -1
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    # brings the searched window to foreground
    if hwnd != 0:
        active_window = ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        # Simulate left mouse button press and release to make window active(only once)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
        ctypes.windll.user32.ShowCursor(False)
        
# create a countdown timer with a "x"-second duration or speficific for a condition
def condition_or_wait_timer(name_or_duration): 
    if name_or_duration == "wait":
        t = 1
    elif name_or_duration == "Tetris":
        t = 30
    else:
        t = float(name_or_duration)
    end_time = time.time() + t
    while time.time() < end_time:
        pass
        
# define a method to create a dummi screen for the responsebox check
def create_dummi_screen_responsecheck():
    pygame.init()
    pygame.display.set_mode((100, 100))
    pygame.display.set_caption("check_responsebox")
    handle = ctypes.windll.user32.FindWindowW(None, "check_responsebox")

    # set the desired window position to be outside of the visible window (e.g., 10000 pixels from the left, 1000 pixels from the top)
    window_x, window_y = 10000, 10000
    ctypes.windll.user32.SetWindowPos(handle, -1, window_x, window_y, 0, 0, 0x0001)
    
def list_keyboards():
    c = wmi.WMI()
    # Query for keyboards
    print("\n--------------------\nConnected Keyboards:")
    for index, item in enumerate(c.Win32_Keyboard(), start=1):  # start=1 begins the index from 1 instead of 0
        print(f"Nr. {index} ID: {item.DeviceID}, Description: {item.Description}")
    print("--------------------\n")