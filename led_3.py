from gpiozero import MotionSensor, LED
from signal import pause
from time import sleep
pir = MotionSensor(4)
led = LED(21)


def led_on():
    print("led on")
    led.on()

def led_off():
    print("led off")
    led.off()

led.on()
print("led show")
sleep(1)
led.off()
print("led off")
pir.when_motion = led_on
pir.when_no_motion = led_off
pause()
