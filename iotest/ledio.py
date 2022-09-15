
from gpiozero import LED, Button
import time

SuckRightBack = LED(17)
SuckRightMiddle = LED(18)
SuckRightFront = LED(16)

SuckLeftBack = LED(6)
SuckLeftMiddle = LED(12)
SuckLeftFront = LED(19)

def suck(enable=False):
    if(enable is False):

        led1.on()
        led2.off()
    else:
        led1.off()
        led2.on()
        
while True:
    suck(False)
    time.sleep(10)
    suck(True)
    time.sleep(10)




