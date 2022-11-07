from interruptingcow import timeout
from time import sleep

try:
    with timeout(1):
        sleep(6)
except:
    print("failed")