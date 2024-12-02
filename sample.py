import re
import time
from machine import Pin, I2C
import ssd1306

time.sleep(2)
i2c = I2C(sda=Pin(6), scl=Pin(7))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

regex = re.compile(",")
f = open("kannousuiken.dat")
for x in range(844):
    a = f.readline()
    b = regex.split(a)
    display.pixel(int(b[0]), int(b[1]), 1)
f.close()

for i in range(30):
    display.scroll(4, 0)
    time.sleep(0.1)
    display.show()
  
