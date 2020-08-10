import time
from sensors import read_sensors
from interface import read_interface

from settings import INTERFACE_TEMP, INTERFACE_ACTIVE, CONTROL_INTERVAL, CONTROL_ACCURACY

def control_temp():
    num = 1
    while True:
        print("woep")
        print(num)
        num += 1
        time.sleep(2)

def control_loop():
    """

    """
    while True:
        # Cooling should be activated
        if INTERFACE_ACTIVE == '1':
            # Check the goal temperature
            goal_temp = read_interface(INTERFACE_TEMP)
            # First get temperature sensors.
            current_temp = read_sensors()[-1]

            if current_temp - goal_temp + CONTROL_ACCURACY > 0:
                print("Cooling")


        time.sleep(CONTROL_INTERVAL)