import socket
import time

hostname = "invalid_hostname_example"
max_retries = 3
retry_delay = 5

for attempt in range(max_retries):
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"Resolved IP address: {ip_address}")
        break
    except socket.gaierror as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    else:
      print("Max retries exceeded. Unable to resolve hostname.")