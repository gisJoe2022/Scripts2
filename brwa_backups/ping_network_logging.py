


import subprocess
import time
import datetime

def check_internet_latency(log_dir=r'S:\Projects\2025_Projects\202517_Latency_Testing\log', interval=5, duration_minutes=2, target='8.8.8.8'):
    # Create a timestamped log file name
    timestamp_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_path = f"{log_dir}\internet_latency_{timestamp_str}.log"

    end_time = time.time() + duration_minutes * 60

    with open(log_file_path, 'a') as log_file:
        while time.time() < end_time:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                result = subprocess.run(['ping', '-c', '1', '208.67.222.222'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'time=' in line:
                            latency = line.split('time=')[1].split(' ')[0]
                            log_file.write(f"{timestamp} - Internet latency: {latency}\n")
                            break
                else:
                    log_file.write(f"{timestamp} - Failed to ping 8.8.8.8. Error: {result.stderr.strip()}\n")
            except Exception as e:
                log_file.write(f"{timestamp} - Exception occurred: {str(e)}\n")

            time.sleep(interval)

# Example usage:
# check_internet_latency(log_dir='C:/path/to/your/logs', interval=10, duration_minutes=30)
