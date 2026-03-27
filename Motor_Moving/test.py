from gpiozero import PWMOutputDevice
from signal import pause

# Change OutputDevice to PWMOutputDevice
#left_back  = PWMOutputDevice(27)
#left_front = PWMOutputDevice(17)
#right_back = PWMOutputDevice(16)
right_front = PWMOutputDevice(22)

# Set speed here (0.0 to 1.0)
# To increase speed, make this number closer to 1.0
speed = 0.3

#left_front.value = speed
#left_back.value = speed
right_front.value = speed
#right_back.value = speed

print(f"GPIO 17 and 27 are ON at speed: {speed}")
pause()