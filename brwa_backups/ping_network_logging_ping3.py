

from ping3 import ping
import time
import datetime
import os

# ============================
# User-defined configuration
# ============================
log_file_path = r'S:\Projects\2025_Projects\202517_Latency_Testing\log'  # Change to your desired directory
                                 # Change to your desired log file name
interval = 5                                                            # Time between pings in seconds
duration_minutes = 2                                                    # Total duration to run in minutes
timestamp1 = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')
#log_file_name = "internet_latency_{timestamp1}.log" 
# ============================
# Construct full log file path
# ============================
full_log_path = os.path.join(log_file_path, f"internet_latency_{timestamp1}.log")

# ============================
# Latency logging function
# ============================
def check_internet_latency(log_file, interval, duration_minutes, target='8.8.8.8'):
    end_time = time.time() + duration_minutes * 60

    with open(log_file, 'a') as log_file_handle:
        while time.time() < end_time:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            try:
                latency = ping(target, timeout=2)  # returns latency in seconds
                if latency is not None:
                    latency_ms = round(latency * 1000, 2)
                    log_file_handle.write(f"{timestamp} - Internet latency to {target}: {latency_ms} ms\n")
                else:
                    log_file_handle.write(f"{timestamp} - No response from {target}\n")
            except Exception as e:
                log_file_handle.write(f"{timestamp} - Error: {str(e)}\n")

            time.sleep(interval)

# ============================
# Run the latency logger
# ============================
check_internet_latency(full_log_path, interval, duration_minutes)
