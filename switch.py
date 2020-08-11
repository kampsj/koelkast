import RPi.GPIO as GPIO


class Switch:
    """
    A SolidStateSwitch, controlled by the GPIO pins.
    Attributes:
        cool_pin: The pin number (GPIO.board) on which the cool switch is connected
    Requirements:
        RPi.GPIO imported as GPIO
    """

    def __init__(self, cool_pin):
        """
        :param pin: Connected GPIO pin, according to GPIO.board
        """
        self.cool_pin = cool_pin
        # Set board mode (for pin numbering)
        GPIO.setmode(GPIO.BOARD)
        # setup=0 (0 is output) initial=0; sets pin to low.
        GPIO.setup(self.cool_pin, 0, initial=0)

    def status(self):
        """
        :Returns: True when on, False when off
        """
        return True if GPIO.input(self.cool_pin) == 1 else False

    def off(self):
        """
        Sets the GPIO output of the cool pin to LOW
        """
        return GPIO.output(self.cool_pin, 0)

    def on(self):
        """
        Sets the GPIO output of the cool pin to HIGH
        """
        return GPIO.output(self.cool_pin, 1)


