import requests
import time
from gpiozero import PWMOutputDevice

# Настройка на пиновете (Вашата конфигурация)
front_left = PWMOutputDevice(17)
front_right = PWMOutputDevice(27)
back_right = PWMOutputDevice(22)
back_left = PWMOutputDevice(16)

SPEED = 0.3 # Мощност на моторите (0.0 до 1.0)
SERVER_URL = "http://localhost:3000/get-command"

def stop():
    front_left.value = 0
    front_right.value = 0
    back_right.value = 0
    back_left.value = 0

def execute(action, duration):
    print(f"Изпълнявам: {action} за {duration:.2f} секунди")
    
    if action == "forward":
        front_left.value = front_right.value = back_left.value = back_right.value = SPEED
    
    elif action == "right":
        # Завой надясно: движат се само десните колела (според вашето желание)
        front_right.value = back_right.value = SPEED
        front_left.value = back_left.value = 0
        
    elif action == "left":
        # Завой наляво: движат се само левите колела
        front_left.value = back_left.value = SPEED
        front_right.value = back_right.value = 0

    time.sleep(duration)
    stop()
    time.sleep(0.5) # Кратка пауза за стабилност

print("Роботът е готов и чака команди...")

while True:
    try:
        response = requests.get(SERVER_URL, timeout=1)
        data = response.json()
        
        if data['action'] != "idle":
            execute(data['action'], data['time'])
            
    except Exception as e:
        # Изчакваме ако сървърът не е пуснат
        pass
    time.sleep(1)