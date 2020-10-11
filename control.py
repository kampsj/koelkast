import time
from sensors import get_sensor_synchronous
from interface import read_interface

from settings import INTERFACE_TEMP, INTERFACE_ACTIVE, CONTROL_INTERVAL, CONTROL_ACCURACY


def control_loop(switch):
    """
    Infinite loop. When the refrigerator temperature is too high, cooling is activated.
    Requires a switch to turn cooling on/off.
    """
    while True:
        # Cooling should be activated
        active = read_interface(INTERFACE_ACTIVE)
        if active == 1.0:
            # Check the goal temperature
            goal_temp = read_interface(INTERFACE_TEMP)
            # First get temperature from the sensors.
            average_temp = get_sensor_synchronous()[-1]
        
            control_temp = average_temp - goal_temp - CONTROL_ACCURACY
            if switch.status():
                # If cooling is active, cool down to -2 * control accuracy.
                # This prevents the cooler from being switched on/off constantly.
                if control_temp < -2 * CONTROL_ACCURACY:
                    switch.off()
            else:
                # When cooling is not active, and temperature is above goal + accuracy, activate cooling.
                if control_temp > 0:
                    switch.on()
        elif active == 0.0:
            switch.off()
        else:
            pass

        time.sleep(CONTROL_INTERVAL)
