#Drive 16x2 LCD screen with Raspberry Pi
#Tutorial : http://osoyoo.com/?p=832

import RPi.GPIO as GPIO
import time

class PiLcd:
    LCD_WIDTH = 16    # Maximum characters per line
    LCD_CHR = True
    LCD_CMD = False

    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005


    LCD_RS = None
    def __init__(self,
                 lcd_e ,
                 lcd_rs ,
                 lcd_d4 ,
                 lcd_d5 ,
                 lcd_d6 ,
                 lcd_d7):
        if (lcd_e is None or lcd_rs is None or lcd_d4 is None or lcd_d5 is None or lcd_d6 is None or lcd_d7 is None):
            raise "params error"

        self.LCD_E = lcd_e
        self.LCD_RS = lcd_rs
        self.LCD_D4 = lcd_d4
        self.LCD_D5 = lcd_d5
        self.LCD_D6 = lcd_d6
        self.LCD_D7 = lcd_d7
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(lcd_e, GPIO.OUT)
        GPIO.setup(lcd_rs, GPIO.OUT)
        GPIO.setup(lcd_d4, GPIO.OUT)
        GPIO.setup(lcd_d5, GPIO.OUT)
        GPIO.setup(lcd_d6, GPIO.OUT)
        GPIO.setup(lcd_d7, GPIO.OUT)

        self.lcd_init()

    def lcd_init(self):
        self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):

        GPIO.output(self.LCD_RS, mode) # RS

        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)

        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
      time.sleep(self.E_DELAY)
      GPIO.output(self.LCD_E, True)
      time.sleep(self.E_PULSE)
      GPIO.output(self.LCD_E, False)
      time.sleep(self.E_DELAY)

    def lcd_string(self,message,line):
      message = message.ljust(self.LCD_WIDTH," ")

      self.lcd_byte(line, self.LCD_CMD)

      for i in range(self.LCD_WIDTH):
        self.lcd_byte(ord(message[i]),self.LCD_CHR)


    def show(self, msg):
        lc = msg.split("\n")

        if lc.__len__() > 2:
            raise Exception("input message must \\n only once")

        for m in lc:
            if m.__len__() > 16:
                raise Exception("The maximum number of characters in a row is 16")

        self.lcd_string(lc[0], self.LCD_LINE_1)
        if lc.__len__() == 2:
            self.lcd_string(lc[1], self.LCD_LINE_2)
        else:
            self.lcd_string("", self.LCD_LINE_2)
