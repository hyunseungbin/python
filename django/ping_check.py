import time
from ping3 import ping
from plyer import notification

def check_network(target_host, interval):
    while True:
        response_time = ping(target_host)
        if response_time is not None:
            print(f"Response time: {response_time} ms")
        else:
            print("No response")
            notification.notify(
                title="Network Monitor",
                message="No response from the target host.",
                app_name="Network Monitor",
            )

        time.sleep(interval)

if __name__ == "__main__":
    target_host = "8.8.8.8"  # Change this to the target host you want to monitor
    interval = 5  # Time interval between checks (in seconds)

    check_network(target_host, interval)