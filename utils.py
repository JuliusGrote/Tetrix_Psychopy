# import libraries
import ctypes, time, json, os
import pygame
from numpy import mean

# checks whether a specific window is created
def is_window_open(window_title):        
    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    return hwnd != 0 


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
    time.sleep(t)
        
# define a method to create a dummi screen for the responsebox check
def create_dummi_screen_responsecheck():
    pygame.init()
    pygame.display.set_mode((100, 100))
    pygame.display.set_caption("check_responsebox")
    handle = ctypes.windll.user32.FindWindowW(None, "check_responsebox")

    # set the desired window position to be outside of the visible window (e.g., 10000 pixels from the left, 1000 pixels from the top)
    window_x, window_y = 10000, 10000
    ctypes.windll.user32.SetWindowPos(handle, -1, window_x, window_y, 0, 0, 0x0001)

def _enforce_min_gap(events, min_gap, total_dur=None):
    events = sorted(events, key=lambda x: x['start_time'])
    adjusted = []
    prev_end = None
    for ev in events:
        start = ev['start_time']
        end = ev['end_time']
        if prev_end is not None and start < prev_end + min_gap:
            shift = (prev_end + min_gap) - start
            start = start + shift
            end = end + shift
        if total_dur is not None and start > total_dur:
            break
        if total_dur is not None and end > total_dur:
            end = total_dur
        if end > start:
            adjusted.append({'start_time': start, 'end_time': end})
            prev_end = end
    return adjusted

def calculate_motor_replay_times(mode, accelerate_type, targeted_duration, min_display_duration=0.1,  min_reappear_gap=0.1, down_interval=0.05):
    motor_replay_times = []
    if os.path.exists('replay_data.json'):
        with open('replay_data.json', 'r') as f:
            r_data = json.load(f)

            r_moves = r_data.get('moves', [])
  
        # for standard keypress assume minimal display duration
        flash_dur = min_display_duration
        # Convert repeated 'down' events into hold periods to mimic block descent
        down_periods = []
        i = 0
        while i < len(r_moves):
            m = r_moves[i]
            if m['action'] == f'down_{accelerate_type}':
                # Start a new hold period
                start_time = m['time']
                end_time = m['time'] + flash_dur

                j = i + 1
                while j < len(r_moves):
                    next_action = r_moves[j]['action']
                    if next_action in [f'down_{accelerate_type}', 'gravity_hold'] and (r_moves[j]['time'] - end_time) <= down_interval*2:
                        end_time = r_moves[j]['time']
                        j += 1
                    else:
                        # Any other action ends the hold period
                        break
                
                down_periods.append({'start': start_time, 'end': end_time})
                i = j  # Skip all processed events
            else:
                i += 1         
         
        # Rebuild keypresses with hold duration info
        r_keypresses_motor = []
        for hold in down_periods:
            if accelerate_type == 'hold':
                r_keypresses_motor.append({'action': f'down_{accelerate_type}', 'time': hold['start'], 'duration': hold['end'] - hold['start']})
            elif accelerate_type == 'drop': # drop requires only a single keypress so disregard duration
                r_keypresses_motor.append({'action': f'down_{accelerate_type}', 'time': hold['start'], 'duration': hold['start'] + flash_dur})

        other_presses = [{'action': m['action'], 'time': m['time']} for m in r_moves if m['action'] in ['left', 'right', 'rotate', 'down']]
        r_keypresses_motor.extend(other_presses)
        r_keypresses_motor.sort(key=lambda x: x['time'])



        # total duration
        total_dur = r_moves[-1]['time']

        if mode == 'exact':
            motor_replay_times = [{'start_time': m['time'], 'end_time': m['time'] + m.get('duration', flash_dur)} for m in r_keypresses_motor]
            motor_replay_times.sort(key=lambda x: x['start_time'])

            if total_dur < targeted_duration:

                # loop the replay to fill the targeted duration
                t_diff = targeted_duration - total_dur

                while t_diff > 0:
                    for m in motor_replay_times:
                        new_start = m['start_time'] + total_dur
                        new_end = m['end_time'] + total_dur
                        if new_start >= targeted_duration:
                            break
                        motor_replay_times.append({'start_time': new_start, 'end_time': new_end})
                    t_diff -= total_dur

        elif mode == 'average':
            # get fraction of down holds & the rest
            down_hold_fraction = len([m for m in r_keypresses_motor if m['action'] == 'down_hold']) / len(r_keypresses_motor)
            other_fraction = 1 - down_hold_fraction

            avg_interval = total_dur / len(r_keypresses_motor)

            hold_dur = mean([m['duration'] for m in r_keypresses_motor if m['action'] == 'down_hold']) if down_hold_fraction > 0 else 0

            weighted_flash_dur = (flash_dur * other_fraction) + (hold_dur * down_hold_fraction)
            motor_replay_times = []

            current_time = 0.0
            while current_time < targeted_duration:
                start_time = current_time
                end_time = start_time + weighted_flash_dur
                motor_replay_times.append({'start_time': start_time, 'end_time': end_time})
                current_time += avg_interval
        


        motor_replay_times = _enforce_min_gap(motor_replay_times, min_reappear_gap, targeted_duration)

    return motor_replay_times
