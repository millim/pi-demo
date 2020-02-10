from lcdtool import lcd
import time
import Adafruit_DHT

obj = lcd.PiLcd(20, 21, 12, 1, 7,8)
dht11_gpio = 26
dht11 = Adafruit_DHT.DHT11
def main():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(dht11, dht11_gpio)
        obj.show(time.strftime("%Y-%m-%d %H:%M", time.localtime())+"\n"+"T:{1:0.1f}C, H:{0:0.1f}%".format(humidity, temperature) )
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        obj.show("Good bye")


