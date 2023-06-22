
from time import sleep
import time

for second in range(3):
    print(time.ctime(), end="\r")
    time.sleep(1)
print("\nGo!")