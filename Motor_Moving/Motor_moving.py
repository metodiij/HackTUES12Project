import requests
import time
from gpiozero import PWMOutputDevice                                                      

# Motor Configuration (Pins 17, 27, 22, 16)
front_left = PWMOutputDevice(17)
front_right = PWMOutputDevice(22)
back_right = PWMOutputDevice(16)
back_left = PWMOutputDevice(27)

SPEED = 0.3
API_URL = "http://192.168.0.5:5000/get-command"

def stop():
    front_left.value = front_right.value = back_left.value = back_right.value = 0

def move_robot(action, duration):
    print(f"Executing: {action} for {duration}s")
    
    if action == "forward":
        front_left.value = front_right.value = back_left.value = back_right.value = SPEED
    elif action == "right":
        # Turn right by moving ONLY right wheels (as requested)
        front_left.value = back_left.value = SPEED
        front_right.value = back_right.value = 0
    elif action == "left":
        # Turn left by moving ONLY left wheels
        front_right.value = back_right.value = SPEED
        front_left.value = back_left.value = 0
    
    time.sleep(duration)
    stop()
    time.sleep(0.5) # Stability pause

print("Robot is standing by...")

while True:
    try:
        response = requests.get(API_URL, timeout=1)
        data = response.json()
        
        if data['action'] != "idle":
            move_robot(data['action'], data['time'])
    except Exception as e:
        # Wait if server is not reachable
        print(f"Error {e}")

    time.sleep(1)