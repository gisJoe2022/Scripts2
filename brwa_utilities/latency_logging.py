

from ping3 import ping
import time
import datetime
import os

# Parameters
log_file_path = r'S:\Projects\2025_Projects\202517_Latency_Testing\log' # Log file location
interval = 1  # Time between pings in seconds
duration_minutes = 60  # Total duration to run in minutes
timestamp1 = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')  # No colons for file name

# Construct full log file path
full_log_path = os.path.join(log_file_path, f"internet_latency_{timestamp1}.log")

def log_and_print(message, log_file_handle=None):
    print(message)
    if log_file_handle:
        log_file_handle.write(message + '\n')
        log_file_handle.flush()  # Ensure immediate write to disk

print(f"Log file will be written to: {full_log_path}")

def check_internet_latency(log_file, interval, duration_minutes, target='8.8.8.8'):
    end_time = time.time() + duration_minutes * 60
    try:
        with open(log_file, 'a', buffering=1) as log_file_handle:  # Line-buffered writing
            log_and_print(f"Successfully opened log file: {log_file}", log_file_handle)
            while time.time() < end_time:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
                try:
                    latency = ping(target, timeout=2)  # Returns latency in seconds
                    if latency is not None:
                        latency_ms = round(latency * 1000, 2)  # Convert to milliseconds
                        log_and_print(f"{timestamp} - Internet latency to {target}: {latency_ms} ms", log_file_handle)
                    else:
                        log_and_print(f"{timestamp} - No response from {target}", log_file_handle)
                except Exception as e:
                    log_and_print(f"{timestamp} - Error during ping: {str(e)}", log_file_handle)
                time.sleep(interval)
    except Exception as file_error:
        print(f"Failed to open log file: {log_file}\nError: {str(file_error)}")

# Run
check_internet_latency(full_log_path, interval, duration_minutes)