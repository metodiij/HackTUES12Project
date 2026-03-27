from gpiozero import PWMOutputDevice
from signal import pause

front_left = PWMOutputDevice(17)
front_right = PWMOutputDevice(27)
back_right = PWMOutputDevice(22)
back_left = PWMOutputDevice(16)


front_left.value = 0.2
front_right.value = 0.2
back_right.value = 0.2
back_left.value = 0.2
print("GPIO 17 ")

pause()