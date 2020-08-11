from settings import TEMPERATURE_SENSOR_IDS


def read_sensors():
    """
    Reads all temperature sensors and calculates the average value.
    :return: list with length 4. entries 0, 1 and 2 are measurements. 3 is the average.
    """
    values = []
    # first grab current values then validate the values.
    for sensor in TEMPERATURE_SENSOR_IDS:
        try:
            with open("/sys/bus/w1/devices/" + TEMPERATURE_SENSOR_IDS[sensor] + "/w1_slave", 'r') as temp_file:
                text = temp_file.readlines()

            temp_line = text[1].split("=")[1].rstrip()  # Temperature info is in the second line of the file,
            # right after the '=' and followed by a newline

            temperature = float(temp_line) / 1000
            values.append(temperature)
        except:
            print('Error in sensor: {}'.format(sensor))

    average = round(sum(values) / len(values), 2)
    values.append(average)

    return values
