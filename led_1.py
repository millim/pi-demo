from gpiozero import LED
from time import sleep


"""
 GPIO21 ---- LED --
                  |
 GND ------R1------
"""

led = LED(21)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
