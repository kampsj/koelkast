import asyncio, aiofiles

from settings import TEMP_SENSORS

async def read_sensors():
    """
    Reads all temperature sensors and calculates the average value.
    :return: list with length 4. entries 0, 1 and 2 are measurements. 3 is the average.
    """
    values = []
    # first grab current values then validate the values.

    t = asyncio.create_task(get_sensor_data(TEMP_SENSORS))

    results = await asyncio.gather(t)
    values = [x for x in results if x]

    try:
        average = round(sum(values) / len(values), 2)
    except ZeroDivisionError:
        average = "SENSOR ERROR"
    values.append(average)

    return values


async def get_sensor_data(sensors):
    for sensor in sensors:
        try:
            async with aiofiles.open("/sys/bus/w1/devices/" + sensor + "/w1_slave", 'r') as temp_file:
                text = await temp_file.readlines()

            temp_line = text[1].split("=")[1].rstrip()  # Temperature info is in the second line of the file,
            # right after the '=' and followed by a newline

            temperature = float(temp_line) / 1000
            return temperature
        except Exception as e:
            print('Error in sensor: {}'.format(sensor))
            print(e)



# async for control loop makes no sense.
def get_sensor_synchronous():
    values = []
    for sensor in TEMP_SENSORS:
        try:
            with open("/sys/bus/w1/devices/" + sensor + "/w1_slave", 'r') as temp_file:
                text =  temp_file.readlines()

            temp_line = text[1].split("=")[1].rstrip()  # Temperature info is in the second line of the file,
            # right after the '=' and followed by a newline

            temperature = float(temp_line) / 1000
            values.append(temperature)
        except Exception as e:
            print('Error in sensor: {}'.format(sensor))
            print(e)

    average = round(sum(values) / len(values), 2)
    values.append(average)
    return values
