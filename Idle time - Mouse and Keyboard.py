from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import pandas as pd
from datetime import datetime, timedelta
import time

last_activity_time = datetime.now()


# Function to log the inactive duration to an Excel sheet
def log_inactive_duration(duration):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {'Time': current_time, 'Inactive Duration': duration}
    df = pd.DataFrame(entry, index=[0])

    try:
        # Load the existing log file
        log_data = pd.read_excel('activity_logger.xlsx')
        log_data = log_data.append(df, ignore_index=True)
    except FileNotFoundError:
        # Create a new log file if it doesn't exist
        log_data = df

    # Save the log to the Excel sheet
    log_data.to_excel('activity_log.xlsx', index=False)
    print(f"Inactive duration logged: {duration} seconds")


# Function to handle mouse clicks
def on_click(x, y, button, pressed):
    global last_activity_time
    last_activity_time = datetime.now()


# Function to handle keyboard key presses
def on_press(key):
    global last_activity_time
    last_activity_time = datetime.now()


# Function to check for user activity
def check_activity():
    global last_activity_time
    inactive_duration = 0

    while True:
        # Calculate the duration since the last activity
        duration_since_last_activity = datetime.now() - last_activity_time
        inactive_duration = duration_since_last_activity.total_seconds()

        # Log the inactive duration if it exceeds 5 minutes
        if inactive_duration >= 300:
            log_inactive_duration(inactive_duration)

        # Sleep for x seconds
        time.sleep(300)


# Start checking for activity
mouse_listener = MouseListener(on_click=on_click)
keyboard_listener = KeyboardListener(on_press=on_press)
mouse_listener.start()
keyboard_listener.start()
check_activity()
